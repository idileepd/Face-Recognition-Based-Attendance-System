import pandas as pd
import datetime
import time
import os
import pickle
import shutil

# import matplotlib.pyplot as plt

def get_today_att_percentage():
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    csv_file_path = './reports/'+date+'.csv'
    pickle_file_path = './encodings/face_names.pkl'
    x = int()
    y = int() 
    if checkfile(csv_file_path):
        if checkfile(pickle_file_path):
            x = get_total_students(pickle_file_path)
            y = get_total_col(csv_file_path)
            return (y/x)*100
        else:
            print("There are no students registered ")
    else:
        print("Today's attendance not taken yet")


def get_total_students(pickle_file_path): 
    with open(pickle_file_path, "rb") as f:
        face_names = pickle.load(f)
        known_face_names = face_names
        return len(known_face_names)
              
def get_total_col(csv_path):
    df = pd.read_csv(csv_path)
    return len(df)


def get_desday_att_percentage(date):
    csv_file_path = './reports/'+date+'.csv'
    pickle_file_path = './encodings/face_names.pkl'
    x = int()
    y = int() 
    if checkfile(csv_file_path):
        if checkfile(pickle_file_path):
            x = get_total_students(pickle_file_path)
            y = get_total_col(csv_file_path)
            return (y/x)*100
        else:
            print("There are no students registered ")
    else:
        print("Today's attendance not taken ")


#return as list contain attendace taken dates
def get_all_att_reports_list():
    reports_list = []
    directory = './reports'
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            reports_list.append(filename)
    return reports_list


#checks whether the given file is present or not
def checkfile(file_path):
    if(os.path.isfile(file_path)):
        return True
    else:
        return False

#get all repots to desktop
def get_all_reports_desktop():
    desktop_path = os.path.expanduser("~\\Desktop")
    desktop_path = desktop_path + '\\FRAS_ALL_REPORTS'
    if os.path.isdir(desktop_path):
        shutil.rmtree(desktop_path)

    os.mkdir(desktop_path)
    for file_name in get_all_att_reports_list():
        shutil.copy2('./reports/'+file_name, desktop_path)
    return 1
