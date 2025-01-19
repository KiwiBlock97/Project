-- phpMyAdmin SQL Dump
-- version 5.2.1deb3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 19, 2025 at 04:13 PM
-- Server version: 8.0.40-0ubuntu0.24.10.1
-- PHP Version: 8.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `buspass`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `Email` varchar(255) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`Email`, `Name`, `Password`) VALUES
('admin@mail.com', 'Admin', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `departments`
--

CREATE TABLE `departments` (
  `department` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `departments`
--

INSERT INTO `departments` (`department`) VALUES
('Computer Engineering'),
('Mechanical Engineering');

-- --------------------------------------------------------

--
-- Table structure for table `pass`
--

CREATE TABLE `pass` (
  `AdmissionId` bigint NOT NULL,
  `FromPlace` varchar(20) NOT NULL,
  `UKey` varchar(255) NOT NULL,
  `fromtime` date NOT NULL,
  `totime` date NOT NULL,
  `Traveled` json NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `pass`
--

INSERT INTO `pass` (`AdmissionId`, `FromPlace`, `UKey`, `fromtime`, `totime`, `Traveled`) VALUES
(9038, 'Kasaragod', 'ba8b8b61-635c-47d3-b7af-570e0a9b3630', '2025-01-19', '2025-01-20', '[]'),
(9038, 'Kasaragod', 'd7439672-98c1-4feb-89c2-d4e6cf2224f7', '2025-01-15', '2025-01-23', '[\"2025-01-19\"]');

-- --------------------------------------------------------

--
-- Table structure for table `pass_order`
--

CREATE TABLE `pass_order` (
  `OrderID` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `Place` varchar(20) NOT NULL,
  `fromtime` date NOT NULL,
  `totime` date NOT NULL,
  `Type` tinyint NOT NULL,
  `UKey` varchar(255) DEFAULT NULL,
  `Time` date NOT NULL,
  `Status` varchar(30) DEFAULT NULL,
  `Price` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `pass_order`
--

INSERT INTO `pass_order` (`OrderID`, `email`, `Place`, `fromtime`, `totime`, `Type`, `UKey`, `Time`, `Status`, `Price`) VALUES
('53d4d257-9d31-4225-9130-5607300ed0b3', 'shdeekshith@gmail.com', 'Kasaragod', '2025-01-18', '2025-01-18', 1, 'd7439672-98c1-4feb-89c2-d4e6cf2224f7', '2025-01-15', 'PROCESSED', 25),
('9af04df7-a1db-468c-8f87-57afebb15071', 'shdeekshith@gmail.com', 'Kasaragod', '2025-01-22', '2025-01-23', 1, 'd7439672-98c1-4feb-89c2-d4e6cf2224f7', '2025-01-19', 'PROCESSED', 50),
('ba8b8b61-635c-47d3-b7af-570e0a9b3630', 'shdeekshith@gmail.com', 'Kasaragod', '2025-01-19', '2025-01-20', 0, NULL, '2025-01-19', 'PROCESSED', 25),
('d7439672-98c1-4feb-89c2-d4e6cf2224f7', 'shdeekshith@gmail.com', 'Kasaragod', '2025-01-15', '2025-01-17', 0, NULL, '2025-01-15', 'PROCESSED', 75);

-- --------------------------------------------------------

--
-- Table structure for table `place`
--

CREATE TABLE `place` (
  `Place` varchar(30) NOT NULL,
  `Price` int UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `place`
--

INSERT INTO `place` (`Place`, `Price`) VALUES
('Cherkala', 20),
('Kasaragod', 25);

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `Aadhar` bigint NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Photo` varchar(50) NOT NULL,
  `Department` varchar(30) NOT NULL,
  `Password` varchar(20) NOT NULL,
  `Verified` tinyint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`Aadhar`, `Name`, `Email`, `Photo`, `Department`, `Password`, `Verified`) VALUES
(123456789012, 'Staff', 'shdeekshithvpn@gmail.com', '123456789012', 'Computer Engineering', '1234', 1);

-- --------------------------------------------------------

--
-- Table structure for table `staff_order`
--

CREATE TABLE `staff_order` (
  `OrderID` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `Place` varchar(20) NOT NULL,
  `Days` int NOT NULL,
  `Time` date NOT NULL,
  `Status` varchar(30) DEFAULT NULL,
  `Price` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `staff_order`
--

INSERT INTO `staff_order` (`OrderID`, `email`, `Place`, `Days`, `Time`, `Status`, `Price`) VALUES
('6e536866-e3f4-4c09-b9ad-136c31c16fc0', 'shdeekshithvpn@gmail.com', 'Cherkala', 5, '2025-01-15', 'PROCESSED', 100),
('e4389650-efbd-4449-acbe-ddb15a5c210e', 'shdeekshithvpn@gmail.com', 'Kasaragod', 2, '2025-01-15', 'PROCESSED', 50),
('e4f50205-37f3-46eb-9a9c-ea2f7fa69db7', 'shdeekshithvpn@gmail.com', 'Kasaragod', 2, '2025-01-15', NULL, 50),
('f1d30d3f-4c1a-4287-afad-bfde57c7388c', 'shdeekshithvpn@gmail.com', 'Kasaragod', 20, '2025-01-19', 'PROCESSED', 500);

-- --------------------------------------------------------

--
-- Table structure for table `staff_pass`
--

CREATE TABLE `staff_pass` (
  `Aadhar` bigint NOT NULL,
  `FromPlace` varchar(20) NOT NULL,
  `UKey` varchar(255) NOT NULL,
  `Days` int NOT NULL,
  `Traveled` json NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `staff_pass`
--

INSERT INTO `staff_pass` (`Aadhar`, `FromPlace`, `UKey`, `Days`, `Traveled`) VALUES
(123456789012, 'Kasaragod', 'f1d30d3f-4c1a-4287-afad-bfde57c7388c', 20, '[]'),
(123456789012, 'Cherkala', 'yuihy7g87my7my8h968mm', 5, '[\"2025-01-19\"]');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `AdmissionId` bigint NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Photo` varchar(50) NOT NULL,
  `Department` varchar(30) NOT NULL,
  `Password` varchar(20) NOT NULL,
  `Verified` tinyint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`AdmissionId`, `Name`, `Email`, `Photo`, `Department`, `Password`, `Verified`) VALUES
(9038, 'Deekshith', 'shdeekshith@gmail.com', '9038', 'Computer Engineering', '1234', 1);

-- --------------------------------------------------------

--
-- Table structure for table `verification`
--

CREATE TABLE `verification` (
  `Email` varchar(255) NOT NULL,
  `Code` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`Email`);

--
-- Indexes for table `departments`
--
ALTER TABLE `departments`
  ADD PRIMARY KEY (`department`);

--
-- Indexes for table `pass`
--
ALTER TABLE `pass`
  ADD PRIMARY KEY (`UKey`),
  ADD KEY `AdmissionId` (`AdmissionId`),
  ADD KEY `FromPlace` (`FromPlace`);

--
-- Indexes for table `pass_order`
--
ALTER TABLE `pass_order`
  ADD PRIMARY KEY (`OrderID`),
  ADD KEY `email` (`email`),
  ADD KEY `Place` (`Place`);

--
-- Indexes for table `place`
--
ALTER TABLE `place`
  ADD PRIMARY KEY (`Place`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`Aadhar`),
  ADD UNIQUE KEY `Email` (`Email`),
  ADD KEY `Department` (`Department`);

--
-- Indexes for table `staff_order`
--
ALTER TABLE `staff_order`
  ADD PRIMARY KEY (`OrderID`),
  ADD KEY `email` (`email`),
  ADD KEY `Place` (`Place`);

--
-- Indexes for table `staff_pass`
--
ALTER TABLE `staff_pass`
  ADD PRIMARY KEY (`UKey`),
  ADD KEY `Aadhar` (`Aadhar`),
  ADD KEY `FromPlace` (`FromPlace`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`AdmissionId`),
  ADD UNIQUE KEY `Email` (`Email`),
  ADD KEY `Department` (`Department`);

--
-- Indexes for table `verification`
--
ALTER TABLE `verification`
  ADD PRIMARY KEY (`Code`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `pass`
--
ALTER TABLE `pass`
  ADD CONSTRAINT `pass_ibfk_1` FOREIGN KEY (`AdmissionId`) REFERENCES `student` (`AdmissionId`) ON DELETE CASCADE,
  ADD CONSTRAINT `pass_ibfk_2` FOREIGN KEY (`FromPlace`) REFERENCES `place` (`Place`) ON DELETE CASCADE;

--
-- Constraints for table `pass_order`
--
ALTER TABLE `pass_order`
  ADD CONSTRAINT `pass_order_ibfk_1` FOREIGN KEY (`email`) REFERENCES `student` (`Email`) ON DELETE CASCADE,
  ADD CONSTRAINT `pass_order_ibfk_2` FOREIGN KEY (`Place`) REFERENCES `place` (`Place`) ON DELETE CASCADE;

--
-- Constraints for table `staff`
--
ALTER TABLE `staff`
  ADD CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`Department`) REFERENCES `departments` (`department`) ON DELETE CASCADE;

--
-- Constraints for table `staff_order`
--
ALTER TABLE `staff_order`
  ADD CONSTRAINT `staff_order_ibfk_1` FOREIGN KEY (`email`) REFERENCES `staff` (`Email`) ON DELETE CASCADE,
  ADD CONSTRAINT `staff_order_ibfk_2` FOREIGN KEY (`Place`) REFERENCES `place` (`Place`) ON DELETE CASCADE;

--
-- Constraints for table `staff_pass`
--
ALTER TABLE `staff_pass`
  ADD CONSTRAINT `staff_pass_ibfk_1` FOREIGN KEY (`Aadhar`) REFERENCES `staff` (`Aadhar`) ON DELETE CASCADE,
  ADD CONSTRAINT `staff_pass_ibfk_2` FOREIGN KEY (`FromPlace`) REFERENCES `place` (`Place`) ON DELETE CASCADE;

--
-- Constraints for table `student`
--
ALTER TABLE `student`
  ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY (`Department`) REFERENCES `departments` (`department`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
