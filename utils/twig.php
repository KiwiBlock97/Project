<?php

require_once $_SERVER['DOCUMENT_ROOT'].'/vendor/autoload.php';

// Set up Twig environment
$loader = new \Twig\Loader\FilesystemLoader($_SERVER['DOCUMENT_ROOT'].'/templates');
$twig = new \Twig\Environment($loader, [
    'debug' => true, // Enable debugging
    'cache' => false, // Disable caching for development
]);

$twig->addExtension(new \Twig\Extension\DebugExtension());

return $twig;
