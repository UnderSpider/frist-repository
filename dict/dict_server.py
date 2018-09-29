'''
name : vfind
'''
from socket import *
import os
import pymysql
import sys
import signal
import time

# 定义需要的全局变量

DICT_TEXT = './dict.txt'
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)


def main():
    # 数据库连接
    db = pymysql.connect(host="localhost",
                         user="root", password="123456",
                         database="Dict")
    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    # 忽略子进程信号
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    while True:
        try:
            c, addr = s.accept()
            print('Connect from', addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print('Error:', e)
            continue

        # 创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            do_child(c, db)
        # 父进程或者创建失败都继续等待下个客户端连接
        else:
            c.close()
            continue


def do_child(c, db):
    while True:
        data = c.recv(128).decode()
        print(c.getpeername(), ";", data)
        if (not data) or data[0] == 'E':
            c.close()
            sys.exit(0)
        if data[0] == 'R':
            do_register(c, db, data)
        if data[0] == 'L':
            do_login(c, db, data)
        if data[0] == 'Q':
            do_query(c, db, data)
        if data[0] == 'H':
            do_hist(c, db, data)


def do_login(c, db, data):
    print('登录操作')
    l = data.split(' ')
    name = l[1]
    password = l[2]
    cursor = db.cursor()
    sql = "select * from user where name='%s' and password='%s'" % (
        name, password)
    cursor.execute(sql)
    r = cursor.fetchone()
    if r == None:
        c.send(b'FALL')
    else:
        c.send(b'OK')
        print('%s登录成功' % name)


def do_register(c, db, data):
    print('注册操作')
    l = data.split(' ')
    name = l[1]
    password = l[2]
    cursor = db.cursor()

    sql = "select * from user where name = '%s'" % name
    cursor.execute(sql)
    r = cursor.fetchone()

    if r != None:
        c.send(b'Exists')
        return
    # 用户不存在插入用户
    sql = "insert into user(name,password) values('%s','%s')" % (
        name, password)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except:
        db.rollback()
        c.send(b'FALL')
    else:
        print('%s注册成功' % name)


def do_query(c, db, data):
    print('查询操作')
    l = data.split(' ')
    name = l[1]
    word = l[2]
    cursor = db.cursor()

    def do_history():
        tm = time.ctime()
        sql = "insert into record(name,word,time) values('%s','%s','%s')" % (
            name, word, tm)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    # 文本查询
    try:
        f = open(DICT_TEXT)
    except:
        c.send(b'FALL')
        return
    for line in f:
        tmp = line.split(' ')[0]
        if tmp > word:
            c.send(b'FALL')
            f.close()
            return

        elif tmp == word:
            c.send(b'OK')
            time.sleep(0.01)
            c.send(line.encode())
            f.close()
            do_history()
            return
    c.send(b'FALL')


def do_hist(c, db, data):
    print('历史记录')
    l = data.split(' ')
    name = l[1]
    cursor = db.cursor()
    sql = "select * from record where name='%s'" % name
    cursor.execute(sql)
    r = cursor.fetchall()
    if not r:
        c.send(b'FALL')
        return
    else:
        c.send(b'OK')
    for i in r:
        time.sleep(0.1)
        msg = '%s   %s   %s' % (i[1], i[2], i[3])
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')


if __name__ == '__main__':
    main()
