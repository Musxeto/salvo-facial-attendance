import cv2

def test_camera_out():
    # Use DirectShow backend explicitly for the time-out camera
    cap_out = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not cap_out.isOpened():
        print("Error: Time-OUT camera is not available.")
        return

    while True:
        success_out, img_out = cap_out.read()
        if success_out:
            cv2.imshow("Time-OUT Camera", img_out)
        else:
            print("Error: Cannot capture frame from Time-OUT camera.")

       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_out.release()
    cv2.destroyAllWindows()

test_camera_out()
