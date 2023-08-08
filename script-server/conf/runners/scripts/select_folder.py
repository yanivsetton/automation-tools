import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

folder_selected = filedialog.askdirectory()
folder_selected = folder_selected.replace('/', '\\')
print(folder_selected)