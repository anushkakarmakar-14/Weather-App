from tkinter import *
import tkinter as tk
import pytz
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import requests 
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
from timezonefinder import TimezoneFinder

root = Tk()
root.title("Weather App 5")
root.geometry("750x470+300+200")
root.resizable(False,False)
root.config(bg="#202731")


def getWeather():
    city = textfield.get()
    geolocator = Nominatim(user_agent="new")
    location = geolocator.geocode(city)
    obj=TimezoneFinder()
    result = obj.timezone_at(lat=location.latitude, lng=location.longitude)
    timezone.config(text=result)

    long_lat.config(text=f"{round(location.latitude,4)}°N {round(location.longitude,4)}°E")

    home=pytz.timezone(result)
    local_time=datetime.now(home)
    current_time=local_time.strftime("%I:%M %p")
    clock.config(text=current_time)

    api_key="d0bebc59ce406c638d2aeb77b036ff4f"
    api = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    json_data=requests.get(api).json()
    print(json_data)

    #current Weather from first Forecast
    current = json_data['list'][0]
    temp = current['main']['temp']
    humidity = current['main']['humidity']
    pressure = current['main']['pressure']
    wind_speed=current['wind']['speed']
    description=current['weather'][0]['description']
    #icon = current['weather'][0]['icon']

    t.config(text=f"{temp}C")
    h.config(text=f"{humidity}%")
    p.config(text=f"{pressure} hPa")
    w.config(text=f"{wind_speed} m/s")
    d.config(text=f"{description}")



#icon
#image_icon=PhotoImage(file="Images/logo.png")
image_icon = PhotoImage(file=r"C:\Users\Anushka\Desktop\git_project\Weather-App\Images\logo.png")
root.iconphoto(False, image_icon)


Round_box=PhotoImage(file=r"C:\Users\Anushka\Desktop\git_project\Weather-App\Images\Rounded Rectangle 1.png")
Label(root,image=Round_box,bg="#202731").place(x=40,y=60)

#label
label1 = Label(root,text="Temperature",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label1.place(x=50,y=120)

label2 = Label(root,text="Humidity",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label2.place(x=50,y=140)

label3 = Label(root,text="Pressure",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label3.place(x=50,y=160)

label4 = Label(root,text="Wind Speed",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label4.place(x=50,y=180)

label5 = Label(root,text="Description",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label5.place(x=50,y=200)

#Search box

Search_image=PhotoImage(file=r"C:\Users\Anushka\Desktop\git_project\Weather-App\Images\Rounded Rectangle 3.png")
myimage = Label(root,image=Search_image,bg="#202731")
myimage.place(x=270,y=122)

weat_image=PhotoImage(file=r"C:\Users\Anushka\Desktop\git_project\Weather-App\Images\Layer 7.png")
weatherimage=Label(root,image=weat_image,bg="#333c4c")
weatherimage.place(x=290,y=127)

textfield = tk.Entry(root,justify="center",width=15,font=("poppins",25,"bold"),bg="#333c4c",border=0,fg="white")
textfield.place(x=370,y=130)

search_icon=PhotoImage(file=r"C:\Users\Anushka\Desktop\git_project\Weather-App\Images\Layer 6.png")
myimage_icon=Button(root,image=search_icon,borderwidth=0,cursor="hand2",bg="#333c4c", command=getWeather)
myimage_icon.place(x=660,y=130)


#Bottom box
frame=Frame(root,width=900,height=180,bg="#7094d4")
frame.pack(side=BOTTOM)

#boxes
firstbox=PhotoImage(file=r"C:\Users\Anushka\Desktop\git_project\Weather-App\Images\Rounded Rectangle 2.png")
secondbox=PhotoImage(file=r"C:\Users\Anushka\Desktop\git_project\Weather-App\Images\Rounded Rectangle 2 copy.png")

#Labels
Label(frame,image=firstbox,bg="#7094d4").place(x=30,y=20)
Label(frame,image=secondbox,bg="#7094d4").place(x=300,y=30)
Label(frame,image=secondbox,bg="#7094d4").place(x=400,y=30)
Label(frame,image=secondbox,bg="#7094d4").place(x=500,y=30)
Label(frame,image=secondbox,bg="#7094d4").place(x=600,y=30)


#clock
clock=Label(root,font=("Helvetica",20),bg="#202731",fg="white")
clock.place(x=30,y=20)

#timezone
timezone=Label(root,font=("Helvetica",20),bg="#202731",fg="white")
timezone.place(x=500,y=20)

long_lat=Label(root,font=("Helvetica",10),bg="#202731",fg="White")
long_lat.place(x=500,y=50)

#thpwd
t=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
t.place(x=150,y=200)

h=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
h.place(x=150,y=200)

p=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
p.place(x=150,y=200)

w=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
w.place(x=150,y=200)

d=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
d.place(x=150,y=200)


#first cell
firstframe=Frame(frame,width=230,height=132,bg="#323661")
firstframe.place(x=35,y=315)

firstimage=Label(firstframe,bg="#323661")
firstimage.place(x=1,y=15)

day1=Label(firstframe,font=("arial 20"),bg="#323661",fg="white")
day1.place(x=100,y=5)

day1temp=Label(firstframe,font=("arial 15 bold"),bg="#323661",fg="white")
day1temp.place(x=100,y=50)

#Second cell
secondframe=Frame(root,width=70,height=115,bg="#eeefea")
secondframe.place(x=305,y=325)

secondimage=Label(secondframe,bg="#eeefea")
secondimage.place(x=7,y=20)

day2=Label(secondframe,bg="#eeefea", fg="#000")
day2.place(x=10,y=5)

day2temp=Label(secondframe,bg="#eeefea",fg="#000")
day2temp.place(x=2,y=70)


#third cell
thirdframe=Frame(root,width=70,height=115,bg="#eeefea")
thirdframe.place(x=405,y=325)

thirdimage=Label(thirdframe,bg="#eeefea")
thirdimage.place(x=7,y=20)

day3=Label(thirdframe,bg="#eeefea", fg="#000")
day3.place(x=10,y=5)

day3temp=Label(thirdframe,bg="#eeefea",fg="#000")
day3temp.place(x=2,y=70)


#fourth cell
fourthframe=Frame(root,width=70,height=115,bg="#eeefea")
fourthframe.place(x=505,y=325)

fourthimage=Label(fourthframe,bg="#eeefea")
fourthimage.place(x=7,y=20)

day4=Label(fourthframe,bg="#eeefea", fg="#000")
day4.place(x=10,y=5)

day4temp=Label(fourthframe,bg="#eeefea",fg="#000")
day4temp.place(x=2,y=70)

#fifth cell
fifthframe=Frame(root,width=70,height=115,bg="#eeefea")
fifthframe.place(x=605,y=325)

fifthimage=Label(fifthframe,bg="#eeefea")
fifthimage.place(x=7,y=20)

day4=Label(fifthframe,bg="#eeefea", fg="#000")
day4.place(x=10,y=5)

day4temp=Label(fifthframe,bg="#eeefea",fg="#000")
day4temp.place(x=2,y=70)




root.mainloop()