import mysql.connector
from fastapi import FastAPI
from models.employee import Employee
from models.database_sql import mydb

app = FastAPI()

# if mydb.is_connected():
#     print("Connected to MySQL database!")
# else:
#     print("Failed to connect to MySQL database.")

mycursor = mydb.cursor()
@app.post("/add_employee")
async def add_employee(employee: Employee):

    # Thực hiện lệnh SQL để thêm nhân viên vào cơ sở dữ liệu
    sql = "INSERT INTO employee (name, age, address, employee_code) VALUES (%s, %s, %s, %s)"
    val = (employee.name, employee.age, employee.address, employee.employee_code)
    mycursor.execute(sql, val)
    try:
        mydb.commit()
        return {"message": "Success"}
    except mysql.connector.Error as e:
        return {"message": "Error inserting record: {}".format(e)}

@app.get("/all_employees")
async def get_all_employees():
    try:
        sql = "SELECT * FROM employee"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return {"employees": result}
    except Exception as e:
        return {"error": str(e)}

