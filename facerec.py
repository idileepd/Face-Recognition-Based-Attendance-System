import face_recognition
import cv2
import os
import pickle
import pandas as pd
import datetime
import time

import pyttsx3


##########################################################################################################
############################################# utilities ##################################################
##########################################################################################################

## Video capture variable
camera_value = 0


##Speak engine

engine = pyttsx3.init()


def check_student(id):
    #loop over student details and if he is present return true else return false
    students = get_all_students()
    for student in students:
        if student == id:
            return True
    return False


def checkfile(report_date):
    file_path = './Data/reports/'+report_date
    if(os.path.isfile(file_path)):
        return True
    else:
        return False


def update_encodes_and_names(kfe,kfn):
    print("replacing old Encodes files")
    with open("./Data/encodings/face_encodes.pkl", "wb") as f:
        pickle.dump(kfe,f)
        print("encodings replaced")

    with open("./Data/encodings/face_names.pkl", "wb") as f:
        pickle.dump(kfn,f)
        print("names replaced")
    

def check_encode_files():
    if os.path.isfile("./Data/encodings/face_names.pkl") and os.path.isfile("./Data/encodings/face_encodes.pkl") :
        return True
    else:
        return False    

def get_all_encodings():
    known_face_encodings = []
    known_face_names = []
    ## check is file there or not 
    if check_encode_files() :
        with open("./Data/encodings/face_names.pkl", "rb") as f:
            face_names = pickle.load(f)
            # print(face_names)
            known_face_names = face_names
        with open("./Data/encodings/face_encodes.pkl", "rb") as f:
            face_encodes = pickle.load(f)
            # print(face_encodes)
            known_face_encodings = face_encodes
        return (known_face_encodings,known_face_names)
    else:
        return (known_face_encodings,known_face_names)

def get_all_students():
    known_face_names = []
    if check_encode_files() :
        with open("./Data/encodings/face_names.pkl", "rb") as f:
            face_names = pickle.load(f)
            # print(face_names)
            known_face_names = face_names
        return known_face_names
    else:
        return known_face_names


def get_img_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    return face_encoding


def give_attendance(datee,time,id):
    file_path = './Data/reports/'+datee+'.csv'
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
            return -2
        else:
            #append at last
            print("Append to old exacel")
            length = len(df)
            df.loc[length]=[id,datee,time]
            df.to_csv(file_path,index=False)
            return id
                
    else:
        # creat a new df and create a file and add attendance
        print("creating new excel ")
        df = pd.DataFrame(columns=['id','date','time'])
        df.loc[0]=[id,datee,time]
        df.to_csv(file_path,index=False)
        return id


def get_date_time():
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    return (date, timeStamp)





###############################################################################################################################################
#################################################### Take Attendance ##########################################################################
###############################################################################################################################################
#1.on camera
#2. take every frame and find face locations and compare those locations with existing encodes
#3. I match found draw his id (when user press 'T' - take attendane for him) and break
#4. If no match found draw "unknown" in image frame 
#5. wait unit user press q and break

#### return flags
# -1 >> tremination
# -2 >> Already given
#  id >> Given att



def take_student_attendance():
    global camera_value
    known_face_encodings, known_face_names = get_all_encodings()
    video_capture = cv2.VideoCapture(camera_value)
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
                # ts = time.time()      
                # date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                # timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                date,timeStamp = get_date_time()
                stu_att['id'] = str(name)
                stu_att['date'] = str(date)
                stu_att['time'] = str(timeStamp)
            
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
        # Hit 'q' on the keyboard to quit!
        
        if cv2.waitKey(1) & 0xFF == ord('t'):
            # print("Giving Attendance ",stu_att['id'])
            if stu_att['id']!="Unknown":
                status = give_attendance(stu_att['date'], stu_att['time'], stu_att['id'])
                break

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            status = -1
            break
    
    # Release handle to the webcam
    cv2.destroyAllWindows()
    video_capture.release()
    return (stu_att['id'],status)









    
##################################################################################################################################################
############################################################## ADDING NEW USER ###################################################################
##################################################################################################################################################

#1.Save image
#2. get all encodes and names
#3. Check if given id is already present in names update the face encodes at that location and update files
#4. else : if not present append to encodes and append to names and save files



def add_student_encodes_and_name(id):
    image_path = str(id)+'.jpg'
    kfe,kfn = get_all_encodings()
    loc_index = -1

    #check for user existence
    for index,name in enumerate(kfn):
        if name == id:
            loc_index = index
            break
    #so already user has taken pic >> update it
    if loc_index!=-1:
        kfe[loc_index]= get_img_encoding(image_path)
        update_encodes_and_names(kfe,kfn)
        # delete_image(image_path)
        os.remove(image_path)
        return str(id)+" : Student sucessfully updated"
    else:
        kfe.append(get_img_encoding(image_path))
        kfn.append(id)
        update_encodes_and_names(kfe,kfn)
        # delete_image(image_path)
        os.remove(image_path)
        return str(id)+" : Student Sucessfully Added"



def save_image(id):
    global camera_value
    path = str(id)+'.jpg'
    flag = 0
    while True:
        face_locations = []
        video_capture = cv2.VideoCapture(camera_value)
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        # print(len(face_locations))

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
            cv2.putText(frame, "press 'T' to save", (left + 6, bottom - 6), font, 0.8, (0, 0, 0), 1)


        # Full screen window
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        # Display the resulting image
        cv2.imshow('window', frame)

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

        # Hit 'q' on the keyboard to quit!
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            flag = -1
            break
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    #delete temp image
    os.remove('temp_img.jpg')
    return flag




#############################################################################################################
#################################### Remove USER ############################################################
#############################################################################################################
#we get id as parameter
#1. get all encodings
#2. compare ids with all current id 
#3. If match found delete that id   del kfn[index] and del kfe[index]
#4. update the encodes and names

# 0 >> sucess
# -1 >> student doesn't exist


def delete_student_encode_and_name(id):
    kfe,kfn = get_all_encodings()
    loc_index = -1

    #check for user existence
    for index,name in enumerate(kfn):
        if name == id:
            loc_index = index
            break

    #so user exist >> update it
    if loc_index!=-1:
        del kfe[loc_index]
        del kfn[loc_index]
        update_encodes_and_names(kfe,kfn)
        return 0
    else:
        return -1









#############################################################################################################################
#################################### Take Group Attendance ##################################################################
#############################################################################################################################



def take_group_attendance():
    global camera_value
    known_face_encodings, known_face_names = get_all_encodings()
    given_attendances = []
    already_presented_guys = []
    # load_encodings() #first load image encodings 
    video_capture = cv2.VideoCapture(camera_value)
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
                # ts = time.time()  
                # date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                # timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                date, timeStamp = get_date_time()
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
                if status ==-2:
                    already_presented_guys.append(x)
                else:
                    given_attendances.append(x)
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
    return msg
    










###############################################################################################################################################
#################################################### Manually Give Attendance     #############################################################
###############################################################################################################################################
#### return flags
# -2 >> Already given
# -3 >> Student id not found
#  id >> Given att


def manual_attendace(id):
    if check_student(id):
        date, timeStamp = get_date_time()
        status = give_attendance(date,timeStamp,id)
        return status
    else:
        return -3





###############################################################################################################################################
#################################################### Change password ##########################################################################
###############################################################################################################################################
## Status
# >>0 >> sucess
# >> -1 >> old pass is wrong

def change_admin_password(e_old_pass, new_pass):
    old_pass = get_old_pass()
    if e_old_pass == old_pass:
        new_pass = [new_pass]
        with open("./Data/pa.pkl", "wb") as f:
            pickle.dump(new_pass,f)
            print(new_pass,": passwrod updated")
            return 0
    else:
        return -1


def get_old_pass():
        with open("./Data/pa.pkl", "rb") as f:
            passwords = pickle.load(f)
            password = passwords[0]
            print("old password",password)
            return password







###############################################################################################################################################
#################################################### REMOVE ENTRIES ##########################################################################
###############################################################################################################################################
## Status


def get_all_entries_today():
    date, _=get_date_time()
    file_path = './Data/reports/'+date+'.csv'
    if checkfile(date+'.csv'):
        df = pd.read_csv(file_path)
        return (list(df.index), list(df.id), list(df.time),list(df.date) )
    else:
        return ([],[],[],[])




def delete_entry(i):
    print(i)
    date, _=get_date_time()
    file_path = './Data/reports/'+date+'.csv'
    if checkfile(date+'.csv'):
        df = pd.read_csv(file_path)
        df.drop(df.index[i], inplace=True)
        df.to_csv(file_path,index=False)
        return "Sucess !!"







###############################################################################################################################################
#################################################### Auto Attendance  ##########################################################################
###############################################################################################################################################
## Status

#### return flags
# -1 >> tremination
# -2 >> Already given
#  id >> Given att

def speak_given_attendance(status):
    if status == -2:
        engine.say('Already Given Attendance')
    else:
        status = str(status) + 'given attendance'
        engine.say(status)
    engine.runAndWait()


def take_auto_attendance():
    global camera_value
    known_face_encodings, known_face_names = get_all_encodings()
    video_capture = cv2.VideoCapture(camera_value)
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
                date,timeStamp = get_date_time()
                stu_att['id'] = str(name)
                stu_att['date'] = str(date)
                stu_att['time'] = str(timeStamp)            
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
        # Hit 'q' on the keyboard to quit!
            
        if stu_att['id']!="Unknown":
            status = give_attendance(stu_att['date'], stu_att['time'], stu_att['id'])
            print("Status")
            speak_given_attendance(status)
            stu_att['id'] = "Unknown"
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            status = -1
            break
    
    # Release handle to the webcam
    cv2.destroyAllWindows()
    video_capture.release()



