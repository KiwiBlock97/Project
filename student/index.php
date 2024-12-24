<?php
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/database.php';
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';

session_start();
if ($_SESSION["type"]!="Student"){
    header("Location: /login.php");
    exit();
}

$user=getUser(null, $_SESSION['admid']);
$bus_pass = getPass($user['AdmissionId']);

$current_date = new DateTime();

$valid_pass = array_filter($bus_pass, function ($pass) use ($current_date) {
    return new DateTime($pass['totime']) >= $current_date;
});

if (empty($valid_pass)) {
    header("Location: /student/apply.php");
    exit();
}

echo $twig->render("student.html.twig",[
    "name" => $user['Name'],
    "department" => $user['Department'],
    "admission" => $user['AdmissionId'],
    "bus_pass" => $valid_pass,
    "usertype" => $user['Type'],
]);
?>