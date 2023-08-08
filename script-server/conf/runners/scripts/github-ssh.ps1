param (
    [string]$PARAM_REPO
)

# Path to the Python script relative to this PowerShell script's location
$pythonScriptPath = Join-Path -Path $PSScriptRoot -ChildPath "select_folder.py"

# Run the Python script and capture the output
$folderSelected = & python $pythonScriptPath

# Extract the repository name from the URL
$repoName = [System.IO.Path]::GetFileNameWithoutExtension((Split-Path $PARAM_REPO -Leaf))
$cloneDestination = Join-Path -Path $folderSelected -ChildPath $repoName

Write-Host "The selected folder is: $folderSelected"
Write-Host "The repository will be cloned to: $cloneDestination"

# Ensure ssh-keygen is available
if (-not (Get-Command "ssh-keygen" -ErrorAction SilentlyContinue)) {
    Write-Error "The ssh-keygen utility is not available. Please install it before running this script."
    exit 1
}

# Define parameters
$sshDir = "$env:USERPROFILE\.ssh"
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$sshFile = "$sshDir\id_rsa_$timestamp"

# Create .ssh directory if it does not exist
if (!(Test-Path -Path $sshDir -PathType Container)) {
    New-Item -ItemType Directory -Force -Path $sshDir
}

# Generate new SSH key
ssh-keygen -t rsa -b 4096 -f $sshFile -N "" -q

# Read the public key
$publicKey = Get-Content -Path "$sshFile.pub"

# Copy to clipboard
$publicKey | Set-Clipboard

Write-Host "Public SSH key has been copied to clipboard"
Start-Process "https://github.com/settings/ssh/new"
Write-Host "Did you paste the ssh key? Please type Y to proceed or N to abort"

$response = Read-Host "Do you want to proceed? (Y/N)"
if ($response -eq 'Y') {
    Write-Host "Proceeding..."

    # Check if Git is installed
    if (-Not (Get-Command -Name 'git' -ErrorAction SilentlyContinue)) {
        Write-Host "Git is not installed on this system. Installing Git via Chocolatey..."

        # Check if Chocolatey is installed
        if (-Not (Get-Command -Name 'choco' -ErrorAction SilentlyContinue)) {
            Write-Host "Chocolatey is not installed on this system. Please install Chocolatey first."
            exit
        }

        # Install Git using Chocolatey
        choco install git -y
    }

    # Check if destination directory already exists
    if (Test-Path -Path $cloneDestination -ErrorAction SilentlyContinue) {
        Write-Host "Destination directory already exists. Please choose a different folder or remove the existing directory."
        exit
    }

    try {
        Write-Host "Cloning repository from $PARAM_REPO to $cloneDestination..."
        git clone $PARAM_REPO $cloneDestination

        if (Test-Path -Path (Join-Path -Path $cloneDestination -ChildPath '.git')) {
            Write-Host "Repository cloned successfully!"
        }
        else {
            Write-Host "An error occurred while cloning the repository."
        }
    }
    catch {
        Write-Host "An error occurred: $_"
    }
} else {
    Write-Host "Aborting..."
    exit
}
