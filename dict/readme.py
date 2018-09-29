项目

了解什么是项目
项目的开发流程

1. 电子词典
2. http服务器

pdb调试
pip的使用
协程的认识
git管理工具的使用

*************************************
什么是项目

软件项目 ： 实现一定完整性功能的代码

软件项目的开发流程

需求分析 ---》 概要设计 ---》项目规划 ---》 详细设计
---》 编码测试 ----》 项目测试，调试修改 ---》项目发布----》 后期维护更新

需求分析 ： 确定用户的真实需求

1. 确定用户的真实需求，即项目的基本功能
2. 对项目的难度和可行性进行分析
3. 完成需求分析文档，进行确认

概要设计 ： 对项目进行整体分析，初步确定技术方向

1. 整体设计，确定项目架构
2. 确定项目功能模块划分
3. 确定大的技术方向
4. 编写项目概要设计文档，开发流程图

项目规划 ： 确定项目分工，按照项目时限进行规划
1. 确定开发顺序
2. 确定开发的时间轴和里程碑
3. 人员的分配
4. 完成甘特图和思维导图指导开发

详细设计 ： 项目具体的开发设计，完成设计手册

1.根据开发内容，形成详细设计文档
  思路，  逻辑流程  ，功能说明，技术点说明，数据结构，代码说明，注意事项，预期效果，环境约束

编码测试 ： 按照规划完成编码，做基本的测试工作

1.写代码
2.代码基本测试
3.技术攻关
4.代码整合

项目测试: 对项目整体功能进行测试
1. 跨平台性，是否符合环境，功能bug，压力测试
2. 完成测试报告
3. 根据测试结果修改bug

项目发布
1.将项目提交给用户，进行发布使用
2.完成项目使用文档

后期维护
1.处理使用中出现的问题
2.项目的升级和功能的添加

项目注意事项
1.按时完成项目开发是首要工作
2.项目实施人员的冲突问题
3.无计划的实施必要带来后期更大的效率低下

项目开发工具

文档编写 ： word  ppt  markdowm   LaTex
项目流程图 ： Mindmanager  Xmind  visio
项目管理： project
代码管理工具：git   svn
编辑工具：  pycharm  Webstream  eclipse
            sublime  vim   vscode  atom

电子词典

功能说明 ：

1. 用户可以登录注册
   登录凭借用户名密码即可 如果输入不正确可以重复输入
   注册 要求用户有填写用户名密码，且用户名不能重复。其他信息随意

2. 用户信息可以长期保存在服务器，保证下次登录可以使    用

3. 能够满足多个用户端程序同时操作的情况

4. 功能分为客户端和服务端，客户端运行后即进入第一界    面
   第一界面 ： 登录   注册   退出
5. 登录成功后进入第二界面
   第二界面 ： 查词   查看历史记录  退出

6. 功能说明
   登录 ： 选择登录功能 输入用户名密码，如果成功进入第二界面，不成功保持在第一界面，提示失败原因
   注册 ： 选择注册功能，填写信息，成功后可以保持第一界面或者使用新注册用户直接完成登录到第二界面，失败提示失败原因
   第一界面退出 ： 直接退出客户端
   查词 ： 可以循环输入单词，显示出单词词义
           输入  # 表示查词结束回到第二界面。如果查询的词不存在则有相应提示

       *单词本 ： 每一行一个单词
                  单词和解释之间一定有空格
              单词有序排列
            1. 文本查找  2.数据库查找

   历史记录： 选择查看历史记录即打印出用户的查询记录
              可以打印所有记录也可以打印最近10条。
               name     word     time

   第二界面退出 ： 第二界面退出相当于注销，即退回到                 第一界面

项目分析

模块 :  socket 套接字
        pymysql/pymongo
    os   multiprocessing   threading   select

服务端

客户端

1.确定服务端和客户端分为哪些功能，每个功能要做什么工作

服务端 
main（）  ：  
创建套接字，父子进程，子进程处理客户端请求，父进程接受新的连接

login  接受客户端信息 
       数据库匹配
       返回结果

register  接受用户数据
          判断是否重复
          插入数据库返回注册成功
      用户存在返回注册失败

query     接受用户单词
          通过数据库或者文件查找单词
          将单词结果返回给用户
      如果没有查到返回相应信息
      如果查词成功则插入历史记录

history   接受客户请求
          查询数据库返回历史记录
      如果用户没有历史记录则返回信息

客户端 ：

main：  创建套接字 ----》 连接 ---》 打印一级界面

login   ：  输入用户名密码
            发送给服务端
        接受返回结果，如果成功则跳转到二级界面
        失败打印结果

register ： 输入用户名密码
            发送给服务端
        接受返回结果

import getpass
passwd = getpass.getpass()

query ：   循环输入单词
           发送单词给服务端
       接受结果并打印

history ：  发送请求 ---》 接受结果打印


2.确定建立什么样的数据表，表的结构，将表建立起来
  
  user  ： id  name  passwd
  hist  ： id  name  word   time
  words ： id  word  interpret
 
  create table user (id int auto_increment primary key,name varchar(32) not null,passwd varchar(16) default '000000');

  create table hist (id int auto_increment primary key,name varchar(32) not null,word varchar(64) not null,time varchar(64));
  
  create table words (id int auto_increment primary key,word varchar(64),interpret text); 


3. 如果要使用数据库查词则编程将单词本内容存入数据库

4. 搭建框架，实现通信 （创建套接字，设定结构，创建并发）

5. 实现具体框架优化和具体功能


cookie
import getpass

passwd = getpass.getpass()
功能 ： 隐藏密码输入


pdb调试

通过pdb模块完成调试功能

功能 ： 断点设置，单步运行，函数查看，代码段查看，变         量值查看

break ， b   设置断点
continue ，c   继续执行
list ， l   查看当前代码段
next， n   单步执行 
step，  s   进入函数单步执行
pp  打印变量值
help  帮助

pdb.set_trace()
功能 ： 设置初始断点，开始进入pdb调试模式

以pdb调试模式运行
python3 -m pdb dict_client.py


协程

定义 ： 纤程，微线程。协程本质只是一个单线程程序

工作原理 ： 通过应用层层程序，记录上下文的执行栈。实现程序在执行过程中的跳跃执行，选择可以不能阻塞的部分执行，这样就可以大大提高IO执行的效率。

yield ---》 python实现协程的基本关键字

sudo  pip3 install greenlet
sudo pip3 install gevent

greenlet

greenlet.greenlet()  生成协程对象
gr.switch()  选择要执行的协程事件


gevent模块

1. 将事件封装为函数
2. 生成协程对象
   gevent.spawn(func,argv)
   功能 ： 将事件变为协程
   参数    func  绑定的协程函数
           argv  给函数传递参数
   返回值 ： 协程对象

3. 回收协程
   gevent.joinall([obj1,obj2.....])

4. 协程阻塞
   gevent.sleep(n)

pip 的使用

作用: 管理python 的标准的第三方库中第三方软件包

sudo apt-get install python3-pip

sudo pip3 install requests#检测是否安装过

pip3 install package #安装软件
e.g. pip3 install ssh

查看软件包: pip3 list
搜索某个名字的python包: pip3 search [name]

查看软件包信息: pip3 show [package]

升级软件包: pip3 install --upgrade [package]

卸载软件包: sudo pip3 uninstall [package]

导出软件包环境: 

pdb调试
pip的使用
协程的认识
git管理工具的使用

pdb调试

通过pdb模块完成调试功能

功能 ： 断点设置，单步运行，函数查看，代码段查看，变         量值查看

break ， b   设置断点
continue ，c   继续执行
list ， l   查看当前代码段
next， n   单步执行 
step，  s   进入函数单步执行
pp  打印变量值
help  帮助
exit 退出调试

pdb.set_trace()
功能 ： 设置初始断点，开始进入pdb调试模式

以pdb调试模式运行
python3 -m pdb dict_client.py


