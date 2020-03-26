-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 26, 2020 at 03:48 PM
-- Server version: 5.7.25-0ubuntu0.18.04.2
-- PHP Version: 7.2.28-3+ubuntu18.04.1+deb.sury.org+1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Log-identificacion`
--

-- --------------------------------------------------------

--
-- Table structure for table `Identificacion`
--

CREATE TABLE `Identificacion` (
  `Id` int(11) NOT NULL,
  `Item` int(11) NOT NULL,
  `File` varchar(50) NOT NULL,
  `Timeline` varchar(50) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `PersonId` varchar(50) NOT NULL,
  `MatchProbability` varchar(50) NOT NULL,
  `GroupId` varchar(50) NOT NULL,
  `LocalPersistedId` varchar(50) NOT NULL,
  `TestNumero` int(11) NOT NULL DEFAULT '-1',
  `CicloTest` int(1) NOT NULL,
  `StartCiclo` varchar(30) NOT NULL,
  `FechaTest` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Identificacion`
--
ALTER TABLE `Identificacion`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Identificacion`
--
ALTER TABLE `Identificacion`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
