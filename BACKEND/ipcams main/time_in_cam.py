from main import get_db_connection,load_known_encodings,start_stream,process_camera_frame
from checkinimutil import WebCamVideoStream,FPS
from datetime import datetime, timedelta
import time
import cv2
mydb = get_db_connection()
cursor = mydb.cursor()
    
    # Load the encodings into a dictionary where employee_id is the key
employee_encodings = load_known_encodings(cursor)
ip_camera_in_url = "rtsp://admin:Admin123@192.168.0.218:554/channel/1"

cap_in, fps_in = start_stream(ip_camera_in_url)
   # cap_out, fps_out = start_stream(ip_camera_out_url)

fps_in.update()

refresh_interval = 60  
last_check_time = datetime.now()
# if not cap_in.read():
#     print("Video stream not found")
    
while True:
    current_time = datetime.now()
    current_date = current_time.date()

    # Process time-in camera
    success_in, img_in = cap_in.read()
# success_out, img_out = cap_out.read()
    
    if not success_in:
        print("Attempting to reconnect...")
        cap_in.stop()  # Use the stop method
        time.sleep(1)
        cap_in, fps_in = start_stream(ip_camera_in_url)  # Reinitialize stream
        continue
    if success_in:
                img_in = process_camera_frame(cursor, mydb, img_in, employee_encodings, 'in', 'IN')
                
    if success_in:
        cv2.imshow("Time-IN Camera", img_in)
        
    if (current_time - last_check_time).total_seconds() >= refresh_interval:
            #employee_encodings = load_known_encodings(cursor)
            last_check_time = current_time
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap_in.release()
cv2.destroyAllWindows()
fps_in.stop()
cursor.close()
mydb.close()
