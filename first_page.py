import get_reports
import facerec
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import plot_graphs


window = Tk()
window.title("FRAS")
# window.geometry('550x400')
window.attributes("-fullscreen",True)

####################################################################################
########################### Create TabController #####################################
####################################################################################
tab_control = ttk.Notebook(window)

#add new Tabs
enter_new_user_tab = ttk.Frame(tab_control)
take_attendance_tab = ttk.Frame(tab_control)
get_reports_tab = ttk.Frame(tab_control)
edit_entries_tab = ttk.Frame(tab_control)
plot_graphs_tab = ttk.Frame(tab_control)




#add created tabs to tab controller
tab_control.add(take_attendance_tab, text='  Take Attendance  ')
tab_control.add(enter_new_user_tab, text='  Enter New User  ')
tab_control.add(get_reports_tab, text='  Get Repots  ')
tab_control.add(plot_graphs_tab, text=' Plot Graphs  ')
tab_control.add(edit_entries_tab, text=' Edit Entries  ')







######################################################################################
################################## Create Widgets add to tabs ########################
######################################################################################

#---------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------TAB 2 ADD USER -----------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------#
######################################### Tab 2 Widgets ##############################
tab_1_title = Label(enter_new_user_tab, text="Add user Details", font=("Arial Bold",30),)
tab_1_title.place(x=0,y=10 )

#Enter ID field
tab_1_label_id = Label(enter_new_user_tab, text="Enter ID   : ",width=10  ,height=2  ,font=('times', 15, ' bold ') ) 
tab_1_label_id.place(relx=0.2,x=-150,y=65 )

tab_1_entry_id = Entry(enter_new_user_tab,width=10  ,bg="white" ,fg="red",font=('times', 15, ' bold '))
tab_1_entry_id.place(relx=0.2,x=50,y=80 )



#Show status
tab_1_label_msg = Label(enter_new_user_tab, text="", width=50, height=2, font=('times', 15, ' bold ') ) 
tab_1_label_msg.place(x=0,y=200 )
# tab_1_label_sucess = Label(enter_new_user_tab, text="Enter Valid input !",width=50 ,fg='red'  ,height=2  ,font=('times', 15, ' bold '),) 


ins_tab2 = """
Instructions : After clicking on "Add user" button
    1. Place your face infront of camera, it will show your face
    2. Adjust your face to get nice picture of your face
    3. press 'T' to take picture
    4. press 'Q' ,  if you want to quit
"""
tab_2_label_msg2 = Label(enter_new_user_tab, text=ins_tab2, width=60, height=10, font=('times', 15, ' bold ') ) 
tab_2_label_msg2.place(x=-20,y=250 )


######################################### Tab 2 Functions ##############################
def clear():
    tab_1_entry_id.delete(0, 'end')  
    res = ""
    tab_1_label_msg.configure(text= res)   

def takeImage():
    id = tab_1_entry_id.get()

    if ((len(id)>0) and id.isalnum()):
        print("all are valid")
        print(id)
        #TAKE IMAGE FUNCTION facere library >> take image and store
        status =  facerec.take_image(id)

        if status == 1:
            tab_1_label_msg.configure(text='Training images please wait ....', fg="blue")
            messagebox.showinfo('info ', 'Training model with new image ')
            #TRAIN FUNCTON here
            facerec.save_encodings()
            tab_1_label_msg.configure(text='Student Sucessfully Entered', fg="green")
            messagebox.showinfo('sucess ', 'Student Sucessfully Entered')
        else :
            messagebox.showerror('Fail', 'User not added !')
            
        clear()
 
    else:
        tab_1_label_msg.configure(text='Enter valid input', fg="red")
        messagebox.showerror('Input Error', 'Enter valid Input')



######################################### Tab 2 Buttons ##############################

take_image_btn = Button(enter_new_user_tab, text="Add User", bg="orange", fg="white", command=takeImage)
take_image_btn.place(relx=0.2,x=50,y=160 )











#---------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------TAB 1 Take Attendance-----------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------#
######################################### Tab 1 Widgets ##############################



ins_tab1 = """
Instructions : After clicking on "Take Attendance" button
    1. Place your face infront of camera it will show your face
    2. Adjust your face to get your rollnumber
    3. Then press  'Q'  to take attencance

"""
tab_1_label_msg2 = Label(take_attendance_tab, text=ins_tab1, width=60, height=15, font=('times', 15, ' bold ') ) 
tab_1_label_msg2.place(x=0,y=0 )

######################################### Tab 1 Functions ##############################

def take_attendances():
    status = facerec.track_image()
    if status == -1:
        messagebox.showerror('No Attendance Given', 'Face is neither Recognized nor Detected')
    elif status == -2:
        messagebox.showwarning('Already taken !', 'Student has already given attendance')
    else:
        msg = status+' : student has given attendance'
        messagebox.showinfo('sucess ',msg)
     




######################################### Tab 1 Buttons ##############################

take_image_btn = Button(take_attendance_tab, text="Take Attendance", bg="red", fg="white", command=take_attendances, font=('times', 15, ' bold '))
take_image_btn.place(relx=0.2,x=0,y=30 )

# take_image_btn = Button(take_attendance_tab, text="Take Image", bg="red", fg="white", command=take_attendances, font=('times', 15, ' bold '))
# take_image_btn.place(relx=0.4,x=0,y=30 )











#---------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------Tab 3 GET REPORTS -----------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------#
######################################### Tab 3 Widgets ##############################

#Enter ID field
# tab_3_label_id = Label(get_reports_tab, text="Enter ID   : ",width=10  ,height=2  ,font=('times', 15, ' bold ') ) 
# tab_3_label_id.place(relx=0.2,x=-150,y=65 )

# tab_3_entry_id = Entry(get_reports_tab,width=10  ,bg="white" ,fg="red",font=('times', 15, ' bold '))
# tab_3_entry_id.place(relx=0.2,x=50,y=80 )


#specific day report store combo
s_d_r_s_combo = ttk.Combobox(get_reports_tab)
s_d_r_s_combo['values'] = tuple( [x[:-4] for x in get_reports.get_all_att_reports_list()  ] )
s_d_r_s_combo.current(1) #set the default on 
s_d_r_s_combo.place(relx=0.2,x=100,y=230 )
#------------------------------
tab_3_label_id = Label(get_reports_tab, text="Get Specific day report : ",width=20  ,height=2  ,font=('times', 15, ' bold ') ) 
tab_3_label_id.place(relx=0.2,x=-150,y=215 )


#specific day Attendance percentage
s_d_a_p_combo = ttk.Combobox(get_reports_tab)
s_d_a_p_combo['values'] = tuple( [x[:-4] for x in get_reports.get_all_att_reports_list()  ] )
s_d_a_p_combo.current(1) #set the default on 
s_d_a_p_combo.place(relx=0.2,x=250,y=270 )
#------------------------------
tab_3_label_id = Label(get_reports_tab, text="Get Specific day Attendance percentage : ",width=30  ,height=2  ,font=('times', 15, ' bold ') ) 
tab_3_label_id.place(relx=0.2,x=-150,y=255 )




######################################### Tab 3 Functions ##############################
def get_t_percentage():
    percentage = get_reports.get_today_att_percentage()
    messagebox.showinfo('sucess ', "Today Attendance Percentage is : "+str(percentage)+"%")
     


def get_rep():
    print(get_reports.get_all_att_reports_list())
    # get_reports.get_all_reports_desktop()

def get_rep_desk():
    status = get_reports.get_all_reports_desktop()
    if status == 1:
        messagebox.showinfo('sucess', "All reports are stored on Desktop in folder :: FRAS_ALL_REPORTS")


def get_rep_all_avg():
    status = get_reports.get_all_reports_avg()
    status = "Average attendance percentage is : "+str(status)+"%"
    messagebox.showinfo('sucess', status)
    

def get_s_d_a_p():
    res = s_d_a_p_combo.get()
    statu = get_reports.get_specific_day_att_per(res)
    messagebox.showinfo('status', statu)

def get_s_d_a_r():
    res = s_d_r_s_combo.get()
    status = get_reports.get_specific_day_reports_desktop(res)
    messagebox.showinfo('Status', status)



######################################### Tab 2 Buttons ##############################
get_t_per_btn = Button(get_reports_tab, text="Get Today's Attendance Percentage", bg="red", fg="white", command=get_t_percentage, font=('times', 15, ' bold '))
get_t_per_btn.place(x=145,y=30 )

get_rep_desk_btn = Button(get_reports_tab, text="Get All Reports to Desktop", bg="red", fg="white", command=get_rep_desk, font=('times', 15, ' bold '))
get_rep_desk_btn.place(x=145,y=100 )

get_rep_perc_avg_btn = Button(get_reports_tab, text="Get Average attendance percentage", bg="red", fg="white", command=get_rep_all_avg, font=('times', 15, ' bold '))
get_rep_perc_avg_btn.place(x=145,y=150 )


get_rep_perc_avg_btn = Button(get_reports_tab, text="Get Percentage", bg="orange", fg="white", command=get_s_d_a_p, font=('times', 8, ' bold '))
get_rep_perc_avg_btn.place(relx=0.5, x=0,y=270 )

get_rep_perc_avg_btn = Button(get_reports_tab, text="Get Report", bg="orange", fg="white", command=get_s_d_a_r, font=('times', 8, ' bold '))
get_rep_perc_avg_btn.place(relx=0.5,x=-150,y=230 )

######## GET RANGE DAYS REPORTS -- > future implementation
# get_rep_perc_avg_btn = Button(get_reports_tab, text="Get Report", bg="orange", fg="white", command=get_s_d_a_r, font=('times', 8, ' bold '))
# get_rep_perc_avg_btn.place(relx=0.5,x=-150,y=230 )





#---------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------4 PLOT GRAPHS -----------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------#
######################################### Tab 4 Widgets ##############################

#specific Start day  store combo
start_dt_combo = ttk.Combobox(plot_graphs_tab)
start_dt_combo['values'] = tuple( [x[:-4] for x in get_reports.get_all_att_reports_list()  ] )
start_dt_combo.current(0) #set the default on 
start_dt_combo.place(relx=0.3,x=55,y=230 )
#------------------------------
end_dt_combo = ttk.Combobox(plot_graphs_tab)
end_dt_combo['values'] = tuple( [x[:-4] for x in get_reports.get_all_att_reports_list()  ] )
end_dt_combo.current(0) #set the default on
end_dt_combo.place(relx=0.3,x=55,y=250 )


tab_4_label_range = Label(plot_graphs_tab, text="Plot Graph  between this date range : ",width=25 ,height=2  ,font=('times', 15, ' bold ') ) 
tab_4_label_range.place(relx=0.1,x=1,y=215 )
######################################### Tab 4 Functions ##############################
def plot_a_p():
    plot_graphs.plot_bar()

def get_r_p():
    status = plot_graphs.get_range_plot(start_dt_combo.get(),end_dt_combo.get())
    if status == -1:
        messagebox.showinfo('Status', "Enter valid range!")


    
######################################### Tab 4 Buttons ##############################

plt_btn = Button(plot_graphs_tab, text="Plot Bar Graph of Attendances vs dates (All Time)", bg="orange", fg="white", command=plot_a_p, font=('times', 15, ' bold '))
plt_btn.place(x=145, y=120 )

plt_rane_btn = Button(plot_graphs_tab, text="Get graph", bg="orange", fg="white", command=get_r_p, font=('times', 8, ' bold '))
plt_rane_btn.place(relx=0.5, x=0,y=240 )





















#---------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------TAB 5 EDIT ENTRIES -----------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------#
######################################### Tab 5 Widgets ##############################


######################################### Tab 5 Functions ##############################


    
######################################### Tab 5 Buttons ##############################
tab4_btn_get_last_entry = Button(edit_entries_tab, text="Get Last Entry of Today Attendance", bg="red", fg="white", command=get_t_percentage, font=('times', 15, ' bold '))
tab4_btn_get_last_entry.place(relx=0.35,x=0,y=30 )























tab_control.pack(expand=1, fill='both')
window.mainloop()










