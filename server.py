from urls import process_urls
from setting import SERVER_ADDRESS
import socket


class Server:
    clients = []
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(SERVER_ADDRESS)

    def run(self):
        # 开始监听连接请求
        self.server_socket.listen()
        print(f'Server is running at http://{SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}...')
        while True:
            # 等待客户端连接请求
            client_socket, client_address = self.server_socket.accept()
            try:
                # 接收客户端发送的TCP数据报
                raw_request = client_socket.recv(1024)
                print(f'Received data from {client_address}',raw_request.decode().split('\n')[0])
                # 根据用户发送的数据请求调用对应的处理函数
                process_urls(raw_request.decode(), self.server_socket, client_socket)
            except Exception as e:
                print('Error:', e)

            # 关闭连接
            client_socket.close()
