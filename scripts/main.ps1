
$DBName = $args[0]
$DBHost = $args[1]
$DBPass = $args[2]
$Output.Flush()
Write-Host "DBName: $DBName"
$Output.Flush()
write-host "DBHost: $DBHost"
$Output.Flush()
Write-Host "DBPass: $DBPass"
$Output.Flush()
i=1
foreach($i in 1..10){
    Write-Host $i
    $Output.Flush()
}
Start-Sleep -s 2
```