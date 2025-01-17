<?php
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/database.php';
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';

session_start();
if ($_SESSION["type"]!="Admin"){
    header("Location: /login.php");
    exit();
}

if ($_SERVER['REQUEST_METHOD'] === 'GET'){
    $stops=getPlace();
    echo $twig->render("admin_stops.html.twig", [
        "places" => $stops
    ]);
}
else{
    $method=$_POST["method"];
    if ($method=="add"){
        addPlace($_POST["place"], intval($_POST["price"]));
    }
    elseif ($method=="delete"){
        removePlace($_POST["place"]);
    }
    header("Location: /admin/stops.php");
}
?>