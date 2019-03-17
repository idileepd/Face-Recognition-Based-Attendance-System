import get_reports
import facerec
# from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import plot_graphs
import group_attendance


from tkinter import Tk
from tkinter import Button
from tkinter import Label

window = Tk()
window.title("FRAS")
window.attributes("-fullscreen",True)



#######################################################################################################################################
####################################################### Create TAB Controller  ########################################################
#######################################################################################################################################
## we want the tabs
# 1. Take Attendance
# 2. Take Group Attendance


#main tab controller
tab_control = ttk.Notebook(window)


#create frames
take_attendance_tab = ttk.Frame(tab_control)
group_attendance_tab = ttk.Frame(tab_control)
auto_attendance_tab = ttk.Frame(tab_control)




#add frames to tab controller
tab_control.add(take_attendance_tab, text='  Normal Attendance  ')
tab_control.add(group_attendance_tab, text='  Group Attendance  ')
tab_control.add(auto_attendance_tab, text=' Auto Attendance  ')






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
####################################################### Tab 2 - auto Attendance #######################################################
########################################################################################################################################

####------------------------------------------------Tab 2 Widgets  -----------------------------------------------------####
instructions_tab3 = """
Instructions : After clicking on "Take Attendance" button
    1. Place your face infront of camera it will show your face
    2. Adjust your face to get your rollnumber and attendance will be automatically given
    3. Do 1,2 steps for each person 
    5. Press 'Q' if you want quit from taking attendance
"""

tab3_ins_label = Label(auto_attendance_tab, text=instructions_tab3, width=60, height=15, font=('times', 15, ' bold ') ) 
tab3_ins_label.place(x=0,y=0 )


####------------------------------------------------Tab 2 Functions  -----------------------------------------------------####

def take_auto_attendance_fun():
    messagebox.showinfo("Auto Attendance", "Press 'Q' if you want to  stop taking attnedance")
    facerec.take_auto_attendance()



####------------------------------------------------Tab 2 Buttons  -----------------------------------------------------####

take_auto_att_btn = Button(auto_attendance_tab, text="Take Auto Attendance", bg="red", fg="white", command=take_auto_attendance_fun, font=('times', 15, ' bold '))
take_auto_att_btn.place(relx=0.2,x=0,y=30 )






















tab_control.pack(expand=1, fill='both')
window.mainloop()










