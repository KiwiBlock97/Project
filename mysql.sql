CREATE TABLE `admin` (
  `Email` varchar(255) PRIMARY KEY NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Password` varchar(20) NOT NULL
);

CREATE TABLE `departments` (
  `department` varchar(255) PRIMARY KEY NOT NULL
);

CREATE TABLE `student` (
  `AdmissionId` bigint PRIMARY KEY NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Email` varchar(255) NOT NULL UNIQUE,
  `Photo` varchar(50) NOT NULL,
  `Department` varchar(30) NOT NULL,
  `Password` varchar(20) NOT NULL,
  `Type` TINYINT NOT NULL,
  FOREIGN KEY (`Department`) REFERENCES `departments` (`department`) ON DELETE CASCADE
  -- 1 is Student
  -- 2 is Staff

);

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`Email`, `Name`, `Password`) VALUES
('admin@mail.com', 'Admin', '1234');

-- --------------------------------------------------------
CREATE TABLE `place` (
  `Place` varchar(30) PRIMARY KEY NOT NULL,
  `Price` int UNSIGNED NOT NULL
);

--
-- Dumping data for table `place`
--

INSERT INTO `place` (`Place`, `Price`) VALUES
('Cherkala', 20),
('Kasaragod', 25);

-- --------------------------------------------------------

CREATE TABLE `pass` (
  `AdmissionId` bigint NOT NULL,
  `FromPlace` varchar(20) NOT NULL,
  `UKey` varchar(255) PRIMARY KEY NOT NULL,
  `fromtime` date NOT NULL,
  `totime` date NOT NULL,
  FOREIGN KEY (`AdmissionId`) REFERENCES `student` (`AdmissionId`) ON DELETE CASCADE,
  FOREIGN KEY (`FromPlace`) REFERENCES `place` (`Place`) ON DELETE CASCADE
);

CREATE TABLE `pass_order` (
  `OrderID` varchar(255) PRIMARY KEY NOT NULL,
  `email` varchar(255) NOT NULL,
  `Place` varchar(20) NOT NULL,
  `fromtime` date NOT NULL,
  `totime` date NOT NULL,
  `Type` tinyint NOT NULL,
  `UKey` varchar(255) DEFAULT NULL,
  `Time` date NOT NULL,
  `Status` varchar(30) DEFAULT NULL,
  `Price` int NOT NULL,
  FOREIGN KEY (`email`) REFERENCES `student` (`Email`) ON DELETE CASCADE,
  FOREIGN KEY (`Place`) REFERENCES `place` (`Place`) ON DELETE CASCADE
);



-- DELIMITER $$

-- CREATE EVENT `auto_remove_expired_records`
-- ON SCHEDULE EVERY 1 MINUTE
--   ENABLE DO BEGIN
--   DELETE FROM pass
--   WHERE Validity <= UNIX_TIMESTAMP();

--   DELETE FROM pass_order
--   WHERE Time + 3600 <= UNIX_TIMESTAMP() AND Status IS NULL;
-- END$$

-- DELIMITER ;
-- COMMIT;

-- SET GLOBAL event_scheduler = OFF; 
-- ALTER EVENT auto_remove_expired_records DISABLE;  -- Temporarily disable
-- DROP EVENT auto_remove_expired_records;           -- Permanently remove