import sqlite3

connection = sqlite3.connect("./test.db")

cursor = connection.cursor()

cursor.execute("create table userData (id text, name text, balance int)")
connection.commit()
connection.close()
