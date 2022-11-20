# ChaoXingSnatchSeat
A python script in order to snatch seat from the chaoxing Library seat reserve.

## setting 
before running the script , you should install a package `pip install pycrypto`

and edit the config.json to make this script work.
```json
{
    "reserve": [
        {"username": "XXXXXXXX", //https://passport2.chaoxing.com/mlogin?loginType=1&newversion=true&fid=&  login this website to make sure your username and password is usable  
        "password": "XXXXXXXX",
        "time": ["08:00","22:00"], // the time between your start and end
        "roomid":"2609", //2609:四楼外圈,5483:四楼内圈,2610:五楼外圈,5484:五楼内圈
        "seatid":"002" // make sure the seat id format is right. "6" is not equal to "006"
        },
        {"username": "xxxxxxx",
        "password": "xxxxxxxxxx",
        "time": ["21:00","22:00"],
        "roomid":"2609",
        "seatid":"002"
        }
        ]
}
```
What you should do is just set a crontab on your server to run this script.

## running

Use `python main.py` to run this script, add arguement `-u config.json` to point the config file posision

In linux , you can just set a crontab : `crontab -e` and add the command :`0 7 * * * python3 main.py`

In windows, you can add a time task:

![](https://zideapicbed.oss-cn-shanghai.aliyuncs.com/QQ%E5%9B%BE%E7%89%8720221120213736.png)