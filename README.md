# Shir automation script, @work Tools
This repo contains script written in powershell as example to install 3rd parties tools without interactive installation:

## Tools supported ATM:
Inteliji community edition</br>
Dbeaver community edition</br>
Adding new connections to dbeaver profiles</br>
copying inteliji configuration

## How to run at developer mode:
<p>Clone this repo</p></br>
git clone https://github.com/yanivsetton/automation-tools.git</br>
cd automation-tools</br>
python3 main.py</br>
the script is running at port 8000 but you can change that</>

## Prod mode:
<p>Clone this repo</p></br>
git clone https://github.com/yanivsetton/automation-tools.git</br>
cd automation-tools</br>
pip install pyinstaller</br>
pyinstaller --onefile main.py</br>
<p>Check in the dist folder @ your workspace the file will be named as your script without the extension</p>
<p>example: main.py --> main.exe</p>


