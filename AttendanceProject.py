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

