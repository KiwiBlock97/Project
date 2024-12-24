<?php
require_once $_SERVER['DOCUMENT_ROOT'] . '/utils/database.php';
require_once $_SERVER['DOCUMENT_ROOT'] . '/utils/cashfree.php';
$twig = require $_SERVER['DOCUMENT_ROOT'] . '/utils/twig.php';


$order_id = $_GET["order_id"];
if (!isset($order_id)) {
    echo "Not Allowed";
    exit();
}
$resp = fetchPayment($order_id);
if ($resp['payment_status'] === "SUCCESS") {
    // Fetch the order
    $order = getOrder($order_id);
    if (in_array($order['Status'], ["SUCCESS", "PROCESSED"])) {
        echo $twig->render('checkout.html.twig', [
            "status" => $resp['payment_status'],
            "payment_id" => $resp['cf_payment_id'],
            "order_id" => $resp['order_id']
        ]);
        exit();
    }
    modifyOrder($order_id, $resp['payment_status']);

    $user = getUser($order['email'], null, "Student");
    $place = getPlace($order['Place']);

    if ($order['Type'] == 0) {
        // Create a new pass
        createPass($user['AdmissionId'], $place['Place'], $order_id, $order['fromtime'], $order['totime']);
    } elseif ($order['Type'] == 1) {
        // Extend the pass
        extendPass($order['totime'], $order['UKey']);
    }

    // Mark the order as processed
    modifyOrder($order_id, "PROCESSED");
} elseif ($resp['payment_status']) {
    // Update the order status for pending, dropped, or failed payments
    modifyOrder($order_id, $resp['payment_status']);
} else {
    // Return a 400 Bad Request response
    http_response_code(400);
    die("Bad Request");
}

// Render the status template
echo $twig->render('checkout.html.twig', [
    "status" => $resp['payment_status'],
    "payment_id" => $resp['cf_payment_id'],
    "order_id" => $resp['order_id']
]);
