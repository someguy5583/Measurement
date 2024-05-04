from customtkinter import *
from customtkinter import CTkFrame
from VideoCapture import VideoCapture
from random import choice
from tkinter import *
import tkinter as tk
vca = VideoCapture()
m_app: CTk = None
is_running = False
measurementHub: CTkToplevel = None
frame: CTkFrame = None

def Measurement():
    global vca, m_app, is_running, measurementHub, frame
    is_running = True

    measurementHub = CTkToplevel(m_app)
    measurementHub.title("Main Hub (Measurement)")
    measurementHub.geometry("1280x720")

    vca = VideoCapture()

    measurementHub.after(1, lambda: measurementHub.focus_force())

    ## ---- UI ---- ##
    btn1 = CTkButton(measurementHub, text="TEST", command=None, corner_radius=15, height=90, width=300)
    btn1.place(relx=0.75, rely=0.25, anchor="center")

    btn3 = CTkButton(measurementHub, text="SETTINGS", command=settings, corner_radius=15, height=100,width=300)
    btn3.place(relx=0.75, rely=0.475, anchor="center")

    btn4 = CTkButton(measurementHub, text="DATA", command=None, corner_radius=15, height=90, width=300)
    btn4.place(relx=0.75, rely=0.7, anchor="center")

    line = CTkButton(measurementHub, text="", command=None, corner_radius=30, height=425, width=10)
    line.place(relx=0.55, rely=0.475, anchor="center")

    vs = CTkLabel(measurementHub, text="Vision System (Measurement)")
    vs.place(relx=0.125, rely=0.15, anchor="w")
    vs.configure(font=('Helvetica bold', 34))

    frame = CTkFrame(master=measurementHub, width=500, height=350)
    frame.place(relx=0.1, rely=0.5, anchor="w")

    measurementHub.protocol("WM_DELETE_WINDOW", MeasurementClose)

    MeasurementUpdate()


def MeasurementUpdate():
    global vca, is_running
    if not is_running:
        return

    img = vca.update_frame()
    label = CTkLabel(frame, image=img, text="")
    label.image = img
    label.place(relx=0.5, rely=0.5, anchor="center")



def MeasurementClose():
    global vca, is_running
    is_running = False

    vca.close_app()
    measurementHub.destroy()

def test():
    pass

def settings():
    global m_app

    MeasurementClose()

    settingsPage = CTkToplevel(m_app)
    settingsPage.title("Settings Page")
    settingsPage.geometry("1280x720")

    settingsPage.after(1, lambda: settingsPage.focus_force())

    ## ---- UI ---- ##
    titleBox = CTkFrame(master=settingsPage, width=1240, height=100)
    titleBox.place(relx=0.5, rely=0.1, anchor="center")
    title = CTkLabel(master=titleBox, text="SETTINGS", text_color="darkgrey")
    title.place(relx=0.5, rely=0.5, anchor="center")
    title.configure(font=('Verdana', 34))

    points = ["Part 1", "Part 2", "Part 3", "Part 4", "Part 5", "Part 6", "Part 7", "Part 8", "Part 9", "Part 10"]

    def pointData():
        pass

    dropdown = CTkComboBox(settingsPage, values=points, command=pointData, height=35, width=200, corner_radius=5, border_width=0, button_color="#4d94ff", button_hover_color="lightskyblue", dropdown_hover_color="#4d94ff", justify="center", dropdown_font=("Helvetica bold", 18))
    dropdown.place(relx=0.0932, rely=0.21, anchor="center")

    new = CTkButton(settingsPage, text="New", command=None, height=35, width=150)
    new.place(relx=0.3, rely=0.21, anchor="center")

    edit = CTkButton(settingsPage, text="Edit", command=None, height=35, width=150)
    edit.place(relx=0.43, rely=0.21, anchor="center")

    save = CTkButton(settingsPage, text="Save", command=None, height=35, width=150)
    save.place(relx=0.56, rely=0.21, anchor="center")

    delete = CTkButton(settingsPage, text="Delete", command=None, height=35, width=150)
    delete.place(relx=0.69, rely=0.21, anchor="center")

    capture = CTkButton(settingsPage, text="Capture", command=None, height=40, width=200)
    capture.place(relx=0.0932, rely=0.35, anchor="center")

    partTextBox1 = CTkTextbox(settingsPage, height=50, width=200)
    partTextBox1.place(relx=0.0932, rely=0.45, anchor="center")
    partTextBox2 = CTkTextbox(settingsPage, height=50, width=200)
    partTextBox2.place(relx=0.0932, rely=0.55, anchor="center")
    partTextBox3 = CTkTextbox(settingsPage, height=50, width=200)
    partTextBox3.place(relx=0.0932, rely=0.65, anchor="center")
    partTextBox4 = CTkTextbox(settingsPage, height=50, width=200)
    partTextBox4.place(relx=0.0932, rely=0.75, anchor="center")

    ImageBox = CTkFrame(settingsPage, width=500, height=350)
    ImageBox.place(relx=0.5, rely=0.55, anchor="c")

    def create_table(window, data):
        num_rows = len(data)
        num_cols = len(data[0])

        for i in range(num_rows):
            for j in range(num_cols):
                label = Label(window, text=data[i][j], borderwidth=1, relief="solid")
                label.grid(row=i, column=j)

    # Example data for the table
    table_data = [
        ["Points", "Spec", "Min", "Maxx "],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],   
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""]
    ]

    # Create a frame to contain the table
    table_frame = Frame(settingsPage)
    table_frame.place(relx=0.85, rely=0.5,anchor="center")

    # Create the table
    create_table(table_frame, table_data)


def data():
    pass

