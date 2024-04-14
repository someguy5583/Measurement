from customtkinter import *
import cv2
from PIL import Image, ImageTk


class VideoCapture():
    def __init__(self):
        # Create a VideoCapture object
        self.cap = cv2.VideoCapture(0)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            # Convert the frame to PIL image
            img = Image.fromarray(frame)

            # Convert the PIL image to Tkinter image
            ctkImg = ImageTk.PhotoImage(image=img)
            return ctkImg
        return None

    def close_app(self):
        # Release the video capture and destroy the window
        self.cap.release()