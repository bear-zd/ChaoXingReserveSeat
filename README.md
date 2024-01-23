# ChaoXingServerSeat
超星图书馆座位预约脚本

## 注意

请拉取最新版程序运行。新字段enc使用py2js对加密的js脚本进行模拟，同时减少了环境依赖的安装。但是相较于之前的速度会较慢（后续有机会再尝试提高性能）

目前版本不支持滑块验证（

## 如何使用

### 本地部署方式

#### 1、安装依赖

运行脚本前先安装两个包（之前使用的pycrypto在3.11版本安装难度较高，所以修改依赖了） 需要python<=3.11 (在python3.12版本下js2py会报错)

```bash
pip install cryptography, js2py
```

#### 2、 获取roomid（图书馆id）和seatid（座位号）

在使用之前需要先在如下获取图书馆对应的id和座位号，下面的配置里已经提供了上海大学图书馆的id。对于不知道id的，可以通过如下方式进行：

![image-20231012153826054](https://zideapicbed.oss-cn-shanghai.aliyuncs.com/img/image-20231012153826054.png)

在进入预约图书馆列表界面时断开网络，点击你想预约的图书馆的`选座`按钮，会提示网页无法打开，此时点击`右上角的三条杠`，选择`复制链接`，会得到类似这样的链接：

> https://office.chaoxing.com/front/apps/seat/select?id=5483&day=2023-10-12&backLevel=2&pageToken=0f46f3acc7be4c60862cb9815870ddfd

其中的`id=5483`的5483即为对应图书馆的id，将其填写到config.json中，座位联网后自己挑即可（详细填写参见后面的setting）

#### 3、running

由于脚本是检测系统时间为7点时进行预约（在main.py 第13行），如果有特殊要求可以修改。通过 `python main.py` 运行脚本, 添加参数 `-u config.json` 来指明配置文件路径

运行`python main.py -m debug`可以立即运行查看配置是否正确。

关于运行的方式，现在提供了多种运行方式：

- Linux环境下：

在Linux下可以使用如下方式添加crontab , 运行：`crontab -e`添加指令 :`0 7 * * * python3 main.py`

- windows环境下：

windows下使用时间任务:

![](https://zideapicbed.oss-cn-shanghai.aliyuncs.com/QQ%E5%9B%BE%E7%89%8720221120213736.png)

### github actions部署方式（目前应该没有问题了）：

  这种方式可以不需要在本地部署环境，只需要把fork该仓库并修改配置文件即可。

1.**fork该仓库**

2.**修改config.json**：这个仿照之前的方式进行修改即可，但是注意，username和password请留空或者随便填以防止泄漏个人账号密码。（具体的需要填写在自己repo的settings中）。时间什么也是需要修改（修改到仓库中）不要忘记。

3.**配置账号密码**：在settings->secrets and variables->Repository secrets 创建两个secret keys。名称分别为USERNAMES，PASSWORDS，填写自己的账号和密码即可。（如果有多个用户，请使用,(英文逗号)隔开，如果密码中有逗号可能会出现问题）。

```
xxxxxxx,xxxxxxx
```

4.**运行action**：在action -> auto_reserve -> run workflows 选择main分支即可。


## config配置
之后编辑config.json并填写相关信息即可
```json
{
    "reserve": [
        {"username": "XXXXXXXX", //https://passport2.chaoxing.com/mlogin?loginType=1&newversion=true&fid=&  在这个网站查看是否可以顺利登陆 
        "password": "XXXXXXXX",
        "time": ["08:00","22:00"], // 预约的起始时间
        "roomid":"2609", //2609:四楼外圈,5483:四楼内圈,2610:五楼外圈,5484:五楼内圈
        "seatid":"002" // 注意要用0补全至3位数，例如6号座位应该填006
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
参考前面的运行方式即可。


## 存在的问题

目前日志输出不是很人性化，如果出现了以下问题请提issue：

- 出现了代码逻辑的错误
- {当前人数过多，请等待5分钟后尝试}。这种是请求方式错误或者请求键值错误导致的，通常是由于学习通更新了预约导致的
- 以字典格式输出的其他错误，仔细查看用户名密码，roomid和seatid是否填写正确。如果问题不能解决请在github上提issue

## ToDo

- 使用github action挂程序
- 优化js执行性能或者使用python实现
