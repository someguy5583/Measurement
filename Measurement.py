import colorsys

import cv2
from customtkinter import *
from customtkinter import CTkFrame
import random
from VideoCapture import VideoCapture
from random import choice
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from HandSafetyTool.Circle import Circle
from HandSafetyTool.Rectangle import Rectangle
from HandSafetyTool.Polygon import Polygon

shapes = []
was_down = False
shape_index = 0
isUpdatingShapes = False
shapeId = 0
connection = sqlite3.connect("pointsData.db")
cursor = connection.cursor()
command1 = """CREATE TABLE IF NOT EXISTS
points(supplierName TEXT, vendorCode TEXT, partNumber INTEGER PRIMARY KEY, partName TEXT, lotCount INTEGER)"""
cursor.execute(command1)

drawCallback = None

vca = VideoCapture()
m_app: CTk = None
is_running = False
measurementHub: CTkToplevel = None
frame: CTkCanvas = None

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

    frame = CTkCanvas(master=measurementHub, width=500, height=350)
    frame.place(relx=0.1, rely=0.5, anchor="w")

    measurementHub.protocol("WM_DELETE_WINDOW", MeasurementClose)
    print("like come")
    MeasurementUpdate()


def MeasurementUpdate():
    global vca, frame
    # Update the frame with the latest image from the video capture
    cv2img = vca.update_frame()
    if drawCallback:
        cv2img = drawCallback(cv2img)
    img = vca.CV2CTk(cv2img)

    # Check if the parent widget exists and is valid
    if frame.winfo_exists():
        # Create a new label widget with the updated image
        frame.delete("all")
        frame.create_image(0, 0, anchor="nw", image=img)
        frame.image = img  # Keep a reference to avoid garbage collection


def getFrame():
    return frame


def MeasurementClose():
    global vca, is_running
    is_running = False

    vca.close_app()
    measurementHub.destroy()

def test():
    pass


def settings():
    global m_app, vca, is_running, frame, drawCallback

    MeasurementClose()

    vca = VideoCapture()
    is_running = True

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

    cursor.execute("""SELECT partNumber FROM points""")
    partNumbers = [x[0] for x in cursor.fetchall()]
    points = ["Select P/N"] + [f"Part {x}" for x in partNumbers]
    print(points)

    def Capture():
        global is_running
        is_running = False
    def pointData(partNumber):
        if partNumber == "Select P/N":
            supplierNameTextBox.delete(1.0, "end-1c")
            vendorCodeTextBox.delete(1.0, "end-1c")
            partNumberTextBox.delete(1.0, "end-1c")
            partNameTextBox.delete(1.0, "end-1c")
            lotCountTextBox.delete(1.0, "end-1c")
            return

        partNumber = int(partNumber.split()[-1])
        cursor.execute(f"""SELECT * FROM points WHERE partNumber={partNumber}""")

        row = cursor.fetchall()
        supplierNameTextBox.delete(1.0, "end-1c")
        supplierNameTextBox.insert("end-1c", row[0][0])
        vendorCodeTextBox.delete(1.0, "end-1c")
        vendorCodeTextBox.insert("end-1c", row[0][1])
        partNumberTextBox.delete(1.0, "end-1c")
        partNumberTextBox.insert("end-1c", row[0][2])
        partNameTextBox.delete(1.0, "end-1c")
        partNameTextBox.insert("end-1c", row[0][3])
        lotCountTextBox.delete(1.0, "end-1c")
        lotCountTextBox.insert("end-1c", row[0][4])

    dropdown = CTkComboBox(settingsPage, values=points, command=pointData, height=35, width=200, corner_radius=5, border_width=0, button_color="#4d94ff", button_hover_color="lightskyblue", dropdown_hover_color="#4d94ff", justify="center", dropdown_font=("Helvetica bold", 18))
    dropdown.place(relx=0.0932, rely=0.21, anchor="center")

    capture = CTkButton(settingsPage, text="Capture", command=Capture, height=40, width=200)
    capture.place(relx=0.0932, rely=0.35, anchor="center")

    supplierNameLabel = CTkLabel(settingsPage, text="Supplier Name:", font=("Verdana", 11))
    supplierNameLabel.place(relx=0.0182, rely=0.38)
    supplierNameLabel.lower()
    supplierNameTextBox = CTkTextbox(settingsPage, height=50, width=200)
    supplierNameTextBox.place(relx=0.0932, rely=0.45, anchor="center")
    vendorCodeLabel = CTkLabel(settingsPage, text="Vendor Code:", font=("Verdana", 11))
    vendorCodeLabel.place(relx=0.0182, rely=0.48)
    vendorCodeLabel.lower()
    vendorCodeTextBox = CTkTextbox(settingsPage, height=50, width=200)
    vendorCodeTextBox.place(relx=0.0932, rely=0.55, anchor="center")
    partNumberLabel = CTkLabel(settingsPage, text="Part Number:", font=("Verdana", 11))
    partNumberLabel.place(relx=0.0182, rely=0.58)
    partNumberLabel.lower()
    partNumberTextBox = CTkTextbox(settingsPage, height=50, width=200)
    partNumberTextBox.place(relx=0.0932, rely=0.65, anchor="center")
    partNameLabel = CTkLabel(settingsPage, text="Part Name:", font=("Verdana", 11))
    partNameLabel.place(relx=0.0182, rely=0.68)
    partNameLabel.lower()
    partNameTextBox = CTkTextbox(settingsPage, height=50, width=200)
    partNameTextBox.place(relx=0.0932, rely=0.75, anchor="center")
    lotCountLabel = CTkLabel(settingsPage, text="Lot Count:", font=("Verdana", 11))
    lotCountLabel.place(relx=0.0182, rely=0.78)
    lotCountLabel.lower()
    lotCountTextBox = CTkTextbox(settingsPage, height=50, width=200)
    lotCountTextBox.place(relx=0.0932, rely=0.85, anchor="center")

    def onImageClick(event):
        global isUpdatingShapes, was_down, shape_index
        if not isUpdatingShapes:
            return
        x, y = event.x, event.y
        positions = [[x, y], [x, y]]
        color = colorsys.hsv_to_rgb(random.random(), random.random() * .5 + .5, 1)
        color = (color[0] * 255, color[1] * 255, color[2] * 255)
        shapes.append(Rectangle(positions, color))
        shape_index = len(shapes) - 1
        print(shape_index)
        was_down = True
    def onImageRelease(event):
        global was_down
        was_down = False

    def onImageDrag(event):
        global was_down, shape_index
        if not was_down:
            return
        x, y = event.x, event.y
        pos1 = shapes[shape_index].get_positions()[0]
        positions = [pos1, [x, y]]
        shapes[shape_index].set_positions(positions)

    frame = CTkCanvas(settingsPage, width=500, height=350, bg="lightgray", highlightthickness=0)
    frame.bind("<Button-1>", onImageClick)
    frame.bind("<ButtonRelease-1>", onImageRelease)
    frame.bind("<B1-Motion>", onImageDrag)

    frame.place(relx=0.45, rely=0.6, anchor="c")

    def renderShapes(frame):
        global shapes, shape_index
        print("disgusting")
        for i in range(len(shapes)):
            shapes[i].render(frame, 6, i, isUpdatingShapes)
        return frame

    MeasurementUpdate()
    drawCallback = renderShapes


    # Function to be called when the "button" is clicked
    def onRectangleButtonClick(event):
        #get pointer position, drag pointer, get pointer position, make rectangle in those pointer positions
        global isUpdatingShapes, shapeId
        isUpdatingShapes = not isUpdatingShapes
        shapeId = 0
        if isUpdatingShapes:
            canvas_button.configure(bg = "lightblue")
        else:
            canvas_button.configure(bg = "blue")
    # Create a Canvas widget to represent the button with a yellow square outline on a blue background
    canvas_button = CTkCanvas(settingsPage, width=50, height=50, bg="blue", highlightthickness=0)
    canvas_button.create_rectangle(10, 10, 40, 40, outline="yellow", width=2)

    # Bind the Canvas widget to the click event
    canvas_button.bind("<Button-1>", onRectangleButtonClick)
    # Place the canvas above the ImageBox
    canvas_button.place(relx=0.275, rely=0.3, anchor="center")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#444",
                    fieldbackground="#444",
                    foreground="white",
                    font=("Arial", 10),
                    borderwidth=1,
                    relief="solid",
                    )

    style.map("Treeview",
              background=[('selected', '#D3D3D3')],
              foreground=[('selected', 'black')],
              )

    table = ttk.Treeview(settingsPage, columns=("Points", "Spec", "Min", "Max"), show="headings")
    table.heading('Points', text='Points')
    table.heading('Spec', text='Spec')
    table.heading('Min', text='Min')
    table.heading('Max', text='Max')

    table.column("Points", width=75)
    table.column("Spec", width=75)
    table.column("Min", width=75)
    table.column("Max", width=75)

    table.insert("", "end", values=("Data1", "Data2", "Data3", "Data4"))

    table.place(relx=0.85, rely=0.6, anchor="center", height = 400)

    def saveData():
        # Retrieve values from textboxes
        supplier_name = supplierNameTextBox.get("1.0", "end").strip()
        vendor_code = vendorCodeTextBox.get("1.0", "end").strip()
        part_number = partNumberTextBox.get("1.0", "end").strip()
        part_name = partNameTextBox.get("1.0", "end").strip()
        lot_count = lotCountTextBox.get("1.0", "end").strip()

        if not (supplier_name and vendor_code and part_number and part_name and lot_count):
            # Ensure all fields are filled before saving
            print("Please fill all fields before saving.")
            return
        saved = messagebox.askokcancel("Continue", "Data saved successfully")
        if saved:
            try:
                # Convert part_number to int
                part_number = int(part_number)
                # Check if part_number already exists in the database
                cursor.execute("SELECT partNumber FROM points WHERE partNumber=?", (part_number,))
                existing_part = cursor.fetchone()
                if existing_part:
                    # If part_number exists, update the record
                    cursor.execute(
                        "UPDATE points SET supplierName=?, vendorCode=?, partName=?, lotCount=? WHERE partNumber=?",
                        (supplier_name, vendor_code, part_name, lot_count, part_number))
                else:
                    # If part_number doesn't exist, insert a new record
                    cursor.execute(
                        "INSERT INTO points (supplierName, vendorCode, partNumber, partName, lotCount) VALUES (?, ?, ?, ?, ?)",
                        (supplier_name, vendor_code, part_number, part_name, lot_count))

                # Commit the transaction
                connection.commit()
                print("Data saved successfully.")

                # Update dropdown menu with new data
                cursor.execute("""SELECT partNumber FROM points""")
                partNumbers = [x[0] for x in cursor.fetchall()]
                points = ["Select P/N"] + [f"{x}" for x in partNumbers]
                dropdown.configure(values=points)  # Update dropdown values
                supplierNameTextBox.delete(1.0, "end")
                vendorCodeTextBox.delete(1.0, "end")
                partNumberTextBox.delete(1.0, "end")
                partNameTextBox.delete(1.0, "end")
                lotCountTextBox.delete(1.0, "end")
            except sqlite3.Error as e:
                print("Error occurred while saving data:", e)

    def deleteData():
        # Get the selected part number from the dropdown menu
        selected_part = dropdown.get()

        # Ensure a valid part number is selected
        if selected_part == "Select P/N":
            print("Please select a valid part number.")
            return

        # Extract the part number from the selected option
        part_number = int(selected_part.split(" ")[1])

        # Ask for confirmation before deletion
        confirm = messagebox.askyesno("Confirmation", f"Do you want to delete Part {part_number}?")

        if confirm:
            try:
                # Execute the SQL DELETE statement to remove the record
                cursor.execute("DELETE FROM points WHERE partNumber=?", (part_number,))

                # Commit the transaction
                connection.commit()
                print("Data deleted successfully.")

                # Update dropdown menu with updated data
                cursor.execute("""SELECT partNumber FROM points""")
                partNumbers = [x[0] for x in cursor.fetchall()]
                points = ["Select P/N"] + [f"Part {x}" for x in partNumbers]
                dropdown.configure(values=points)  # Update dropdown values

                # Clear the text fields after successful deletion
                supplierNameTextBox.delete(1.0, "end")
                vendorCodeTextBox.delete(1.0, "end")
                partNumberTextBox.delete(1.0, "end")
                partNameTextBox.delete(1.0, "end")
                lotCountTextBox.delete(1.0, "end")

            except sqlite3.Error as e:
                print("Error occurred while deleting data:", e)

    # Inside the settings() function, after creating the delete button:
    delete = CTkButton(settingsPage, text="Delete", command=deleteData, height=35, width=150)
    delete.place(relx=0.515, rely=0.21, anchor="center")

    save = CTkButton(settingsPage, text="Save", command=saveData, height=35, width=150)
    save.place(relx=0.385, rely=0.21, anchor="center")


def data():
    pass

