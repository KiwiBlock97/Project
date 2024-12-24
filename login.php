<?php

require_once 'utils/vars.php'; 
require_once 'utils/database.php';
require_once 'utils/utils.php';
$twig = require 'utils/twig.php';

$email=$_POST["email"];
$password=$_POST["password"];
if ($_SERVER['REQUEST_METHOD'] === 'GET' || (!$email && !$password)) {
    echo $twig->render('login.html.twig', []);
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $resp = authUser($email, $password);
    if (!$resp[0]){
        echo "Invalid Email or Password";
        exit();
    }
    if ($resp[1]=="Student" && $resp[0]['Verified']==0){
        $code=genCode($email);
        $text = "<html><head></head><body><p>Verify your email address by opening this link<br>" . Config::URL . "/verify.php?code=$code</p></body></html>";
        sendMail($resp[0]['Name'], $email, $text, "Email Verification");
        echo "Refresh this page or Login again after verifying your Email by Opening Link sent to Provided Email Address";
        exit();
    }
    session_start();
    $_SESSION["email"]=$email;
    $_SESSION["type"]=$resp[1];

    http_response_code(303);
    if ($resp[1]=="Admin"){
        header("Location: /admin");
    }
    elseif ($resp[1]=="Student"){
        $_SESSION["admid"]=$resp[0]['AdmissionId'];
        header("Location: /student");
    }
}