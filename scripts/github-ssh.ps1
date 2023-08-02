 # Ensure ssh-keygen is available
 if (-not (Get-Command "ssh-keygen" -ErrorAction SilentlyContinue)) {
    Write-Error "The ssh-keygen utility is not available. Please install it before running this script."
    exit 1
}

# Define parameters
$sshDir = "$env:USERPROFILE\.ssh"

# Generate a timestamp string
$timestamp = Get-Date -Format "yyyyMMddHHmmss"

$sshFile = "$sshDir\id_rsa_$timestamp"

# Create .ssh directory if it does not exist
if (!(Test-Path -Path $sshDir -PathType Container)) {
    New-Item -ItemType Directory -Force -Path $sshDir
}

# Validate if .ssh directory was created
if (!(Test-Path -Path $sshDir -PathType Container)) {
    Write-Error "Failed to create the directory for the SSH key."
    exit 1
}

# Generate new SSH key
ssh-keygen -t rsa -b 4096 -f $sshFile -N "" -q

# Ensure ssh key generation was successful
if (-not (Test-Path -Path $sshFile -PathType Leaf)) {
    Write-Error "Failed to generate the SSH key."
    exit 1
}

# Read the public key
$publicKey = Get-Content -Path "$sshFile.pub"

# Copy to clipboard
$publicKey | Set-Clipboard

Write-Host "Public SSH key has been copied to clipboard"

# Open GitHub SSH settings in the default browser
Start-Process "https://github.com/settings/ssh/new"
 
