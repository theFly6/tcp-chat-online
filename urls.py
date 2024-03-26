import views
import socket
from myHttp import Request

urlpatterns = {
    '/': views.index,
    '/index': views.index,
    '/login/client': views.login,
    '/sent/message': views.load_message,
    '/fresh/message': views.fresh_message,
    '/logout': views.logout,
}


def process_urls(raw_request: str, server: socket.socket, client: socket.socket):
    req = Request.parse_request(raw_request)
    # 图片静态资源
    if req.path[:11] == '/static/img':
        func = views.load_img
    # 静态js、css资源
    elif req.path[:7] == '/static':
        func = views.load_static
    # 其余静态HTML、JSON资源
    else:
        func = urlpatterns.get(req.path.split('?')[0], None)
    if func is not None:
        response = func(req)
        if response.status_code == 200:
            client.sendall(response.src)
            return None
    # 如果不是请求的上述资源就报404错误
    res_404 = views.wrong()
    client.sendall(res_404.src)

