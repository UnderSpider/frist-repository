import pymysql
import re

db = pymysql.connect(host="localhost",
                     user="root", password="123456",
                     database="Dict")

cursor = db.cursor()
f = open('dict.txt')

for line in f:
    l = re.split(r'\s+', line)
    word = l[0]
    interpret = ' '.join(l[1:])
    sql = "insert into dict(word,interpret) values('%s','%s')" % (
        word, interpret)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
f.close()
