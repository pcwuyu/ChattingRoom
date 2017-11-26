from channels import route, include

# This function will display all messages received in the console


def message_handler(message):
    print(message['text'])


channel_routing = [
    # we register our message handler
    route("websocket.receive", message_handler),
    include("openchat.routing.websocket_routing", path=r"^/chat/stream"),
    include("openchat.routing.custom_routing"),
]
