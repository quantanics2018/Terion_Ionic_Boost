-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 06, 2026 at 04:28 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ionic_boost`
--

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `whatsapp_number` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `pincode` varchar(10) DEFAULT NULL,
  `shipment_id` varchar(50) DEFAULT NULL,
  `awb_code` varchar(50) DEFAULT NULL,
  `courier_name` varchar(50) DEFAULT NULL,
  `tracking_url` varchar(255) DEFAULT NULL,
  `order_id_sr` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `product_id`, `name`, `whatsapp_number`, `email`, `address`, `city`, `state`, `pincode`, `shipment_id`, `awb_code`, `courier_name`, `tracking_url`, `order_id_sr`, `created_at`) VALUES
(1, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1002583282', '14112356639969', 'Xpressbees Surface', 'https://shiprocket.co/tracking/14112356639969', '1006186157', '2025-10-18 09:29:43'),
(2, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1002586362', '14112356639957', 'Xpressbees Surface', 'https://shiprocket.co/tracking/14112356639957', '1006189239', '2025-10-18 09:32:41'),
(3, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1002586716', '14112356639956', 'Xpressbees Surface', 'https://shiprocket.co/tracking/14112356639956', '1006189592', '2025-10-18 09:33:10'),
(4, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1002591121', '14112356639903', 'Xpressbees Surface', 'https://shiprocket.co/tracking/14112356639903', '1006194001', '2025-10-18 09:37:38'),
(5, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1002604649', '14112356639822', 'Xpressbees Surface', 'https://shiprocket.co/tracking/14112356639822', '1006207535', '2025-10-18 09:50:53'),
(6, 1, 'sam', '9087940111', 'Admsqeqin@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '6250100', NULL, NULL, NULL, NULL, NULL, '2025-10-18 09:52:42'),
(7, 1, 'sam', '9087940111', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1002607655', '14112356639807', 'Xpressbees Surface', 'https://shiprocket.co/tracking/14112356639807', '1006210541', '2025-10-18 09:53:40'),
(8, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', NULL, NULL, NULL, NULL, NULL, '2025-10-18 10:14:17'),
(9, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', NULL, NULL, NULL, NULL, NULL, '2025-10-18 10:15:33'),
(10, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', NULL, NULL, NULL, NULL, NULL, '2025-10-18 10:22:28'),
(11, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', NULL, NULL, NULL, NULL, NULL, '2025-10-18 10:22:31'),
(12, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', NULL, NULL, NULL, NULL, NULL, '2025-10-18 10:22:37'),
(13, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', NULL, NULL, NULL, NULL, NULL, '2025-10-18 10:24:37'),
(14, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', NULL, NULL, NULL, NULL, NULL, '2025-10-18 10:25:58'),
(15, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', NULL, NULL, NULL, NULL, NULL, '2025-10-18 10:28:24'),
(16, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1002652304', '14112356640998', 'Xpressbees Surface', 'https://shiprocket.co/tracking/14112356640998', '1006255210', '2025-10-18 10:34:11'),
(17, 1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1002656951', '14112356640967', 'Xpressbees Surface', 'https://shiprocket.co/tracking/14112356640967', '1006259855', '2025-10-18 10:38:38'),
(18, 6, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1002668869', '14112356640870', 'Xpressbees Surface', 'https://shiprocket.co/tracking/14112356640870', '1006271782', '2025-10-18 10:49:04'),
(19, 5, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', NULL, NULL, NULL, NULL, NULL, '2025-10-18 11:06:22'),
(20, 5, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1002685074', '14112356640831', 'Xpressbees Surface', 'https://shiprocket.co/tracking/14112356640831', '1006287992', '2025-10-18 11:06:55'),
(21, 3, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1002687457', '14112356640822', 'Xpressbees Surface', 'https://shiprocket.co/tracking/14112356640822', '1006290376', '2025-10-18 11:09:03');

-- --------------------------------------------------------

--
-- Table structure for table `order_1`
--

CREATE TABLE `order_1` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `whatsapp_number` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `pincode` varchar(10) DEFAULT NULL,
  `shipment_id` varchar(100) DEFAULT NULL,
  `awb_code` varchar(100) DEFAULT NULL,
  `courier_name` varchar(100) DEFAULT NULL,
  `tracking_url` text DEFAULT NULL,
  `manifest_url` text DEFAULT NULL,
  `label_url` text DEFAULT NULL,
  `order_id_sr` text DEFAULT NULL,
  `invoice_url` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `whatsapp_sent` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_1`
--

INSERT INTO `order_1` (`id`, `name`, `whatsapp_number`, `email`, `address`, `city`, `state`, `pincode`, `shipment_id`, `awb_code`, `courier_name`, `tracking_url`, `manifest_url`, `label_url`, `order_id_sr`, `invoice_url`, `created_at`, `whatsapp_sent`) VALUES
(1, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1007876929', NULL, NULL, 'https://shiprocket.co/tracking/364571799719', NULL, NULL, '1011481537', NULL, '2025-10-23 11:16:18', 0),
(2, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1007995585', NULL, NULL, 'https://shiprocket.co/tracking/364573800284', NULL, NULL, '1011600259', NULL, '2025-10-23 13:39:23', 0),
(3, 'martin', '6383077690', 'vetrinishanth@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamilnadu', '625016', '1008005343', NULL, NULL, NULL, NULL, NULL, '1011610021', NULL, '2025-10-23 13:49:52', 0),
(4, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1009209004', NULL, NULL, NULL, NULL, NULL, '1012814304', NULL, '2025-10-24 15:59:31', 0),
(5, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1009244072', NULL, NULL, NULL, NULL, NULL, '1012849380', NULL, '2025-10-24 16:37:31', 0),
(6, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1009600296', NULL, NULL, NULL, NULL, NULL, '1013205690', NULL, '2025-10-25 05:14:15', 0),
(7, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1011893269', NULL, NULL, NULL, NULL, NULL, '1015499287', NULL, '2025-10-27 06:26:39', 0),
(8, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', '1011895476', NULL, NULL, NULL, NULL, NULL, '1015501495', NULL, '2025-10-27 06:28:12', 0),
(9, 'Adhiban', 'R', 'rajeshadhiban2005@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamilnadu', '625016', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-01-05 14:05:15', 0);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `sku` varchar(50) NOT NULL,
  `price` float NOT NULL,
  `weight` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `sku`, `price`, `weight`) VALUES
(1, 'ESP32', 'esp32sku', 550, 0.1),
(2, 'ESP8266', 'esp8266sku', 400, 0.1),
(3, 'Arduino Uno', 'arduinosku', 650, 0.2),
(4, 'Relays', 'relaysku', 300, 0.15),
(5, 'Breadboard', 'breadboardsku', 150, 0.05),
(6, 'Ultrasonic Sensor', 'ultrasonicsku', 120, 0.05),
(7, 'DHT11', 'dht11sku', 100, 0.03),
(8, 'Soil Moisture Sensor', 'soilmoisturesku', 150, 0.05),
(9, 'Raindrop Sensor', 'raindropsku', 100, 0.03),
(10, 'MQ2 Sensor', 'mq2sku', 250, 0.05);

-- --------------------------------------------------------

--
-- Table structure for table `purchases`
--

CREATE TABLE `purchases` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `item_name` varchar(255) DEFAULT NULL,
  `purchase_date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `shiprocket_orders`
--

CREATE TABLE `shiprocket_orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `razorpay_order_id` varchar(100) NOT NULL,
  `razorpay_payment_id` varchar(100) DEFAULT NULL,
  `shiprocket_order_id` varchar(100) DEFAULT NULL,
  `shipment_id` varchar(100) DEFAULT NULL,
  `tracking_url` text DEFAULT NULL,
  `status` varchar(50) DEFAULT 'created',
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shiprocket_orders`
--

INSERT INTO `shiprocket_orders` (`id`, `user_id`, `razorpay_order_id`, `razorpay_payment_id`, `shiprocket_order_id`, `shipment_id`, `tracking_url`, `status`, `created_at`) VALUES
(2, 11, 'undefined', 'pay_RRLhEPXVi8hc7Z', '975095493', '971511893', NULL, 'NEW', '2025-10-09 10:55:45'),
(3, 11, 'undefined', 'pay_RRLjnmVmnalqct', '975095493', '971511893', NULL, 'NEW', '2025-10-09 10:58:11'),
(4, 11, 'undefined', 'pay_RRLw9pR8kE98PG', '975095493', '971511893', NULL, 'NEW', '2025-10-09 11:09:52'),
(5, 11, 'undefined', 'pay_RRM4X2kDFKDYf4', '975095493', '971511893', NULL, 'NEW', '2025-10-09 11:17:48'),
(6, 11, 'undefined', 'pay_RRMCqBMUUI9mx8', '975095493', '971511893', NULL, 'NEW', '2025-10-09 11:25:40'),
(7, 11, 'undefined', 'pay_RRMFmDemx75bOq', '975095493', '971511893', NULL, 'NEW', '2025-10-09 11:28:27'),
(8, 11, 'undefined', 'pay_RRMIXm4lZXrt46', '975095493', '971511893', NULL, 'NEW', '2025-10-09 11:31:04'),
(9, 11, 'undefined', 'pay_RRMKmkyciQR5cz', '975095493', '971511893', NULL, 'NEW', '2025-10-09 11:33:12'),
(10, 11, 'undefined', 'pay_RRNEVcrkb32zit', '975095493', '971511893', NULL, 'NEW', '2025-10-09 12:25:56'),
(11, 11, 'undefined', 'pay_RRNLUnXO6o4oP2', '975095493', '971511893', NULL, 'NEW', '2025-10-09 12:32:34'),
(12, 11, 'undefined', 'pay_RRNQrG4VDes9g8', '975095493', '971511893', NULL, 'NEW', '2025-10-09 12:37:38'),
(13, 11, 'undefined', 'pay_RRNSXGNv96lMam', '975095493', '971511893', NULL, 'NEW', '2025-10-09 12:39:13'),
(14, 11, 'undefined', 'pay_RRNhtgYcirR0eD', '975095493', '971511893', NULL, 'NEW', '2025-10-09 12:53:46'),
(15, 11, 'undefined', 'pay_RRevO3Fui0X9JO', '975095493', '971511893', NULL, 'created', '2025-10-10 05:44:19'),
(16, 11, 'order_RRfB3j8d622tdr', 'pay_RRfBftSDHG3IGW', '995719842', '992120598', 'https://shiprocket.co/tracking/14112356483135', 'awb_generated', '2025-10-10 05:59:46'),
(17, 11, 'order_RRfEP1eWrMcTVP', 'pay_RRfEboxUKeTZuY', '995723157', '992123911', 'https://shiprocket.co/tracking/14112356483046', 'awb_generated', '2025-10-10 06:02:33');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `order_id` varchar(255) NOT NULL,
  `payment_id` varchar(255) DEFAULT NULL,
  `signature` varchar(255) DEFAULT NULL,
  `amount` int(11) NOT NULL,
  `currency` varchar(10) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `user_address` text DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `pincode` varchar(20) DEFAULT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `order_id`, `payment_id`, `signature`, `amount`, `currency`, `status`, `user_name`, `user_address`, `city`, `state`, `pincode`, `payment_method`, `created_at`) VALUES
(1, 'undefined', 'pay_RRLhEPXVi8hc7Z', NULL, 10000, 'INR', NULL, 'Test User', 'Test Address', 'Test City', 'Test State', '000000', 'UPI', '2025-10-09 10:55:44'),
(2, 'undefined', 'pay_RRLjnmVmnalqct', NULL, 10000, 'INR', NULL, 'Test User', 'Test Address', 'Test City', 'Test State', '000000', 'UPI', '2025-10-09 10:58:10'),
(3, 'undefined', 'pay_RRLw9pR8kE98PG', NULL, 10000, 'INR', NULL, 'Test User', 'Test Address', 'Test City', 'Test State', '000000', 'UPI', '2025-10-09 11:09:52'),
(4, 'undefined', 'pay_RRM4X2kDFKDYf4', NULL, 10000, 'INR', NULL, 'Test User', 'Test Address', 'Test City', 'Test State', '000000', 'UPI', '2025-10-09 11:17:47'),
(5, 'undefined', 'pay_RRMCqBMUUI9mx8', NULL, 10000, 'INR', NULL, 'Test User', 'Test Address', 'Test City', 'Test State', '000000', 'UPI', '2025-10-09 11:25:39'),
(6, 'undefined', 'pay_RRMFmDemx75bOq', NULL, 10000, 'INR', NULL, 'Test User', 'Test Address', 'Test City', 'Test State', '000000', 'UPI', '2025-10-09 11:28:26'),
(7, 'undefined', 'pay_RRMIXm4lZXrt46', NULL, 10000, 'INR', NULL, 'Test User', 'Test Address', 'Test City', 'Test State', '000000', 'UPI', '2025-10-09 11:31:03'),
(8, 'undefined', 'pay_RRMKmkyciQR5cz', NULL, 10000, 'INR', NULL, 'Test User', 'Test Address', 'Test City', 'Test State', '000000', 'UPI', '2025-10-09 11:33:11'),
(9, 'undefined', 'pay_RRNEVcrkb32zit', NULL, 10000, 'INR', NULL, 'Test User', 'Test Address', 'Test City', 'Test State', '000000', 'UPI', '2025-10-09 12:25:55'),
(10, 'undefined', 'pay_RRNLUnXO6o4oP2', NULL, 10000, 'INR', NULL, 'Test User', 'Test Address', 'Test City', 'Test State', '000000', 'UPI', '2025-10-09 12:32:32'),
(11, 'undefined', 'pay_RRNQrG4VDes9g8', NULL, 10000, 'INR', NULL, 'Test User', 'Test Address', 'Test City', 'Test State', '000000', 'UPI', '2025-10-09 12:37:37'),
(12, 'undefined', 'pay_RRNSXGNv96lMam', NULL, 10000, 'INR', NULL, 'Test User', 'Test Address', 'Test City', 'Test State', '000000', 'UPI', '2025-10-09 12:39:12'),
(13, 'undefined', 'pay_RRNhtgYcirR0eD', NULL, 10000, 'INR', NULL, 'Test User', 'Test Address', 'Test City', 'Test State', '000000', 'UPI', '2025-10-09 12:53:45');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `whatsapp_number` varchar(15) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `address` text NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `pincode` varchar(10) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `whatsapp_number`, `email`, `address`, `city`, `state`, `pincode`, `password_hash`, `created_at`) VALUES
(7, 'Joe', '9999999999', 'prajan@gmail.com', 'f', 'd', 'w', '738221', 'scrypt:32768:8:1$BGzheyKRIO9uH9XN$7e7b2f75728e3119590326dab6dbce07c65a2f22355b1f0fe4c6b3854f267e774e5654913239ba53502761fa084cba7e615ae1731a22155bdb49fa034ca9293e', '2025-09-17 14:15:51'),
(10, 'john', '9842878776', '2115021@nec.edu.in', '26D,theni main road, P.P.Chavadi', 'Madurai South', 'Tamil Nadu', '625016', 'scrypt:32768:8:1$zBlao0MHQIc5QsnG$f600d05b86f5690b882a35603047f74146a5c39592211f8bc622a20ed7709bdc1b014bb441098f1b32faa54effd4a299766eb9ab2e719315f046c06302b4176a', '2025-09-23 15:27:59'),
(11, 'martin', '6383077690', 'vetrinishanth@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamilnadu', '625016', 'scrypt:32768:8:1$i1MySL4YCnw5eFGv$a31629229036db4a770fc14e0032d85268653bd810fd818cb4d357e1535a686d0f2dc36e741b7ffe7a9405b48ba463de18e125c684b441045e5697ec28e976d2', '2025-10-09 10:52:49'),
(12, 'vetri', '9894552303', 'vetrixavier832@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamil Nadu', '625016', 'scrypt:32768:8:1$LIYl9OlW6NeCWh65$1d5eef53826e75fedda56e0ce567c96f3c08cae32fbc76771d7617c2551a5c0b5771f40ff51135c64b9c4fab69db99c13965b344292e81055b90e816fe87f63d', '2025-10-23 11:15:17'),
(13, 'Adhiban', 'R', 'rajeshadhiban2005@gmail.com', '26D,theni main road, P.P.Chavadi', 'Madurai', 'Tamilnadu', '625016', 'scrypt:32768:8:1$si5UFyCfVeCOC16x$e2b4d3308b068c74a331ee4bb2e7edaa67b279d106c464541765f56795968c8ed1f3e7c314d7d9788819b5ebbaa050481a98174344602a4d28fd5dc9c4d74e1a', '2026-01-05 13:42:05');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `order_1`
--
ALTER TABLE `order_1`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `purchases`
--
ALTER TABLE `purchases`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `shiprocket_orders`
--
ALTER TABLE `shiprocket_orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `whatsapp_number` (`whatsapp_number`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `order_1`
--
ALTER TABLE `order_1`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `purchases`
--
ALTER TABLE `purchases`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `shiprocket_orders`
--
ALTER TABLE `shiprocket_orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `purchases`
--
ALTER TABLE `purchases`
  ADD CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `shiprocket_orders`
--
ALTER TABLE `shiprocket_orders`
  ADD CONSTRAINT `shiprocket_orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
