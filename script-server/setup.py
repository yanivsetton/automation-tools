from cx_Freeze import setup, Executable

executables = [Executable("launcher.py")]

setup(
    name="ScriptServer",
    version="1.0",
    description="Script Server Application",
    executables=executables
)