<?php
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/database.php';
require_once $_SERVER['DOCUMENT_ROOT'].'/utils/cashfree.php';
$twig = require $_SERVER['DOCUMENT_ROOT'].'/utils/twig.php';


session_start();
if ($_SESSION["type"]!="Student"){
    header("Location: /login.php");
    exit();
}

$user=getUser(null, $_SESSION['admid']);

if (isset($_POST['ukey'])) {
    // Fetch bus pass using the ukey
    $ukey = $_POST['ukey'];
    $buspass = getPass(null, $ukey); // Replace with your database call
    $datefrom = (new DateTime($buspass['totime']))->modify('+1 day')->format('Y-m-d');
    $place = $buspass['FromPlace'];
} else {
    $datefrom = $_POST['datefrom'];
    $place = $_POST['from-to'];
}

// Generate UUID
$uuid4 = uniqid('', true);

// Extract user details
$admid = $user['AdmissionId'];
$name = $user['Name'];
$email = $user['Email'];
$dateto = $_POST['dateto'];
$phoneno = $_POST['phone'];

// Calculate validity
$startDate = new DateTime($datefrom);
$endDate = new DateTime($dateto);
$curent_date=$startDate;
$no_days = $endDate->diff($startDate)->days + 1;
$no_sun = 0;

while ($curent_date <= $endDate) {
    if ($curent_date->format('w') == 0) {
        $no_sun = $no_sun+1;
    }
    
    $curent_date->modify('+1 day');
}
$validity = $no_days-$no_sun;

// Fetch place details and calculate amount
$dbPlace = getPlace($place); // Replace with your database call
$price = intval($dbPlace['Price']);
$amount = $price * $validity;

// Create payment order
$paymentId = createOrder($admid, $phoneno, $name, $email, $uuid4, $amount);

if ($paymentId) {
    // Store order details in the database
    createOrderDB($uuid4, $email, $place, $datefrom, $dateto, isset($ukey) ? 1 : 0, $ukey ?? null, null, $amount);

    // Render checkout template
    echo $twig->render('student_order_confirm.html.twig', [
        'sessionid' => $paymentId,
        'name' => $name,
        'department' => $user['Department'],
        'place' => $place,
        'validity' => $endDate->format('d-m-Y'),
        'adm_no' => $admid,
        'price' => $amount,
        'order_id' => $uuid4,
        'renew' => isset($ukey) ? 'Yes' : 'No',
        'usertype' => $user['Type']
    ]);
} else {
    http_response_code(500); // Internal Server Error
    echo "An error occurred while processing the payment.";
}
?>