
import facerec

print("##################################################")
print("######## WELCOME TO FACE RECOGNITION #############")
print("##################################################")

print("1.Train mages\n2.Track Image")
ch = int(input("Enter Your choice"))


if(ch==1):
    print("Training Images Started ...")
    facerec.save_encodings()
elif(ch==2):
    print("Tracking Images started ...")
    facerec.track_image()
else:
    print("Wrong choice entered")