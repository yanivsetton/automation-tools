 #Setting Variables
#$DBName = Read-Host -Prompt 'Input your server  name'
#$DBHost = Read-Host -Prompt 'Input your server  url'
#$DBUser = Read-Host -Prompt 'Input your user name'
#$DBPass = Read-Host -Prompt 'Input your user password'
$DBName = $args[0]
$DBHost = $args[1]
$DBPass = $args[2]
#Dbeaver-cli path
$dbeaverCliPath = "C:\Program Files\DBeaver\dbeaver-cli.exe"

# Start-Process -FilePath $dbeaverCliPath "-con name=$DBName|driver=mysql|host=$DBHost|port=3306|user=$env:USERNAME|password=$DBPass" 

 param (
    [string]$newHost,
    [string]$user,
    [string]$password,
    [string]$port,
    [string]$database
)

# Path to the JSON file
$jsonFile = "C:\Users\Administrator\Documents\automation-tools\scripts\dbeaver-json.json"

# Read the JSON content as a single string
$jsonString = Get-Content -Path $jsonFile -Raw

# Replace the variables directly in the JSON string using regular expressions
$jsonString = $jsonString -replace '(?<="host": ")[^"]+', $newHost
$jsonString = $jsonString -replace '(?<="user": ")[^"]+', $user
$jsonString = $jsonString -replace '(?<="password": ")[^"]+', $password
$jsonString = $jsonString -replace '(?<="port": ")[^"]+', $port
$jsonString = $jsonString -replace '(?<="database": ")[^"]+', $database

# Write the updated JSON string back to the same file
$jsonString | Set-Content -Path $jsonFile

Write-Output "JSON file has been updated with new connection values."

# Destination path for the copied JSON file
$destinationPath = "C:\Users\Administrator\AppData\Roaming\DBeaverData\workspace6\General\.dbeaver\data-sources-2.json"

# Create the destination directory if it does not exist
$destinationDirectory = Split-Path -Parent $destinationPath
New-Item -ItemType Directory -Force -Path $destinationDirectory | Out-Null

# Copy the updated JSON file to the destination path with overwrite
Copy-Item -Path $jsonFile -Destination $destinationPath -Force

Write-Output "Updated JSON file has been copied to $destinationPath."
 
powershell.exe -ExecutionPolicy Bypass -File DBeaver-connections.ps1 -newHost "another-test" -user "$env:USERNAME" -password "new_password" -port "3306" -database "new_database-again" 

