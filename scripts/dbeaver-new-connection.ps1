 param (
    [Parameter(Mandatory = $true)]
    [string]$newPassword
)

# Force create the destination directory if it doesn't exist
$destinationDir = "C:\Users\$env:USERNAME\AppData\Roaming\DBeaverData\workspace6\General\.dbeaver"
if (-not (Test-Path -Path $destinationDir -PathType Container)) {
    New-Item -ItemType Directory -Path $destinationDir -Force | Out-Null
}

# Get the current username from the environment variable
$newUsername = $env:USERNAME

# Define the JSON file path from the previous response
$jsonFilePath = "C:\Users\Administrator\Documents\automation-tools\scripts\dbeaver-json.json"

# Read the JSON data from the file as a simple text
try {
    $jsonContent = Get-Content -Path $jsonFilePath -Raw
} catch {
    Write-Host "Error: Failed to read JSON data from the file."
    return
}

# Replace the username and password directly in the JSON content
$jsonContent = $jsonContent -replace ('"user":\s*".*?"', ('"user": "{0}"' -f $newUsername))
$jsonContent = $jsonContent -replace ('"password":\s*".*?"', ('"password": "{0}"' -f $newPassword))

# Save the updated JSON back to the original file
$jsonContent | Out-File -FilePath $jsonFilePath -Force

# Copy the JSON to the destination location
$destinationPath = "$destinationDir\data-sources-2.json"
Copy-Item -Path $jsonFilePath -Destination $destinationPath -Force

Write-Host "JSON data updated and copied successfully."
 
