import colorsys
from EntryPopup import EntryPopup

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
import math

shapes = []
creating_poly = False
was_down = False
shape_index = 0
isUpdatingShapes = False
shape_type = 0
freeze_frame = None
frozen = False

connection = sqlite3.connect("pointsData.db")
cursor = connection.cursor()
command1 = """CREATE TABLE IF NOT EXISTS
points(supplierName TEXT, vendorCode TEXT, part_number INTEGER PRIMARY KEY, partName TEXT, lotCount INTEGER)"""
cursor.execute(command1)
command2 = """CREATE TABLE IF NOT EXISTS
shapes(idx INTEGER PRIMARY KEY, spec INTEGER, min INTEGER, max INTEGER, shape TEXT, shape_index INTEGER, part_number INTEGER, FOREIGN KEY(part_number) REFERENCES points(part_number))"""
cursor.execute(command2)

drawCallback = None

vca = VideoCapture()
m_app: CTk = None
is_running = False
measurementHub: CTkToplevel = None
frame: CTkCanvas = None

def Measurement():
    global vca, m_app, is_running, measurementHub, frame, drawCallback
    is_running = True

    measurementHub = CTkToplevel(m_app)
    measurementHub.title("Main Hub (Measurement)")
    measurementHub.geometry("1280x720")

    vca = VideoCapture()

    measurementHub.after(1, lambda: measurementHub.focus_force())

    ## ---- UI ---- ##
    btn1 = CTkButton(measurementHub, text="TEST", command=test, corner_radius=15, height=90, width=300)
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

    drawCallback = None
    MeasurementUpdate()


def MeasurementUpdate():
    global vca, frame, freeze_frame, frozen
    # Update the frame with the latest image from the video capture
    cv2img = vca.update_frame()
    if frozen:
        cv2img = freeze_frame.copy()

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
    global m_app, vca, is_running, frame, drawCallback

    MeasurementClose()

    vca = VideoCapture()
    is_running = True

    testPage = CTkToplevel(m_app)
    testPage.title("Testing Page")
    testPage.geometry("1280x720")

    testPage.after(1, lambda: testPage.focus_force())
    testPage.after(201, lambda: testPage.iconbitmap('logo.jpeg'))

    dropdown = CTkComboBox(testPage, values=None, command=None, height=35, width=200, corner_radius=5,
                           border_width=0, button_color="#4d94ff", button_hover_color="lightskyblue",
                           dropdown_hover_color="#4d94ff", justify="center", dropdown_font=("Helvetica bold", 18))
    dropdown.place(relx=0.0075, rely=0.01, anchor="nw")


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

    cursor.execute("""SELECT part_number FROM points""")
    partNumbers = [x[0] for x in cursor.fetchall()]
    points = ["Select P/N"] + [f"Part {x}" for x in partNumbers]
    print(points)

    def Capture():
        global freeze_frame, frozen, partNumber
        freeze_frame = vca.update_frame()
        partNumber = 0
        try:
            partNumber = int(partNumberTextBox.get('1.0', 'end').strip())
        except:
            return
        frozen = True
        cv2.imwrite(f"image{partNumber}.jpeg", freeze_frame)
    def pointData(partNumber):
        global shapes, freeze_frame, frozen
        if partNumber == "Select P/N":
            supplierNameTextBox.delete(1.0, "end-1c")
            vendorCodeTextBox.delete(1.0, "end-1c")
            partNumberTextBox.delete(1.0, "end-1c")
            partNameTextBox.delete(1.0, "end-1c")
            lotCountTextBox.delete(1.0, "end-1c")

            frozen = False
            freeze_frame = None

            for i in range(len(shapes)):
                shapes.pop()
                popRow()
            return

        partNumber = int(partNumber.split()[-1])
        cursor.execute(f"""SELECT * FROM points WHERE part_number={partNumber}""")

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

        cursor.execute(f"SELECT * FROM shapes WHERE part_number={partNumber}")
        rows = cursor.fetchall()
        shapesstr = [shape[4] for shape in rows]
        shapes = []

        for i in range(len(rows)):
            color = colorsys.hsv_to_rgb(random.random(), random.random() * .5 + .5, 1)
            color = (color[0] * 255, color[1] * 255, color[2] * 255)

            sus = shapesstr[i].split('|')
            if sus[0] == "Rect":
                shapes.append(Rectangle(Rectangle.read(sus[1]), color))
                print(shapes[-1])
            elif sus[0] == "Circle":
                shapes.append(Circle(Circle.read(sus[1]), color))
            else:
                shapes.append(Polygon(Polygon.read(sus[1]), color))
            addRow(-1, rows[i][1], rows[i][2], rows[i][3])

        freeze_frame = cv2.imread(f"image{partNumber}.jpeg")
        if freeze_frame is not None:
            frozen = True
        else:
            frozen = False

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
        global isUpdatingShapes, was_down, shape_index, shape_type, creating_poly
        if not isUpdatingShapes:
            return
        x, y = event.x, event.y
        positions = [[x, y], [x, y]]
        color = colorsys.hsv_to_rgb(random.random(), random.random() * .5 + .5, 1)
        color = (color[0] * 255, color[1] * 255, color[2] * 255)

        if shape_type == 0:
            shapes.append(Rectangle(positions, color))
        elif shape_type == 1:
            shapes.append(Circle(positions, color))
        elif shape_type == 2:
            if creating_poly:
                if len(shapes) != 0 and len(shapes[shape_index].positions) == 0:
                    shapes.pop(shape_index)
                color = colorsys.hsv_to_rgb(random.random(), random.random() * .5 + .5, 1)
                color = (color[0] * 255, color[1] * 255, color[2] * 255)
                shapes.append(Polygon([[x, y]], color))
                creating_poly = False
            else:
                shapes[shape_index].add_position([x, y])
        elif shape_type == 3:
            shapes.append(Polygon(positions, color, name="Line"))

        shape_index = len(shapes) - 1

        was_down = True
    def onImageRelease(event):
        global was_down, isUpdatingShapes
        was_down = False
        if isUpdatingShapes:
            addRow(shape_index)

    def onImageDrag(event):
        global was_down, shape_index
        if not was_down:
            return
        x, y = event.x, event.y
        positions = shapes[shape_index].get_positions()
        positions = positions[:-1]+[[x, y]]
        shapes[shape_index].set_positions(positions)

    frame = CTkCanvas(settingsPage, width=500, height=350, bg="lightgray", highlightthickness=0)
    frame.bind("<Button-1>", onImageClick)
    frame.bind("<ButtonRelease-1>", onImageRelease)
    frame.bind("<B1-Motion>", onImageDrag)

    frame.place(relx=0.45, rely=0.6, anchor="c")

    def renderShapes(frame):
        global shapes, shape_index
        for i in range(len(shapes)):
            shapes[i].render(frame, 2, i, isUpdatingShapes)
        return frame

    MeasurementUpdate()
    drawCallback = renderShapes

    def onCircleButtonClick(event):
        if not frozen:
            return

        global isUpdatingShapes, shape_type
        global creating_poly
        creating_poly = False
        if shape_type == 1:
            isUpdatingShapes = not isUpdatingShapes
        else:
            isUpdatingShapes = True
        shape_type = 1
        if isUpdatingShapes:
            circle_button.configure(bg="lightblue")
            rectangle_button.configure(bg="blue")
            polygon_button.configure(bg="blue")
            line_button.configure(bg="blue")
        else:
            circle_button.configure(bg="blue")
            rectangle_button.configure(bg="blue")
            polygon_button.configure(bg="blue")
            line_button.configure(bg="blue")

    # Create a Canvas widget to represent the button with a yellow circle outline on a blue background
    circle_button = CTkCanvas(settingsPage, width=50, height=50, bg="blue", highlightthickness=0)
    circle_button.create_oval(10, 10, 40, 40, outline="yellow", width=2)

    # Bind the Canvas widget to the click event
    circle_button.bind("<Button-1>", onCircleButtonClick)

    # Place the circle_button to the right of the existing canvas_button
    circle_button.place(relx=0.325, rely=0.3, anchor="center")

    # Function to be called when the "button" is clicked
    def onRectangleButtonClick(event):
        if not frozen:
            return

        global creating_poly
        creating_poly = False
        global isUpdatingShapes, shape_type
        if shape_type == 0:
            isUpdatingShapes = not isUpdatingShapes
        else:
            isUpdatingShapes = True
        shape_type = 0
        if isUpdatingShapes:
            circle_button.configure(bg="blue")
            rectangle_button.configure(bg="lightblue")
            polygon_button.configure(bg="blue")
            line_button.configure(bg="blue")
        else:
            circle_button.configure(bg="blue")
            rectangle_button.configure(bg="blue")
            polygon_button.configure(bg="blue")
            line_button.configure(bg="blue")
    # Create a Canvas widget to represent the button with a yellow square outline on a blue background
    rectangle_button = CTkCanvas(settingsPage, width=50, height=50, bg="blue", highlightthickness=0)
    rectangle_button.create_rectangle(10, 10, 40, 40, outline="yellow", width=2)

    # Bind the Canvas widget to the click event
    rectangle_button.bind("<Button-1>", onRectangleButtonClick)
    # Place the canvas above the ImageBox
    rectangle_button.place(relx=0.275, rely=0.3, anchor="center")

    fixed_polygon_points = [(15, 15), (35, 15), (45, 35), (25, 45), (5, 35)]

    # Function to be called when the "button" is clicked
    def onPolygonButtonClick(event):
        if not frozen:
            return

        global isUpdatingShapes, shape_type, shape_index, creating_poly
        creating_poly = True
        if shape_type == 2:
            isUpdatingShapes = not isUpdatingShapes
        else:
            isUpdatingShapes = True
        shape_type = 2
        if isUpdatingShapes:
            circle_button.configure(bg="blue")
            rectangle_button.configure(bg="blue")
            polygon_button.configure(bg="lightblue")
            line_button.configure(bg="blue")
        else:
            circle_button.configure(bg="blue")
            rectangle_button.configure(bg="blue")
            polygon_button.configure(bg="blue")
            line_button.configure(bg="blue")

    # Create a Canvas widget to represent the button with a yellow polygon outline on a blue background
    polygon_button = CTkCanvas(settingsPage, width=50, height=50, bg="blue", highlightthickness=0)
    polygon_button.create_polygon(fixed_polygon_points, outline="yellow", width=2, fill="")

    # Bind the Canvas widget to the click event
    polygon_button.bind("<Button-1>", onPolygonButtonClick)

    # Place the polygon_button to the right of the existing circle_button
    polygon_button.place(relx=0.275 + 0.05 * 2, rely=0.3, anchor="center")

    def onLineButtonClick(event):
        if not frozen:
            return

        global isUpdatingShapes, shape_type, shape_index
        global creating_poly
        creating_poly = False
        if shape_type == 3:
            isUpdatingShapes = not isUpdatingShapes
        else:
            isUpdatingShapes = True
        shape_type = 3
        if isUpdatingShapes:
            circle_button.configure(bg="blue")
            rectangle_button.configure(bg="blue")
            polygon_button.configure(bg="blue")
            line_button.configure(bg="lightblue")
        else:
            circle_button.configure(bg="blue")
            rectangle_button.configure(bg="blue")
            polygon_button.configure(bg="blue")
            line_button.configure(bg="blue")

    # Create a Canvas widget to represent the button with a gray line and arrows on both sides
    line_button = CTkCanvas(settingsPage, width=150, height=50, bg="blue", highlightthickness=0)

    # Draw the line
    line_button.create_line(10, 25, 140, 25, fill="yellow", width=2)

    # Draw the left arrow
    line_button.create_polygon(10, 25, 20, 20, 20, 30, fill="yellow", outline="yellow")

    # Draw the right arrow
    line_button.create_polygon(140, 25, 130, 20, 130, 30, fill="yellow", outline="yellow")

    # Bind the Canvas widget to the click event
    line_button.bind("<Button-1>", onLineButtonClick)

    # Place the line_button to the right of the existing polygon_button
    line_button.place(relx=0.275 + 0.05 * 3.75, rely=0.3, anchor="center")

    def undoShape():
        global shapes, shape_index, creating_poly
        shapes.pop()
        shape_index = len(shapes)-1
        if shape_type == 2:
            creating_poly = True
        popRow()


    undoButton = CTkButton(settingsPage, text="Undo", command=undoShape, height=50, width=150)
    undoButton.place(relx=0.275 + 0.1 * 3.1, rely=0.3, anchor="center")

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
              background=[('selected', '#FF00FF'), ('', '#00FF00')],
              foreground=[('selected', 'black')],
              )

    entryPopup = None
    def onDoubleClick(event):
        global entryPopup
        '''Executed, when a row is double-clicked'''
        # close previous popups
        try:  # in case there was no previous popup
            entryPopup.destroy()
        except:
            pass

        # what row and column was clicked on
        rowid = table.identify_row(event.y)
        column = table.identify_column(event.x)

        # return if the header was double clicked
        if not rowid:
            return

        # get cell position and cell dimensions
        x, y, width, height = table.bbox(rowid, column)
        print(x, y, width, height)

        # y-axis offset
        pady = height // 2

        # place Entry Widget
        text = table.item(rowid, 'values')[int(column[1:]) - 1]
        entryPopup = EntryPopup(table, rowid, int(column[1:]) - 1, text, updateTable)
        entryPopup.place(x=x, y=y + pady, width=width, height=height, anchor='w')
        
    table = ttk.Treeview(settingsPage, columns=("Points", "Spec", "Min", "Max"), show="headings")
    table.heading('Points', text='Points')
    table.heading('Spec', text='Spec')
    table.heading('Min', text='Min')
    table.heading('Max', text='Max')

    table.column("Points", width=75)
    table.column("Spec", width=75)
    table.column("Min", width=75)
    table.column("Max", width=75)

    table.bind("<Double-1>", onDoubleClick)

    table.place(relx=0.85, rely=0.6, anchor="center", height = 400)

    def addRow(indix, spec=0, min=0, max=0):
        part_number = partNumberTextBox.get("1.0", "end").strip()
        print(indix)
        table.insert("", "end", values=(f'{shapes[indix].name}_{indix}', str(spec), str(min), str(max)))

    def popRow(i: int = -1):
        print(len(table.get_children()) + i if i<0 else i)
        print(i)
        table.delete(table.get_children()[i])
    def updateTable(idx, vals:list):
        pass

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
        saved = messagebox.askokcancel("Continue", "Are you sure?")
        if saved:
            try:
                # Convert part_number to int
                part_number = int(part_number)
                # Check if part_numberx already exists in the database
                cursor.execute("SELECT part_number FROM points WHERE part_number=?", (part_number,))
                existing_part = cursor.fetchone()
                if existing_part:
                    # If part_number exists, update the record
                    cursor.execute(
                        "UPDATE points SET supplierName=?, vendorCode=?, partName=?, lotCount=? WHERE part_number=?",
                        (supplier_name, vendor_code, part_name, lot_count, part_number))

                    cursor.execute("DELETE FROM shapes WHERE part_number=?", (part_number,))
                    for shape_idx in range(len(shapes)):
                        cursor.execute(
                            "INSERT INTO shapes (spec, min, max, shape, shape_index, part_number) VALUES (?, ?, ?, ?, ?, ?)",
                            (0, 0, 0, str(shapes[shape_idx]), shape_idx, part_number))
                        print(shapes[shape_idx])

                    connection.commit()
                else:
                    # If part_number doesn't exist, insert a new record
                    cursor.execute(
                        "INSERT INTO points (supplierName, vendorCode, part_number, partName, lotCount) VALUES (?, ?, ?, ?, ?)",
                        (supplier_name, vendor_code, part_number, part_name, lot_count))

                # Commit the transaction
                connection.commit()
                print("Data saved successfully.")

                # Update dropdown menu with new dataj
                cursor.execute("""SELECT part_number FROM points""")
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

            for i in shapes:
                print(i)

    def deleteData():
        # Get the selected part number from the dropdown menu
        selected_part = dropdown.get()

        # Ensure a valid part number is selected
        if selected_part == "Select P/N":
            print("Please select a valid part number.")
            return

        # Extract the part number from the selected option
        part_number = int(partNumberTextBox.get("1.0", "end").strip())

        # Ask for confirmation before deletion
        confirm = messagebox.askyesno("Confirmation", f"Do you want to delete Part {part_number}?")

        if confirm:
            try:
                # Execute the SQL DELETE statement to remove the record
                cursor.execute("DELETE FROM points WHERE part_number=?", (part_number,))

                # Commit the transaction
                connection.commit()
                print("Data deleted successfully.")

                # Update dropdown menu with updated data
                cursor.execute("""SELECT part_number FROM points""")
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

