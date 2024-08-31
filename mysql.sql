CREATE TABLE `admin` (
  `Email` varchar(255) PRIMARY KEY NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Password` varchar(20) NOT NULL
);

CREATE TABLE `student` (
  `AdmissionId` int PRIMARY KEY NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Email` varchar(255) NOT NULL UNIQUE,
  `Photo` varchar(50) NOT NULL,
  `Department` varchar(30) NOT NULL,
  `Password` varchar(20) NOT NULL
);

CREATE TABLE `place` (
  `Place` varchar(30) PRIMARY KEY NOT NULL,
  `Price` int UNSIGNED NOT NULL
);

CREATE TABLE `pass` (
  `AdmissionId` int PRIMARY KEY NOT NULL,
  `FromPlace` varchar(20) NOT NULL,
  `Validity` int NOT NULL,
  `UKey` varchar(255) NOT NULL,
  FOREIGN KEY (`AdmissionId`) REFERENCES `student` (`AdmissionId`) ON DELETE CASCADE,
  FOREIGN KEY (`FromPlace`) REFERENCES `place` (`Place`) ON DELETE CASCADE
);

CREATE TABLE `pass_order` (
  `OrderID` varchar(255) PRIMARY KEY NOT NULL,
  `email` varchar(255) NOT NULL,
  `Place` varchar(20) NOT NULL,
  `Validity` int NOT NULL,
  `Type` tinyint NOT NULL,
  `UKey` varchar(255) DEFAULT NULL,
  `Time` int UNSIGNED NOT NULL,
  `Status` varchar(30) DEFAULT NULL,
  FOREIGN KEY (`email`) REFERENCES `student` (`Email`) ON DELETE CASCADE,
  FOREIGN KEY (`Place`) REFERENCES `place` (`Place`) ON DELETE CASCADE
);


DELIMITER $$

CREATE DEFINER=`root`@`localhost` EVENT `auto_remove_expired_records` ON SCHEDULE EVERY 1 MINUTE STARTS '2024-08-31 19:42:06' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
  DELETE FROM pass
  WHERE Validity <= UNIX_TIMESTAMP();

  DELETE FROM pass_order
  WHERE Time + 3600 <= UNIX_TIMESTAMP() AND Status IS NULL;
END$$

DELIMITER ;
COMMIT;

-- SET GLOBAL event_scheduler = OFF; 
-- ALTER EVENT auto_remove_expired_records DISABLE;  -- Temporarily disable
-- DROP EVENT auto_remove_expired_records;           -- Permanently remove