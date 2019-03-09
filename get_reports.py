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
    csv_file_path = './Data/reports/'+date+'.csv'
    pickle_file_path = './Data/encodings/face_names.pkl'
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




#return as list contain attendace taken dates
def get_all_att_reports_list():
    reports_list = []
    directory = './Data/reports'
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

#get all repots to desktop #NOTEEEEEEEEEE ::: USE SHUTIL.copytree
def get_all_reports_desktop():
    desktop_path = os.path.expanduser("~\\Desktop")
    desktop_path = desktop_path + '\\FRAS_ALL_REPORTS'
    if os.path.isdir(desktop_path): 
        shutil.rmtree(desktop_path)

    os.mkdir(desktop_path)
    for file_name in get_all_att_reports_list():
        shutil.copy2('./Data/reports/'+file_name, desktop_path)
    return 1



def get_all_reports_avg():
    percentage_list = []
    x= 0
    for date in get_all_att_reports_list():
        date = date[:-4]
        percentage_list.append(get_desday_att_percentage(str(date)))
    for per in percentage_list:
        x=x+per
    return x/len(percentage_list)





def get_desday_att_percentage(date):
    csv_file_path = './Data/reports/'+date+'.csv'
    pickle_file_path = './Data/encodings/face_names.pkl'
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



# def get_specific_day_att_per(date):
#     return get_desday_att_percentage(date)


def get_specific_day_att_per(date):
    if checkfile('./Data/reports/'+date+'.csv'):
        return get_desday_att_percentage(date)
    else:
        return "Report not exist !"


def get_specific_day_reports_desktop(date):
    desktop_path = os.path.expanduser("~\\Desktop")
    desktop_path = desktop_path + '\\'+date+'.csv'
    file_path = "./Data/reports/"+date+".csv"
    if os.path.isdir(desktop_path): 
        shutil.rmtree(desktop_path)
    if checkfile(file_path):
        shutil.copy2(file_path, desktop_path)
        return date+": Report Sucessfully stored at Location :: /desktop/"
    else:
        return "Report not exist !"