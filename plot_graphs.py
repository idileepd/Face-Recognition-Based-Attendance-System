import matplotlib.pyplot as plt
import numpy as np

import get_reports
import datetime

def get_diff_dates(x,y):
    diff = x-y
    return diff.days



dates =[]
percentages = []

def plot_bar():
    # this is for plotting purpose
    load_dates_per()
    index = np.arange(len(dates))
    plt.bar(index, percentages)
    plt.xlabel('Dates', fontsize=7)
    plt.ylabel('Attendance Percentage', fontsize=7)
    plt.xticks(index, dates, fontsize=10, rotation=30)
    plt.title('Attendance Percentage Statistics')
    plt.ion()
    plt.show()
    dates.clear()
    percentages.clear()


def load_dates_per():
    global dates 
    global percentages 

    for date in get_reports.get_all_att_reports_list():
        dates.append(date[:-4])
        percentages.append(  get_reports.get_desday_att_percentage(date[:-4]))
    

def checkdates(x,y):
    if x<y:
        return True
    else:
        return False

def get_range_plot(start, end):
    if checklen(start,end):

        start_dt = start
        end_dt = end   
        start_dt = get_as_date(start_dt)
        end_dt = get_as_date(end_dt)
        if(start_dt>end_dt):
            print("Entered")
            temp = start_dt
            start_dt = end_dt
            end_dt = temp
            #swap dates too
            t = start
            start = end
            end = t

        print("Out")
        # print("sad")
        global dates
        global percentages
        print(start,end)
        print(start<end)

        if  (start_dt<end_dt) and (end_dt-start_dt).days >0 :
            start_index =0
            end_index = 0 
            print("Entered")
            #find starting date index
            for index,date in  enumerate(get_reports.get_all_att_reports_list()):
                if date[:-4] == start:
                    start_index =index
                    break
            #find Ending date index
            for index,date in enumerate(get_reports.get_all_att_reports_list()):
                if date[:-4] == end:
                    end_index =index
                    break
            temp_list = get_reports.get_all_att_reports_list()
            temp_list = temp_list[start_index:end_index+1] 
            for date in temp_list:
                dates.append(date[:-4])
            for date in dates:
                percentages.append(get_reports.get_desday_att_percentage(date))
            plot_range(dates,percentages)
            dates.clear()
            percentages.clear()
            print("done ")
            return 1
        else:
            return -1
    else:
        return -1

def get_as_date(st):
    return datetime.date(int(st[:4]), int(st[5:7]), int(st[8:]))


def checklen(start,end):
    if len(start)==10 and len(end)==10:
        return True
    else:
        return False

def plot_range(dates,percentages):
    index = np.arange(len(dates))
    plt.bar(index, percentages)
    plt.xlabel('Dates', fontsize=7)
    plt.ylabel('Attendance Percentage', fontsize=7)
    plt.xticks(index, dates, fontsize=10, rotation=30)
    plt.title('Custom dates range attendance percentage bargraph')
    plt.ion()    
    plt.show()

# get_range_plot('2019-03-06','2019-03-07')

# checkdates('2019-03-06','2019-03-07')




    