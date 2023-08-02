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

Start-Process -FilePath $dbeaverCliPath "-con name=$DBName|driver=mysql|host=$DBHost|port=3306|user=$env:USERNAME|password=$DBPass" 
