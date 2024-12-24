<?php
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';

session_start();
if ($_SESSION["type"]!="Admin"){
    header("Location: /login.php");
    exit();
}
echo $twig->render("admin.html.twig",[]);
?>