<?php
    session_start();
    $admid=$_SESSION['admid'];
    if ($_SESSION["type"]=="Admin"){
        $admid=$_GET["id"];
    }
    if (isset($admid)){
        $attachment_location = $_SERVER["DOCUMENT_ROOT"] . "/photo/$admid";
        if (file_exists($attachment_location)) {

            header($_SERVER["SERVER_PROTOCOL"] . " 200 OK");
            header("Content-Transfer-Encoding: Binary");
            header("Content-Length:".filesize($attachment_location));
            header("Content-Disposition: attachment; filename=$admid");
            readfile($attachment_location);
            die();        
        } else {
            die("Error: File not found.");
        }
    }
?>