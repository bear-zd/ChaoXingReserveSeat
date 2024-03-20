
from utils import AES_Encrypt, enc, captcha_key_and_token
import json
import requests
import re
import time
import datetime
from urllib3.exceptions import InsecureRequestWarning

class reserve:
    def __init__(self, sleep_time=0.2, max_attempt=5, enable_slider=False):
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

        self.sleep_time = sleep_time
        self.max_attempt = max_attempt
        self.enable_slider = enable_slider

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def _get_token(self, url):
        response = self.requests.get(url=url, verify=False)
        html = response.content.decode('utf-8')
        token = re.findall(
            'token: \'(.*?)\'', html)[0] if len(re.findall('token: \'(.*?)\'', html)) > 0 else ""
        
        return token

    def get_login_status(self):
        self.requests.headers = self.login_headers
        self.requests.get(url=self.login_page, verify=False)

    def get_submit(self, url, times, token, roomid, seatid, captcha="", action=False):
        day = datetime.date.today() + datetime.timedelta(days=0)  # 预约今天，修改days=1表示预约明天
        if action:
            day = datetime.date.today() + datetime.timedelta(days=1)  # 预约今天，修改days=1表示预约明天
        parm = {
            "roomId": roomid,
            "startTime": times[0],
            "endTime": times[1],
            "day": str(day),
            "seatNum": seatid,
            "captcha": captcha,
            "token": token
        }
        parm["enc"] = enc(parm)
        html = self.requests.post(
            url=url, params=parm, verify=True).content.decode('utf-8')
        self.submit_msg.append(
            times[0] + "~" + times[1] + ':  ' + str(json.loads(html)))
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


    def submit(self, times, roomid, seatid, action):
        for seat in seatid:
            suc = False
            while ~suc and self.max_attempt > 0:
                token = self._get_token(self.url.format(roomid, seat))
                captcha = self.resolve_captcha(token) if self.enable_slider else "" 
                suc = self.get_submit(self.submit_url, times,
                                      token, roomid, seat, captcha, action)
                if suc:
                    return suc
                time.sleep(self.sleep_time)
                self.max_attempt -= 1
        return suc
    
    def roomid(self, encode):
        url = f"https://office.chaoxing.com/data/apps/seat/room/list?cpage=1&pageSize=100&firstLevelName=&secondLevelName=&thirdLevelName=&deptIdEnc={encode}"
        json_data = self.requests.get(url=url).content.decode('utf-8')
        ori_data = json.loads(json_data)
        for i in ori_data["data"]["seatRoomList"]:
            info = f'{i["firstLevelName"]}-{i["secondLevelName"]}-{i["thirdLevelName"]} id为：{i["id"]}'
            print(info)
    def resolve_captcha(self, roomid, page_token, action):
        captcha_token, bg, tp = self.get_slide_captcha_data(roomid, page_token, action)
        x = self.x_distance(bg, tp)
        headers = {
            "Referer": "https://reserve.chaoxing.com/"
        }
        params = {
            "callback": "jQuery33105878581853212221_1698141785783",
            "captchaId": "42sxgHoTPTKbt0uZxPJ7ssOvtXr3ZgZ1",
            "type": "slide",
            "token": captcha_token,
            "textClickArr": json.dumps([{"x": x}]),
            "coordinate": json.dumps([]),
            "runEnv": "10",
            "version": "1.1.14",
            "_": int(time.time() * 1000)
        }
        response = self.session.get(
            f'https://captcha.chaoxing.com/captcha/check/verification/result', params=params, headers=headers)
        text = response.text.replace('jQuery33105878581853212221_1698141785783(', "").replace(')', "")
        # 解析出验证签名
        data = json.loads(text)
        return json.loads(data["extraData"])['validate']

    def get_slide_captcha_data(self, roomid, page_token, action):
        url = "https://captcha.chaoxing.com/captcha/get/verification/image"
        day = datetime.date.today() + datetime.timedelta(days=0) if not action else datetime.date.today() + datetime.timedelta(days=1)  # 预约今天，修改days=1表示预约明天
        timestamp = int(time.time() * 1000)
        capture_key, token = captcha_key_and_token(timestamp)
        referer = f"https://reserve.chaoxing.com/front/third/apps/seat/select?id={roomid}&day={str(day)}&backLevel=2&pageToken={page_token}"

        params = {
            "callback": "jQuery33105878581853212221_1698141785783",
            "captchaId": "42sxgHoTPTKbt0uZxPJ7ssOvtXr3ZgZ1",
            "type": "slide",
            "version": "1.1.14",
            "captchaKey": capture_key,
            "token": token,
            "referer": referer,
            "_": timestamp
        }
        response = self.requests.get(url=url, params=params)
        content = response.text()
        data = content.replace("jQuery33105878581853212221_1698141785783(",
                            ")").replace(")", "")
        data = json.loads(data)
        captcha_token = data["token"]
        bg = data["imageVerificationVo"]["shadeImage"]
        tp = data["imageVerificationVo"]["cutoutImage"]
        return captcha_token, bg, tp
    
    def x_distance(self, bg, tp):
        import numpy as np
        import cv2
        def cut_slide(slide):
            slider_array = np.frombuffer(slide, np.uint8)
            slider_image = cv2.imdecode(slider_array, cv2.IMREAD_UNCHANGED)
            slider_part = slider_image[:, :, :3]
            mask = slider_image[:, :, 3]
            mask[mask != 0] = 255
            x, y, w, h = cv2.boundingRect(mask)
            cropped_image = slider_part[y:y + h, x:x + w]
            return cropped_image
        bgc, tpc = self.requests.get(bg), self.requests.get(tp)
        bg, tp = bgc.content.read(), tpc.content.read() 
        bg_img = cv2.imdecode(np.frombuffer(bg, np.uint8), cv2.IMREAD_COLOR)  # 背景图片
        tp_img = cut_slide(tp)
        bg_edge = cv2.Canny(bg_img, 100, 200)
        tp_edge = cv2.Canny(tp_img, 100, 200)
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
        tl = max_loc
        return tl[0]