from django.conf.urls import url
from . import views


app_name = 'openchat'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^chat/$', views.chat, name='chat'),
    # websocket 相关

]
