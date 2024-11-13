-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 28, 2023 at 10:12 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hotel`
--

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `id` int(11) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `tipe` varchar(255) NOT NULL,
  `checkin` date NOT NULL,
  `checkout` date NOT NULL,
  `status` enum('Confirm','Booking','Leave') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`id`, `nama`, `email`, `phone`, `tipe`, `checkin`, `checkout`, `status`) VALUES
(1, 'joshua', 'joshua@gmail.com', '081111111111', 'Deluxe Room', '2023-06-01', '2023-06-02', 'Confirm'),
(2, 'wilson', 'wilson1@gmail.com', '081222222222', 'Family Room', '2023-07-02', '2023-07-03', 'Booking');

-- --------------------------------------------------------

--
-- Table structure for table `tb_users`
--

CREATE TABLE `tb_users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `level` enum('Admin','User') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_users`
--

INSERT INTO `tb_users` (`id`, `username`, `email`, `password`, `level`) VALUES
(1, 'jose', 'jose07pavell@gmail.com', 'pbkdf2:sha256:260000$gdcpAfvffgvbSCyQ$5b6e74b2e0bf8de805b181c209162677fb6002576158efa7b261299e13513a50', 'User'),
(2, 'joshua', 'joshuapavell23@gmail.com', 'pbkdf2:sha256:260000$PnQUIiP4cVOBfSNJ$ca752019f1d7debce26aceb86251381e31086c22ff07888c06d6199dca718c5e', 'Admin'),
(3, 'admin', 'admin@gmail.com', 'pbkdf2:sha256:260000$kCRShfhIIZAtiV2Q$396c09a457a7b0ba4809cd3927b1c337942f4d7b19b29ce36fcd212e29fd55ba', 'Admin'),
(4, 'user', 'user@gmail.com', 'pbkdf2:sha256:260000$K5v0JkRgX3R3FB7r$a6fa8f45bd4098de6015d25c8d0e033b74ad7213a8d3431b27456f711d78396f', 'User');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_users`
--
ALTER TABLE `tb_users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tb_users`
--
ALTER TABLE `tb_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
