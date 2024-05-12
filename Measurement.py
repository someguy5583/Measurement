from customtkinter import *
from customtkinter import CTkFrame
from VideoCapture import VideoCapture
from random import choice
from tkinter import *
from tkinter import ttk
import sqlite3

connection = sqlite3.connect("pointsData.db")
cursor = connection.cursor()
command1 = """CREATE TABLE IF NOT EXISTS
points(supplierName TEXT, vendorCode TEXT, partNumber INTEGER PRIMARY KEY, partName TEXT, lotCount INTEGER)"""

cursor.execute(command1)



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

    cursor.execute("""SELECT partNumber FROM points""")
    points = ["Select P/N"]+[f"Part {x[0]}" for x in cursor.fetchall()]
    print(points)

    def pointData(partNumber):
        partNumber = int(partNumber[-1])
        cursor.execute(f"""SELECT * FROM points WHERE partNumber={partNumber}""")



    dropdown = CTkComboBox(settingsPage, values=points, command=pointData, height=35, width=200, corner_radius=5, border_width=0, button_color="#4d94ff", button_hover_color="lightskyblue", dropdown_hover_color="#4d94ff", justify="center", dropdown_font=("Helvetica bold", 18))
    dropdown.place(relx=0.0932, rely=0.21, anchor="center")

    new = CTkButton(settingsPage, text="New", command=None, height=35, width=150)
    new.place(relx=0.3, rely=0.21, anchor="center")

    edit = CTkButton(settingsPage, text="Edit", command=None, height=35, width=150)
    edit.place(relx=0.43, rely=0.21, anchor="center")

    delete = CTkButton(settingsPage, text="Delete", command=None, height=35, width=150)
    delete.place(relx=0.69, rely=0.21, anchor="center")

    capture = CTkButton(settingsPage, text="Capture", command=None, height=40, width=200)
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



    ImageBox = CTkFrame(settingsPage, width=500, height=350)
    ImageBox.place(relx=0.45, rely=0.55, anchor="c")

    style = ttk.Style()
    style.theme_use("clam")  # Use the "clam" theme to enable background color changes
    style.configure("Treeview",
                    background="#444",  # Darker background color
                    fieldbackground="#444",  # Background color of the fields
                    foreground="white",  # Font color
                    font=("Arial", 10),  # Example font configuration
                    borderwidth=1,  # Border width to separate cells
                    relief="solid",  # Border style
                    )

    # Configure the Treeview to show grid lines
    style.map("Treeview",
              background=[('selected', '#D3D3D3')],  # Background color when selected
              foreground=[('selected', 'black')],  # Text color when selected
              )

    # Create the Treeview widget
    table = ttk.Treeview(settingsPage, columns=("Points", "Spec", "Min", "Max"), show = "headings")
    table.heading('Points', text='Points')
    table.heading('Spec', text='Spec')
    table.heading('Min', text='Min')
    table.heading('Max', text='Max')

    # Set column widths
    table.column("Points", width=75)
    table.column("Spec", width=75)
    table.column("Min", width=75)
    table.column("Max", width=75)

    # Insert some sample data
    table.insert("", "end", values=("Data1", "Data2", "Data3", "Data4"))
    table.insert("", "end", values=("Data5", "Data6", "Data7", "Data8"))

    # Apply the style to the entire table
    table.tag_configure("Treeview", background="#444444", foreground="white")

    # Place the table on the settingsPage
    table.place(relx=0.85, rely=0.55, anchor="center", height = 400)

    def saveData():
        # Retrieve values from textboxes
        supplier_name = supplierNameTextBox.get("1.0", "end")
        vendor_code = vendorCodeTextBox.get("1.0", "end")
        part_number = partNumberTextBox.get("1.0", "end")
        part_name = partNameTextBox.get("1.0", "end")
        lot_count = lotCountTextBox.get("1.0", "end")

        # Execute SQL query to insert data into the database
        cursor.execute(
            "INSERT INTO points (supplierName, vendorCode, partNumber, partName, lotCount) VALUES (?, ?, ?, ?, ?)",
            (supplier_name, vendor_code, part_number, part_name, lot_count))
        connection.commit()  # Commit the transaction

        # Optionally, you can fetch the inserted data for display or further processing
        cursor.execute("SELECT * FROM points")
        rows = cursor.fetchall()
        print(rows)

    save = CTkButton(settingsPage, text="Save", command=saveData, height=35, width=150)
    save.place(relx=0.56, rely=0.21, anchor="center")
def data():
    pass

