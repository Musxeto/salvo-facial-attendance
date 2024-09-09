import cv2
import numpy as np
import face_recognition
import os

path = 'images'
images = []
classNames = []
folderImages = os.listdir(path)
print("Images in the folder:", folderImages)

for image in folderImages:
    currentImg = cv2.imread(f'{path}/{image}')
    images.append(currentImg)
    classNames.append(os.path.splitext(image)[0])
    
print("Class names:", classNames)

def find_encodings(images):
    encodings = []
    
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encoding = face_recognition.face_encodings(image)[0]
        encodings.append(encoding)
        
    return encodings

imageEncodings = find_encodings(images)

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
        
        if matches[bestMatchIndex] and faceDistance[bestMatchIndex] < 0.5:
            name = classNames[bestMatchIndex].upper()
            print(f"Match found: {name}")
            
            top, right, bottom, left = facesCurrentFrame[bestMatchIndex]
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
            
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    cv2.imshow('Webcam Face Recognition', img)
    
    cv2.waitKey(1)

