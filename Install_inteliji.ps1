# Define variables
#$installerUrl = 'https://download.jetbrains.com/idea/ideaIU-2023.1.4.exe?_gl=1*vmm28x*_ga*MTczMTY4NDk1OS4xNjg5NzcxMjMx*_ga_9J976DJZ68*MTY4OTc4NzAyMy40LjAuMTY4OTc4NzAyNC4wLjAuMA..&_ga=2.32101822.1293864214.1689771231-1731684959.1689771231'
#$installerExe = 'IntelliJ-Ultimate-Installer.exe'
#$installPath = 'C:\Program Files\JetBrains\IntelliJ IDEA Ultimate Edition'

# Download the installer
#Invoke-WebRequest -Uri $installerUrl -OutFile $installerExe

# Install IntelliJ IDEA Ultimate silently
#Start-Process -FilePath $installerExe -ArgumentList "/S", "/D=$installPath" -Wait

# Remove the installer file
#Remove-Item -Path $installerExe -Force
# Check if Chocolatey is installed
if (!(Test-Path "$env:ProgramData\chocolatey\choco.exe")) {
    Write-Host "Chocolatey is not installed. Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}

# Install IntelliJ IDEA Ultimate with Chocolatey
Write-Host "Installing IntelliJ IDEA Ultimate..."
choco install intellijidea-ultimate -y

# Check if the installation was successful
if (!(Test-Path "$env:ProgramFiles\JetBrains\IntelliJ IDEA Ultimate Edition")) {
    Write-Host "IntelliJ IDEA Ultimate installation failed. Please check the logs for any errors."
}
else {
    Write-Host "IntelliJ IDEA Ultimate installed successfully!"
}
