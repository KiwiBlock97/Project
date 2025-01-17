<?php
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/database.php';
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';

session_start();
if ($_SESSION["type"]!="Admin"){
    header("Location: /login.php");
    exit();
}

$today = (new DateTime())->format('Y-m-d');
$passes = getPass(null, null, true, $today, $today);

echo $twig->render("admin_tickets_today.html.twig", [
    'passes' => $passes
]);
?>