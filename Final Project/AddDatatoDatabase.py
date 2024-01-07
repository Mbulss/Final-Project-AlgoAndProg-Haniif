import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Load Firebase service account credentials from the provided JSON file
cred = credentials.Certificate("serviceAccountKey.json")

# Initialize Firebase app with the obtained credentials and specify the database URL
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerl-default-rtdb.firebaseio.com/"
})

# Get a reference to the 'Students' node in the Firebase Realtime Database
ref = db.reference('Students')

# Data to be added to the 'Students' node in the database
data = {
    "2019202403":
        {
            "name": "Evi Apita Maya",
            "major": "DPD-RI",
            "starting_year": 2019,
            "total_attendance": 99,
            "standing": "Good",
            "year": 5,
            "last_attendance_time": "2023-12-20 00:54:34"
        },
    "2702358065":
        {
            "name": "Haniif Satria Wardana",
            "major": "CS",
            "starting_year": 2023,
            "total_attendance": 4,
            "standing": "Good",
            "year": 1,
            "last_attendance_time": "2023-12-20 00:54:34"
        },
    "2746528900":
        {
            "name": "Ratu Bilqish FFMR",
            "major": "Doctor",
            "starting_year": 2023,
            "total_attendance": 0,
            "standing": "Good",
            "year": 1,
            "last_attendance_time": "2023-12-20 00:54:34"
        },
    "6047001401":
        {
            "name": "Jude Joseph LM, MCS",
            "major": "Alogprog Lec",
            "starting_year": 2008,
            "total_attendance": 0,
            "standing": "Good",
            "year": 16,
            "last_attendance_time": "2023-12-20 00:54:34"
        }
}

# Loop through the data dictionary to add each student's information to the database
for key, value in data.items():
    # Set the value of each key (student ID) with its corresponding data in the 'Students' node
    ref.child(key).set(value)