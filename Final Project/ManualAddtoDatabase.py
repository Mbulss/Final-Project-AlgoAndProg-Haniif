# manual adding to realtimedata base

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

class StudentAttendance:
    def __init__(self, service_account_key_path, database_url):
        """
        Initializes the StudentAttendance class.

        Args:
        - service_account_key_path (str): Path to the Firebase service account key JSON file.
        - database_url (str): URL of the Firebase Realtime Database.
        """
        self.cred = credentials.Certificate(service_account_key_path)  # Loading Firebase credentials
        firebase_admin.initialize_app(self.cred, {'databaseURL': database_url})  # Initializing Firebase app
        self.ref = db.reference('Students')  # Reference to the 'Students' node in the database

    def update_attendance(self, student_id):
        """
        Updates the attendance of a student in the Firebase Realtime Database.

        Args:
        - student_id (str): ID of the student whose attendance needs to be updated.
        """
        student_info = self.ref.child(student_id).get()  # Retrieve student information from the database
        datetime_object = datetime.strptime(student_info['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
        # Calculate the time elapsed since the last attendance
        seconds_elapsed = (datetime.now() - datetime_object).total_seconds()

        if seconds_elapsed > 30:  # Check if the time elapsed is more than 30 seconds
            # Increment the total attendance count and update the last attendance time
            student_info['total_attendance'] += 1
            student_info['last_attendance_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Update the student information in the database
            self.ref.child(student_id).update(student_info)
            print(f"Attendance updated for student ID: {student_id}")
        else:
            # Print a message if attendance is not updated within 30 seconds
            print(f"Not updating attendance for student ID: {student_id}, attendance within 30 seconds")


if __name__ == "__main__":
    # Path to the Firebase service account key JSON file
    service_account_key_path = "serviceAccountKey.json"

    # URL of the Firebase Realtime Database
    database_url = "https://faceattendancerl-default-rtdb.firebaseio.com/"

    # Create an instance of StudentAttendance class
    attendance_manager = StudentAttendance(service_account_key_path, database_url)

    # Student ID for which attendance needs to be updated
    student_id_to_update = "2702358065"

    # Update the attendance for the specified student ID
    attendance_manager.update_attendance(student_id_to_update)