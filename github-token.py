import os
import subprocess
import webbrowser
import pyperclip
import sys

def create_ssh(email):
    # Generate new SSH key silently, overwriting if it exists
    print(f"Generating a new SSH key for {email} silently...")
    os.system(f'echo y | ssh-keygen -q -t ed25519 -C "{email}" -f {os.path.expanduser("~/.ssh/id_ed25519")} -N ""')

    # Copy the SSH key to your clipboard
    print("Copying the SSH key to your clipboard...")
    with open(os.path.expanduser("~/.ssh/id_ed25519.pub"), 'r') as f:
        ssh_key = f.read()
    pyperclip.copy(ssh_key)

    # Open GitHub in your browser
    print("Opening GitHub in your browser...")
    webbrowser.open("https://github.com/settings/ssh/new")

    print("Done. Now you need to manually add the SSH key to your GitHub account.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        email = sys.argv[1]
        create_ssh(email)
    else:
        print("Please provide an email address as a command line argument.")
