import numpy as np
import mysql.connector
from datetime import datetime, timedelta
import cv2
import face_recognition
import os
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cms"
    )


def today_attenance(cursor, mydb, employee_id, date):
    query = "SELECT log_time FROM rawdata WHERE employee_id=%s AND date=%s"
    cursor.execute(query, (employee_id, date))
    result = cursor.fetchall()
    print("result", result)
    if len(result) >1:
        log_times = [log_time[0] for log_time in result]
        in_time = min(log_times)
        out_time = max(log_times)

        Status = "present"
        print("in time", in_time)
        print("out time", out_time)
        worked = out_time - in_time
        hours_worked = worked.total_seconds() / 3600
        overtime = max(0, hours_worked - 8)
        sql='INSERT into employee_management_attendance (employee_id, date, time_in, time_out,status,comments,hours_worked,is_overtime) VALUES (%s, %s, %s, %s,%s, %s, %s, %s)'
        val=(employee_id, date, in_time, out_time, Status, "ok", hours_worked, overtime)
        cursor.execute(sql, val)
        mydb.commit()

        print(f"Attendance for {employee_id} on {date} has been added to the database")



        print("More then 1 record found")
        

        return


    
def load_known_encodings(cursor):
    employee_ids = []
    encoding_list_known = []
    last_updated = None
    
    print("Loading encoded file...")
    query = "SELECT EmployeeID, Encoding, updated_at FROM Encodings"
    cursor.execute(query)
    employees_data = cursor.fetchall()

    for employee_id, encodings, updated_at in employees_data:
        employee_ids.append(employee_id)
        encodings = encodings.replace('\n', '').strip('[]')
        try:
            encoding = np.fromstring(encodings, sep=',', dtype=float)
            if encoding.shape == (128,):
                encoding_list_known.append(encoding)
            else:
                print(f"Warning: Encoding for {employee_id} does not have the expected shape.")
        except ValueError as e:
            print(f"Error parsing encoding for {employee_id}: {e}")

        last_updated = updated_at

    print("Loaded encoded file")
    return employee_ids, encoding_list_known, last_updated


def cleanupdata(cursor, CurrentDate):
    daybeforeyesterday = CurrentDate - timedelta(days=2)
    query = "DELETE FROM rawdata WHERE date<=%s"
    cursor.execute(query, (daybeforeyesterday,))
    print("Attendance data for", daybeforeyesterday, "has been deleted")

# def calculate_attendance(cursor, mydb, employee_id, date):  
#     print("Calculating attendance for", employee_id, "on", date)      
#     query = "SELECT min(log_time) as in_time, max(log_time) as out_time FROM rawdata WHERE employee_id=%s AND date=%s"
#     cursor.execute(query, (employee_id, date))
#     print("in time, out time calculated")
#     result = cursor.fetchone()

#     if result is None:
#         print("No attendance data found for the given employee_id and date")
#         return

#     in_time, out_time = result
#     Status = "present"
#     print("in time", in_time)
#     print("out time", out_time)
#     worked = out_time - in_time
#     hours_worked = worked.total_seconds() / 3600
#     overtime = max(0, hours_worked - 8)
    
#     query = "SELECT * FROM employee_management_attendance WHERE employee_id=%s AND date=%s"
#     cursor.execute(query, (employee_id, date))
#     result = cursor.fetchone()
#     print("Duplicates:", result)

#     if result is None:
#         try:
#             query1 = "INSERT INTO employee_management_attendance (employee_id, date, time_in, time_out, status, hours_worked, is_overtime, comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             cursor.execute(query1, (employee_id, date, in_time, out_time, Status, hours_worked, overtime, "ok"))
#             mydb.commit()
#         except Exception as e:
#             print("Error:", str(e))
#             return
#     else:
#         print("Attendance Record Already Exists")
 
#     print(f"Attendance for {employee_id} on {date} has been added to the database")

# def final_Attendance(cursor, mydb, employee_ids, date):
#     for employee_id in employee_ids:
#         calculate_attendance(cursor, mydb, employee_id[0], date)

def log_attendance(cursor, mydb, employee_id):
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    check_current_time = datetime.now().time() 
    total_seconds = check_current_time.hour * 3600 + check_current_time.minute * 60 + check_current_time.second + check_current_time.microsecond / 1_000_000
    print("total seconds", total_seconds)
    
    query = "SELECT * FROM rawdata WHERE employee_id=%s AND date=%s ORDER BY log_time DESC LIMIT 1"
    cursor.execute(query, (employee_id, current_date))
    result = cursor.fetchone()
    print("result", result)
    print("!")
    if result is not None:
        print("here")
        last_log_time = result[3]  
        print("last log time", last_log_time)
        print("type " , type(last_log_time))
        
        print("current time", check_current_time)
        print("last log time in seconds`", last_log_time.seconds)
        time_difference = total_seconds - last_log_time.total_seconds()
        print("time difference", time_difference)
        if time_difference < 10:
            return

    query = "INSERT INTO rawdata (employee_id, date, log_time) VALUES (%s, %s, %s)"
    cursor.execute(query, (employee_id, current_date, current_time))
    mydb.commit()
    print(f"Attendance logged for {employee_id} at {current_time}")

def main():
    mydb = get_db_connection()
    cursor = mydb.cursor()

    # Load initial encodings
    employee_ids, encoding_list_known, last_update = load_known_encodings(cursor)

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  
    cap.set(4, 720)   

    refresh_interval = 60  # Check for updates every 60 seconds
    last_check_time = datetime.now()

    while True:
        current_time = datetime.now()
        current_date = current_time.date() 
        previous_date = current_time.date() - timedelta(days=1)
        current_time_only = current_time.time()



        success, img = cap.read()
        if not success:
            print("Failed to capture image")
            break
        img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

        face_current_frame = face_recognition.face_locations(img_small)
        encode_current_frame = face_recognition.face_encodings(img_small, face_current_frame)

        for encode_face, face_location in zip(encode_current_frame, face_current_frame):
            # Compare faces and get distances
            face_distance = face_recognition.face_distance(encoding_list_known, encode_face)

            if len(face_distance) <= 0:
                print("No face distances found.")
                continue

            # Find the best match with minimum distance
            best_match_index = np.argmin(face_distance)
            best_distance = face_distance[best_match_index]

            # Set a stricter threshold for the distance (e.g., 0.4)
            if best_distance < 0.4:
                employee_id = employee_ids[best_match_index]
                print(f"Known face detected: {employee_id} with distance: {best_distance}")

                # Draw rectangle around the face
                top, right, bottom, left = face_location
                top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
                cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

                # Display the employee ID
                employee_id_str = str(employee_id)
                cv2.putText(img, employee_id_str, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                # Log attendance
                log_attendance(cursor, mydb, employee_id)
            else:
                print(f"Face distance too large: {best_distance}, no match.")
        
        # Check if it's time to refresh encodings
        if (current_time - last_check_time).total_seconds() >= refresh_interval:
            employee_ids, encoding_list_known, new_last_update = load_known_encodings(cursor)
            if last_update != new_last_update:
                print("Encodings updated.")
                last_update = new_last_update
            last_check_time = current_time

        
        print("Attendance for the day has been closed")
        query = "SELECT DISTINCT employee_id FROM rawdata WHERE date=%s"
        cursor.execute(query, (current_date,))
        result = cursor.fetchall()
        print("result", result)
        for employee_id in result:
            today_attenance(cursor,mydb,employee_id[0],current_date)
        print("Attendance added to the database")
        cleanupdata(cursor,current_date)

        cv2.imshow("Face Attendance", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    cursor.close()
    mydb.close()

main()



# mydb = get_db_connection()
# cursor = mydb.cursor()
# today_attenance(cursor, mydb, 56, "2024-09-16")