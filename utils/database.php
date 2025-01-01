<?php
require_once $_SERVER['DOCUMENT_ROOT'] . '/config.php';

function getDatabaseConnection() {
    $host = Config::DB_HOST;
    $dbname = Config::DB_NAME;
    $username = Config::DB_USERNAME;
    $password = Config::DB_PASSWORD;

    try {
        $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $username, $password, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
        return $pdo;
    } catch (PDOException $e) {
        die("Database connection failed: " . $e->getMessage());
    }
}

// Done
function createUser($admission_number, $name, $email, $photo, $department, $password, $user_type) {
    $pdo = getDatabaseConnection();
    try {
        $user_type_map = ['Student' => 1, 'Staff' => 2, 'Other' => 3];
        $user_type_id = $user_type_map[$user_type] ?? 3;

        $stmt = $pdo->prepare("INSERT INTO student (AdmissionId, Name, Email, Photo, Department, Password, Type, Verified) 
                               VALUES (?, ?, ?, ?, ?, ?, ?, 0)");
        $stmt->execute([$admission_number, $name, $email, $photo, $department, $password, $user_type_id]);

        return "success";
    } catch (PDOException $e) {
        if ($e->getCode() == 23000) { // Duplicate entry
            return "exist";
        }
        throw $e;
    }
}

function authUser($email, $password) {
    $pdo = getDatabaseConnection();
    try {
        // Check in students table
        $stmt = $pdo->prepare("SELECT AdmissionId, Verified, Name FROM student WHERE Email = ? AND Password = ?");
        $stmt->execute([$email, $password]);
        $result = $stmt->fetch();
        if ($result) {
            return [$result, "Student"];
        }

        // Check in admins table
        $stmt = $pdo->prepare("SELECT Email FROM admin WHERE Email = ? AND Password = ?");
        $stmt->execute([$email, $password]);
        $result = $stmt->fetch();
        if ($result) {
            return [$result, "Admin"];
        }

        return [null, null];
    } catch (PDOException $e) {
        throw $e;
    }
}

function getUser($email = null, $admid = null, $user_type = null) {
    $pdo = getDatabaseConnection();
    try {
        if (isset($admid)) {
            $stmt = $pdo->prepare("SELECT * FROM student WHERE AdmissionId = ?");
            $stmt->execute([$admid]);
        } elseif ($user_type === "Admin") {
            $stmt = $pdo->prepare("SELECT * FROM admin WHERE Email = ?");
            $stmt->execute([$email]);
        } elseif ($user_type === "Student") {
            $stmt = $pdo->prepare("SELECT * FROM student WHERE Email = ?");
            $stmt->execute([$email]);
        } else {
            return null;
        }
        return $stmt->fetch();
    } catch (PDOException $e) {
        throw $e;
    }
}

function getPass($admid=null, $key=null, $regular=null, $fromdate=null, $todate=null) {
    $pdo = getDatabaseConnection();
    try {
        if ($admid){
            $stmt = $pdo->prepare("SELECT * FROM pass WHERE AdmissionId=?");
            $stmt->execute([$admid]);
            $result=$stmt->fetchAll();
        }
        elseif ($key){
            $stmt = $pdo->prepare("select * from pass where UKey=?");
            $stmt->execute([$key]);
            $result=$stmt->fetch();
        }
        elseif ($regular){
            $stmt = $pdo->prepare("select * from pass where (fromtime <= ? AND totime >= ?) ");
            $stmt->execute([$fromdate, $todate]);
            $result=$stmt->fetchAll();
        }
        return $result;
    } catch (PDOException $e) {
        throw $e;
    }
}

function createPass($admid, $place, $uuid, $fromtime, $totime) {
    $pdo = getDatabaseConnection();
    try {
        $stmt = $pdo->prepare("INSERT INTO pass (AdmissionId, FromPlace, UKey, fromtime, totime) VALUES (?, ?, ?, ?, ?)");
        $stmt->execute([$admid, $place, $uuid, $fromtime, $totime]);
    } catch (PDOException $e) {
        throw $e;
    }
}

function extendPass($todate, $UKey){
    $pdo = getDatabaseConnection();
    try {
        $stmt = $pdo->prepare("update pass set totime=? where UKey=?");
        $stmt->execute([$todate, $UKey]);
    } catch (PDOException $e) {
        throw $e;
    }
}

function getPlace($place=null){
    $pdo = getDatabaseConnection();
    try {
            if (isset($place)){
                $stmt = $pdo->prepare("select * from place where Place=?");
                $stmt->execute([$place]);
                return $stmt->fetch();
            }
            else{
                $stmt = $pdo->query("select * from place");
                return $stmt->fetchAll(); 
            }
        } catch (PDOException $e) {
            throw $e;
        }
    }

function removePlace($place){
    $pdo = getDatabaseConnection();
    try {
        $stmt = $pdo->prepare("delete from place where place=?");
        $stmt->execute([$place]);
    }
    catch (PDOException $e) {
            throw $e;
    }
}

function addPlace($place, $price){
    $pdo = getDatabaseConnection();
    try {
        $stmt = $pdo->prepare("insert into place values(?, ?)");
        $stmt->execute([$place, $price]);
    }
    catch (PDOException $e) {
            throw $e;
    }
}

function getStudents() {
    $pdo = getDatabaseConnection();
    try {
        $stmt = $pdo->query("SELECT * FROM student");
        return $stmt->fetchAll();
    } catch (PDOException $e) {
        throw $e;
    }
}

function createOrderDB($OrderId, $email, $place, $fromtime, $totime, $renew, $ukey, $status, $price){
    $pdo = getDatabaseConnection();
    try {
        $stmt = $pdo->prepare("insert into pass_order values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
        $stmt->execute([$OrderId, $email, $place, $fromtime, $totime, $renew, $ukey, (new DateTime())->format('Y-m-d'), $status, $price]);
    } catch (PDOException $e) {
        throw $e;
    }
}

function getOrder($OrderId = null, $fromdate = null, $todate = null, $department = null) {
    $pdo = getDatabaseConnection(); // Replace with your actual database connection function

    try {
        if ($OrderId) {
            // Fetch a specific order by OrderId
            $stmt = $pdo->prepare("SELECT * FROM pass_order WHERE OrderID = ?");
            $stmt->execute([$OrderId]);
            $result = $stmt->fetch();
            return $result;
        } else {
            // Fetch orders based on date range and optionally department
            $query = "SELECT s.Name, s.Department, po.fromtime, po.totime, po.Price, po.Place 
                      FROM pass_order po 
                      JOIN student s ON po.email = s.Email 
                      WHERE po.Status = 'PROCESSED' 
                        AND (po.Time BETWEEN ? AND ?)";
            
            $params = [$fromdate, $todate];
            
            if ($department) {
                $query .= " AND s.Department = ?";
                $params[] = $department;
            }
            
            $stmt = $pdo->prepare($query);
            $stmt->execute($params);
            $result = $stmt->fetchAll();
            
            return $result ? $result : [];
        }
    } catch (PDOException $e) {
        error_log("Database Error: " . $e->getMessage());
        return null; // You can handle errors more robustly based on your application's requirements
    }
}

function modifyOrder($orderId, $status){
    $pdo = getDatabaseConnection();
    try {
        $stmt = $pdo->prepare("update pass_order set Status=? where OrderID=?");
        $stmt->execute([$status, $orderId]);
    } catch (PDOException $e) {
        throw $e;
    }
}

function removeStudent($admission_number){
    $pdo = getDatabaseConnection();
    try {
        $stmt = $pdo->prepare("delete from student where AdmissionId=?");
        $stmt->execute([$admission_number]);
    }
    catch (PDOException $e) {
            throw $e;
    }
}

function removePass($uuid4){
    $pdo = getDatabaseConnection();
    try {
        $stmt = $pdo->prepare("delete from pass where UKey=?");
        $stmt->execute([$uuid4]);
    }
    catch (PDOException $e) {
            throw $e;
    }
}

function getDepartments() {
    $pdo = getDatabaseConnection();
    try {
        $stmt = $pdo->query("select * from departments");
        return $stmt->fetchAll();
    } catch (PDOException $e) {
        throw $e;
    }
}

function removeDepartment($department){
    $pdo = getDatabaseConnection();
    try {
        $stmt = $pdo->prepare("delete from departments where department=?");
        $stmt->execute([$department]);
    }
    catch (PDOException $e) {
            throw $e;
    }
}

function addDepartment($department){
    $pdo = getDatabaseConnection();
    try {
        $stmt = $pdo->prepare("insert into departments values(?)");
        $stmt->execute([$department]);
    }
    catch (PDOException $e) {
            throw $e;
    }
}

function genCode($email) {
    $pdo = getDatabaseConnection(); // Assuming this function returns a valid PDO connection
    try {
        // Delete any existing verification record for the email
        $stmt = $pdo->prepare("DELETE FROM verification WHERE Email = ?");
        $stmt->execute([$email]);

        // Generate a unique code
        $code = uniqid();

        // Insert the new verification code
        $stmt = $pdo->prepare("INSERT INTO verification (Email, Code) VALUES (?, ?)");
        $stmt->execute([$email, $code]);

        // Return the generated code
        return $code;
    } catch (PDOException $e) {
        throw $e; // Throw the exception for higher-level handling
    }
}

function verifyCode($code) {
    $pdo = getDatabaseConnection(); // Assuming this function returns a valid PDO connection
    try {
            // Insert the new verification code
            $stmt1 = $pdo->prepare("SELECT * FROM verification where Code=?");
            $stmt1->execute([$code]);
            $result=$stmt1->fetch();
            if ($result){
                $stmt2 = $pdo->prepare("DELETE FROM verification WHERE Email = ?");
                $stmt2->execute([$result['Email']]);
                $stmt3 = $pdo->prepare("UPDATE student SET Verified=1 where Email = ?");
                $stmt3->execute([$result['Email']]);
                return true;
            }
            return false;
    } catch (PDOException $e) {
        throw $e; // Throw the exception for higher-level handling
    }
}