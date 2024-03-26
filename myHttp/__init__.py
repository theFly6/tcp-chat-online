"""
1.连接热点时本机的ipv4：192.168.xx.xx:8080
2.通过下面两种方式访问：192.168.xx.xx:8080/index?id=18
    (1)收到的浏览器的请求格式：
        GET /index?id=18 HTTP/1.1
        Host: 192.168.xx.xx:8080
        Connection: keep-alive
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
        Accept-Encoding: gzip, deflate
        Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
    (2)收到的来自python的requests库的请求格式：
        GET /index?id=18 HTTP/1.1
        Host: 192.168.xx.xx:8080
        User-Agent: python-requests/2.28.1
        Accept-Encoding: gzip, deflate
        Accept: */*
        Connection: keep-alive
    (3)收到来自手机的请求格式：
        GET /favicon.ico HTTP/1.1
        Host: 192.168.xx.xx:8080
        Connection: keep-alive
        User-Agent: Mozilla/5.0 (Linux; U; Android 13; zh-CN; V2001A Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/100.0.4896.58 Quark/6.10.0.510 Mobile Safari/537.36
        Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
        Accept-Encoding: gzip, deflate
        Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
        Cookie: __itrace_wid=2a577f13-9f45-45cc-89ff-cfa4795ebcf1
        Referer: http://192.168.xx.xx:8080/
3. POST方法的请求格式：
        POST /index?id=18 HTTP/1.1
        Host: 192.168.xx.xx:8080
        User-Agent: python-requests/2.28.1
        Accept-Encoding: gzip, deflate
        Accept: */*
        Connection: keep-alive
        Content-Length: 13
        Content-Type: application/x-www-form-urlencoded

        name=zhangsan&age=18
"""
import os
import urllib.parse

class Request:
    path = '',
    method = '',
    protocol = '',

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return '<myHttp.Request object>: {\n\t' + \
               ",\n\t".join([f"{key}: {value}" for key, value in self.__dict__.items()]) + \
               '\n}'

    @classmethod
    def parse_request(cls, request):
        lines = request.strip().split("\n")

        headers = {}
        method, path, protocol = lines[0].strip().split()
        for line in lines[1:]:
            if line.strip():
                if ': ' in line and len(line.split(": ")) == 2:
                    key, value = line.split(": ")
                    headers[key.strip()] = value.strip()
        # 解析请求数据
        data = {}
        if method == "POST" and "Content-Type" in headers and headers[
            "Content-Type"] == "application/x-www-form-urlencoded":
            request_data = lines[-1].strip()
            for item in request_data.split("&"):
                key, value = item.split("=")
                data[key] = value
        elif method == "GET" and '?' in path:
            request_data = path.split('?')[-1]
            request_data = urllib.parse.unquote(request_data)
            for item in request_data.split("&"):
                key, value = item.split("=")
                data[key] = value
        return cls(method=method, path=path, protocol=protocol, data=data, **headers)

import json
class JsonResponse:
    src = 'HTTP/1.1 {} {}\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {}\r\n\r\n{}'
    def __init__(self, d) -> None:
        self.status_code = 200
        self.message = 'OK'
        self.src = self.src.format(
            self.status_code,
            self.message,
            len(json.dumps(d)),
            json.dumps(d)
        ).encode()




class Response:
    SUCCESS = 200
    NOT_FOUND = 404
    status_code = ''
    content = ''
    target = ''
    message = ''
    src = 'HTTP/1.1 {} {}\n{}\n\n{}'

    def __init__(self, file_path: str, status_code=200, is_pic=False):
        """
        根据文件路径设置响应内容。
        如果文件存在，则设置内容为文件内容，否则抛出异常。
        """
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                content = file.read()
            self.status_code = status_code
            self.message = 'OK' if status_code == 200 else 'Not Found'
            self.target = os.path.realpath(file_path)
            self.content = content
        else:
            self.status_code = 404
            self.message = 'Not Found'
            self.target = os.path.realpath(file_path)
        if not is_pic:
            self.src = self.src.format(self.status_code, self.message, 'Access-Control-Allow-Origin: *',self.content.decode()).encode()
        else:
            self.src = self.src.format(self.status_code, self.message, 'Content-Type: image/jpeg\nAccess-Control-Allow-Origin: *', '').encode() + self.content

    def __str__(self):

        return '<myHttp.Request object>: {\n\t' + \
               ",\n\t".join([f"{key}: {value}" for key, value in self.__dict__.items()]) + \
               '\n}'


if __name__ == '__main__':
    TCP_DATA1 = '''
        GET /index?id=18 HTTP/1.1
        Host: 192.168.xx.xx:8080
        Connection: keep-alive
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
        Accept-Encoding: gzip, deflate
        Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
    '''
    TCP_DATA2 = '''
        GET /index?id=18 HTTP/1.1
        Host: 192.168.xx.xx:8080
        User-Agent: python-requests/2.28.1
        Accept-Encoding: gzip, deflate
        Accept: */*
        Connection: keep-alive
    '''
    TCP_DATA3 = '''GET /favicon.ico HTTP/1.1
        Host: 192.168.xx.xx:8080
        Connection: keep-alive
        User-Agent: Mozilla/5.0 (Linux; U; Android 13; zh-CN; V2001A Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/100.0.4896.58 Quark/6.10.0.510 Mobile Safari/537.36
        Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
        Accept-Encoding: gzip, deflate
        Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
        Cookie: __itrace_wid=2a577f13-9f45-45cc-89ff-cfa4795ebcf1
        Referer: http://192.168.xx.xx:8080/
    '''
    TCP_DATA4 = '''
        POST /index?id=18 HTTP/1.1
        Host: 192.168.xx.xx:8080
        User-Agent: python-requests/2.28.1
        Accept-Encoding: gzip, deflate
        Accept: */*
        Connection: keep-alive
        Content-Length: 13
        Content-Type: application/x-www-form-urlencoded
    
        name=zhangsan&age=18
    '''
    print('GET from local:\n', Request.parse_request(TCP_DATA1), sep='', end='\n\n')
    print('GET from python requests.get:\n', Request.parse_request(TCP_DATA2), sep='', end='\n\n')
    print('GET from mobile:\n', Request.parse_request(TCP_DATA3), sep='', end='\n\n')
    print('POST from python requests.get:\n', Request.parse_request(TCP_DATA4), sep='', end='\n\n')
