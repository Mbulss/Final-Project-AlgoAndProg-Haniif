import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage

# Initialize Firebase credentials using the service account key
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerl-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerl.appspot.com"
})


# Importing student images from a specified folder
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []

# Upload images to Firebase Cloud Storage and prepare student IDs list
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path))) # Read and store images
    studentIds.append(os.path.splitext(path)[0])  # Extract student IDs from image filenames

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)  # Upload images to Firebase Cloud Storage


    # print(path)
    # print(os.path.splitext(path)[0])
print(studentIds) # Print the list of student IDs


# Function to find encodings for a list of images
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image to RGB format
        encode = face_recognition.face_encodings(img)[0]  # Get face encodings
        encodeList.append(encode) # Append encodings to the list

    return encodeList # Return the list of encodings


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList) # Obtain face encodings for the student images
encodeListKnownWithIds = [encodeListKnown, studentIds]  # Combine encodings with IDs
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')  # Open a file for writing
pickle.dump(encodeListKnownWithIds, file) # Serialize the encodings and student IDs to a file
file.close() # Close the file
print("File Saved") # Print a message confirming the file has been saved