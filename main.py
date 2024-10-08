#import libraries
import cv2
import numpy as np
import csv
from datetime import datetime
import face_recognition

video_capture = cv2.VideoCapture(0)

#Load known faces
user1_image = face_recognition.load_image_file("faces/user1.jpg")
user1_encoding = face_recognition.face_encodings(user1_image)[0]

user2_image = face_recognition.load_image_file("faces/user2.jpg")
user2_encoding = face_recognition.face_encodings(user2_image)[0]

user3_image = face_recognition.load_image_file("faces/user3.jpg")
user3_encoding = face_recognition.face_encodings(user3_image)[0]

known_face_encodings = [user1_encoding, user2_encoding, user3_encoding]
known_face_names = ["User 1", "User 2", "User 3"]

#list of expected users
users = known_face_names.copy()

face_locations = []
face_encodings = []

#get current time and date
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    #Recognize faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)

        if(matches[best_match_index]):
            name = known_face_names[best_match_index]

        #Add text if a user is present
        if name in known_face_names:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10, 100)
            fontScale = 1.5
            fontColor = (255, 0 , 0)
            thickness = 3
            lineType = 2
            cv2.putText(frame, name + " Present", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)

            if name in users:
                users.remove(name)
                current_time = now.strftime("%H-%M-%S")
                lnwriter.writerow([name, current_time])

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
