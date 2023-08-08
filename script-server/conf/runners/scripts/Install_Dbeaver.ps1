param (
    [string]$newPassword
)

$message = "Installing DBeaver for you..`nYap totally full automation`nOhh.. also`nCreating for you the profiles and connections`n starting now.."
$delay = 100 # time in milliseconds

Write-Host ""

foreach ($character in $message.ToCharArray()) {
    Write-Host -NoNewline $character
    Start-Sleep -Milliseconds $delay
}

Write-Host "" # newline at the end
Write-Host ""

# Check if Chocolatey is already installed
if (!(Test-Path -path "$env:ProgramData\chocolatey")) {
    # Install Chocolatey
    Set-ExecutionPolicy Bypass -Scope Process -Force; 
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; 
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}

# Package name to check
$packageName = 'dbeaver'

# Check if DBeaver is already installed
$checkInstall = choco list --local-only $packageName

if ($checkInstall -like "*$packageName*") {
    Write-Host "DBeaver is already installed."
} else {
    # Install DBeaver using Chocolatey with the latest version and silent switch
    $chocoInstallScript = "choco install $packageName --yes --force --params '/S'"

    # Run the installation command
    Invoke-Expression $chocoInstallScript
    Write-Host "DBeaver has been installed."
}

$destinationPath = "C:\Users\$env:USERNAME\AppData\Roaming"
$archivePath = Join-Path -Path $PSScriptRoot -ChildPath "assets\DBeaverData.zip"
Expand-Archive -Path $archivePath -DestinationPath $destinationPath -Force
# Define the file path
$filePath = "C:\Users\$env:USERNAME\AppData\Roaming\DBeaverData\workspace6\Pontera\.dbeaver\data-sources.json"

# Set the values of $param and $newPassword to the desired values
$param = $env:USERNAME
$newPassword = $newPassword

# Read the content of the file line by line
$content = Get-Content -Path $filePath

# Process the content line by line and perform the replacements for "user" and "password" fields
$modifiedContent = $content | ForEach-Object {
    if ($_ -match '"user":\s*"(.*)"') {
        $_ -replace ('"user":\s*"{0}"' -f [regex]::Escape($matches[1])), ('"user": "{0}"' -f $param)
    } elseif ($_ -match '"password":\s*"(.*)"') {
        $_ -replace ('"password":\s*"{0}"' -f [regex]::Escape($matches[1])), ('"password": "{0}"' -f $newPassword)
    } else {
        $_
    }
}

# Save the modified content back to the file
$modifiedContent | Set-Content -Path $filePath -Force

# Find the path to python executable in the global PATH variable
$pythonExecutable = $env:PATH -split ';' | Where-Object { Test-Path (Join-Path $_ 'python.exe') } | Select-Object -First 1

if ($pythonExecutable) {
    $pythonScriptPath = Join-Path -Path $PSScriptRoot -ChildPath "open_program.py"
    $programSelected = & $pythonExecutable $pythonScriptPath
} else {
    Write-Host "Python executable not found in the global PATH. Cannot execute the Python script."
}

$message = "Dbeaver installation and configuration`nhas been successfully applied"
$delay = 50 # time in milliseconds

Write-Host ""

foreach ($character in $message.ToCharArray()) {
    Write-Host -NoNewline $character
    Start-Sleep -Milliseconds $delay
}

Write-Host "" # newline at the end
