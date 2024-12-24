<?php
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/database.php';
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';

session_start();
if ($_SESSION["type"]!="Student"){
    header("Location: /login.php");
    exit();
}

$bus_pass = getPass(null, $_GET["key"]);
$user = getUser(null, $bus_pass['AdmissionId']);
echo $twig->render('print.html.twig',[
    "name" => $user['Name'],
    "department" => $user['Department'],
    "admission" => $user['AdmissionId'],
    "ticket" => $bus_pass,
    "usertype" => $user['Type'],
]);

?>