import cv2
import face_recognition
import os
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="cms"
)

cursor = mydb.cursor()

folderpath = 'images'
pathlist = os.listdir(folderpath)
imagelist = []
employeeids = []
print(pathlist)

# Append images and employee IDs based on the file names
for path in pathlist:
    imagelist.append(cv2.imread(os.path.join(folderpath, path)))
    employeeids.append(os.path.splitext(path)[0])  # Correct usage of 'path' here
print(employeeids)

def findoneencodings(folderpath, imagepath):
    # Initialize lists for employee ID and image
    image = cv2.imread(os.path.join(folderpath, imagepath))
    employeeid = os.path.splitext(imagepath)[0]  # Use imagepath, not image, to get the employee ID

    # Convert the image from BGR to RGB as required by the face_recognition library
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Find face encodings for the image
    encode = face_recognition.face_encodings(img_rgb)[0]

    # Save the found encoding and employee ID
    return encode, employeeid



def findencodings(imageslist):
    encodinglist = []
    # Convert each image to RGB and find encodings
    for img in imageslist:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img_rgb)[0]
        encodinglist.append(encode)

    return encodinglist

############################################################################################
#Test encoding and saving for multiple images
print("Encoding has started")
encodelistknown = findencodings(imagelist)
encodindlistknownwithids = [encodelistknown, employeeids]
print("Encoding has completed")

for idx, employee_id in enumerate(encodindlistknownwithids[1]):
    encoding_str = ','.join(map(str, encodindlistknownwithids[0][idx]))
    print(f"Encodings for employee id {employee_id}: {encodindlistknownwithids[0][idx]}")

    sql = "INSERT INTO Encodings (employeeID, Encoding) VALUES (%s, %s)"
    values = (employee_id, encoding_str)
    try:
        cursor.execute(sql, values)
        mydb.commit()
        print(f"Inserted encoding for employee id {employee_id} into the database.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()
    

############################################################################################
# Test encoding and saving for a single image
# image = '38.jpeg'
# encode,employeeid=findoneencodings(folderpath, image)

# print(f"Encodings for employee id {employeeid}: {encode}")
# sql = "INSERT INTO Encodings (employeeID, Encoding) VALUES (%s, %s)"
# encoding_str = str(encode)
# values = (employeeid, encoding_str)
# try:
#     cursor.execute(sql, values)
#     mydb.commit()
#     print(f"Inserted encoding for employee id {employeeid} into the database.")
# except mysql.connector.Error as err:
#     print(f"Error: {err}")
#     mydb.rollback()
# # Final message to confirm completion
# print("Encoding has completed")