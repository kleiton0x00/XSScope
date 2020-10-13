<?php
// Make sure PHP has permissons to write to test.png

$data = $_POST['png'];

$data = substr($data, 22);

$f = fopen("Browser_Screenshot.png", "w+");
fputs($f, base64_decode($data));
fclose($f);
