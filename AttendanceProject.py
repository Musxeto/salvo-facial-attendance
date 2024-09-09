import cv2
import numpy as np
import face_recognition
import os

path = 'images'


images = []
classNames = []
folderImages = os.listdir(path)
print(folderImages)

for image in folderImages:
    currentImg = cv2.imread(f'{path}/{image}')
    images.append(currentImg)
    classNames.append(os.path.splitext(image)[0])
    
print(images, classNames)

def find_encodings(images):
    encodings = []
    
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encoding = face_recognition.face_encodings(image)[0]
        encodings.append(encoding)
        
    return(encodings)

imageEncodings = find_encodings(images)

print('Image Encodings: ',imageEncodings)