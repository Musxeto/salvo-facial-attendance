import logging
logging.basicConfig(level=logging.INFO)
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime, date, time, timedelta
import mysql.connector
import json
import os
from fastapi.staticfiles import StaticFiles


app = FastAPI()
IMAGE_FOLDER = './images'
app.mount("/images", StaticFiles(directory=IMAGE_FOLDER), name="images")

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
    date: date
    log_time: time
    employee_name: str
    employee_image: str
    

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
            try:
                query3 = "SELECT username from employee_management_employee where id=%s"
                cursor.execute(query3, (employee_id,))
                userLog = cursor.fetchone()
            except:
                raise HTTPException(status_code=500, detail="Failed to fetch employee info")
            employee_name = userLog[0]
            if isinstance(log_time, timedelta):
                log_time = (datetime.min + log_time).time()
            elif isinstance(log_time, time):
                pass
            else:
                raise ValueError("Unexpected log_time type")
            result.append(
                {"employee_id": employee_id, "employee_name":employee_name, "date": current_date, "log_time": log_time}
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch logs: {str(e)}")

def find_employee_image(employee_id: int) -> str:
    # Check for supported image formats: jpg and png
    for extension in ['jpg', 'png']:
        image_path = os.path.join(IMAGE_FOLDER, f"{employee_id}.{extension}")
        if os.path.exists(image_path):
            return f"/images/{employee_id}.{extension}"
    return None  # Return None if no image is found

@app.get("/last_log/", response_model=PopupResponse)
def get_last_log():
    current_date = datetime.now().date()
    try:
        mydb = get_db_connection()
        cursor = mydb.cursor()
        query = "SELECT employee_id, log_time FROM rawdata WHERE date=%s ORDER BY log_time DESC LIMIT 1"
        cursor.execute(query, (current_date,))
        log = cursor.fetchone()
        
        if log:
            employee_id = log[0]
            log_time = log[1]
            
            # Fetch employee name
            try:
                query3 = "SELECT username from employee_management_employee where id=%s"
                cursor.execute(query3, (employee_id,))
                userLog = cursor.fetchone()
            except:
                raise HTTPException(status_code=500, detail="Failed to fetch employee info")
            
            employee_name = userLog[0]

            # Handle log_time format
            if isinstance(log_time, timedelta):
                log_time = (datetime.min + log_time).time()
            elif isinstance(log_time, time):
                pass
            else:
                raise ValueError("Unexpected log_time type")
            
            # Find the image for the employee
            employee_image = find_employee_image(employee_id)
            
            return {
                "employee_id": employee_id,
                "employee_name": employee_name,
                "date": current_date,
                "log_time": log_time,
                "employee_image": employee_image
            }
        
        raise HTTPException(status_code=404, detail="No logs found for today")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch last log: {str(e)}")
    
# WebSocket endpoint
active_connections = []

@app.websocket("/ws/attendance")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logging.info("WebSocket connection established")
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logging.info(f"Received data: {data}")
            # Broadcast to all connected clients
            for connection in active_connections:
                if connection is not websocket:
                    await connection.send_text(data)
    except WebSocketDisconnect:
        logging.info("WebSocket disconnected")
        active_connections.remove(websocket)
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
        active_connections.remove(websocket)

async def notify_new_log(log_data):
    for connection in active_connections:
        await connection.send_text(json.dumps(log_data))
        
