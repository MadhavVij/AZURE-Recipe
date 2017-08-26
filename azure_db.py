import os
import time
import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)

path = '/home/madhav/quiz8/Data/'

def connectDB():
    return mysql.connector.connect(host="", port=3306, user="",
                           password="", database="")

@app.route('/db')
def countItem():
    conn = connectDB()
    cur = conn.cursor()
    cur.execute('select count(*) from food')
    value = cur.fetchone()[0]
    cur.close()
    conn.close()
    return value


def walkFiles():
    conn = connectDB()
    cur = conn.cursor()
    for root, dirs, files in os.walk(path):
        for file in files:
            img_file = file.replace('csv', 'jpg')
            print(img_file)
            if file.endswith(".csv"):
                with open(path + file) as f:
                    name = file[:-4]
                    lines = f.readlines()
                    digits = lines[0].replace('\r', '')
                    ingred = lines[1].replace('\r', '')
                    category = lines[2].replace('\r', '')
                    with open(path + img_file, 'rb') as img:
                        image = img.read()
                    sql = 'insert into FOOD (NAME,DIGITS,INGRED,CATEGORY,PICTURE) values (%s,%s,%s,%s,%s)'
                    args = (name,digits, ingred, category, image)
                    cur.execute(sql, args)
                    conn.commit()
    cur.close()
    conn.close()

@app.route('/test')
def test():
    conn = connectDB()
    cur = conn.cursor()
    name = 'Omelette'
    cur.execute('select PICTURE from food WHERE NAME like "%'+name+'%"')
    data = cur.fetchone()[0]
    with open('/home/madhav/quiz8/static/'+name+'.jpg','w') as local_file:
        local_file.write(data)
    img_name = name+'.jpg'

    cur.close()
    conn.close()
    return render_template('display.html',img_name = img_name)



@app.route('/')
def hello_world():
    start_time = time.time()
    count = countItem()
    #walkFiles()
    displayContent()
    end_time = time.time()
    total = end_time-start_time
    return render_template('index.html',count=count,total=total)



if __name__ == '__main__':
    app.run()


@app.route('/try')
def displayContent():
    start_time = time.time()
    conn = connectDB()
    cur = conn.cursor(buffered=True)
    count = countItem()
    filelist = []
    calList = []
    categoryList = []
    nameList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg"):
                filelist.append(file)



    for file in filelist:
        name = file[:-4]
        nameList.append(name)
        sql = 'select DIGITS,CATEGORY from food WHERE NAME like "%'+name+'%"'
        cur.execute(sql)
        data = cur.fetchone()

        digits = data[0]
        cat = data[1]

        digList = digits.split(',')
        calorie = digList[1]
        catList = cat.split(',')
        category = catList[0]
        calList.append(calorie)
        categoryList.append(category)
    cur.close()
    conn.close()
    end_time = time.time()
    total = end_time - start_time
    return render_template('display.html',nameList=nameList,calList=calList,categoryList=categoryList,total=total,
                           count=count)


