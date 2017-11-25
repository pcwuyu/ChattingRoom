from django.db import models

# Create your models here.


class Room(models.Model):
    """
    聊天室model
    """
    title = models.CharField('房间名字', max_length=255),

    def __str__(self):
        return self.title
