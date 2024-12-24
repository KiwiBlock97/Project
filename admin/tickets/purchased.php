<?php
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/database.php';
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';

session_start();
if ($_SESSION["type"]!="Admin"){
    header("Location: /login.php");
    exit();
}

$departments=getDepartments();

if(!(isset($_GET["fromdate"]) && isset($_GET["todate"]))){
    echo $twig->render("purchased.html.twig",[
        "departments" => $departments
    ]);
    exit();
}

$fromdate=$_GET["fromdate"];
$todate=$_GET["todate"];
$department=$_GET["department"];
$orders=getOrder(null, $fromdate, $todate, $department);
$sum=0;
foreach ($orders as $row){
    $sum=$sum+$row['Price'];
}
echo $twig->render("purchased.html.twig", [
    "orders" => $orders,
    "sum" => $sum,
    "departments" => $departments,
    "count" => count($orders),
    "fromdate" => $fromdate,
    "todate" => $todate
]);
?>