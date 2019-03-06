import pandas as pd
import datetime
import time
import os
import pickle

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







def checkfile(file_path):
    if(os.path.isfile(file_path)):
        return True
    else:
        return False
