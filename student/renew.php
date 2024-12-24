<?php
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/database.php';
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';

session_start();
if ($_SESSION["type"]!="Student"){
    header("Location: /login.php");
    exit();
}

$key=$_GET["key"];
if (!isset($key)){
    exit();
}
$bus_pass=getPass(null, $key);
if (empty($bus_pass)){
    header("Location: /student/apply.php");
    exit();
}

$place=getPlace($bus_pass['FromPlace']);
$user=getUser(null, $_SESSION['admid']);

$totime = new DateTime($bus_pass['totime']);
$totime->modify('+1 day');

echo $twig->render("renew.html.twig", [
    "name" => $user["Name"],
    "department" => $user['Department'],
    "place" => $bus_pass['FromPlace'],
    "adm_no" => $user['AdmissionId'],
    "price" => $place['Price'],
    "ukey" => $bus_pass['UKey'],
    "fromdate" => $totime->format('Y-m-d')
]);
?>