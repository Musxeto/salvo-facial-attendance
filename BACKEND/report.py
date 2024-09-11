import mysql.connector
from datetime import datetime
import json

def fetch_attendance_by_date(date_str):
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="faceattendancedb"
    )
    
    cursor = mydb.cursor()

    # Convert the date string to the appropriate format (YYYY-MM-DD)
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return json.dumps({"error": "Incorrect date format. Please use YYYY-MM-DD."})
    
    # Query to fetch attendance data for the given date
    query = """
        SELECT employee_id, entry_time
        FROM attendance
        WHERE DATE(entry_time) = %s
    """
    
    cursor.execute(query, (date,))
    result = cursor.fetchall()

    # Prepare the data to be returned as JSON
    attendance_list = []
    for row in result:
        attendance_list.append({
            "employee_id": row[0],
            "entry_time": row[1].strftime('%Y-%m-%d %H:%M:%S')  # Format the timestamp for JSON
        })

    # Close the database connection
    cursor.close()
    mydb.close()

    # Check if we have any attendance records, if not return a message
    if attendance_list:
        return json.dumps({"date": date_str, "attendance": attendance_list}, indent=4)
    else:
        return json.dumps({"date": date_str, "message": "No attendance records found for this date."}, indent=4)

# Example usage
attendance_json = fetch_attendance_by_date("2024-09-05")  # Replace with the date you want to check
print(attendance_json)
