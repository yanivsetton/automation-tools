param (
    [string]$PARAM_IDEA_FILE # Still not in use // todo: add the setting.xml
)

$message = "Installing Inteliji for you..`nYap totally full automation`nOhh.. also`nSetting for you the profiles`n starting now.."
$delay = 100 # time in milliseconds

Write-Host ""
Write-Host ""

foreach ($character in $message.ToCharArray()) {
    Write-Host -NoNewline $character
    Start-Sleep -Milliseconds $delay
}

Write-Host "" # newline at the end
# Check if Chocolatey is already installed
if (!(Test-Path "$env:ProgramData\chocolatey\choco.exe")) {
    Write-Host "Chocolatey is not installed. Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}

# Define installation path (change it to your desired location)
$installationPath = "C:\Program Files\JetBrains\IntelliJ IDEA Ultimate Edition"

# Define the package name
$packageName = 'intellijidea-ultimate'

# Check if IntelliJ IDEA Ultimate is already installed
$checkInstall = choco list --local-only $packageName

if ($checkInstall -like "*$packageName*") {
    Write-Host "IntelliJ IDEA Ultimate is already installed."
} else {
    # Install IntelliJ IDEA Ultimate with Chocolatey (silent with default options)
    Write-Host "Installing IntelliJ IDEA Ultimate..."
    choco install $packageName -y --ia "/S /D=$installationPath"
    
    # Check if the installation was successful
    if (!(Test-Path "$installationPath")) {
        Write-Host "IntelliJ IDEA Ultimate installation failed. Please check the logs for any errors."
    } else {
        Write-Host "IntelliJ IDEA Ultimate installed successfully!"
    }
}
# Find the path to python executable in the global PATH variable
$pythonExecutable = "C:\Python311\python.exe"
#$pythonExecutable = $env:PATH -split ';' | Where-Object { Test-Path (Join-Path $_ 'python.exe') } | Select-Object -First 1

if ($pythonExecutable) {
    $pythonScriptPath = Join-Path -Path $PSScriptRoot -ChildPath "open_inteliji.py"
    $programSelected = & Start-Process -FilePath $pythonExecutable -ArgumentList $pythonScriptPath 
} else {
    Write-Host "Python executable not found in the global PATH. Cannot execute the Python script."
}