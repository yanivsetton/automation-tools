# Define variables
$installerUrl = 'https://download.jetbrains.com/idea/ideaIC-2023.1.4.exe?_gl=1*72tzvq*_ga*MTczMTY4NDk1OS4xNjg5NzcxMjMx*_ga_9J976DJZ68*MTY4OTc3NDUxOC4yLjEuMTY4OTc3NTM3Mi4wLjAuMA..&_ga=2.125547274.1293864214.1689771231-1731684959.1689771231'
$installerExe = 'IntelliJ-Community-Installer.exe'
$installPath = 'C:\Program Files\JetBrains\IntelliJ IDEA Community Edition'

# Download the installer
Invoke-WebRequest -Uri $installerUrl -OutFile $installerExe

# Install IntelliJ IDEA silently
Start-Process -FilePath $installerExe -ArgumentList "/S", "/D=$installPath" -Wait

# Remove the installer file
Remove-Item -Path $installerExe -Force
