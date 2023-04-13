import mysql.connector

# Kết nối tới MySQL
mydb_sql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="fastapi"
)

