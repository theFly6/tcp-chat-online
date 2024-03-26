from myHttp import Request, Response, JsonResponse


def wrong(*args):
    return Response('templates/404.html', status_code=404)


def index(req: Request):
    if req.method == 'GET':
        return Response('templates/index.html')


def load_static(req: Request):
    # print('static: ', req)
    if req.method == 'GET':
        return Response(req.path[1:])


def load_img(req: Request):
    if req.method == 'GET':
        return Response(req.path[1:], is_pic=True)


# 十张可用用户头像随机分配
def get_str_mode_n(s, n=10):
    # 将字符串转换为十进制数
    decimal_value = sum(ord(char) for char in s)
    # 对十进制数取模n
    result = decimal_value % n
    return f'{result+1:02d}'

def sys_message(name, choice=0):
    messages = [
        f'{name}进入了聊天室',
        f'{name}离开了聊天室',
    ]
    res = {
        'chat_type': 'system_info',
        'message': messages[choice]
    }
    return res


user_list = []  # 保存大厅内的用户
                #     'user_list': [{
                #                     'name': '张三',
                #                     'img': '03'
                #                 }, 
                #                 {
                #                     'name': '李四',
                #                     'img': '04'
                #                 }, {
                #                     'name': '王二',
                #                     'img': '02'
                #                 }],
room_chat = []  # 保存大厅中的聊天记录
                #     'room_chat': [{
                #                     'chat_type': 'system_info',
                #                     'message': '张三加入了群聊'
                #                 },
                #                 {
                #                     'chat_type': 'comment',
                #                     'name': '张三',
                #                     'img': '03',
                #                     'message': '大家好, 我是法外狂徒'
                #                 }]
priv_chat = dict()  # 记录任意两个人之间的聊天记录
                # priv_chat = {
                #     'a b':[{
                #         'chat_type': 'comment',
                #         'name': 'a',
                #         'img': '08',
                #         'message': '你好，我是a'
                #     },
                #     {
                #         'chat_type': 'comment',
                #         'name': 'b',
                #         'img': '09',
                #         'message': '你好，我是b'
                #     }]
                # }
def login(req: Request):
    print(req)
    if req.method == 'GET':
        req_name = req.data['nickname']
        req_img  = get_str_mode_n(req_name)
        req_user = {
            'name': req_name,
            'img': req_img
        }
        # 如果用户已注册就报错
        if(req_user in user_list):
            return JsonResponse({'status': False})
        
        # 如果是新用户就将其加入用户列表并在大厅提示信息
        user_list.append(req_user)
        room_chat.append(sys_message(req_name))
        data = {
            'status': True,
            'user_list': user_list,
            'room_chat': room_chat,
            'img': req_img
        }
        return JsonResponse(data)
    
def logout(req: Request):
    if req.method == 'GET':
        req_name = req.data['nickname']
        req_img  = get_str_mode_n(req_name)
        req_user = {
            'name': req_name,
            'img': req_img
        }
        if(req_user in user_list):
            user_list.remove(req_user)
            room_chat.append(sys_message(req_name,1))
        data = {
            'status': True
        }
        return JsonResponse(data)

# 根据目前的聊天对象'room' or 'xxx'
# 返回聊天信息内容列表
def load_message(req: Response):
    if req.method == 'GET':
        piece = {
            'chat_type': 'comment',
            'name': req.data['nickname'],
            'img': req.data['img'],
            'message': req.data['message']
        }
        data = {
            'status': True,
            'priv_chat': [],
            'room_chat': []
        }
        if req.data['chat_obj'] == 'room':
            room_chat.append(piece)
            data['room_chat']=room_chat
        else:
            coversation = [req.data['nickname'], req.data['chat_obj']]
            key = ' '.join(sorted(coversation))
            if priv_chat.get(key, False):
                priv_chat[key].append(piece)
                data['priv_chat']=priv_chat[key]
            else:
                priv_chat[key] = [piece]
                data['priv_chat']= priv_chat[key]
        return JsonResponse(data) 
        

def fresh_message(req):
    if req.method == 'GET':
        data = {
            'status': True,
            'priv_chat': [],
            'room_chat': [],
            'user_list': user_list,
        }
        if req.data['chat_obj'] == 'room':
            data['room_chat']=room_chat
        else:
            coversation = [req.data['nickname'], req.data['chat_obj']]
            key = ' '.join(sorted(coversation))
            if priv_chat.get(key, False):
                data['priv_chat']=priv_chat[key]
        return JsonResponse(data) 