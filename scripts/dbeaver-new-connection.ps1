 param (
    [string]$newUser,
    [string]$newPassword
)

# Path to the JSON file
$jsonFile = "C:\Users\Administrator\Documents\automation-tools\scripts\dbeaver-json.json"

# Read the JSON content as a single string
$jsonString = Get-Content -Path $jsonFile -Raw

# Replace the variables directly in the JSON string using regular expressions
$jsonString = $jsonString -replace '(?<="user": ")[^"]+', $newUser
$jsonString = $jsonString -replace '(?<="password": ")[^"]+', $newPassword

# Write the updated JSON string back to the same file
$jsonString | Set-Content -Path $jsonFile

Write-Output "JSON file has been updated with new username and password."

# Destination path for the copied JSON file
$destinationPath = "C:\Users\Administrator\AppData\Roaming\DBeaverData\workspace6\General\.dbeaver\data-sources-2.json"

# Create the destination directory if it does not exist
$destinationDirectory = Split-Path -Parent $destinationPath
New-Item -ItemType Directory -Force -Path $destinationDirectory | Out-Null

# Copy the updated JSON file to the destination path with overwrite
Copy-Item -Path $jsonFile -Destination $destinationPath -Force

Write-Output "Updated JSON file has been copied to $destinationPath."
