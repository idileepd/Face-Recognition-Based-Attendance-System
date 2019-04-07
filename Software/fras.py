# from tkinter import *
from tkinter import ttk
from os import system
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import Tk
from tkinter import messagebox

import pickle


window = Tk()
window.title("FRAS")
# window.geometry('550x400')
window.attributes("-fullscreen",True)


########################################################################################################
################################ widgets ###############################################################
########################################################################################################
#title
label_title = Label(window, text="FACE RECOGNITION BASED ATTENDANCE SYSTEM",width=60  ,height=2 , bg='green', fg='white' ,font=('times', 30, ' bold ') ) 
label_title.place(x=0,y=0 )


#Enter  password
label_pass = Label(window, text="Enter password   : ",width=13  ,height=2  ,font=('times', 15, ' bold ') ) 
label_pass.place(relx=0.6,rely=0.3,x=-20 )

entry_pass = Entry(window,width=7  ,bg="white" ,fg="red",font=('times', 13, ' bold '), )
entry_pass.place(relx=0.7,rely=0.3,y=17 )




########################################################################################################
################################ Functions #############################################################
########################################################################################################

def clear():
    entry_pass.delete(0,'end')



def get_old_pass():
    with open("./Data/pa.pkl", "rb") as f:
        passwords = pickle.load(f)
        password = passwords[0]
        print("old password",password)
        return password         



def admin_area():
    pwd = get_old_pass()
    if pwd == entry_pass.get():
        cmd = "python admin_area.py"
        system(cmd)
        clear()

    else:
        messagebox.showerror("Authentication error","Wrong password !   ")
    
    




def student_area():
#     messagebox.showinfo("loading","Loading please wait...")
    cmd = "python student_area.py"
    system(cmd)





########################################################################################################
################################ buttons #############################################################
########################################################################################################




take_group_att_btn = Button(window, text="TAKE ATTENDANCE", bg="blue", fg="white", command=student_area, font=('times', 20, ' bold '))
take_group_att_btn.place(relx=0.2, rely=0.4,  )


take_group_att_btn = Button(window, text="ADMIN AREA", bg="red", fg="white", command=admin_area, font=('times', 20, ' bold '))
take_group_att_btn.place(relx=0.6, rely=0.4,  )


take_group_att_btn = Button(window, text="Quit", bg="black", fg="white", command=quit, font=('times', 18, ' bold '))
take_group_att_btn.place(relx=0.8, rely=0.8,  )



























window.mainloop()


