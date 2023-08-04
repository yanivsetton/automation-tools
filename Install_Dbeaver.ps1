Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
# Install DBeaver using Chocolatey (latest version, silent installation)
$packageName = 'dbeaver'

# Install DBeaver using Chocolatey with the latest version and silent switch
$chocoInstallScript = "choco install $packageName --yes --params '/S'"

# Run the installation command
Invoke-Expression $chocoInstallScript
#choco install dbeaver -y --params "/S"

