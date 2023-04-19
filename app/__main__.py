import logging
import uvicorn
import mysql.connector
from bson import Binary
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, File, UploadFile, Response
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.employee import Employee, Image
# from app.models.database_sql import mydb_sql
from app.models.database_nosql import collection_employee, collection_image
import bson.binary
from PIL import Image
from io import BytesIO
app = FastAPI()


# mycursor = mydb_sql.cursor()
@app.get("/")
async def main():
    return {"message": "Welcome Fastapi project"}

#
#
# #Connect DB SQL:
# ##################### SQL########################
# mycursor = mydb_sql.cursor()
# @app.post("/sql/add_employee")
# async def sql_add_employee(employees: list[Employee]):
#     try:
#         for i in employees:
#             sql = "INSERT INTO employee (name, age, address, employee_code) VALUES (%s, %s, %s, %s)"
#             val = (i.name, i.age, i.address, i.employee_code)
#             mycursor.execute(sql, val)
#             mydb_sql.commit()
#         return {"message": "Success"}
#     except mysql.connector.Error as e:
#         raise HTTPException(status_code=500, detail="Add Employees failed")
#
# @app.get("/sql/all_employees")
# async def sql_get_all_employees():
#     try:
#         sql = "SELECT * FROM employee"
#         mycursor.execute(sql)
#         result = mycursor.fetchall()
#         fields = [i[0] for i in mycursor.description]
#         results = []
#         for row in result:
#             results.append(dict(zip(fields, row)))
#         return {"employees": results}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Can't show employess")
#
# @app.put("/sql/update_employee")
# async def sql_update_imployee(employee: Employee):
#     try:
#         sql = "UPDATE employee SET name = %s, age = %s, address = %s, employee_code = %s WHERE id = %s"
#         val = (employee.name, employee.age, employee.address, employee.employee_code, employee.id,)
#         mycursor.execute(sql, val)
#         mydb_sql.commit()
#         return {"message": "Success"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Update employee failed")
#
# @app.delete("/sql/delete_employee")
# async def sql_delete_imployee(request_body: dict):
#     try:
#         sql = "DELETE from employee WHERE id = %s"
#         val = (request_body.get('id'),)
#         mycursor.execute(sql, val)
#         mydb_sql.commit()
#         return {"message": "Success"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Delete employee failed")
#


#################### NOSQL########################
@app.post("/nosql/add_employee")
async def add_employee(employees: list[Employee]):
    try:
        employees_data = []
        for i in employees:
            employees_data.append(dict(i))
        collection_employee.insert_many(employees_data)
        return {"message": "Success"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail="Add Employees failed")

@app.get("/nosql/all_employees")
async def get_all_employees():
    try:
        get_all_employees = collection_employee.find()
        results = []
        for docs in get_all_employees:
            employee_dict = {k: v for k,v in docs.items() if k != '_id'}
            results.append(employee_dict)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Can't show employess")

@app.put("/nosql/update_employee")
async def sql_update_imployee(employee: list[Employee]):
    try:
        for i in employee:
            search = {'id': i.id}
            new_values = {'name': i.name,'age': i.age,'address': i.address,'employee_code': i.employee_code}
            print(search)
            print(new_values)
            collection_employee.update_one(filter=search, update={"$set": new_values}, upsert= False)
        return {"message": "Success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Update employee failed")


@app.delete("/nosql/delete_employee")
async def sql_delete_imployee(request_body: dict):
    try:
        if not collection_employee.find({'id': request_body.get('id')}):
            return {"message": "Employee cannot be found"}
        collection_employee.delete_one({'id': request_body.get('id')})
        return {"message": "Success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Delete employee failed")

@app.post("/nosql/upload_image")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    data = bson.binary.Binary(contents)
    image = {"name": "a", "id": 1, "data": data}
    result = collection_image.insert_one(image)
    return {"id": str(result.inserted_id)}

@app.get("/images/{image_id}")
async def read_image(image_id: int):
    image = collection_image.find_one({"id": image_id})
    if image:
        response = Response(content=image['data'], media_type="image/jpeg")
        return response
    return {"error": "Image not found"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)


