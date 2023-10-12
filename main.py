
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
from pyjs import encode

def AES_Encrypt(data):
    key = b"u2oh6Vu^HWe4_AES"  # Convert to bytes
    iv = b"u2oh6Vu^HWe4_AES"  # Convert to bytes
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode('utf-8')) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    enctext = base64.b64encode(encrypted_data).decode('utf-8')
    return enctext

import json
import base64
import requests
import re
import time
import datetime
import json
from urllib3.exceptions import InsecureRequestWarning
import argparse
import os

SLEEPTIME = 0.2
ENDTIME = "07:01:00"




class reserve:
    def __init__(self):
        self.login_page = "https://passport2.chaoxing.com/mlogin?loginType=1&newversion=true&fid="
        self.url = "https://office.chaoxing.com/front/third/apps/seat/code?id={}&seatNum={}"
        self.submit_url = "https://office.chaoxing.com/data/apps/seat/submit"
        self.seat_url = "https://office.chaoxing.com/data/apps/seat/getusedtimes"
        self.login_url = "https://passport2.chaoxing.com/fanyalogin"
        self.token = ""
        self.success_times = 0
        self.fail_dict = []
        self.submit_msg = []
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
        token = re.findall(
            'token: \'(.*?)\'', html)[0] if len(re.findall('token: \'(.*?)\'', html)) > 0 else ""
        
        return token

    def get_login_status(self):
        self.requests.headers = self.login_headers
        self.requests.get(url=self.login_page, verify=False)

    def get_submit(self, url, seat, token, roomid, seatid, captcha):
        day = datetime.date.today() + datetime.timedelta(days=0)  # 预约今天，修改days=1表示预约明天
        enc = encode(roomid, str(day), seat[0],seat[1],seatid,token)
        parm = {
            "roomId": roomid,
            "day": str(day),
            "startTime": seat[0],
            "endTime": seat[1],
            "seatNum": seatid,
            "token": token,
            "captcha": "",
            "type":1,
            "verifyData":1,
            "enc":enc

        }
        print(parm)
        html = self.requests.post(
            url=url, params=parm, verify=True).content.decode('utf-8')
        self.submit_msg.append(
            seat[0] + "~" + seat[1] + ':  ' + str(json.loads(html)))
        print(json.loads(html))
       
        return json.loads(html)["success"]

    def login(self, username, password):
        username = AES_Encrypt(username)
        password = AES_Encrypt(password)
        parm = {
            "fid": -1,
            "uname": username,
            "password": password,
            "refer": "http%3A%2F%2Foffice.chaoxing.com%2Ffront%2Fthird%2Fapps%2Fseat%2Fcode%3Fid%3D4219%26seatNum%3D380",
            "t": True
        }
        jsons = self.requests.post(
            url=self.login_url, params=parm, verify=False)
        obj = jsons.json()
        if obj['status']:
            return (True, '')
        else:
            return (False, obj['msg2'])

    def submit(self, i, roomid, seatid):
        for seat in seatid:
            suc = False
            remaining_times_for_seat = 2 # 每一个的座位尝试次数
            while ~suc and remaining_times_for_seat > 0:
                token = self.get_html(self.url.format(roomid, seat))
                suc = self.get_submit(self.submit_url, i,
                                      token, roomid, seat, 0)
                if suc:
                    return suc
                time.sleep(SLEEPTIME)
                remaining_times_for_seat-=1
        return suc    
                

def main(users):
    current_time = time.strftime("%H:%M:%S", time.localtime())
    suc = False
    while current_time < ENDTIME:
        for user in users:
            username, password, times, roomid, seatid = user.values()
            s = reserve()
            s.get_login_status()
            s.login(username, password)
            s.requests.headers.update({'Host': 'office.chaoxing.com'})
            suc = s.submit(times, roomid, seatid)
            if suc:
                continue
        current_time = time.strftime("%H:%M:%S", time.localtime())

def debug(users):
        for user in users:
            username, password, times, roomid, seatid = user.values()
            s = reserve()
            s.get_login_status()
            s.login(username, password)
            s.requests.headers.update({'Host': 'office.chaoxing.com'})
            suc = s.submit(times, roomid, seatid)
            if suc:
                return


if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    parser = argparse.ArgumentParser(prog='Chao Xing seat auto reserve')
    parser.add_argument('-u','--user', default=config_path, help='user config file')
    parser.add_argument('-d','--debug', default=False, help='for debug')
    args = parser.parse_args()
    with open(args.user, "r+") as data:
        usersdata = json.load(data)["reserve"]
    if args.debug:
        debug(usersdata)
    else:
        main(usersdata)
