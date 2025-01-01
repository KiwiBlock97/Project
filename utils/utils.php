<?php
require_once $_SERVER['DOCUMENT_ROOT'] . '/config.php'; 

function sendMail($name, $email, $text, $subject) {
    $url = "https://api.brevo.com/v3/smtp/email";
    $apiKey = Config::BREVO_API;

    $headers = [
        'Accept: application/json',
        'api-key: ' . $apiKey,
        'Content-Type: application/json',
    ];

    $jsonData = [
        'sender' => [
            'name' => 'Springs Fern',
            'email' => 'mail@springsfern.in',
        ],
        'to' => [
            [
                'email' => $email,
                'name' => $name,
            ],
        ],
        'subject' => $subject,
        'htmlContent' => $text,
    ];

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($jsonData));

    $response = curl_exec($ch);

    if (curl_errno($ch)) {
        throw new Exception('Request Error: ' . curl_error($ch));
    }

    curl_close($ch);

    return json_decode($response, true);
}

?>