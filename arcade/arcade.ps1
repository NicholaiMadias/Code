$a = Get-Random -Minimum 1 -Maximum 7
$b = Get-Random -Minimum 1 -Maximum 7
$msg = "Rolled $a + $b = $($a + $b)"
if ($a -eq $b) { $msg += " - Doubles! You win!" }
$msg
