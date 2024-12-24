<?php
require_once 'utils/database.php';
$twig = require 'utils/twig.php';

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $departments=getDepartments();
    echo $twig->render("signup.html.twig", [
        'departments' => $departments,
        'json' => json_encode($departments),
    ]);
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // Check if all required POST data is available
        if (isset($_FILES['photo'], $_POST['admission-number'], $_POST['name'], $_POST['email'], $_POST['department'], $_POST['pass'], $_POST['user-type'])) {
            $photo = $_FILES['photo'];
            $admission_number = $_POST['admission-number'];
            $name = $_POST['name'];
            $email = $_POST['email'];
            $department = $_POST['department'];
            $password = $_POST['pass'];
            $user_type = $_POST['user-type'];
    
            // Call the function to create user
            $status = createUser($admission_number, $name, $email, $admission_number, $department, $password, $user_type);
    
            if ($status == 'exist') {
                // User already exists
                echo "User Already Exist";
            } else {
                // Save the photo to the server
                $target_directory = "photo/";
                $target_file = $target_directory . basename($admission_number);
                
                if (move_uploaded_file($photo['tmp_name'], $target_file)) {
                    // File successfully uploaded, now redirect
                    header("Location: /login.php");
                    exit();
                } else {
                    echo "Error uploading file.";
                }
            }
        } else {
            echo "Missing required fields.";
        }
}