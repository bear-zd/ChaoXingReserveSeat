
import json
import time
import argparse
import os

from utils import reserve
get_current_time = lambda action: time.strftime("%H:%M:%S", time.localtime(time.time() + 8*3600)) if action else time.strftime("%H:%M:%S", time.localtime(time.time()))
get_current_dayofweek = lambda action: time.strftime("%A", time.localtime(time.time() + 8*3600)) if action else time.strftime("%A", time.localtime(time.time()))


SLEEPTIME = 0.2 # 每次抢座的间隔
ENDTIME = "07:01:00" # 根据学校的预约座位时间+1min即可

ENABLE_SLIDER = True # 是否有滑块验证
MAX_ATTEMPT = 4 # 最大尝试次数

                

def login_and_reserve(users, usernames, passwords, action, success_list=None):
    if len(usernames.split(",")) != len(users):
        raise Exception("user number should match the number of config")
    if success_list is None:
        success_list = [False] * len(users)
    current_dayofweek = get_current_dayofweek(action)
    for index, user in enumerate(users):
        username, password, times, roomid, seatid, dayofweek = user.values()
        if action:
            username, password = usernames.split(',')[index], passwords.split(',')[index]
        if(dayofweek != current_dayofweek):
            continue
        if not success_list[index]: 
            s = reserve(sleep_time=SLEEPTIME, enable_slider=ENABLE_SLIDER)
            s.get_login_status()
            s.login(username, password)
            s.requests.headers.update({'Host': 'office.chaoxing.com'})
            suc = s.submit(times, roomid, seatid, action)
            success_list[index] = suc
    return success_list


def main(users, action=False):
    current_time = get_current_time(action)
    print(f"start time {current_time}")
    attempt_times = 0
    try:
        usernames = os.environ['USERNAMES'] if action else ""
        passwords = os.environ['PASSWORDS'] if action else ""
    except KeyError:
        print("github secret keys not config correctly.")
        return 
    success_list = None
    current_dayofweek = get_current_dayofweek(action)
    today_reservation_num = sum(1 for d in users if d.get('dayofweek') == current_dayofweek)
    while current_time < ENDTIME:
        attempt_times += 1
        try:
            success_list = login_and_reserve(users, usernames, passwords, action, success_list)
        except Exception as e:
            print(f"An error occurred: {e}")
        print(f"attempt time {attempt_times}, time now {current_time}, success list {success_list}")
        current_time = get_current_time(action)
        if sum(success_list) == today_reservation_num:
            print(f"reserved successfully!")
            return

def debug(users, action):
    suc = False
    if action:
        usernames = os.environ['USERNAMES']
        passwords = os.environ['PASSWORDS']
    current_dayofweek = get_current_dayofweek(action)
    for index, user in enumerate(users):
        username, password, times, roomid, seatid, dayofweek = user.values()
        if action:
            username ,password = usernames.split(',')[index], passwords.split(',')[index]
        if(dayofweek != current_dayofweek):
            continue
        s = reserve(sleep_time=SLEEPTIME, enable_slider=ENABLE_SLIDER)
        s.get_login_status()
        s.login(username, password)
        s.requests.headers.update({'Host': 'office.chaoxing.com'})
        suc = s.submit(times, roomid, seatid, action)
        if suc:
            return

def get_roomid(**kwargs):
    username = input("请输入用户名：")
    password = input("请输入密码：")
    s = reserve(sleep_time=SLEEPTIME, enable_slider=ENABLE_SLIDER)
    s.get_login_status()
    s.login(username=username, password=password)
    s.requests.headers.update({'Host': 'office.chaoxing.com'})
    encode = input("请输入deptldEnc：")
    s.roomid(encode)


if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    parser = argparse.ArgumentParser(prog='Chao Xing seat auto reserve')
    parser.add_argument('-u','--user', default=config_path, help='user config file')
    parser.add_argument('-m','--method', default="reserve" ,choices=["reserve", "debug", "room"], help='for debug')
    parser.add_argument('-a','--action', action="store_true",help='use --action to enable in github action')
    args = parser.parse_args()
    func_dict = {"reserve": main, "debug":debug, "room": get_roomid}
    with open(args.user, "r+") as data:
        usersdata = json.load(data)["reserve"]
    func_dict[args.method](usersdata, args.action)
