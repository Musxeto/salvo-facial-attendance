import cv2
import numpy as np
import face_recognition
import os

# Load images 
path = 'images'
images = []
classNames = []
folderImages = os.listdir(path)
print("Images in the folder:", folderImages)

# Reading each image 
for image in folderImages:
    currentImg = cv2.imread(f'{path}/{image}')
    images.append(currentImg)
    classNames.append(os.path.splitext(image)[0])
    
print("Class names:", classNames)

# Function to encode 
def find_encodings(images):
    encodings = []
    
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(image)
        if len(face_encodings) > 0:
            encodings.append(face_encodings[0])
        else:
            print("No faces found in an image.")
        
    return encodings

# Generate encodings for the images
imageEncodings = find_encodings(images)

if len(imageEncodings) == 0:
    print("No face encodings were found. Exiting.")
    exit()

capture = cv2.VideoCapture(0)

while True:
    success, img = capture.read()
    if not success:
        print("Failed to capture image from the webcam.")
        break
    
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)
    
    facesCurrentFrame = face_recognition.face_locations(imgSmall)
    encodeCurrentFrame = face_recognition.face_encodings(imgSmall, facesCurrentFrame)
    
    for encodedFace, faceLocation in zip(encodeCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(imageEncodings, encodedFace)
        faceDistance = face_recognition.face_distance(imageEncodings, encodedFace)
        print("Face distances:", faceDistance)
        
        bestMatchIndex = np.argmin(faceDistance)
        
        if matches[bestMatchIndex] and faceDistance[bestMatchIndex] < 0.5:  # Adjust the threshold here
            name = classNames[bestMatchIndex].upper()  
            print(f"Match found: {name}")
            
            top, right, bottom, left = faceLocation
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
            
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
            
            cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            
            cv2.putText(img, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        else:
            print("No match found or face is too distant.")
    
    cv2.imshow('Webcam Face Recognition', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
