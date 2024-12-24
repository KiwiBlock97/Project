<?php
require_once 'utils/database.php';

$code=$_GET["code"];
$resp=verifyCode($code);
if ($resp){
    echo "Email Verified successfully. Please Login Again";
}
else{

    echo "invalid Link or Account already verified";
}
?>