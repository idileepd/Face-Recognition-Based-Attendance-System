import face_recognition
import cv2
import os
import pickle

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

#we put out face encodings saved in a file
known_face_encodings = []
known_face_names = []

def save_encodings():
    #iterate over directory of images 
    directory = '.\images'
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"): 
            path = os.path.join(directory, filename)
            print(path)
            image = face_recognition.load_image_file(path)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(filename[:-4])
            continue
        else:
            continue
    with open("./encodings/face_encodes.pkl", "wb") as f:
        pickle.dump(known_face_encodings,f)
        print("encodings saved")

    with open("./encodings/face_names.pkl", "wb") as f:
        pickle.dump(known_face_names,f)
        print("names saved")

# save_encodings()

def load_encodings():
    global known_face_encodings
    global known_face_names
    #load pickle
    with open("./encodings/face_names.pkl", "rb") as f:
        face_names = pickle.load(f)
        # print(face_names)
        known_face_names = face_names

    with open("./encodings/face_encodes.pkl", "rb") as f:
        face_encodes = pickle.load(f)
        # print(face_encodes)
        known_face_encodings = face_encodes

# load_encodings()

def track_image():
    load_encodings()
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]
        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s) #Note:: TOLERANE best 0.6 >> detecting twins also so don't go 0.4 >> less tolerance
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.4)
            name = "Unknown"
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        # Display the resulting image
        cv2.imshow('Video', frame)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
