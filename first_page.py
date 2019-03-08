import get_reports
import facerec
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import plot_graphs
import group_attendance


window = Tk()
window.title("FRAS")
# window.geometry('550x400')
window.attributes("-fullscreen",True)



#######################################################################################################################################
####################################################### Create TAB Controller  ########################################################
#######################################################################################################################################
## we want the tabs
# 1. Take Attendance
# 2. Take Group Attendance
# 3. Add New User
# 4. Report Generation
# 5. Graph Generation
# 6. Edit Attendance Entries
# 7. Change Password 


#main tab controller
tab_control = ttk.Notebook(window)


#create frames
take_attendance_tab = ttk.Frame(tab_control)
group_attendance_tab = ttk.Frame(tab_control)
add_new_student_tab = ttk.Frame(tab_control)
delete_student_tab = ttk.Frame(tab_control)
reports_generation_tab = ttk.Frame(tab_control)
graph_generation_tab = ttk.Frame(tab_control)
edit_attendance_entries_tab = ttk.Frame(tab_control)
change_password_tab = ttk.Frame(tab_control)



#add frames to tab controller
tab_control.add(take_attendance_tab, text='  Take Attendance  ')
tab_control.add(group_attendance_tab, text=' Take Group Attendance  ')
tab_control.add(add_new_student_tab, text='  Add New Student  ')
tab_control.add(delete_student_tab, text='  Delete Student  ')
tab_control.add(reports_generation_tab, text='  Generate Reports  ')
tab_control.add(graph_generation_tab, text=' Generate Graphs  ')
tab_control.add(change_password_tab, text=' Change Password  ')


# to quit from app
def quit():
    global window
    window.quit()

take_group_att_btn = Button(window, text="Quit", bg="black", fg="white", command=quit, font=('times', 20, ' bold '))
take_group_att_btn.place(relx=0.8, rely=0.8, x=0,y=30 )






###-----------------------------------------------------------------------------------------------------------------------------###
###-----------------------------------------Create widgets to add Tabs ---------------------------------------------------------###
###-----------------------------------------------------------------------------------------------------------------------------###






########################################################################################################################################
####################################################### Tab 1 - Take Attendance ########################################################
########################################################################################################################################

####------------------------------------------------Tab 1 Widgets  -----------------------------------------------------####

instructions_tab1 = """
Instructions : After clicking on "Take Attendance" button
    1. Place your face infront of camera it will show your face
    2. Adjust your face to get your rollnumber, If you can see your rollnumber
    3. Then press  'T'  to take attencance
    4. If you want quit from taking press 'Q'
"""
tab1_ins_label = Label(take_attendance_tab, text=instructions_tab1, width=60, height=15, font=('times', 15, ' bold ') ) 
tab1_ins_label.place(x=0,y=0 )



####------------------------------------------------Tab 1 functions  -----------------------------------------------------####

def take_student_attendance():
    Id,status = facerec.take_student_attendance()
    if status == -1:
        messagebox.showerror('No Attendance Given', 'Terminated by user')
    elif status == -2:
        messagebox.showwarning('Already taken', str(Id)+': Student has already given attendance')
    else:
        msg = str(Id)+' : Student has given attendance'
        messagebox.showinfo('sucess ',msg)



####------------------------------------------------Tab 1 Buttons  ------------------------------------------------------####


take_att_btn = Button(take_attendance_tab, text="Take Attendance", bg="red", fg="white", command=take_student_attendance, font=('times', 15, ' bold '))
take_att_btn.place(relx=0.2,x=0,y=30 )











########################################################################################################################################
####################################################### Tab 2 - Group Attendance #######################################################
########################################################################################################################################

####------------------------------------------------Tab 2 Widgets  -----------------------------------------------------####
instructions_tab2 = """
Instructions : After clicking on "Take Attendance" button
    1. Place your face infront of camera it will show your face
    2. Adjust your face to get your rollnumber
    3. Do 1,2 steps for each person 
    4. Then press  'T'  to take attencance for all people
    5. Press 'Q' if you want quit from taking attendance
"""

tab1_ins_label = Label(group_attendance_tab, text=instructions_tab2, width=60, height=15, font=('times', 15, ' bold ') ) 
tab1_ins_label.place(x=0,y=0 )


####------------------------------------------------Tab 2 Functions  -----------------------------------------------------####

def take_group_attendance():
    status = facerec.take_group_attendance()
    if status == -1:
        messagebox.showerror('No Attendance Given', 'Terminated by user !')
    else:
        messagebox.showinfo('sucess ',status)



####------------------------------------------------Tab 2 Buttons  -----------------------------------------------------####

take_grp_att_btn = Button(group_attendance_tab, text="Take Group Attendance", bg="red", fg="white", command=take_group_attendance, font=('times', 15, ' bold '))
take_grp_att_btn.place(relx=0.2,x=0,y=30 )







########################################################################################################################################
####################################################### Tab 3 - Add New Student ########################################################
########################################################################################################################################


####------------------------------------------------------Tab 3 Widgets (ADD User) ------------------------------------------------####

tab3_label_title = Label(add_new_student_tab, text="Add Student", font=("Arial Bold",23),)
tab3_label_title.place(x=0,y=10 )

#instructions
instructions_tab3 = """
Instructions : After clicking on "Add user" button
    1. Place your face infront of camera, it will show your face
    2. Adjust your face to get nice picture of your face
    3. press 'T' to take picture
    4. press 'Q' ,  if you want to quit
"""
tab3_label_ins = Label(add_new_student_tab, text=instructions_tab3, width=60, height=10, font=('times', 15, ' bold ') ) 
tab3_label_ins.place(x=-20,y=250 )

#Enter ID field
tab3_label_id = Label(add_new_student_tab, text="Enter ID   : ",width=10  ,height=2  ,font=('times', 15, ' bold ') ) 
tab3_label_id.place(relx=0.2,x=-150,y=65 )

tab3_entry_id = Entry(add_new_student_tab,width=10  ,bg="white" ,fg="red",font=('times', 15, ' bold '))
tab3_entry_id.place(relx=0.2,x=50,y=80 )



####------------------------------------------------------Tab 3 Widgets (Add User) ------------------------------------------------####
def clear_tab3():
    tab3_entry_id.delete(0,'end')

def add_new_student():
    id = tab3_entry_id.get()

    if ((len(id)>0) and id.isalnum()):
        status =  facerec.save_image(id)
        if status == 1:
            msg = facerec.add_student_encodes_and_name(id)
            messagebox.showinfo('sucess ', msg)
            clear_tab3()
        else :
            messagebox.showerror('Fail', 'User not added !')
    else:
        messagebox.showerror('Input Error', 'Enter valid Input')



####------------------------------------------------------Tab 3 Widgets (Add User) ------------------------------------------------####

take_image_btn = Button(add_new_student_tab, text="Add User", bg="orange", fg="white", command=add_new_student)
take_image_btn.place(relx=0.2,x=50,y=140 )









########################################################################################################################################
####################################################### Tab 4 - Delete Student  ########################################################
########################################################################################################################################


####------------------------------------------------------Tab 4 Widgets (delete User) ------------------------------------------------####

tab4_label_title = Label(delete_student_tab, text="Delete Student", font=("Arial Bold",23),)
tab4_label_title.place(x=0,y=10 )

#Enter ID field
tab4_label_id = Label(delete_student_tab, text="Enter ID   : ",width=10  ,height=2  ,font=('times', 15, ' bold ') ) 
tab4_label_id.place(relx=0.2,x=-150,y=65 )

tab4_entry_id = Entry(delete_student_tab,width=10  ,bg="white" ,fg="red",font=('times', 15, ' bold '))
tab4_entry_id.place(relx=0.2,x=50,y=80 )



####------------------------------------------------------Tab 4 Delete (Add User) ------------------------------------------------####
def clear_tab4():
    tab4_entry_id.delete(0,'end')

def delete_student():
    id = tab4_entry_id.get()

    if ((len(id)>0) and id.isalnum()):
        
        status =  facerec.delete_student_encode_and_name(id)
        if status == 0 :
            messagebox.showinfo('info ', 'Student Removed Sucessfully !')
            clear_tab4()
        else :
            messagebox.showerror('Fail', "Student Doesn't Exist")
    else:
        messagebox.showerror('Input Error', 'Enter valid. Input')



####------------------------------------------------------Tab 2 Widgets (Add User) ------------------------------------------------####

take_image_btn = Button(delete_student_tab, text="Delete User", bg="orange", fg="white", command=delete_student)
take_image_btn.place(relx=0.2,x=50,y=140 )

















#########################################################################################################################################
####################################################### Tab 5 - Generate Reports ########################################################
#########################################################################################################################################

####------------------------------------------------------Tab 5 Widgets (Generate Reports) ------------------------------------------------####

#specific day report store combo
s_d_r_s_combo = ttk.Combobox(reports_generation_tab)
s_d_r_s_combo['values'] = tuple( [x[:-4] for x in get_reports.get_all_att_reports_list()  ] )
s_d_r_s_combo.current(1) #set the default on 
s_d_r_s_combo.place(relx=0.2,x=100,y=230 )

tab_3_label_id = Label(reports_generation_tab, text="Get Specific day report : ",width=20  ,height=2  ,font=('times', 15, ' bold ') ) 
tab_3_label_id.place(relx=0.2,x=-150,y=215 )


#specific day Attendance percentage
s_d_a_p_combo = ttk.Combobox(reports_generation_tab)
s_d_a_p_combo['values'] = tuple( [x[:-4] for x in get_reports.get_all_att_reports_list()  ] )
s_d_a_p_combo.current(1) #set the default on 
s_d_a_p_combo.place(relx=0.2,x=250,y=270 )

tab_3_label_id = Label(reports_generation_tab, text="Get Specific day Attendance percentage : ",width=30  ,height=2  ,font=('times', 15, ' bold ') ) 
tab_3_label_id.place(relx=0.2,x=-150,y=255 )




####------------------------------------------------------Tab 5 functions (Generate Reports) ------------------------------------------------####
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



####------------------------------------------------------Tab 5 functions (Generate Reports) ------------------------------------------------####

get_t_per_btn = Button(reports_generation_tab, text="Get Today's Attendance Percentage", bg="red", fg="white", command=get_t_percentage, font=('times', 15, ' bold '))
get_t_per_btn.place(x=145,y=30 )

get_rep_desk_btn = Button(reports_generation_tab, text="Get All Reports to Desktop", bg="red", fg="white", command=get_rep_desk, font=('times', 15, ' bold '))
get_rep_desk_btn.place(x=145,y=100 )

get_rep_perc_avg_btn = Button(reports_generation_tab, text="Get Average attendance percentage", bg="red", fg="white", command=get_rep_all_avg, font=('times', 15, ' bold '))
get_rep_perc_avg_btn.place(x=145,y=150 )


get_rep_perc_avg_btn = Button(reports_generation_tab, text="Get Percentage", bg="orange", fg="white", command=get_s_d_a_p, font=('times', 8, ' bold '))
get_rep_perc_avg_btn.place(relx=0.5, x=0,y=270 )

get_rep_perc_avg_btn = Button(reports_generation_tab, text="Get Report", bg="orange", fg="white", command=get_s_d_a_r, font=('times', 8, ' bold '))
get_rep_perc_avg_btn.place(relx=0.5,x=-150,y=230 )





#########################################################################################################################################
####################################################### Tab 5 - Generate Graphs ########################################################
#########################################################################################################################################
######################################### Tab 4 Widgets ##############################

#specific Start day  store combo
start_dt_combo = ttk.Combobox(graph_generation_tab)
start_dt_combo['values'] = tuple( [x[:-4] for x in get_reports.get_all_att_reports_list()  ] )
start_dt_combo.current(0) #set the default on 
start_dt_combo.place(relx=0.3,x=55,y=230 )

end_dt_combo = ttk.Combobox(graph_generation_tab)
end_dt_combo['values'] = tuple( [x[:-4] for x in get_reports.get_all_att_reports_list()  ] )
end_dt_combo.current(0) #set the default on
end_dt_combo.place(relx=0.3,x=55,y=250 )


tab_4_label_range = Label(graph_generation_tab, text="Plot Graph  between this date range : ",width=25 ,height=2  ,font=('times', 15, ' bold ') ) 
tab_4_label_range.place(relx=0.1,x=1,y=215 )
######################################### Tab 4 Functions ##############################
def plot_a_p():
    plot_graphs.plot_bar()

def get_r_p():
    status = plot_graphs.get_range_plot(start_dt_combo.get(),end_dt_combo.get())
    if status == -1:
        messagebox.showinfo('Status', "Enter valid range!")


    
######################################### Tab 4 Buttons ##############################

plt_btn = Button(graph_generation_tab, text="Plot Bar Graph of Attendances vs dates (All Time)", bg="orange", fg="white", command=plot_a_p, font=('times', 15, ' bold '))
plt_btn.place(x=145, y=120 )

plt_rane_btn = Button(graph_generation_tab, text="Get graph", bg="orange", fg="white", command=get_r_p, font=('times', 8, ' bold '))
plt_rane_btn.place(relx=0.5, x=0,y=240 )







































































tab_control.pack(expand=1, fill='both')
window.mainloop()










