Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
# Install DBeaver Community Edition silently
choco install dbeaver -y --params "/S"

# Create a shortcut on the desktop
$installDir = Get-Command dbeaver | Select-Object -ExpandProperty Source
$shortcutPath = "$env:USERPROFILE\Desktop\DBeaver.lnk"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "$installDir\dbeaver.exe"
$shortcut.Save()
