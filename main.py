import json
import time
import login
import os

def start(add=False):
    if len(os.listdir('./user/')) == 0 or add:
        print("请输入手机号")
        phone = input(">> ")
        if login.sendCode(phone):
            print('我们向你的手机号发送了一个验证码，请输入')
            vcode = input(">> ")
            if login.verifyCode(phone,vcode)[0]:
                print('登录成功！')
                tk = login.verifyCode(phone, vcode)[1]
                # 导入配置
                json_import = json.loads('{"phone": "' + phone + '", "token": "' + tk + '","delay": 60}')
                with open(f'./user/{phone}.json', 'wt') as f:
                    json.dump(json_import, f)
            else:
                print('检查你的验证码是否输入正确')
        else:
            print('可能出错了')
        
    else:
        print('你当前可以选用的账号如下（输入数字选择）-1新增')
        userlist = os.listdir('./user/')
        for i in range(len(userlist)):
            print(f'[{i}] {userlist[i]}')
        select = input('>> ')
        if select == '-1':
            start(True)
        else:
            print('选择成功！！！')
            with open(f'./user/{userlist[int(select)]}', 'r') as f:
                config = json.load(f)
            token = config['token']
            delay = config['delay']
            print("请选择你需要蹲的机器类型")
            print('[0] 洗衣机')
            print('[1] 烘干机')
            types = int(input('>> '))
            mctype = ['洗衣机', '烘干机']
            print('选择成功！')
            print('请输入你想要蹲几号楼的机器，数字即可')
            lh = f"城院{input('>> ')}号楼"
            print('蹲蹲已经开始蹲啦，届时会有消息提示，请注意查看')
            flag = True
            while flag:
                data = login.getMacState(types, token)
                for i in data:
                    if lh in i:
                        print(i)
                        login.show_notification('蹲蹲机', '成功蹲到了 ' + lh + ' 的 ' + mctype[types] + ' 请尽快前往！')
                        flag = False
                time.sleep(delay)


if __name__ == '__main__':
    print("欢迎使用 蹲蹲小助手 帮你解决烦恼")
    start()
