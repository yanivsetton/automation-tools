import subprocess
from tkinter import messagebox, Tk

# Ask the user if they want to open a specific program
root = Tk()
root.withdraw() # Hide the main window
open_program = messagebox.askyesno("Question", "Do you want to open DBeaver?")

if open_program:
    program_path = "C:\Program Files\DBeaver\dbeaver.exe" # Change this to the path of the program you want to open
    subprocess.Popen([program_path])
