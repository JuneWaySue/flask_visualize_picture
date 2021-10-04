import pymysql

class Mysql(object):
	
    def __init__(self,age,face,area,num):
        self.conn = pymysql.connect(host='localhost',user='',password='',database='',charset="utf8")
        self.cursor = self.conn.cursor()  # 游标对象
        self.age=[int(i) for i in age.split('-')] if age is not None else None
        self.face=[int(i) for i in face.split('-')] if face is not None else None
        self.area=area
        self.num=num

    def get_items(self):
        sql = 'select name,address,age,img_path,url,motto,score from youyuan where'
        if self.age is not None:
            sql+=f' age between {self.age[0]} and {self.age[1]} and'
        if self.face is not None:
            sql+=f' score between {self.face[0]} and {self.face[1]} and'
        if self.area is not None:
            sql+=f' address like "{self.area}%" and'
        if sql != 'select name,address,age,img_path,url,motto,score from youyuan where':
            self.cursor.execute(sql[:-4]+f' limit {self.num*20},20')
            data=self.cursor.fetchall()
            return len(data),data
        else:
            self.cursor.execute(sql[:-6] + f' limit {self.num*20},20')
            data = self.cursor.fetchall()
            return len(data), data

    def db_close(self):
        self.cursor.close()
        self.conn.close()
