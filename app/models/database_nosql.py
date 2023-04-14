from pymongo import MongoClient
from beanie import init_beanie
# Kết nối tới NoSQL (MongoDB)

#
# print('Processing connecting to Database...')
# async def init():
#     client = AsyncIOMotorClient(
#         "mongodb://localhost:27017/"
#     )
#     # Initialize beanie with the Product document class and a database
#     await init_beanie(database=client.db_name, document_models=[Employee])
#
# print('Connected to MongoDB')
client = MongoClient("mongodb://localhost:27017/")
db = client["fastapi"]
collection_employee = db["employee"]

# client = MongoClient("mongodb://localhost:27017/")
# db_names = client.list_database_names()
#
# # In tên của các database
# for db_name in db_names:
#     print(db_name)

