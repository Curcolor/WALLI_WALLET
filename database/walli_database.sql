-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: walli_database
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) NOT NULL,
  `documento_identidad` int NOT NULL,
  `correo_electronico` varchar(100) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'jairo','arcia',1043311427,'jairo@gmail.com','2006-03-12','2024-11-24 14:13:50'),(2,'daniela','villa',1043312427,'daniela-villasb@gmail.com','2003-04-23','2024-11-24 14:54:07'),(3,'jorge','solano',1141312427,'jorge-solano@gmail.com','2001-12-01','2024-11-24 15:03:47'),(6,'Sara','Sierra',1043311421,'SaraSierra@gmail.com','2001-12-22','2024-11-25 10:02:05');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cuentas`
--

DROP TABLE IF EXISTS `cuentas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuentas` (
  `id_cuenta` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `saldo_actual` decimal(10,2) NOT NULL DEFAULT '0.00',
  `tipo_cuenta` enum('corriente','cats','ahorro') NOT NULL,
  `fecha_apertura` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `clave_ingreso` varchar(4) NOT NULL,
  `numero_telefono_ingreso` varchar(10) NOT NULL,
  `estado` varchar(20) DEFAULT 'activa',
  PRIMARY KEY (`id_cuenta`),
  UNIQUE KEY `cuentas_id_cliente_unique` (`id_cliente`),
  CONSTRAINT `cuentas_id_cliente_foreign` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuentas`
--

LOCK TABLES `cuentas` WRITE;
/*!40000 ALTER TABLE `cuentas` DISABLE KEYS */;
INSERT INTO `cuentas` VALUES (1,1,10000.00,'ahorro','2024-11-24 14:13:50','1234','3103778136','activa'),(2,2,0.00,'ahorro','2024-11-24 14:54:07','1234','3123171136','activa'),(3,3,0.00,'ahorro','2024-11-24 15:03:47','1234','3024516690','activa'),(4,6,0.00,'ahorro','2024-11-25 10:02:05','5678','3024516691','activa');
/*!40000 ALTER TABLE `cuentas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deposito`
--

DROP TABLE IF EXISTS `deposito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deposito` (
  `id_deposito` int NOT NULL AUTO_INCREMENT,
  `id_cuenta` int NOT NULL,
  `monto` decimal(8,2) NOT NULL,
  `fecha_deposito` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `canal` varchar(50) NOT NULL,
  `estado` enum('completado','en proceso','rechazado') NOT NULL,
  PRIMARY KEY (`id_deposito`),
  KEY `deposito_id_cuenta_index` (`id_cuenta`),
  CONSTRAINT `deposito_id_cuenta_foreign` FOREIGN KEY (`id_cuenta`) REFERENCES `cuentas` (`id_cuenta`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deposito`
--

LOCK TABLES `deposito` WRITE;
/*!40000 ALTER TABLE `deposito` DISABLE KEYS */;
INSERT INTO `deposito` VALUES (1,1,10000.00,'2024-11-25 10:12:48','web','completado');
/*!40000 ALTER TABLE `deposito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagosservicios`
--

DROP TABLE IF EXISTS `pagosservicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagosservicios` (
  `id_pago` int NOT NULL AUTO_INCREMENT,
  `id_cuenta` int NOT NULL,
  `id_servicio` int NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `fecha_pago` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('completado','en proceso','rechazado') NOT NULL,
  PRIMARY KEY (`id_pago`),
  KEY `pagosservicios_id_cuenta_index` (`id_cuenta`),
  KEY `pagosservicios_id_servicio_index` (`id_servicio`),
  CONSTRAINT `pagosservicios_id_cuenta_foreign` FOREIGN KEY (`id_cuenta`) REFERENCES `cuentas` (`id_cuenta`),
  CONSTRAINT `pagosservicios_id_servicio_foreign` FOREIGN KEY (`id_servicio`) REFERENCES `servicios` (`id_servicio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagosservicios`
--

LOCK TABLES `pagosservicios` WRITE;
/*!40000 ALTER TABLE `pagosservicios` DISABLE KEYS */;
/*!40000 ALTER TABLE `pagosservicios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `retiros`
--

DROP TABLE IF EXISTS `retiros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `retiros` (
  `id_retiro` int NOT NULL AUTO_INCREMENT,
  `id_cuenta` int NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `fecha_retiro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `canal_retiro` varchar(50) NOT NULL,
  `codigo_retiro` varchar(50) NOT NULL,
  `estado` enum('completado','en proceso','rechazado') NOT NULL,
  PRIMARY KEY (`id_retiro`),
  KEY `retiros_id_cuenta_index` (`id_cuenta`),
  CONSTRAINT `retiros_id_cuenta_foreign` FOREIGN KEY (`id_cuenta`) REFERENCES `cuentas` (`id_cuenta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retiros`
--

LOCK TABLES `retiros` WRITE;
/*!40000 ALTER TABLE `retiros` DISABLE KEYS */;
/*!40000 ALTER TABLE `retiros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicios`
--

DROP TABLE IF EXISTS `servicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicios` (
  `id_servicio` int NOT NULL AUTO_INCREMENT,
  `nombre_servicio` varchar(255) NOT NULL,
  `categoria` enum('Agua','Luz','Gas','Servicio móvil') NOT NULL,
  `descripcion` text NOT NULL,
  PRIMARY KEY (`id_servicio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicios`
--

LOCK TABLES `servicios` WRITE;
/*!40000 ALTER TABLE `servicios` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaccion`
--

DROP TABLE IF EXISTS `transaccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaccion` (
  `id_transaccion` int unsigned NOT NULL AUTO_INCREMENT,
  `id_cuenta_origen` int NOT NULL,
  `id_cuenta_envio` int NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `fecha_transaccion` timestamp NOT NULL,
  `canal` varchar(255) NOT NULL,
  `estado` enum('completado','en proceso','rechazado') NOT NULL,
  PRIMARY KEY (`id_transaccion`),
  KEY `transaccion_id_cuenta_origen_index` (`id_cuenta_origen`),
  KEY `transaccion_id_cuenta_envio_index` (`id_cuenta_envio`),
  CONSTRAINT `transaccion_id_cuenta_envio_foreign` FOREIGN KEY (`id_cuenta_envio`) REFERENCES `cuentas` (`id_cuenta`),
  CONSTRAINT `transaccion_id_cuenta_origen_foreign` FOREIGN KEY (`id_cuenta_origen`) REFERENCES `cuentas` (`id_cuenta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaccion`
--

LOCK TABLES `transaccion` WRITE;
/*!40000 ALTER TABLE `transaccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `transaccion` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-25  5:23:52
