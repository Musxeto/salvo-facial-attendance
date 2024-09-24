import cv2
import face_recognition
import os
import mysql.connector
from face_recognition.face_recognition_cli import image_files_in_folder
import json

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cms"
    )

def main():
    verbose = False
    mydb = get_db_connection()
    cursor = mydb.cursor()

    folderpath = 'images'
    pathlist = os.listdir(folderpath)

    encodings_dict = {}  # Dictionary to hold encodings for each person

    # Loop through each person in the training set
    for class_dir in os.listdir(folderpath):
        if not os.path.isdir(os.path.join(folderpath, class_dir)):
            continue

        # Initialize an empty list for the current person's encodings
        encodings_dict[class_dir] = []

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(folderpath, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                if verbose:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # Add face encoding for current image to the list for the current person
                encodings = face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)
                if encodings:  # Check if encodings were found
                    encodings_dict[class_dir].append(encodings[0].tolist())  # Convert to list

    print("Encodings dictionary:", encodings_dict)

    for employee_id, encodings in encodings_dict.items():

        encoding_json = json.dumps(encodings)  
        

        cursor.execute(
            "INSERT INTO encodings (employeeid, encoding) VALUES (%s, %s)",
            (employee_id, encoding_json)
        )
    

    mydb.commit()

    cursor.close()
    mydb.close()

if __name__ == "__main__":
    main()
