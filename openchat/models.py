from django.db import models
from channels import Group
import json
# Create your models here.


class Room(models.Model):
    """
    聊天室model
    """

    name = models.CharField(
        '房间名字',
        max_length=128,
        default='待编辑'
    )

    def __str__(self):
        return self.name

    @property
    def websocket_group(self):
        '''
        返回一个channels 群组，
        让websocket在其中广播对应的信息
        '''
        return Group('房间id：{}'.format(self.pk))

    def send_message(self, message, user):
        '''
        向该用户所在的房间里发送信息
        '''
        final_msg = {
            'room': str(self.pk),
            'message': message,
            'user': user.username,
        }
        # 发送信息
        self.websocket_group.send(
            {'text': json.dumps(final_msg)}
        )
