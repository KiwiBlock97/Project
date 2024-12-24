<?php
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/database.php';
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';

session_start();
if ($_SESSION["type"]!="Admin"){
    header("Location: /login.php");
    exit();
}

$fromdate=$_GET["fromdate"];
$todate=$_GET["todate"];
$params=["fromdate" => $fromdate, "todate" => $todate];
if ($fromdate && $todate){
    $passes=getPass(null, null, true, $fromdate, $todate);
    $params["passes"]=$passes;
}
echo $twig->render("regular.html.twig", $params);
?>