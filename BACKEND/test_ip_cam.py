import cv2
import time

# Start the video stream
cap = cv2.VideoCapture("rtsp://admin:Salvo%401212@192.168.1.64:554/Streaming/Channels/101", cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Initialize frame counter
frame_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        print(f"Error: Could not read frame. ret={ret}, frame_count={frame_count}")
        time.sleep(0.1)  # Introduce a small delay
        continue  # Continue to the next iteration if frame read fails

    # Display the frame
    cv2.imshow("Video Stream", frame)

    # Increment the frame counter
    frame_count += 1

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

# Print the total number of frames displayed
print(f"Total frames displayed: {frame_count}")
