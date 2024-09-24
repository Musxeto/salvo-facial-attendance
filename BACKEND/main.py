import numpy as np
import mysql.connector
from datetime import datetime, timedelta
import cv2
import face_recognition

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cms"
    )

def today_attendance(cursor, mydb, employee_id, date):
    # Check if an entry for the employee on the given date already exists
    check_query = "SELECT time_in, time_out FROM employee_management_attendance WHERE employee_id=%s AND date=%s"
    cursor.execute(check_query, (employee_id, date))
    attendance_record = cursor.fetchone()
    
    # Fetch log times from rawdata table
    query = "SELECT log_time FROM rawdata WHERE employee_id=%s AND date=%s"
    cursor.execute(query, (employee_id, date))
    result = cursor.fetchall()
    
    if len(result) > 1:
        # Extract in_time and out_time
        log_times = [log_time[0] for log_time in result]
        in_time = min(log_times)
        out_time = max(log_times)
        
        Status = "present"
        
        # Calculate hours worked and overtime
        worked = out_time - in_time
        hours_worked = worked.total_seconds() / 3600
        overtime = max(0, hours_worked - 8)

        if attendance_record:
            # Update time_out if record exists
            update_query = '''
                UPDATE employee_management_attendance
                SET time_out = %s, hours_worked = %s, is_overtime = %s
                WHERE employee_id = %s AND date = %s
            '''
            cursor.execute(update_query, (out_time, hours_worked, overtime, employee_id, date))
            mydb.commit()  # Ensure the update is committed

        else:
            # Insert new record
            sql = '''
                INSERT INTO employee_management_attendance 
                (employee_id, date, time_in, time_out, status, comments, hours_worked, is_overtime)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            '''
            val = (employee_id, date, in_time, out_time, Status, "ok", hours_worked, overtime)
            cursor.execute(sql, val)
            mydb.commit()
    else:
        # If only one log, insert in_time and leave out_time as NULL
        if len(result) == 1:
            in_time = result[0][0]
            Status = "present"
            
            if not attendance_record:
                sql = '''
                    INSERT INTO employee_management_attendance 
                    (employee_id, date, time_in, time_out, status, comments, hours_worked, is_overtime)
                    VALUES (%s, %s, %s, NULL, %s, %s, NULL, 0)
                '''
                val = (employee_id, date, in_time, Status, "Logged in, no time out yet")
                cursor.execute(sql, val)
                mydb.commit()
        else:
            print("Insufficient records to calculate in/out time.")
    
    return
def load_known_encodings(cursor):
    employee_encodings = {}

    print("Loading encoded file...")
    query = "SELECT EmployeeID, Encoding FROM Encodings"
    cursor.execute(query)
    employees_data = cursor.fetchall()

    for employee_id, encodings in employees_data:
        # Assume the encodings are stored as a string of list of lists
        encodings = encodings.replace('\n', '').strip('[]')
        encoding_lists = encodings.split('], [')  # Split multiple encodings

        employee_encodings_list = []
        for enc in encoding_lists:
            enc = enc.strip('[]')  # Clean up each encoding
            try:
                encoding = np.fromstring(enc, sep=',', dtype=float)
                if encoding.shape == (128,):  # Validate the encoding shape
                    employee_encodings_list.append(encoding)
                else:
                    print(f"Warning: Encoding for {employee_id} does not have the expected shape.")
            except ValueError as e:
                print(f"Error parsing encoding for {employee_id}: {e}")

        # Add to the dictionary: employee_id -> list of encodings
        employee_encodings[employee_id] = employee_encodings_list

    print("Loaded encoded file")
    print("Employee encodings:", employee_encodings)
    return employee_encodings

def cleanupdata(cursor, current_date):
    daybeforeyesterday = current_date - timedelta(days=2)
    query = "DELETE FROM rawdata WHERE date<=%s"
    cursor.execute(query, (daybeforeyesterday,))
    print("Attendance data for", daybeforeyesterday, "has been deleted")

def log_attendance(cursor, mydb, employee_id):
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    total_seconds = current_time.hour * 3600 + current_time.minute * 60 + current_time.second + current_time.microsecond / 1_000_000
    
    query = "SELECT * FROM rawdata WHERE employee_id=%s AND date=%s ORDER BY log_time DESC LIMIT 1"
    cursor.execute(query, (employee_id, current_date))
    result = cursor.fetchone()

    if result is not None:
        last_log_time = result[3]  
        time_difference = total_seconds - last_log_time.total_seconds()
        if time_difference < 2:
            return

    query = "INSERT INTO rawdata (employee_id, date, log_time) VALUES (%s, %s, %s)"
    cursor.execute(query, (employee_id, current_date, current_time))
    mydb.commit()
    print(f"Attendance logged for {employee_id} at {current_time}")

def main():
    mydb = get_db_connection()
    cursor = mydb.cursor()

    # Load the encodings into a dictionary where employee_id is the key
    employee_encodings = load_known_encodings(cursor)

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # Width
    cap.set(4, 720)   # Height

    refresh_interval = 60  # Check for updates every 60 seconds
    last_check_time = datetime.now()

    while True:
        current_time = datetime.now()
        current_date = current_time.date() 
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
            best_match_index = None
            best_distance = float('inf')  # Initialize with a large number
            employee_id_best = None

            # Compare current frame encoding against all known encodings for each employee
            for employee_id, known_encodings in employee_encodings.items():
                for known_encoding in known_encodings:
                    face_distance = face_recognition.face_distance([known_encoding], encode_face)[0]
                    
                    if face_distance < best_distance:
                        best_distance = face_distance
                        employee_id_best = employee_id

            # Set a threshold for the minimum distance
            if best_distance < 0.35 : # Adjust threshold as needed
                print(f"Known face detected: {employee_id_best} with distance: {best_distance}")

                # Draw rectangle and display employee ID
                top, right, bottom, left = face_location
                top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
                cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

                employee_id_str = str(employee_id_best)
                cv2.putText(img, employee_id_str, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                # Log attendance
                log_attendance(cursor, mydb, employee_id_best)
            else:
                print(f"Face distance too large: {best_distance}, no match.")

        # Check if it's time to refresh encodings
        if (current_time - last_check_time).total_seconds() >= refresh_interval:
            employee_encodings = load_known_encodings(cursor)
            last_check_time = current_time

        # Process daily attendance after a specific time (e.g., 5 PM)
        if current_time_only >= datetime.strptime("17:00", "%H:%M").time():
            query = "SELECT DISTINCT employee_id FROM rawdata WHERE date=%s"
            cursor.execute(query, (current_date,))
            result = cursor.fetchall()
            for employee_id in result:
                today_attendance(cursor, mydb, employee_id[0], current_date)
            print("Attendance added to the database")
            cleanupdata(cursor, current_date)

        cv2.imshow("Face Attendance", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    cursor.close()
    mydb.close()

main()