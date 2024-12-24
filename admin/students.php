<?php
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/database.php';
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';

session_start();
if ($_SESSION["type"]!="Admin"){
    header("Location: /login.php");
    exit();
}

if ($_SERVER['REQUEST_METHOD'] === 'GET'){
    $students=getStudents();
    echo $twig->render("admin_students.html.twig", [
        "students" => $students
    ]);
}
else {
    $admid=$_POST["admid"];
    if ($admid){
        removeStudent(intval($admid));
    }
    header("Location: /admin/students.php");
}