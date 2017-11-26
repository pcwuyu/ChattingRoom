import json

from channels import Channel
from channels.auth import channel_session_user, channel_session_user_from_http

from .models import Room


# This decorator copies the user from the HTTP session (only available in
# websocket.connect or http.request messages) to the channel session (available
# in all consumers with the same reply_channel, so all three here)
@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    message.channel_session['rooms'] = []


@channel_session_user
def ws_disconnect(message):
    for room_id in message.channel_session.get('rooms', set()):
        try:
            room = Room.objcets.get(pk=room_id)
            # 将该用户从当前的广播群组中移除
            room.websocket_group.discard(message.reply_channel)
        except:
            pass


# Unpacks the JSON in the received WebSocket frame and puts it onto a channel
# of its own with a few attributes extra so we can route it
# This doesn't need @channel_session_user as the next consumer will have that,
# and we preserve message.reply_channel (which that's based on)
def ws_receive(message):
    # All WebSocket frames have either a text or binary payload; we decode the
    # text part here assuming it's JSON.
    # You could easily build up a basic framework that did this encoding/decoding
    # for you as well as handling common errors.
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("ChatRoom.receive").send(payload)


@channel_session_user
def chat_join(message):
    room = Room.objects.get(pk=message["room"])
    # Send a "enter message" to the room if available
    room.send_message(None, message.user, 'entered')
    # OK, add them in. The websocket_group is what we'll send messages
    # to so that everyone in the chat room gets them.
    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(
        set(message.channel_session['rooms']).union([room.id]))
    # Send a message back that will prompt them to open the room
    # Done server-side so that we could, for example, make people
    # join rooms automatically.
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "name": room.name,
        }),
    })


@channel_session_user
def chat_leave(message):
    # Reverse of join - remove them from everything.
    room = Room.objects.get(pk=message["room"])

    # Send a "leave message" to the room if available
    room.send_message(None, message.user, 'leave')
    room.websocket_group.discard(message.reply_channel)
    message.channel_session['rooms'] = list(
        set(message.channel_session['rooms']).difference([room.id]))
    # Send a message back that will prompt them to close the room
    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(room.id),
        }),
    })


@channel_session_user
def chat_send(message):
    room = Room.objects.get(pk=message["room"])
    room.send_message(message["message"], message.user)
