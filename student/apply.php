<?php
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/database.php';
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';

session_start();
if ($_SESSION["type"]!="Student"){
    header("Location: /login.php");
    exit();
}

$user=getUser(null, $_SESSION['admid']);
$place=getPlace();
echo $twig->render("apply.html.twig", [
    "name" => $user['Name'],
    "department" => $user['Department'],
    "adm_no" => $user['AdmissionId'],
    "place" => $place,
    "usertype" => $user['Type']
]);
?>