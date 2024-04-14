from customtkinter import *
import cv2
from VideoCapture import *
import Measurement
from PIL import Image, ImageTk

set_appearance_mode("light")
set_default_color_theme("blue")

app = CTk()
app.title("Main/Central Hub")
app.geometry("1280x720")
Measurement.m_app = app

def Safety():
    safetyHub = CTkToplevel(app)
    safetyHub.title("Main Hub (Safety)")
    safetyHub.geometry("1280x720")

    # safetyHub.after(1, lambda: safetyHub.focus_force())
    safetyHub.focus_force()
def ObjDetection():
    OBJdetectionHub = CTkToplevel(app)
    OBJdetectionHub.title("Main Hub (Object Detection)")
    OBJdetectionHub.geometry("1280x720")

    OBJdetectionHub.after(1, lambda: OBJdetectionHub.focus_force())


def Color():
    ColorHub = CTkToplevel(app)
    ColorHub.title("Main Hub (Color)")
    ColorHub.geometry("1280x720")

    ColorHub.after(1, lambda: ColorHub.focus_force())


btn1 = CTkButton(master=app, text="SAFETY", command=Safety, corner_radius=15, height=90, width=300)
btn1.place(relx=0.75, rely=0.25, anchor="center")

btn2 = CTkButton(master=app, text="MEASUREMENT", command=Measurement.Measurement, corner_radius=15, height=90, width=300)
btn2.place(relx=0.75, rely=0.4, anchor="center")

btn3 = CTkButton(master=app, text="OBJECT DETECTION", command=ObjDetection, corner_radius=15, height=90, width=300)
btn3.place(relx=0.75, rely=0.55, anchor="center")

btn4 = CTkButton(master=app, text="COLOR", command=Color, corner_radius=15, height=90, width=300)
btn4.place(relx=0.75, rely=0.7, anchor="center")

line = CTkButton(master=app, text="", command=None, corner_radius=30, height=425, width=10, state="disabledb")
line.place(relx=0.55, rely=0.475, anchor="center")

vs = CTkLabel(master=app, text="Vision System")
vs.place(relx=0.225, rely=0.15, anchor="w")
vs.configure(font=('Verdana', 34))

themeValue = StringVar(value="off")


def toggleTheme():
    if themeValue.get() == "on":
        set_appearance_mode("dark")
    else:
        set_appearance_mode('light')

themeToggleButton = CTkSwitch(master=app, text="Dark Mode", command=toggleTheme, variable=themeValue, onvalue = "on", offvalue="off")
themeToggleButton.place(relx=0.96, rely=0.95, anchor=SE)
themeToggleButton.configure(font=("Helvetica bold", 26))

is_running = True
def OnWindowClose():
    global is_running
    is_running = False
    # app.destroy()

app.protocol("WM_DELETE_WINDOW", OnWindowClose)


while True:
    if not is_running:
        break

    app.update_idletasks()
    app.update()

    print(Measurement.is_running)

    if Measurement.is_running:
        Measurement.MeasurementUpdate()
