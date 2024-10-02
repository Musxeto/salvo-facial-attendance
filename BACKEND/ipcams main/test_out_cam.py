from main import get_db_connection,load_known_encodings,start_stream,process_camera_frame
from checkinimutil import WebCamVideoStream,FPS
from datetime import datetime, timedelta
import time
import cv2



mydb = get_db_connection()
cursor = mydb.cursor()

# Load the encodings into a dictionary where employee_id is the key
employee_encodings = load_known_encodings(cursor)

ip_camera_out_url = "rtsp://admin:Admin123@192.168.0.215:554/channel/1"



cap_out, fps_out = start_stream(ip_camera_out_url)

fps_out.update()

# Camera for time-out
# cap_in.set(3, 1280)  # Width for time-in camera
# cap_in.set(4, 720)   # Height for time-in camera
# cap_out.set(3, 1280)  # Width for time-out camera
# cap_out.set(4, 720)   # Height for time-out camera

refresh_interval = 60  
last_check_time = datetime.now()
# if not cap_in.read():
#     print("Video stream not found")
    
while True:
    current_time = datetime.now()
    current_date = current_time.date()

    # Process time-in camera
    success_out, img_out = cap_out.read()
    

    if not success_out:
        print("Attempting to reconnect...")
        cap_out.stop()  # Use the stop method
        time.sleep(1)
        cap_out, fps_out = start_stream(ip_camera_out_url)  # Reinitialize stream
        continue


    #     continue
    if success_out:
     img_out = process_camera_frame(cursor, mydb, img_out, employee_encodings, 'out', 'OUT')


    if success_out:
        cv2.imshow("Time-out Camera", img_out)
        
        


    # Refresh known encodings every minute
    if (current_time - last_check_time).total_seconds() >= refresh_interval:
        #employee_encodings = load_known_encodings(cursor)
        last_check_time = current_time


    
    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap_out.release()
cv2.destroyAllWindows()
fps_out.stop()
cursor.close()
mydb.close()
