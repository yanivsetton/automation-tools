Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
# Install DBeaver Community Edition silently
# Install DBeaver using Chocolatey
$packageName = 'dbeaver'
$installArgs = '/S'
$chocoInstallScript = "choco install $packageName $installArgs"

# Run the installation command
Invoke-Expression $chocoInstallScript
#choco install dbeaver -y --params "/S"

