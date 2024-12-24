<?php
require_once $_SERVER['DOCUMENT_ROOT'] . '/utils/vars.php';


function createOrder($admid, $phoneno, $name, $email, $uuid4, $amount)
{
    $url = "https://sandbox.cashfree.com/pg/orders"; // Update to production URL for live
    $x_client_id = Config::CF_CLIENTID; // Replace with your Cashfree client ID
    $x_client_secret = Config::CF_CLIENTSECRET; // Replace with your Cashfree client secret
    $x_api_version = "2023-08-01";

    // Prepare request data
    $postData = [
        "order_id" => $uuid4,
        "order_amount" => $amount,
        "order_currency" => "INR",
        "customer_details" => [
            "customer_id" => "$admid",
            "customer_email" => $email,
            "customer_phone" => $phoneno,
            "customer_name" => $name,
        ],
        "order_meta" => [
            "return_url" => Config::URL."/student/order/checkout.php?order_id={order_id}",
            "payment_methods" => "cc,dc,upi"
        ]
    ];

    // Initialize cURL
    $ch = curl_init($url);

    // Set cURL options
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($postData));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Content-Type: application/json",
        "x-api-version: $x_api_version",
        "x-client-id: $x_client_id",
        "x-client-secret: $x_client_secret"
    ]);

    // Execute the request
    $response = curl_exec($ch);

    // Check for errors
    if (curl_errno($ch)) {
        error_log('cURL error: ' . curl_error($ch));
        return null;
    }

    // Close cURL
    curl_close($ch);

    // Decode the JSON response
    $responseData = json_decode($response, true);

    // Check for the payment_session_id and return it
    if (isset($responseData['payment_session_id'])) {
        return $responseData['payment_session_id'];
    } else {
        error_log('Error in response: ' . $response);
        return null;
    }
}

function fetchPayment($order_id){
    $url = "https://sandbox.cashfree.com/pg/orders/$order_id/payments";
    $x_client_id = Config::CF_CLIENTID;
    $x_client_secret = Config::CF_CLIENTSECRET;
    $x_api_version = "2023-08-01";

    // Initialize cURL
    $ch = curl_init($url);

    // Set cURL options
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "x-client-id: $x_client_id",
        "x-client-secret: $x_client_secret",
        "Accept: application/json",
        "x-api-version: $x_api_version"
    ]);

    $response = curl_exec($ch);

    if (curl_errno($ch)) {
        error_log('cURL error: ' . curl_error($ch));
        return null;
    }
    curl_close($ch);

    $responseData = json_decode($response, true);

    if (is_array($responseData) && isset($responseData[0])) {
        return $responseData[0];
    } else {
        error_log('Invalid response format: ' . $response);
        return null;
    }
}
?>