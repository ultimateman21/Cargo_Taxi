CREATE DATABASE  IF NOT EXISTS `1` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `1`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: 1
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `id` int NOT NULL AUTO_INCREMENT,
  `human_id` int NOT NULL,
  `phone_num` varchar(45) NOT NULL,
  `password` varchar(65) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `c_human_idx` (`human_id`),
  CONSTRAINT `c_human` FOREIGN KEY (`human_id`) REFERENCES `human` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES (5,1,'+79996987550','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'),(9,2,'+79096987550','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4');
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `human_id` int NOT NULL,
  `phone_num` varchar(45) NOT NULL,
  `password` varchar(65) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `e_human_idx` (`human_id`),
  CONSTRAINT `e_human` FOREIGN KEY (`human_id`) REFERENCES `human` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,3,'000000000000','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `human`
--

DROP TABLE IF EXISTS `human`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `human` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name_1` varchar(45) NOT NULL,
  `name_2` varchar(45) NOT NULL,
  `name_3` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `human`
--

LOCK TABLES `human` WRITE;
/*!40000 ALTER TABLE `human` DISABLE KEYS */;
INSERT INTO `human` VALUES (1,'Фомин','Олег','Константинович'),(2,'Владимир','Владимиров','Владимирович'),(3,'тест','тест','тест');
/*!40000 ALTER TABLE `human` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `data` datetime NOT NULL,
  `text` varchar(200) NOT NULL,
  `sender` varchar(15) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `m_order_idx` (`order_id`),
  CONSTRAINT `m_order` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (1,4,'2024-06-09 20:50:21','j','client'),(2,4,'2024-06-09 21:12:58','0','worker'),(3,4,'2024-06-09 22:17:06','ftunyugutfbin\nevdtut78nfghfj\n989yyiftrdes','worker'),(4,4,'2024-08-16 20:26:05','поапаш','client'),(5,4,'2024-10-13 23:55:48','это куда','client'),(6,6,'2024-10-13 23:57:45','это зачем','client'),(7,10,'2024-10-14 00:01:52','это куда','worker'),(8,12,'2024-10-21 14:57:59','dfghuieyrtuio\n','worker');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `client_id` int NOT NULL,
  `vehicle_id` int DEFAULT NULL,
  `from` varchar(150) NOT NULL,
  `to` varchar(150) NOT NULL,
  `dist` int NOT NULL,
  `date` datetime NOT NULL,
  `price` int NOT NULL,
  `space` float NOT NULL,
  `capacity` float NOT NULL,
  `weight` float NOT NULL,
  `state` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `o_client_idx` (`client_id`),
  KEY `o_vehicle_idx` (`vehicle_id`),
  CONSTRAINT `o_client` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `o_vehicle` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (4,5,6,'Ростов-на-Дону, улица Волкова, 8 к 1','Ростов-на-Дону, улица Большая Садовая, 55',7754,'2024-05-04 01:01:00',640,1,8,1,1),(5,5,NULL,'Ростов-на-Дону, улица Волкова, 8 к 1','Шахты, улица Рылеева, 53',72520,'2024-05-06 02:02:00',7300,10,10,40,0),(6,5,7,'Ростов-на-Дону, улица Большая Садовая, 55','Шахты, улица Рылеева, 53',76654,'2024-05-06 03:03:00',7700,1,10,10,1),(10,9,5,'Ростов-на-Дону, улица Большая Садовая, 55','Каменск-Шахтинский, пер. Крупской, 99',140373,'2024-10-13 00:00:00',15000,10,10,70,2),(12,5,12,'Ростов-на-Дону, улица Волкова, 8','Ростов-на-Дону, улица Большая Садовая, 60',7970,'2024-10-21 12:00:00',800,10,10,60,3),(13,9,NULL,'Ростов-на-Дону, улица Большая Садовая, 60','Ростов-на-Дону, улица Волкова, 8',8040,'2024-10-21 14:00:00',1800,10,20,70,0),(14,5,5,'Ростов-на-Дону, ул. Волкова, 8 к 1','Ростов-на-Дону, ул. Большая Садовая, 55',7754,'2024-10-22 00:00:00',480,1,6,40,3),(15,5,12,'Ростов-на-Дону, улица Волкова, 10','Ростов-на-Дону, улица Большая Садовая, 65',7059,'2024-10-23 04:00:00',2400,15,30,50,2);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `selected_order`
--

DROP TABLE IF EXISTS `selected_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `selected_order` (
  `worker_vehicle_id` int NOT NULL,
  `order_id` int NOT NULL,
  `state` int NOT NULL DEFAULT '0',
  KEY `so_wv_idx` (`worker_vehicle_id`),
  KEY `so_order_idx` (`order_id`),
  CONSTRAINT `so_order` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `so_wv` FOREIGN KEY (`worker_vehicle_id`) REFERENCES `worker_vehicle` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `selected_order`
--

LOCK TABLES `selected_order` WRITE;
/*!40000 ALTER TABLE `selected_order` DISABLE KEYS */;
INSERT INTO `selected_order` VALUES (1,6,1),(8,4,0),(1,5,2);
/*!40000 ALTER TABLE `selected_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle`
--

DROP TABLE IF EXISTS `vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `worker_id` int NOT NULL,
  `reg_num` varchar(15) NOT NULL,
  `space` float NOT NULL,
  `capacity` float NOT NULL,
  `weight` float NOT NULL,
  `state` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `v_worker_idx` (`worker_id`),
  CONSTRAINT `v_worker` FOREIGN KEY (`worker_id`) REFERENCES `worker` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle`
--

LOCK TABLES `vehicle` WRITE;
/*!40000 ALTER TABLE `vehicle` DISABLE KEYS */;
INSERT INTO `vehicle` VALUES (5,1,'a000aa161rus',10,20,100,1),(6,1,'a001aa161rus',5,10,85,0),(7,2,'b000bb161rus',5,15,200,0),(12,2,'b001bb161rus',20,40,60,1),(13,1,'a002aa161rus',10,10,50,0);
/*!40000 ALTER TABLE `vehicle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worker`
--

DROP TABLE IF EXISTS `worker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worker` (
  `id` int NOT NULL AUTO_INCREMENT,
  `human_id` int NOT NULL,
  `phone_num` varchar(45) NOT NULL,
  `password` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `w_human_idx` (`human_id`),
  CONSTRAINT `w_human` FOREIGN KEY (`human_id`) REFERENCES `human` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worker`
--

LOCK TABLES `worker` WRITE;
/*!40000 ALTER TABLE `worker` DISABLE KEYS */;
INSERT INTO `worker` VALUES (1,1,'+79996987550','fe2592b42a727e977f055947385b709cc82b16b9a87f88c6abf3900d65d0cdc3'),(2,2,'+79096987550','fe2592b42a727e977f055947385b709cc82b16b9a87f88c6abf3900d65d0cdc3');
/*!40000 ALTER TABLE `worker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worker_vehicle`
--

DROP TABLE IF EXISTS `worker_vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worker_vehicle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `worker_id` int NOT NULL,
  `vehicle_id` int NOT NULL,
  `state` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `wv_worker_idx` (`worker_id`),
  KEY `wv_vehicle_idx` (`vehicle_id`),
  CONSTRAINT `wv_vehicle` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `wv_worker` FOREIGN KEY (`worker_id`) REFERENCES `worker` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worker_vehicle`
--

LOCK TABLES `worker_vehicle` WRITE;
/*!40000 ALTER TABLE `worker_vehicle` DISABLE KEYS */;
INSERT INTO `worker_vehicle` VALUES (1,1,5,0),(2,1,6,1),(3,2,7,0),(8,2,12,1);
/*!40000 ALTER TABLE `worker_vehicle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database '1'
--
/*!50003 DROP PROCEDURE IF EXISTS `cancel_order_c` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `cancel_order_c`(
    IN id_ INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		IF (SELECT state FROM `order` WHERE id = id_) = 0 THEN
			DELETE FROM `order` WHERE id = id_;
		END IF;
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `cancel_order_w` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `cancel_order_w`(
    IN id_ INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		IF (SELECT state FROM `order` WHERE id = id_) = 1 THEN
			UPDATE `order` SET state = 2 WHERE id = id_;
		END IF;
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `check_reg` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `check_reg`(
    IN phone VARCHAR(45),
    IN pass VARCHAR(65),
    OUT `table_name` VARCHAR(20),
    OUT id_ INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		SELECT 'client' INTO `table_name` WHERE EXISTS (
		SELECT 1 FROM `client` WHERE phone_num = phone AND `password` = pass);

		SELECT 'worker' INTO `table_name` WHERE EXISTS (
		SELECT 1 FROM worker WHERE phone_num = phone AND `password` = pass);
		
		SELECT 'employee' INTO `table_name` WHERE EXISTS (
		SELECT 1 FROM employee WHERE phone_num = phone AND `password` = pass);

		IF `table_name` IS NOT NULL THEN
			CASE `table_name`
				WHEN 'client' THEN
					SELECT id INTO id_ FROM `client` WHERE phone_num = phone AND `password` = pass;
				WHEN 'worker' THEN
					SELECT id INTO id_ FROM worker WHERE phone_num = phone AND `password` = pass;
				WHEN 'employee' THEN
					SELECT id INTO id_ FROM employee WHERE phone_num = phone AND `password` = pass;
			END CASE;
		END IF;
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `choose_order` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `choose_order`(
	IN id_w INT,
    IN id_order INT
)
BEGIN
	DECLARE v_id INT;
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		SELECT id INTO v_id FROM vehicle WHERE (worker_id, state) = (id_w, 1);
		
		IF (SELECT COUNT(*) FROM `order` WHERE (vehicle_id, state) = (v_id, 1)) = 0 THEN
			UPDATE `order` SET vehicle_id = v_id WHERE id = id_order;
            UPDATE `order` SET state = 1 WHERE id = id_order;
		END IF;
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `choose_vehicle` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `choose_vehicle`(
	IN id_w INT,
    IN id_v INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		UPDATE vehicle SET state = 0 WHERE worker_id = id_w;
		UPDATE vehicle SET state = 1 WHERE (worker_id, id) = (id_w, id_v);
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `finish_order` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `finish_order`(
    IN id_ INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		IF (SELECT state FROM `order` WHERE id = id_) = 1 THEN
			UPDATE `order` SET state = 3 WHERE id = id_;
		END IF;
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_chat_fios` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_chat_fios`(
	IN order_id INT,
    OUT worker_ TEXT,
    OUT client_ TEXT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		SELECT CONCAT_WS(';', CONCAT_WS(' ', name_1, name_2, name_3), phone_num) INTO worker_
		FROM worker a JOIN human b ON a.human_id = b.id WHERE a.id = (
		SELECT a.id FROM worker a JOIN vehicle b ON a.id = b.worker_id
		JOIN `order` c ON b.id = c.vehicle_id WHERE c.id = order_id);
		
		SELECT CONCAT_WS(';', CONCAT_WS(' ', name_1, name_2, name_3), phone_num) INTO client_
		FROM `client` a JOIN human b ON a.human_id = b.id WHERE a.id = (
		SELECT a.id FROM `client` a JOIN `order` b ON a.id = b.client_id WHERE b.id = order_id);
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_h_orders_c` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_h_orders_c`(
	IN id_ INT,
    OUT rows_ TEXT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		SELECT GROUP_CONCAT(CONCAT_WS('|', `from`, `to`, dist, `date`, price, space, capacity, weight, state) SEPARATOR ';')
		INTO rows_ FROM `order` WHERE client_id = id_ AND state > 1;
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_h_orders_w` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_h_orders_w`(
	IN id_ INT,
    OUT rows_ TEXT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		SELECT GROUP_CONCAT(CONCAT_WS('|', `from`, `to`, dist, `date`, price, space, capacity, weight, state) SEPARATOR ';')
		INTO rows_ FROM `order` WHERE vehicle_id = (SELECT id FROM vehicle WHERE worker_id = id_ AND state = 1) AND state > 1;
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_messages` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_messages`(
	IN order_ INT,
    OUT rows_ TEXT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		SELECT GROUP_CONCAT(CONCAT_WS('|', `data`, `text`, sender) SEPARATOR ';')
		INTO rows_ FROM message WHERE order_id = order_;
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_name` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_name`(
	IN `role` VARCHAR(20),
    IN id_ INT,
    OUT name123 TEXT
)
BEGIN
	DECLARE fk_value INT;
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
	START TRANSACTION;
		CASE `role`
			WHEN 'client' THEN
				SELECT human_id INTO fk_value FROM `client` WHERE id = id_;
			WHEN 'worker' THEN
				SELECT human_id INTO fk_value FROM worker WHERE id = id_;
			WHEN 'employee' THEN
				SELECT human_id INTO fk_value FROM employee WHERE id = id_;
		END CASE;

		SELECT CONCAT_WS(' ', name_1, name_2, name_3) INTO name123 FROM human WHERE id = fk_value;
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_orders_c` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_orders_c`(
	IN id_ INT,
    OUT rows_ TEXT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		SELECT GROUP_CONCAT(CONCAT_WS('|', id, `from`, `to`, dist, `date`, price, space, capacity, weight, state) SEPARATOR ';')
		INTO rows_ FROM `order` WHERE client_id = id_;
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_orders_w` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_orders_w`(
	IN id_ INT,
    OUT rows_ TEXT
)
BEGIN
	DECLARE space_ INT;
	DECLARE capacity_ INT;
	DECLARE weight_ INT;
	DECLARE other_select TEXT;
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
	
    START TRANSACTION;
		SELECT `space`, capacity, weight INTO space_, capacity_, weight_ FROM vehicle WHERE (worker_id, state) = (id_, 1);

		SELECT GROUP_CONCAT(id) INTO other_select FROM `order` WHERE vehicle_id IS NOT NULL AND
		vehicle_id != (SELECT id FROM vehicle WHERE (worker_id, state) = (id_, 1));
        
		SELECT GROUP_CONCAT(CONCAT_WS('|', id, `from`, `to`, dist, `date`, price, space, capacity, weight, state) SEPARATOR ';')
		INTO rows_ FROM `order` WHERE `space` <= space_ AND capacity <= capacity_ AND weight <= weight_ AND state < 2 AND
		NOT IFNULL(FIND_IN_SET(id, other_select), 0);
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_phone` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_phone`(
	IN id_ INT,
    IN `role` VARCHAR(20),
    OUT phone VARCHAR(20)
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		CASE `role`
			WHEN 'client' THEN
				SELECT phone_num INTO phone FROM `client` WHERE id = id_;
			WHEN 'worker' THEN
				SELECT phone_num INTO phone FROM worker WHERE id = id_;
			WHEN 'employee' THEN
				SELECT phone_num INTO phone FROM employee WHERE id = id_;
		END CASE;
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_user_grants` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_user_grants`(
    IN user_names TEXT, 
    IN host_names TEXT, 
    OUT grants_result TEXT
)
BEGIN
    DECLARE user_name VARCHAR(255);
    DECLARE host_name VARCHAR(255);
    DECLARE grant_statement TEXT DEFAULT '';
    DECLARE user_count INT DEFAULT 1;
    DECLARE host_count INT DEFAULT 1;
    
    DECLARE user_total INT DEFAULT LENGTH(user_names) - LENGTH(REPLACE(user_names, ',', '')) + 1;
    DECLARE host_total INT DEFAULT LENGTH(host_names) - LENGTH(REPLACE(host_names, ',', '')) + 1;

    DECLARE cur CURSOR FOR 
        SELECT CONCAT('GRANT EXECUTE ON PROCEDURE ', db, '.', routine_name, ' TO ', user_name, '@', host_name, ' WITH GRANT OPTION')
        FROM mysql.procs_priv
        WHERE user = user_name AND host = host_name;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET grant_statement = NULL;

    SET grants_result = '';

    IF user_total = host_total THEN
        WHILE user_count <= user_total DO
            SET user_name = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(user_names, ',', user_count), ',', -1));
            SET host_name = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(host_names, ',', host_count), ',', -1));

            OPEN cur;

            read_loop: LOOP
                FETCH cur INTO grant_statement;

                IF grant_statement IS NULL THEN
                    LEAVE read_loop;
                END IF;

                SET grants_result = CONCAT(grants_result, grant_statement, ';\n');
            END LOOP;

            CLOSE cur;

            SET user_count = user_count + 1;
            SET host_count = host_count + 1;
        END WHILE;
    ELSE
        SET grants_result = 'Error: User count and host count do not match.';
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_vehicles` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_vehicles`(
	IN id_ INT,
    OUT rows_ TEXT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		SELECT GROUP_CONCAT(CONCAT_WS('|', id, reg_num, `space`, capacity, weight, state) SEPARATOR ';')
		INTO rows_ FROM vehicle WHERE worker_id = id_;
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `new_message` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `new_message`(
	IN order_ INT,
    IN date_ VARCHAR(20),
    IN text_ VARCHAR(200),
    IN role_ VARCHAR(15)
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		INSERT INTO message (order_id, `data`, `text`, sender) VALUES 
		(order_, STR_TO_DATE(date_, '%Y-%m-%d %H:%i:%s'), text_, role_);
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `new_order` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `new_order`(
	IN id_ INT,
    IN from_ VARCHAR(150),
    IN to_ VARCHAR(150),
    IN dist INT,
    IN d_t VARCHAR(20),
    IN price INT,
    IN space_ FLOAT,
    IN capacity FLOAT,
    IN weight FLOAT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		INSERT INTO `order` (client_id, `from`, `to`, dist, `date`, price, `space`, capacity, weight)
		VALUES (id_, from_, to_, dist, STR_TO_DATE(d_t, '%d-%m-%Y %H:%i'), price, space_, capacity, weight);
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `new_vehicle` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `new_vehicle`(
	IN id_ INT,
    IN num VARCHAR(15),
    IN space_ INT,
    IN capacity_ INT,
    IN weight_ INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		INSERT INTO vehicle (worker_id, reg_num, `space`, capacity, weight) VALUES (id_, num, space_, capacity_, weight_);
	COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `register` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `register`(
    IN name1 VARCHAR(45),
    IN name2 VARCHAR(45),
    IN name3 VARCHAR(45),
    IN phone VARCHAR(45),
    IN pass VARCHAR(65),
    OUT o INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
		ROLLBACK;
	END;
    
    START TRANSACTION;
		IF NOT EXISTS (SELECT 1 FROM `human` WHERE (name_1, name_2, name_3) = (name1, name2, name3)) THEN
			INSERT INTO human (name_1, name_2, name_3) VALUES (name1, name2, name3);
			INSERT INTO `client` (human_id, phone_num, `password`) VALUES (LAST_INSERT_ID(), phone, pass);
        ELSE
			SELECT 0 INTO o;
        END IF;
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `test` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `test`(
    IN user_name VARCHAR(255), 
    IN host_name VARCHAR(255), 
    OUT grants_result TEXT
)
BEGIN
    DECLARE grant_statement TEXT DEFAULT '';
    
    DECLARE cur CURSOR FOR 
        SELECT CONCAT('GRANT EXECUTE ON PROCEDURE ', db, '.', routine_name, ' TO ', user_name, '@', host_name, ' WITH GRANT OPTION') AS grant_stmt
        FROM mysql.procs_priv
        WHERE user = user_name AND host = host_name;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET grant_statement = NULL;

    SET grants_result = '';

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO grant_statement;

        IF grant_statement IS NULL THEN
            LEAVE read_loop;
        END IF;

        SET grants_result = CONCAT(grants_result, grant_statement, '\n');
    END LOOP;

    CLOSE cur;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-26 20:14:33
