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

def today_attendance(cursor, mydb, employee_id, log_time, log_type):
    date = log_time.date()
    check_query = "SELECT time_in, time_out FROM employee_management_attendance WHERE employee_id=%s AND date=%s"
    cursor.execute(check_query, (employee_id, date))
    attendance_record = cursor.fetchone()

    if log_type == 'in':
        if not attendance_record:
            sql = '''
                INSERT INTO employee_management_attendance 
                (employee_id, date, time_in, status, comments, hours_worked, is_overtime)
                VALUES (%s, %s, %s, %s, %s, NULL, 0)
            '''
            val = (employee_id, date, log_time.time(), "present", "Logged in")  # Store as TIME
            cursor.execute(sql, val)
            mydb.commit()
            print(f"Time-in logged for employee {employee_id} at {log_time}.")
        else:
            print(f"Time-in already logged for employee {employee_id}.")

    if log_type == 'out':
        if attendance_record and attendance_record[0]:  # Ensure time_in is present
            time_in = attendance_record[0]
            if time_in is None:
                print(f"Time-in is None for employee {employee_id}.")
                return  # Exit or handle the error
            
            # Convert time_in from timedelta to time
            time_in = (datetime.min + time_in).time()  # Convert to time

            log_time_only = log_time.time()  # Extract the time part for comparison

            # Calculate worked time
            worked = datetime.combine(datetime.min, log_time_only) - datetime.combine(datetime.min, time_in)
            if isinstance(worked, timedelta):  # Ensure worked is a timedelta object
                hours_worked = worked.total_seconds() / 3600
                overtime = max(0, hours_worked - 8)

                update_query = '''
                    UPDATE employee_management_attendance
                    SET time_out = %s, hours_worked = %s, is_overtime = %s
                    WHERE employee_id = %s AND date = %s
                '''
                try:
                    cursor.execute(update_query, (log_time.time(), hours_worked, overtime, employee_id, date))
                    mydb.commit()
                    print(f"Time-out updated for employee {employee_id} at {log_time}.")
                except Exception as e:
                    print(f"Error updating time-out for employee {employee_id}: {e}")
            else:
                print(f"Worked time calculation error for employee {employee_id}.")
        else:
            print(f"Cannot log time-out without time-in for employee {employee_id}.")

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

def log_attendance(cursor, mydb, employee_id, log_type):
    current_time = datetime.now()

    # Log time-in or time-out directly based on the camera's purpose
    today_attendance(cursor, mydb, employee_id, current_time, log_type)

def process_camera_frame(cursor, mydb, img, employee_encodings, log_type, label):
    img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    face_current_frame = face_recognition.face_locations(img_small)
    encode_current_frame = face_recognition.face_encodings(img_small, face_current_frame)

    for encode_face, face_location in zip(encode_current_frame, face_current_frame):
        best_match_index = None
        best_distance = float('inf')
        employee_id_best = None

        for employee_id, known_encodings in employee_encodings.items():
            for known_encoding in known_encodings:
                face_distance = face_recognition.face_distance([known_encoding], encode_face)[0]
                if face_distance < best_distance:
                    best_distance = face_distance
                    employee_id_best = employee_id

        if best_distance < 0.35:
            print(f"Known face detected: {employee_id_best} with distance: {best_distance}")
            log_attendance(cursor, mydb, employee_id_best, log_type)

            # Draw rectangle and add label for the recognized face
            top, right, bottom, left = face_location
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(img, f"ID: {employee_id_best}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        else:
            print(f"Face distance too large: {best_distance}, no match.")

    # Add label for the frame (IN/OUT)
    cv2.putText(img, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

    return img

def main():
    mydb = get_db_connection()
    cursor = mydb.cursor()
    
    # Load the encodings into a dictionary where employee_id is the key
    employee_encodings = load_known_encodings(cursor)

    cap_in = cv2.VideoCapture(0)  # Camera for time-in
    cap_out = cv2.VideoCapture(1)  # Camera for time-out
    cap_in.set(3, 1280)  # Width for time-in camera
    cap_in.set(4, 720)   # Height for time-in camera
    cap_out.set(3, 1280)  # Width for time-out camera
    cap_out.set(4, 720)   # Height for time-out camera

    refresh_interval = 60  
    last_check_time = datetime.now()

    while True:
        current_time = datetime.now()
        current_date = current_time.date()

        # Process time-in camera
        success_in, img_in = cap_in.read()
        if success_in:
            img_in = process_camera_frame(cursor, mydb, img_in, employee_encodings, 'in', 'IN')

        # Process time-out camera
        success_out, img_out = cap_out.read()
        if success_out:
            img_out = process_camera_frame(cursor, mydb, img_out, employee_encodings, 'out', 'OUT')

        # Display the frames
        if success_in:
            cv2.imshow("Time-IN Camera", img_in)
        if success_out:
            cv2.imshow("Time-OUT Camera", img_out)

        # Refresh known encodings every minute
        if (current_time - last_check_time).total_seconds() >= refresh_interval:
            employee_encodings = load_known_encodings(cursor)
            last_check_time = current_time

        cleanupdata(cursor,current_date)
        # Quit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_in.release()
    cap_out.release()
    cv2.destroyAllWindows()
    cursor.close()
    mydb.close()

main()