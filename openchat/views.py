from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from .models import Room


# Create your views here.
def index(request):
    '''
    渲染聊天室的首页
    '''
    return render(request, 'index.html')


def login(request):
    '''
    获取昵称
    '''
    if request.method == 'POST':
        name = request.POST.get('name', '')
        if name != '':
            request.session['name'] = name
            return redirect('/chat')
        else:
            return HttpResponse('请输入聊天昵称')


def chat(request):
    '''
    聊天页面的封装
    返回当前系统内所有的聊天室
    '''
    rooms = Room.objects.all()
    try:
        name = request.session['name']
        return render(request, 'chat.html', {'rooms': rooms, })
    except:
        return redirect('/index')


# def joined(request):
#     '''
#     当有人进入聊天室之后，会从客户端发送一条加入房间的信息
#     并且这个条信息会向所有在当前频道的人广播
#     '''
#     while True:
#         message = request.websocket.wait()
#         request.websocket.send('return' + message)
