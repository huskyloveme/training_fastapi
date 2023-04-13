from pymongo import MongoClient

# Kết nối tới NoSQL (MongoDB)
client = MongoClient("mongodb://localhost:27017/")
db = client["fastapi"]
collection_employee = db["employee"]



