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
    $chocoInstallScript = "choco install $packageName --yes --params '/S'"

    # Run the installation command
    Invoke-Expression $chocoInstallScript
    Write-Host "DBeaver has been installed."
}
