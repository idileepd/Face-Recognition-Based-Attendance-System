
# import facerec

# print("##################################################")
# print("######## WELCOME TO FACE RECOGNITION #############")
# print("##################################################")

# print("1.Train mages\n2.Track Image")
# ch = int(input("Enter Your choice"))


# if(ch==1):
#     print("Training Images Started ...")
#     facerec.save_encodings()
# elif(ch==2):
#     print("Tracking Images started ...")
#     facerec.track_image()
# else:
#     print("Wrong choice entered")


import facerec
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


window = Tk()
window.title("FRAS")
window.geometry('550x400')
# window.attributes("-fullscreen",True)
# window.grid_rowconfigure(0, weight=1)
# window.grid_columnconfigure(0, weight=1)

# lbl = Label(window, text="Welcome ", font=("Arial Bold",50),pady=40)
# lbl.place(relx=0.5,x=-50,y=10 )

# # can= Canvas(window, bg='red', height=100, width=100)
# # can.place(relx=0.5, rely=0.5, anchor=CENTER)




# txt = Entry(window, width=10)
# txt.grid(column=1, row=2)




# def clicked():
#     res = "welcome " + txt.get()
#     txt.configure(state='disabled')
#     lbl.configure(text=res)

# btn = Button(window, text="Click Me", bg="orange", fg="black", command=clicked)
# btn.grid(column=1, row=0)

####################################################################################
########################### Create TabController #####################################
####################################################################################
tab_control = ttk.Notebook(window)

#add new Tabs
enter_new_user_tab = ttk.Frame(tab_control)
take_attendance_tab = ttk.Frame(tab_control)
get_reports_tab = ttk.Frame(tab_control)


#add created tabs to tab controller
tab_control.add(enter_new_user_tab, text='  Enter New User  ')
tab_control.add(take_attendance_tab, text='  Take Attendance  ')
tab_control.add(get_reports_tab, text='  Get Repots  ')


######################################################################################
################################## Create Widgets add to tabs ########################
######################################################################################

#---------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------TAB 1 -----------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------#
######################################### Tab 1 Widgets ##############################
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


######################################### Tab 1 Functions ##############################
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
        facerec.take_image(id)



        tab_1_label_msg.configure(text='Training images ....', fg="blue")
        messagebox.showinfo('info ', 'Training model with new image ')
        #TRAIN FUNCTON here
        facerec.save_encodings()
        tab_1_label_msg.configure(text='Student Sucessfully Entered', fg="green")
        messagebox.showinfo('sucess ', 'Student Sucessfully Entered')
        clear()
 
    else:
        tab_1_label_msg.configure(text='Enter valid input', fg="red")
        messagebox.showerror('Input Error', 'Enter valid Input')





######################################### Tab 1 Buttons ##############################

take_image_btn = Button(enter_new_user_tab, text="Take Image", bg="orange", fg="white", command=takeImage)
take_image_btn.place(relx=0.2,x=50,y=160 )






#---------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------TAB 2 -----------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------#
######################################### Tab 2 Widgets ##############################



######################################### Tab 1 Functions ##############################

def take_attendance():
    status = facerec.track_image()
    if status:
        messagebox.showinfo('Sucess ', 'Student attendance given Sucessfully')        
    else:
        messagebox.showerror('No Attendance Given', 'Face is neither Recognized nor Detected')



######################################### Tab 2 Buttons ##############################

take_image_btn = Button(take_attendance_tab, text="Take Image", bg="pink", fg="white", command=take_attendance, font=('times', 15, ' bold '))
take_image_btn.place(relx=0.2,x=0,y=30 )









#---------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------TAB 3 -----------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------#
######################################### Tab 3 Widgets ##############################



######################################### Tab 3 Functions ##############################

def take_attendances():
    status = facerec.track_image()
    if status == 0:
        messagebox.showerror('No Attendance Given', 'Face is neither Recognized nor Detected')
    elif status == 1:
        messagebox.showwarning('Already taken !', 'Student has already given attendance')
    else:
        messagebox.showinfo('sucess ', 'Student has given attendance')
     




######################################### Tab 3 Buttons ##############################

take_image_btn = Button(take_attendance_tab, text="Take Image", bg="pink", fg="white", command=take_attendances, font=('times', 15, ' bold '))
take_image_btn.place(relx=0.2,x=0,y=30 )







































tab_control.pack(expand=1, fill='both')
window.mainloop()










