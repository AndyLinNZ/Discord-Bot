import sqlite3

connection = sqlite3.connect("./test.db")

cursor = connection.cursor()

cursor.execute("create table userInfo (id varchar(20), name varchar(32), balance int)")
connection.commit()
connection.close()
