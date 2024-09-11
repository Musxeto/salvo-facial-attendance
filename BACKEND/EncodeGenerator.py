import cv2
import face_recognition
import os
import pickle
folderpath='images'
pathlist=os.listdir(folderpath)
imagelist=[]
employeeids=[]
print(pathlist)
for path in pathlist:
    imagelist.append(cv2.imread(os.path.join(folderpath,path)))

    employeeids.append(os.path.splitext(path)[0])
print(employeeids)




def findencodings(imageslist):
    encodinglist=[]
    for img in imageslist:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodinglist.append(encode)

    return encodinglist
print("Encoding has startrd")
encodelistknown = findencodings(imagelist)
encodindlistknownwithids=[encodelistknown,employeeids]
print("Encoding has completed") 


file = open("Encodefile.p","wb")
pickle.dump(encodindlistknownwithids,file)
file.close()

print("file saved")