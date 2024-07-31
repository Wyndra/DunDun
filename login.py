import os
import platform
from plyer import notification
import requests
import json


def sendCode(phone):
    url = "https://userapi.qiekj.com/common/sms/sendCode"

    payload = f"phone={phone}&template=reg"
    headers = {
        'Host': 'userapi.qiekj.com',
        'channel': 'ios_app',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Cookie': 'SERVERID=f2b5f835c45a6ca30a9d3ff318bef498|1687271707|1687271654; '
                  'acw_tc=781bad3416872716540207737e51e812c531a8ba6c0c4f4ce9c92f7c6340ef; '
                  'SERVERID=f2b5f835c45a6ca30a9d3ff318bef498|1687272051|1687271654',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Version': '1.28.2',
        'User-Agent': 'QEUser/1.28.2 (com.qiekj.QEUser; build:2; iOS 16.5.0) Alamofire/5.6.4',
        'Accept-Language': 'zh-Hant-HK;q=1.0, zh-Hans-CN;q=0.9, en-CN;q=0.8, en-GB;q=0.7, ja-CN;q=0.6, '
                           'yue-Hant-CN;q=0.5',
        'Accept-Encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
        'Content-Length': '30'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    state = json.loads(response.text)['msg']
    if state == '成功':
        return True
    else:
        return False


def verifyCode(phone, code):
    print(phone, code)
    # 成功即刻返回token
    url = "https://userapi.qiekj.com/user/reg"

    payload=f'channel=ios_app&phone={phone}&verify={code}'
    headers = {
        'Accept': '*/*',
        'Content-Length': '45',
        'Host': 'userapi.qiekj.com',
        'channel': 'ios_app',
        'Accept-Encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-Hant-HK;q=1.0, zh-Hans-CN;q=0.9, en-CN;q=0.8, en-GB;q=0.7, ja-CN;q=0.6, yue-Hant-CN;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Cookie': 'SERVERID=6fda55701a8e85b8ca777fbce1ef92f1|1705755386|1705755295; acw_tc=76b20fea17057539561948022e63a0fa0dce826b58ffaa6dc69c881ae98218; SERVERID=6fda55701a8e85b8ca777fbce1ef92f1|1705758344|1705758344',
        'Version': '1.40.1'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        result = json.loads(response.text)
        print(result)
    except json.JSONDecodeError as e:
        print(response.text)
        return [False, 'error']
    state = result['msg']
    if state == '成功':
        tk = result['data']['token']
        return [True, tk]
    else:
        return [False, 'error']


def getMacState(t, tk, ):
    result = []
    url = "https://userapi.qiekj.com/machineModel/near/machines"
    machines = ['c9892cb4-bd78-40f6-83c2-ba73383b090a', '4a245cde-538b-47d8-aa35-dd4a28c0e901']
    payload = f"goodsPage=1&machineTypeId={machines[t]}&pageSize=20&shopId=201901021533390000082157&token={tk}"
    headers = {
        "Host": "userapi.qiekj.com",
        "channel": "ios_app",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Cookie": "SERVERID=40512ddb9a12b9ada666a84a5b904e8b|1687262213|1687262096; "
                  "acw_tc=781bad3716872606990245450e4632350e42cef70895d1776d5c985de95ec7; "
                  "SERVERID=40512ddb9a12b9ada666a84a5b904e8b|1687262479|1687262096",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Version": "1.28.2",
        "User-Agent": "QEUser/1.28.2 (com.qiekj.QEUser; build:2; iOS 16.5.0) Alamofire/5.6.4",
        "Accept-Language": "zh-Hant-HK;q=1.0, zh-Hans-CN;q=0.9, en-CN;q=0.8, en-GB;q=0.7, ja-CN;q=0.6, "
                           "yue-Hant-CN;q=0.5",
        "Accept-Encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
        "Content-Length": "145"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    jsonroot = json.loads(response.text)['data']['items']
    for item in jsonroot:
        result.append(item['name'])
    return result


def show_notification(title, text):
    sysstr = platform.system()
    if sysstr == "Darwin":
        os.system(
            """osascript -e 'display notification "{}" with title "{}"'""".format(text, title))
    else:
        notification.notify(
            title=title,
            message=text,
            timeout=10, )
