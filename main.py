from tkinter import *
import tkinter as tk
import pytz
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import requests 
from PIL import Image, ImageTk
from tkinter import messagebox, ttk

root = Tk()
root.title("Weather App 5")
root.geometry("750x470+300+200")
root.resizable(False,False)
root.config(bg="#202731")




#icon
image_icon=PhotoImage(file="Images/logo.png")
root.iconphoto(False, image_icon)


Round_box=PhotoImage(file="Images/Round Rectangle 1.png")
Label(root,image=Round_box,bg="#202731").place(x=0,y=0)


root.mainloop()