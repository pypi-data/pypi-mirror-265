# -*- coding:utf-8 -*- 

import mysql.connector
from mysql.connector import Error


class Mysqldb:
    def __init__(self,**kwargs):
        self.user = kwargs['user_demo']
        self.password = kwargs['password_demo']
        self.host = kwargs['host_demo']
        self.database = kwargs['database_demo']
        self.conn = None
        self.cur = None
        self.connect()
        
    def connect(self):
        try:
            self.conn = mysql.connector.connect(user=self.user, password=self.password, 
                                                host=self.host, database=self.database)
            self.cur = self.conn.cursor()
        except Error as e:
            print("数据库连接错误: ", e)
        
    def query(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()
    
    def close(self):
        self.cur.close()
        self.conn.close()
        