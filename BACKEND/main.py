import cv2
import pickle
import numpy as np
import face_recognition
import mysql.connector
from datetime import datetime
# Function to log attendance to the database
from datetime import datetime, timedelta


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="cms"
)

cursor = mydb.cursor()


cap = cv2.VideoCapture(0)
cap.set(3, 1280)  
cap.set(4, 720)   


print("Loading encoded file...")
with open("Encodefile.p", "rb") as file:
    encoding_list_known_with_ids = pickle.load(file)

encoding_list_known, employee_ids = encoding_list_known_with_ids
print("Loaded encoded file")

def cleanupdata(current_date):
    
    daybeforeyesterday = current_date - timedelta(days=2)
    query = "DELETE FROM rawdata WHERE date<%s"
    cursor.execute(query, (daybeforeyesterday,))
    mydb.commit()
    
def calculate_attendance(employee_id, date):  
    print("Calculating attendance for", employee_id, "on", date)      

    # Query to fetch in_time and out_time
    query = "SELECT min(log_time) as in_time, max(log_time) as out_time FROM rawdata WHERE employee_id=%s AND date=%s"
    cursor.execute(query, (employee_id, date))
    print("in time, out time calculated")
    result = cursor.fetchone()

    if result is None:
        print("No attendance data found for the given employee_id and date")
        return

    in_time, out_time = result
    Status = "present"

    # Calculate hours worked and overtime
    worked = out_time - in_time
    hours_worked = worked.total_seconds() / 3600
    if hours_worked > 8:
        overtime = hours_worked - 8
    else:
        overtime = 0
        
    # Check for existing record
    query = "SELECT * FROM employee_management_attendance WHERE employee_id=%s AND date=%s"
    cursor.execute(query, (employee_id, date))
    result = cursor.fetchone()
    print("Duplicates:", result)

    if result is None:
        try:
            query1 = "INSERT INTO employee_management_attendance (employee_id, date, time_in, time_out, status, hours_worked, is_overtime, comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query1, (employee_id, date, in_time, out_time, Status, hours_worked, overtime, "ok"))
            mydb.commit()
        except Exception as e:
            print("Error:", str(e))
            return
    else:
        print("Attendance Record Already Exists")
 
    print(f"Attendance for {employee_id} on {date} has been added to the database")

def final_Attendance(employee_ids, date):
    for employee_id in employee_ids:
        calculate_attendance(employee_id[0], date)

  


def log_attendance(employee_id):
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
            # If the time difference is less than 10 minutes, don't log again
        if time_difference < 10:  # 600 seconds = 10 minutes
            #print(f"Attendance for {employee_id} has already been logged within the last 10 minutes.")
            return

    # If no log is found or time difference is more than 10 minutes, log the attendance
    query = "INSERT INTO rawdata (employee_id, date, log_time) VALUES (%s, %s, %s)"
    cursor.execute(query, (employee_id, current_date, current_time))
    mydb.commit()
    print(f"Attendance logged for {employee_id} at {current_time}")


while True:
    current_time = datetime.now()
    current_date = current_time.date() 
    previous_date = current_time.date() - timedelta(days=1)
    print("previous date", previous_date)
    current_time_only = current_time.time()



# Define the time range for comparison
    start_time = datetime.strptime('15:56:00', '%H:%M:%S').time()
    end_time = datetime.strptime('18:30:00', '%H:%M:%S').time()

    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break
    img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

   
    face_current_frame = face_recognition.face_locations(img_small)
    encode_current_frame = face_recognition.face_encodings(img_small, face_current_frame)

    
    for encode_face, face_location in zip(encode_current_frame, face_current_frame):
        matches = face_recognition.compare_faces(encoding_list_known, encode_face)
        face_distance = face_recognition.face_distance(encoding_list_known, encode_face)
        
                
        match_index = np.argmin(face_distance)

        if matches[match_index]:
           
            employee_id = employee_ids[match_index]
            print(f"Known face detected: {employee_id}")

            top, right, bottom, left = face_location
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4  
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

            
            cv2.putText(img, employee_id, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            
            log_attendance(employee_id)
            
    if start_time <= current_time_only <= end_time:
        print("Attendance for the day has been closed")
        query = "SELECT DISTINCT employee_id FROM rawdata WHERE date=%s"
        cursor.execute(query, (current_date,))
        result = cursor.fetchall()
        print("result", result)
        final_Attendance(result, current_date)
        cleanupdata(current_date)
        print("Attendance added to the database")
    else:
        print("Outside the time range for closing attendance")

    cv2.imshow("Face Attendance", img)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
cursor.close()
mydb.close()
