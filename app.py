import cv2
import numpy as np
import face_recognition

imageRomanTrain = face_recognition.load_image_file('images/roman_train.jpeg')
imageRomanTrain = cv2.cvtColor(imageRomanTrain,cv2.COLOR_BGR2RGB)

imageRomanTest = face_recognition.load_image_file('images/seth_test.jpeg')
imageRomanTest = cv2.cvtColor(imageRomanTest,cv2.COLOR_BGR2RGB)

faceLocation = face_recognition.face_locations(imageRomanTrain)[0]
encodeRoman = face_recognition.face_encodings(imageRomanTrain)[0]
cv2.rectangle(imageRomanTrain,(faceLocation[3],faceLocation[0]),(faceLocation[1],faceLocation[1]),(0,250,0),2)

faceLocationTest = face_recognition.face_locations(imageRomanTest)[0]
encodeRomanTest = face_recognition.face_encodings(imageRomanTest)[0]
cv2.rectangle(imageRomanTest,(faceLocationTest[3],faceLocationTest[0]),(faceLocationTest[1],faceLocationTest[1]),(0,250,0),2)

encodeRoman = np.array(encodeRoman)
encodeRomanTest = np.array(encodeRomanTest)

results = face_recognition.compare_faces([encodeRoman], encodeRomanTest)
print("Are the faces the same?", results)

cv2.imshow('Roman Reigns',imageRomanTrain)

cv2.imshow('Roman Reigns Test',imageRomanTest)
cv2.waitKey(0)

