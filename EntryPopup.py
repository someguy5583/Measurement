import tkinter as tk
from tkinter import ttk
class EntryPopup(ttk.Entry):
    def __init__(self, parent, iid, column, text, onReturnCallback, **kw):
        super().__init__(parent, **kw)
        self.tv = parent  # reference to parent window's treeview
        self.iid = iid  # row id
        self.column = column
        self.onReturnCallback = onReturnCallback

        self.insert(0, text)
        self['exportselection'] = False  # Prevents selected text from being copied to
        # clipboard when widget loses focus
        self.focus_force()  # Set focus to the Entry widget
        self.select_all()  # Highlight all text within the entry widget
        self.bind("<Return>", self.on_return)  # Enter key bind
        self.bind("<Control-a>", self.select_all)  # CTRL + A key bind
        self.bind("<Escape>", lambda *ignore: self.destroy())  # ESC key bind


    def on_return(self, event):
        '''Insert text into treeview, and delete the entry popup'''
        rowid = self.tv.focus()  # Find row id of the cell which was clicked
        vals = self.tv.item(rowid, 'values')  # Returns a tuple of all values from the row with id, "rowid"
        vals = list(vals)  # Convert the values to a list so it becomes mutable
        vals[self.column] = self.get()  # Update values with the new text from the entry widget
        self.tv.item(rowid, values=vals)  # Update the Treeview cell with updated row values
        self.onReturnCallback(rowid, vals)
        self.destroy()  # Destroy the Entry Widget


    def select_all(self, *ignore):
        ''' Set selection on the whole text '''
        self.selection_range(0, 'end')
        return 'break'  # returns 'break' to interrupt default key-bindings
