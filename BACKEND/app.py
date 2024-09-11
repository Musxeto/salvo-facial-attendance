from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime, date, time, timedelta
import mysql.connector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost", user="root", password="root", database="cms"
    )


class AttendanceRecord(BaseModel):
    employee_id: int
    date: date
    log_time: time
    employee_name: str


class LogRequest(BaseModel):
    date: date


class PopupResponse(BaseModel):
    employee_id: int
    log_time: datetime


@app.get("/today_logs/", response_model=List[AttendanceRecord])
def get_today_logs():
    current_date = datetime.now().date()
    try:
        mydb = get_db_connection()
        cursor = mydb.cursor()
        query = "SELECT employee_id, log_time FROM rawdata WHERE date=%s"
        cursor.execute(query, (current_date,))
        logs = cursor.fetchall()

        result = []
        for log in logs:
            employee_id = log[0]
            log_time = log[1]
            print(employee_id)
            try:
                query3 = "SELECT username from employee_management_employee where id=%s"
                cursor.execute(query3, (employee_id,))
                userLog = cursor.fetchone()
                print(userLog)
            except:
                print("query masla")
            employee_name = userLog[0]
            if isinstance(log_time, timedelta):
                # Handle timedelta if returned by the database
                log_time = (datetime.min + log_time).time()
            elif isinstance(log_time, time):
                pass  # Already a time object
            else:
                # Handle other types if necessary
                raise ValueError("Unexpected log_time type")
            result.append(
                {"employee_id": employee_id, "employee_name":employee_name, "date": current_date, "log_time": log_time}
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch logs: {str(e)}")


@app.get("/last_log/", response_model=PopupResponse)
def get_last_log():
    current_date = datetime.now().date()
    try:
        mydb = get_db_connection()
        cursor = mydb.cursor()
        query = "SELECT employee_id, log_time FROM rawdata WHERE date=%s ORDER BY log_time DESC LIMIT 1"
        cursor.execute(query, (current_date,))
        log = cursor.fetchone()
        cursor.close()
        mydb.close()
        if log:
            employee_id = log[0]
            log_time = log[1]
            if isinstance(log_time, timedelta):
                # Handle timedelta if returned by the database
                log_time = (datetime.min + log_time).time()
            elif isinstance(log_time, time):
                pass  # Already a time object
            else:
                # Handle other types if necessary
                raise ValueError("Unexpected log_time type")
            return {
                "employee_id": employee_id,
                "log_time": datetime.combine(current_date, log_time),
            }
        raise HTTPException(status_code=404, detail="No logs found for today")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch last log: {str(e)}"
        )
