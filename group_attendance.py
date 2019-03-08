import face_recognition
import cv2
import os
import pickle
import pandas as pd
import datetime
import time

#we put out face encodings saved in a file
known_face_encodings = []
known_face_names = []


given_attendances = []
already_presented_guys = []


def load_encodings():
    global known_face_encodings
    global known_face_names

    global given_attendances
    global already_presented_guys

    #load pickle
    with open("./encodings/face_names.pkl", "rb") as f:
        face_names = pickle.load(f)
        # print(face_names)
        known_face_names = face_names

    with open("./encodings/face_encodes.pkl", "rb") as f:
        face_encodes = pickle.load(f)
        # print(face_encodes)
        known_face_encodings = face_encodes


def take_group_attendance():
    load_encodings() #first load image encodings 
    video_capture = cv2.VideoCapture(1)
    # stu_att ={
    #     'id':'Unknown',
    #     'time':'',
    #     'date':''
    # }
    g_date = ''
    g_time = ''
    g_id = 'Unknown'
    stu_set = set()
    msg = ''

    name =''
    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1] #Remove color channels
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s) #Note:: TOLERANE best 0.6 >> detecting twins also so don't go 0.4 >> less tolerance
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.4)
            name = "Unknown"
            g_id = "Unknown"
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                #also save to dict for later attendance
                ts = time.time()  
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                g_id = str(name)
                stu_set.add(name)
                g_date = str(date)
                g_time = str(timeStamp)
            
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        
        # Full screen window
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        # Display the resulting image
        cv2.imshow('window', frame)


        if cv2.waitKey(1) & 0xFF == ord('t'):
            print("Taking Attendacenes ")
            print (stu_set)
            for x in stu_set:
                status = give_attendance(g_date, g_time, x)
                if status ==1:
                    given_attendances.append(x)
                else:
                    already_presented_guys.append(x)
                msg = 'Given Attendances : '+str(given_attendances)+'\n Already present : '+ str(already_presented_guys)
            break


        # Hit 'q' on the keyboard to quit!
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            msg = -1
            break
    
    # Release handle to the webcam
    cv2.destroyAllWindows()
    video_capture.release()
    print(msg)
    given_attendances.clear()
    already_presented_guys.clear()
    return msg
    






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
            # print("Student already Taken Attendance!")
            return 0
        else:
            #append at last
            # print("Append to old exacel")
            length = len(df)
            df.loc[length]=[id,datee,time]
            df.to_csv(file_path,index=False)
            return 1
                
    else:
        # creat a new df and create a file and add attendance
        # print("creating new excel ")
        df = pd.DataFrame(columns=['id','date','time'])
        df.loc[0]=[id,datee,time]
        df.to_csv(file_path,index=False)
        return 1







def checkfile(report_date):
    file_path = './reports/'+report_date
    if(os.path.isfile(file_path)):
        return True
    else:
        return False










# take_group_attendance()
