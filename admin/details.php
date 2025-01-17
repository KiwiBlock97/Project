<?php
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/database.php';
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';

session_start();
if ($_SESSION["type"]!="Admin"){
    header("Location: /login.php");
    exit();
}

$ticket=$_GET["pass"];
if ($ticket){
    removePass($ticket);
}
$admid=$_GET["id"];
if ($admid){
    $user=getUser(null, $admid);
    $bus_pass = getPass($user['AdmissionId']);

    $current_date = new DateTime();

    $valid_pass = array_filter($bus_pass, function ($pass) use ($current_date) {
        return new DateTime($pass['totime']) >= $current_date;
    });

    echo $twig->render("admin_details.html.twig", [
        "AdmissionId" => $user['AdmissionId'],
        "Name" => $user['Name'],
        "Email" => $user['Email'],
        "Department" => $user['Department'],
        "bus_pass" => $valid_pass,
    ]);
}
?>