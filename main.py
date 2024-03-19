import customtkinter
import tkinter as tk
from customtkinter import *

set_appearance_mode("light")
set_default_color_theme("green")

app = CTk()
app.geometry("1280x720")

def Safety():
    pass
def Measurement():
    pass
def ObjDetection():
    pass
def Color():
    pass


btn1 = CTkButton(master=app, text="SAFETY", command=Safety, corner_radius=15, height=90, width=300)
btn1.place(relx=0.75, rely=0.25, anchor="center")

btn2 = CTkButton(master=app, text="MEASUREMENT", command=Measurement, corner_radius=15, height=90, width=300)
btn2.place(relx=0.75, rely=0.4, anchor="center")

btn3 = CTkButton(master=app, text="OBJECT DETECTION", command=ObjDetection, corner_radius=15, height=90, width=300)
btn3.place(relx=0.75, rely=0.55, anchor="center")

btn4 = CTkButton(master=app, text="COLOR", command=Color, corner_radius=15, height=90, width=300)
btn4.place(relx=0.75, rely=0.7, anchor="center")

line = CTkButton(master=app, text="", command=None, corner_radius=30, height=425, width=10)
line.place(relx=0.55, rely=0.475, anchor="center")

textbox = customtkinter.CTkTextbox(app)
textbox.insert("0.0", "new text to insert")  # insert at line 0 character 0
text = textbox.get("0.0", "end")  # get text from line 0 character 0 till the end
textbox.configure(state="disabled")  # configure textbox to be read-only

vs = CTkLabel(master=app, text="Vision System")
vs.place(relx=0.225, rely=0.15, anchor="w")
vs.configure(font=('Helvetica bold', 34))

themeValue = StringVar(value="off")
def toggleTheme():
    if themeValue.get() == "on":
        set_appearance_mode("dark")
    else:
        set_appearance_mode('light')

themeToggleButton = CTkSwitch(master=app, text="Dark Mode", command=toggleTheme, variable=themeValue, onvalue = "on", offvalue="off")
themeToggleButton.place(relx=0.96, rely=0.95, anchor=SE)
themeToggleButton.configure(font=("Helvetica bold", 26))




app.mainloop()
