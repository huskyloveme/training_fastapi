import mysql.connector

# Kết nối tới MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="fastapi"
)

