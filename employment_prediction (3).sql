-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 26, 2025 at 02:36 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `employment_prediction`
--

-- --------------------------------------------------------

--
-- Table structure for table `employment_data`
--

CREATE TABLE `employment_data` (
  `id` int(11) NOT NULL,
  `Sex` varchar(20) DEFAULT NULL,
  `Age` int(11) DEFAULT NULL,
  `Marital_status` varchar(100) DEFAULT NULL,
  `Unpaid_work` varchar(100) DEFAULT NULL,
  `Educational_level` varchar(100) DEFAULT NULL,
  `TVET` varchar(100) DEFAULT NULL,
  `Field_of_education` varchar(100) DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `employment_output`
--

CREATE TABLE `employment_output` (
  `id` int(11) NOT NULL,
  `Sex` varchar(20) DEFAULT NULL,
  `Age` int(11) DEFAULT NULL,
  `Marital_status` varchar(100) DEFAULT NULL,
  `Unpaid_work` varchar(100) DEFAULT NULL,
  `Educational_level` varchar(100) DEFAULT NULL,
  `TVET` varchar(100) DEFAULT NULL,
  `Field_of_education` varchar(100) DEFAULT NULL,
  `prediction` varchar(100) DEFAULT NULL,
  `confidence` float DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `employment_output`
--

INSERT INTO `employment_output` (`id`, `Sex`, `Age`, `Marital_status`, `Unpaid_work`, `Educational_level`, `TVET`, `Field_of_education`, `prediction`, `confidence`, `timestamp`) VALUES
(1, 'Female', 34, 'Divorced', 'Yes', 'University', 'Completed TVET', 'engineering, manufacturing and construction', 'Employed', 99.94, '2025-05-17 12:33:04'),
(2, 'Female', 25, 'Married', 'No', 'University', 'Completed general', 'Education', 'Unemployed', 94.72, '2025-05-17 22:24:20'),
(3, 'Male', 16, 'Single', 'Yes', 'Lower secondary', 'No level completed', 'Social Science business and art', 'Employed', 95.95, '2025-05-20 16:03:15'),
(4, 'Male', 26, 'Living together', 'No', 'Upper secondary', 'Completed TVET', 'Agriculture', 'Unemployed', 76.55, '2025-05-20 16:05:14');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `created_at`) VALUES
(7, 'admin', 'uwanyagasanijerome@gmail.com', 'scrypt:32768:8:1$fby0pX7X5yWYMf3A$27b0824bc574b34f2e580ff73bb9de9ea8b34a5fb8cf4766d95356be3f8db4ee5ef26e27a2f82f8b7efdfc9ed760c55d045a5541d406d760c341aa5fc3210b35', '2025-05-20 10:33:28'),
(8, 'ujerome', 'ujerome250@gmail.com', 'scrypt:32768:8:1$OunJFJDlkjm0Dbks$3eaf0c9a86dbed5b127f979baea192ec2212324831767ef522b8f40d28c5e69b8eac0728a5ed404a9252bf255a39a9cad03f3c46d05acd7c4392e3fd0b8ac804', '2025-05-20 12:38:33'),
(9, 'admin1', '510103150114@rtb.ac.rw', 'scrypt:32768:8:1$tddwxv0gqvM5U3AF$3bf284d6ba5e3b077fec71918a138d935193bb24d9c419f856ff9d3ed0a5934004fc161ebf029f02dc42fd409073a15c7cecbb956831c6524220795f9eb45919', '2025-05-20 12:41:10'),
(10, 'ujerome12', 'aaroniron2050@gmail.com', 'scrypt:32768:8:1$SZxoizx3GuvfbviB$772ee6037c43263675f7985fcbf06b2bf029f7d69f6d7242dc5ec96f722aa185654a5f2806dc501d6eb51707048b02f74d89fd80ad97b02c0547aa9aa524d0c8', '2025-05-20 12:45:16');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `employment_data`
--
ALTER TABLE `employment_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `employment_output`
--
ALTER TABLE `employment_output`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `employment_data`
--
ALTER TABLE `employment_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `employment_output`
--
ALTER TABLE `employment_output`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
