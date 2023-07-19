# Define variables
$installerUrl = 'https://download.jetbrains.com/idea/ideaIU-2023.1.4.exe?_gl=1*vmm28x*_ga*MTczMTY4NDk1OS4xNjg5NzcxMjMx*_ga_9J976DJZ68*MTY4OTc4NzAyMy40LjAuMTY4OTc4NzAyNC4wLjAuMA..&_ga=2.32101822.1293864214.1689771231-1731684959.1689771231'
$installerExe = 'IntelliJ-Ultimate-Installer.exe'
$installPath = 'C:\Program Files\JetBrains\IntelliJ IDEA Ultimate Edition'
$licenseFile = 'C:\Path\To\Your\License\idea.license'

# Download the installer
Invoke-WebRequest -Uri $installerUrl -OutFile $installerExe

# Copy the license file to the installation directory
Copy-Item -Path $licenseFile -Destination $installPath -Force

# Install IntelliJ IDEA Ultimate silently
Start-Process -FilePath $installerExe -ArgumentList "/S", "/D=$installPath" -Wait

# Remove the installer file
Remove-Item -Path $installerExe -Force
