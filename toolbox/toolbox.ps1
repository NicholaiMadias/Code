$text = $args -join ' '
$chars = $text.ToCharArray()
[array]::Reverse($chars)
-join $chars
