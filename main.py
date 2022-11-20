"""
滑动验证码解决
"""
import time
import json
import base64
import os
import requests, re
from binascii import b2a_hex, a2b_hex, b2a_base64

import random, time, datetime, json, http.cookiejar

from urllib3.exceptions import InsecureRequestWarning

# user_name, password, times_dict, room, seat, email
stu_dect = [
    ("0wL5SUvL9VE0A1aczcHVkQ==", "eaqOa84KlXUQHC91SGrKGQ==", [("09:00", "22:00")], '2609', '242', "xxxxxxxxxxxxxxxxx@163.com")
]


class tieba_login:
    def __init__(self):
        self.sut_dect = stu_dect
        self.login_page = "https://passport2.chaoxing.com/mlogin?loginType=1&newversion=true&fid="
        self.url = "https://office.chaoxing.com/front/third/apps/seat/code?id={}&seatNum={}"
        self.is_can_appoint_url = "https://office.chaoxing.com/data/apps/seat/room/info"
        self.submit_url = "https://office.chaoxing.com/data/apps/seat/submit"
        self.seat_url = "https://office.chaoxing.com/data/apps/seat/getusedtimes"
        self.login_url = "https://passport2.chaoxing.com/fanyalogin"
        self.token = ""
        self.success_times = 0
        self.fail_dict = []
        self.submit_msg = []
        self.start_time = None
        self.end_time = None
        self.requests = requests.session()
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.3 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 wechatdevtools/1.05.2109131 MicroMessenger/8.0.5 Language/zh_CN webview/16364215743155638",
            "X-Requested-With": "com.tencent.mm"
        }
        self.login_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.3 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 wechatdevtools/1.05.2109131 MicroMessenger/8.0.5 Language/zh_CN webview/16364215743155638",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "passport2.chaoxing.com"
        }
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def get_html(self, url):
        response = self.requests.get(url=url, verify=False)
        html = response.content.decode('utf-8')
        token = re.findall('token: \'(.*?)\'', html)[0] if len(re.findall('token: \'(.*?)\'', html)) > 0 else ""

        return token

    def get_login_html(self):
        self.requests.headers = self.login_headers
        response = self.requests.get(url=self.login_page, verify=False)
        html = response.content.decode('utf-8')
        # print(html)

    def get_submit(self, url, seat, token, roomid, seatid, captcha):
        day = datetime.date.today() + datetime.timedelta(days=0)  # 预约明天
        # day = datetime.date.today()
        parm = {
            "roomId": roomid,
            "day": str(day),
            "startTime": seat[0],
            "endTime": seat[1],
            "seatNum": seatid,
            "token": token,
            "captcha": "",
            "type": 1
        }
        print(parm)
        html = self.requests.post(url=url, params=parm, verify=False).content.decode('utf-8')
        self.submit_msg.append(seat[0] + "~" + seat[1] + ':  ' + str(json.loads(html)))
        print(self.submit_msg)
        print(html)
        return json.loads(html)["success"]

    def get_seat(self, url, roomid, seatid):
        parm = {
            "roomId": roomid,
            "day": str(datetime.date.today()),
            "seatNum": seatid
        }
        html = self.requests.post(url=url, params=parm, verify=False).content.decode('utf-8')



    # 登录
    def login(self, username, password):


        parm = {
            "fid": -1,
            "uname": username,
            "password": password,
            "refer": "http%3A%2F%2Foffice.chaoxing.com%2Ffront%2Fthird%2Fapps%2Fseat%2Fcode%3Fid%3D4219%26seatNum%3D380",
            "t": True
        }
        jsons = self.requests.post(url=self.login_url, params=parm, verify=False)
        obj = jsons.json()
        print(obj)
        if obj['status']:
            return (True, '')
        else:
            return (False, obj['msg2'])

    def submit(self, i, roomid, seatid):
        flag = 3
        suc = False
        while flag > 1 and ~suc:
            token = self.get_html(self.url.format(roomid, seatid))
            # captcha = self.getSlideResult(roomid, seatid)
            suc = self.get_submit(self.submit_url, i, token, roomid, seatid,0)
            flag -= 1

    def submit_final(self, seat_dict, roomid, seatid):
        self.start_time = time.time()
        # executor1 = ThreadPoolExecutor()
        for i in seat_dict:
            self.submit(i, roomid, seatid)
        self.end_time = time.time()


def loginaction(username, password):
    s = tieba_login()
    s.get_login_html()
    result = s.login(username, password)
    return result


def run(username, password, timeArr, roomid, seatid, email):
    s = tieba_login()
    s.get_login_html()
    s.login(username, password)
    s.requests.headers.update({'Host': 'office.chaoxing.com'})
    s.submit_final(timeArr, roomid, seatid)
    #time.sleep(3)
    #s.send(email, username)
    return None




def tesT(username, password, roomid, seatid):
    s = tieba_login()
    s.get_login_html()
    s.login(username, password)
    s.requests.headers.update({'Host': 'office.chaoxing.com'})
    # s.getSlideResult(roomid, seatid)

def main():
    run(stu_dect[0][0], stu_dect[0][1], stu_dect[0][2], stu_dect[0][3], stu_dect[0][4], stu_dect[0][5])


if __name__ == "__main__":
    main()

