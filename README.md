## 微信采集系统项目文档
---
**项目由来：** 参考（copy） https://github.com/xzkzdx/weixin-spider ,在此做了一些修改

**采集目标：** 微信公众号文章的阅读数、在看数、评论数、评论列表，还有微信公众号的账号基本信息。

**采集难点：** 采集以上数据需要客户端的一些参数，比如 **x-wechat-key** 、  **__biz**  、**appmsg_token** 、**pass_ticket**等。

**采集方式：**  通过Windows客户端+mitmproxy的方式获取加密参数

**采集流程：**

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201105155228440.png?text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzU4MjEwMQ==,size_16,color_FFFFFF,t_70)

**备注：** 一个微信号每天只能获取5000-8000篇文章的阅读/点赞等数据

 如果图片不显示，前往：https://blog.csdn.net/weixin_43582101/article/details/109449733

---
## 环境配置

#### 1. mitmproxy安装:
可直接使用pip进行安装，如果下载缓慢需要换源下载。

```powershell
pip install mitmproxy==4.0.4 --use-feature=2020-resolver
```

安装完成之后，在cmd命令行中输入 mitmdump ,默认是8080端口。

```powershell
mitmdump
```

启动成功后，下载mitm证书：访问 [http://mitm.it/](http://mitm.it/)
点击windows，下载安装。 

如果网页显示  If you can see this, traffic is not passing through mitmproxy。
按照第二步设置windows本地代理后再次安装。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201103091731858.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzU4MjEwMQ==,size_16,color_FFFFFF,t_70)


#### 2. windows本地代理：
windows10本地： 设置 ==> 网络 ==> 代理 ==> 手动设置代理 中打开使用代理并将IP地址修改为127.0.0.1 
端口修改为默认8080或修改后的端口。 (记得点击保存)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201104104707385.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzU4MjEwMQ==,size_16,color_FFFFFF,t_70)


#### 3. 数据库
**mysql：** 下载完成之后启动服务，修改项目settings配置文件，创建数据库**weixin_spider**，字符集utf8mb4。
```powershell
create database weixin_spider  DEFAULT CHARACTER SET utf8mb4;
```
**redis：**  下载安装后启动服务，修改项目settings配置文件，以及addons.py文件。

参考项目代码自行安装配置。


#### 4. 本地模块
参照 requirements文件安装 python库，如有遗漏，根据提示自行安装

---



## 准备工作
首先确定使用环境安装完毕，然后请确保端口（5000、8080）不冲突。

1、确定mysql 、redis服务开启状态，并可正常连接

2、运行 webapp\models.py 文件创建数据库表，查看表结构是否生成正确

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201105161005879.png)

3、登录微信PC版，找到 文件传输助手 对话框， 双击 文件传输助手 ，文件传输助手会自动弹出单独的对话窗口，把对话框锁死在屏幕左上角，具体位置可能需要根据显示器调整。

![在这里插入图片描述](https://img-blog.csdnimg.cn/2020110410360554.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzU4MjEwMQ==,size_16,color_FFFFFF,t_70)

4、依次运行py脚本(亦可运行.sh文件代替)
- 运行 wx_monitor.py ，确定程序是否成功启动
- 运行 manage.py  ，打开网页 http://127.0.0.1:5000/  ，确认成功开启web服务。


5、开启mitmproxy，确保可以拦截到数据（需要cd到tools目录下）
```powershell
cd tools/ && mitmdump -s ./addons.py  --ssl-insecure
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/2020110410520676.png)

---

## 启动测试
准备工作完成之后，访问 http://127.0.0.1:5000/ 。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201104141920420.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzU4MjEwMQ==,size_16,color_FFFFFF,t_70)

添加公众号，**该公众号需要微信已经关注过**。

点击启动，即可进行采集。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201104142127793.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzU4MjEwMQ==,size_16,color_FFFFFF,t_70)

---

## 目录结构 
**weixin-spider** 
│  manage.py   （web服务启动文件）
│  README.md  （项目说明文档）
│  requirements.txt  （项目安装包）
│  wx_monitor.py      （任务调度中心）
│
├─**api**
│  │  crawlerapi.py  （爬虫文件）
│  │  __init__.py
│  │
├─exceptions (异常捕获目录)
│
├─**tools**
│  │  addons.py  （mitm配置）
│  │  handle.py    （自动化操作）
│  │  keys.py         （redis-keys管理）
│  │  proxy.py        （本地代理）
│
├─**webapp**
│  │  models.py （数据库表模型）
│  │  \__init__.py   
│  ├─static （静态资源目录）
│  ├─templates（html文件目录）
│  │
│  ├─wxapp
│  │  │  selffilter.py (过滤器)
│  │  │  views.py   (视图文件、接口)

---

模拟点击的位置需要根据自己显示器分辨率调整，可根据测试文件确定坐标
