import face_recognition
import cv2
import os
import pickle
import pandas as pd
import datetime
import time

# Get a reference to webcam #0 (the default one)

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

def track_image():
    load_encodings() #first load image encodings 
    video_capture = cv2.VideoCapture(1)
    stu_att ={
        'id':'Unknown',
        'time':'',
        'date':''
    }
    name =''
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
            stu_att['id'] = "Unknown"
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                
                #also save to dict for later attendance
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                stu_att['id'] = str(name)
                stu_att['date'] = str(date)
                stu_att['time'] = str(timeStamp)
            
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
    cv2.destroyAllWindows()
    video_capture.release()
    ##Save student's attendance
    if(stu_att['id']!="Unknown"):
        print("Given Attendance  :): ",stu_att['id'])
        status = give_attendance(stu_att['date'],stu_att['time'],stu_att['id'])
        print(status)

        return status
    else:
        # print(os.path.isfile("D:\Project new\FRAS\fras\attendance_reorts\10.xls"))
        print("attendance not given")
        return 0
    


def give_attendance(datee,time,id):
    file_path = './reports/'+datee+'.csv'
    exist_flag = False
    if(checkfile(datee+'.csv')):
        #check if already taken attendance
        df = pd.read_csv(file_path)
        for x in df['id']:
            if str(x)==id:
                
                exist_flag = True
                break
        if exist_flag == True:
            print("Student already Taken Attendance!")
            return 1
        else:
            #append at last
            print("Append to old exacel")
            length = len(df)
            df.loc[length]=[id,datee,time]
            df.to_csv(file_path,index=False)
            return 2
                
    else:
        # creat a new df and create a file and add attendance
        print("creating new excel ")
        df = pd.DataFrame(columns=['id','date','time'])
        df.loc[0]=[id,datee,time]
        df.to_csv(file_path,index=False)
        return 3




def checkfile(report_date):
    file_path = './reports/'+report_date
    if(os.path.isfile(file_path)):
        return True
    else:
        return False

    




def take_image(id):
    path = './images/'+id+'.jpg'
    print(path)
    flag = 0
    while True:
        face_locations = []
        video_capture = cv2.VideoCapture(1)
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        print(len(face_locations))

        #save the original frame
        cv2.imwrite('temp_img.jpg',frame)

        # Process frame put frame and text
        for (top, right, bottom, left) in face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, "save image ? press 't'", (left + 6, bottom - 6), font, 0.8, (0, 0, 0), 1)

        if cv2.waitKey(1) & 0xFF == ord('t'):
            print("taking image !!")
            if(len(face_locations)) ==1:
                print("saving image")
                img_temp = cv2.imread('temp_img.jpg')
                cv2.imshow('save image ', img_temp)
                cv2.imwrite(path,img_temp)
                print("Image saved !")
                flag = 1
                break
            

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            flag = -1
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return flag
