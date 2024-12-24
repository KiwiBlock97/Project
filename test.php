<?php
session_start();
echo json_encode($_SESSION);
// session_destroy();
echo json_encode($_SESSION);
?>
