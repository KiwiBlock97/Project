<?php
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/database.php';
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';

session_start();
if ($_SESSION["type"]!="Admin"){
    header("Location: /login.php");
    exit();
}

if ($_SERVER['REQUEST_METHOD'] === 'GET'){
    $departments=getDepartments();
    echo $twig->render("departments.html.twig",[
        "departments" => $departments
    ]);
}
else{
    $method=$_POST["method"];
    $department=$_POST["department"];
    if ($method=="add" && isset($department)){
        addDepartment($department);
    }
    elseif ($method=="delete" && isset($department)){
        removeDepartment($department);
    }
    header("Location: /admin/departments.php");
}
?>