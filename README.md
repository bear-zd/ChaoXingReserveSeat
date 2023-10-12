# ChaoXingServerSeat
超星图书馆抢座脚本，在使用之前需要先在如下网站获取图书馆对应的id和座位号（需要手机端在对应网站进行抓包，下面的配置里有上大图书馆的id）
https://office.chaoxing.com/front/third/apps/seat/code?id={}&seatNum={}

## 注意

请拉取最新版程序运行。新字段enc使用py2js对加密的js脚本进行模拟，同时减少了环境依赖的安装。但是相较于之前的速度会较慢（后续有机会再尝试提高性能）


## setting 
运行脚本前先安装两个包（之前使用的pycrypto在3.11版本安装难度较高，所以修改依赖了） `pip install cryptography, py2js`

之后编辑config.json并填写相关信息即可
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
只需要使用crontab运行即可

## running

通过 `python main.py` 运行脚本, 添加参数 `-u config.json` 来指明配置文件路径

在Linux下可以使用如下方式添加crontab , 运行：`crontab -e`添加指令 :`0 7 * * * python3 main.py`

windows下使用时间任务:

![](https://zideapicbed.oss-cn-shanghai.aliyuncs.com/QQ%E5%9B%BE%E7%89%8720221120213736.png)
