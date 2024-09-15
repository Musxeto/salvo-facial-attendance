import cv2
import face_recognition
import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cms"
    )

def main():
    mydb = get_db_connection()
    cursor = mydb.cursor()

    folderpath = 'images'
    pathlist = os.listdir(folderpath)

    for path in pathlist:
        image_path = os.path.join(folderpath, path)
        image = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img_rgb)

        if encodings:
            encoding = encodings[0]
            encoding_str = ','.join(map(str, encoding.tolist()))
            employee_id = os.path.splitext(path)[0]

            # Store the encoding in the database
            query = "INSERT INTO encodings (employee_id, encoding) VALUES (%s, %s)"
            values = (employee_id, encoding_str)
            cursor.execute(query, values)
            mydb.commit()
        else:
            print(f"No face detected in the image: {path}")

    cursor.close()
    mydb.close()

if __name__ == "__main__":
    main()
