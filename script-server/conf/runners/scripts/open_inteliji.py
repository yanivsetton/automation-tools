import subprocess
from tkinter import messagebox, Tk

# Ask the user if they want to open a specific program
root = Tk()
root.withdraw() # Hide the main window
open_program = messagebox.askyesno("Question", "Do you want to open Inteliji?")

if open_program:
    program_path = "C:\Program Files\JetBrains\IntelliJ IDEA 2023.2.0 S D=C\Program Files\JetBrains\IntelliJ IDEA Ultimate Edition\bin\idea64.exe" # Change this to the path of the program you want to open
    subprocess.Popen([program_path])