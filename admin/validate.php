<?php
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/database.php';
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';

session_start();
if ($_SESSION["type"]!="Admin"){
    header("Location: /login.php");
    exit();
}

$key=$_GET["ticket-id"];
if ($key){
    $bus_pass=getPass(null, $key);
    $user=$bus_pass ? getUser(null, $bus_pass['AdmissionId']) : null;
    $context=[
        "key" => $key,
        "ticket" => $bus_pass,
        "user" => $user,
        "validity" => $bus_pass ? $bus_pass["totime"] : 0
    ];
}
else{
    $context = ["key" => null];
}
echo $twig->render("validate.html.twig", $context);
?>