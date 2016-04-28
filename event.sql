-- MySQL dump 10.13  Distrib 5.7.11, for osx10.11 (x86_64)
--
-- Host: localhost    Database: event
-- ------------------------------------------------------
-- Server version	5.5.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `budget`
--

DROP TABLE IF EXISTS `budget`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `budget` (
  `id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`event_id`),
  KEY `fk_budget_event1_idx` (`event_id`),
  CONSTRAINT `fk_budget_event1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `budget`
--

LOCK TABLES `budget` WRITE;
/*!40000 ALTER TABLE `budget` DISABLE KEYS */;
INSERT INTO `budget` VALUES (1,1),(2,2),(3,3),(4,4),(5,5);
/*!40000 ALTER TABLE `budget` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `date_start` datetime NOT NULL,
  `date_end` datetime DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `setup_start` datetime DEFAULT NULL,
  `teardown_end` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,'newTest','2015-10-10 10:10:10','2015-10-10 10:10:10','newTest1','2015-10-10 10:10:10','2015-10-10 10:10:10'),(2,'testEvent2','2015-02-02 02:02:02',NULL,'testEvent2',NULL,NULL),(3,'testEvent3','2015-03-03 03:03:03',NULL,'testEvent3',NULL,NULL),(4,'testEvent','2015-01-01 01:01:01',NULL,'testEvent',NULL,NULL),(5,'testEvent','2015-01-01 01:01:01',NULL,'testEvent',NULL,NULL),(12,'testEvent','0000-00-00 00:00:00','2015-10-10 00:00:00','test','2015-10-10 00:00:00','2015-10-10 00:00:00'),(13,'test','0000-00-00 00:00:00','1010-10-10 00:00:00','test','1010-10-10 00:00:00','1010-10-10 00:00:00'),(14,'CreateTest','0000-00-00 00:00:00','1010-10-10 00:00:00','TestEvent','1010-10-10 00:00:00','1010-10-10 00:00:00'),(15,'CreateTest','0000-00-00 00:00:00','2015-10-10 00:00:00','TestEvent','2015-10-10 00:00:00','2015-10-10 00:00:00'),(16,'CreateTest','0000-00-00 00:00:00','2015-10-10 00:00:00','TestEvent','2015-10-10 00:00:00','2015-10-10 00:00:00'),(17,'test','0000-00-00 00:00:00','1010-10-10 00:00:00','test','1010-10-10 00:00:00','1010-10-10 00:00:00'),(18,'test','0000-00-00 00:00:00','1010-10-10 00:00:00','test','1010-10-10 00:00:00','1010-10-10 00:00:00'),(19,'test','0000-00-00 00:00:00','1010-10-10 00:00:00','test','1010-10-10 00:00:00','1010-10-10 00:00:00'),(20,'test','0000-00-00 00:00:00','1010-10-10 00:00:00','test','1010-10-10 00:00:00','1010-10-10 00:00:00'),(21,'test','0000-00-00 00:00:00','1010-10-10 00:00:00','test','1010-10-10 00:00:00','1010-10-10 00:00:00'),(22,'CreateTest','0000-00-00 00:00:00','2010-10-10 10:10:10','TestEvent','2010-10-10 10:10:10','2010-10-10 10:10:10'),(23,'CreateTest','0000-00-00 00:00:00','2010-10-10 10:10:10','TestEvent','2010-10-10 10:10:10','2010-10-10 10:10:10'),(24,'CreateTest','0000-00-00 00:00:00','2010-10-10 10:10:10','TestEvent','2010-10-10 10:10:10','2010-10-10 10:10:10'),(25,'CreateTest','0000-00-00 00:00:00','2010-10-10 10:10:10','TestEvent','2010-10-10 10:10:10','2010-10-10 10:10:10'),(26,'CreateTest','0000-00-00 00:00:00','2010-10-10 10:10:10','TestEvent','2010-10-10 10:10:10','2010-10-10 10:10:10'),(27,'CreateTest','0000-00-00 00:00:00','2010-10-10 10:10:10','TestEvent','2010-10-10 10:10:10','2010-10-10 10:10:10'),(28,'CreateTest','0000-00-00 00:00:00','2010-10-10 10:10:10','TestEvent','2010-10-10 10:10:10','2010-10-10 10:10:10'),(29,'CreateTest','0000-00-00 00:00:00','2010-10-10 10:10:10','TestEvent','2010-10-10 10:10:10','2010-10-10 10:10:10'),(30,'CreateTest','0000-00-00 00:00:00','1010-10-10 00:00:00','test','1010-10-10 00:00:00','1010-10-10 00:00:00'),(31,'newPath','0000-00-00 00:00:00','2010-10-10 10:10:10','newPath','2010-10-10 10:10:10','2010-10-10 10:10:10'),(32,'My New Event','0000-00-00 00:00:00','1010-10-10 00:00:00','My New Event','1010-10-10 00:00:00','1010-10-10 00:00:00'),(33,'This New Event','0000-00-00 00:00:00','2015-10-10 00:00:00','This New Event','2015-10-10 00:00:00','2015-10-10 00:00:00'),(34,'myNewEvent','2016-04-21 10:00:00','2016-04-21 10:00:00','','2016-04-21 10:00:00','2016-04-21 10:00:00'),(35,'myNewTestEvent','2016-04-28 10:54:07','2016-04-28 10:54:07','Fun','2016-04-28 10:54:07','2016-04-28 10:54:07');
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_for_user`
--

DROP TABLE IF EXISTS `event_for_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_for_user` (
  `assignedTo` varchar(45) NOT NULL,
  `event_id` int(11) NOT NULL,
  PRIMARY KEY (`event_id`,`assignedTo`),
  KEY `fk_event_for_user_user1_idx` (`assignedTo`),
  KEY `fk_event_for_user_event1_idx` (`event_id`),
  CONSTRAINT `fk_event_for_user_event1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_event_for_user_user1` FOREIGN KEY (`assignedTo`) REFERENCES `user` (`email`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_for_user`
--

LOCK TABLES `event_for_user` WRITE;
/*!40000 ALTER TABLE `event_for_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_for_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice`
--

DROP TABLE IF EXISTS `invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `invoice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `total` varchar(45) NOT NULL,
  `description` varchar(45) DEFAULT NULL,
  `isPaid?` tinyint(1) NOT NULL,
  `budget_id` int(11) NOT NULL,
  `vendor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_invoices_budget1_idx` (`budget_id`),
  KEY `fk_invoices_vendors1_idx` (`vendor_id`),
  CONSTRAINT `fk_invoices_budget1` FOREIGN KEY (`budget_id`) REFERENCES `budget` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_invoices_vendors1` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice`
--

LOCK TABLES `invoice` WRITE;
/*!40000 ALTER TABLE `invoice` DISABLE KEYS */;
INSERT INTO `invoice` VALUES (1,'54.61','test1',1,1,1),(2,'24.31','test2',0,1,3),(3,'52.54','test3',1,2,5),(4,'401.43','test4',1,3,4),(5,'4341.09','test5',1,4,2),(6,'54.23','test6',1,5,1),(7,'975.45','test7',0,2,2),(8,'5291.51','test8',0,3,3);
/*!40000 ALTER TABLE `invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task`
--

DROP TABLE IF EXISTS `task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `priority` int(11) DEFAULT NULL,
  `name` varchar(45) NOT NULL,
  `dateDue` datetime DEFAULT NULL,
  `status` varchar(1) NOT NULL,
  `assignedTo` varchar(45) NOT NULL,
  `event_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_task_user1_idx` (`assignedTo`),
  KEY `fk_task_event1_idx` (`event_id`),
  CONSTRAINT `fk_task_event1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_task_user1` FOREIGN KEY (`assignedTo`) REFERENCES `user` (`email`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task`
--

LOCK TABLES `task` WRITE;
/*!40000 ALTER TABLE `task` DISABLE KEYS */;
INSERT INTO `task` VALUES (1,1,'newTask1','2010-01-01 01:01:01','1','admin@admin.com',1),(2,3,'testTask','2010-10-10 10:10:10','2','admin@admin.com',1),(3,2,'TestTask','2010-10-10 10:10:10','4','admin@admin.com',1),(4,1,'testTask','2010-10-10 10:10:10','1','admin@admin.com',1),(5,1,'Lighting Job','2010-10-10 10:10:10','1','admin@admin.com',1),(6,1,'Sound Job','2010-10-10 10:10:10','0','admin@admin.com',1),(7,1,'myNewTask','2016-04-28 10:49:20','1','admin@admin.com',1);
/*!40000 ALTER TABLE `task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticket` (
  `id` int(11) NOT NULL,
  `price` varchar(45) NOT NULL,
  `section` varchar(45) DEFAULT NULL,
  `seat_num` varchar(45) DEFAULT NULL,
  `isSold` tinyint(1) NOT NULL,
  `event_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_ticket_event1_idx` (`event_id`),
  CONSTRAINT `fk_ticket_event1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES (1,'5.00','1','1',1,1),(2,'54.64','1','2',0,1),(3,'76.45','1','3',0,1),(4,'54.43','1','4',1,1),(5,'60.00','2','1',1,1),(6,'60.00','2','2',1,1),(7,'60.00','2','3',0,1),(8,'60.00','2','4',1,1),(9,'79.94','1','1',0,2),(10,'65.76','1','1',0,3),(11,'65.65','1','1',0,4),(12,'65.90','1','1',0,5),(13,'34.65','1','2',0,5);
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `isAdmin` tinyint(1) NOT NULL DEFAULT '0',
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `isAuthenticated` tinyint(1) NOT NULL,
  `isActive` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','admin@admin.com','admin',1,1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor`
--

DROP TABLE IF EXISTS `vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vendor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor`
--

LOCK TABLES `vendor` WRITE;
/*!40000 ALTER TABLE `vendor` DISABLE KEYS */;
INSERT INTO `vendor` VALUES (1,'testVendor','111-111-1111','123 Easy St, Upland, IN 46989','test@example.com'),(2,'testVendor2','222-222-2222','130 S Forest Dr, Kokomo, IN 46901','test2@exmaple.com'),(3,'testVendor3','333-333-3333','1715 W Sycamore, Kokomo, IN 46901','test3@example.com'),(4,'testVendor4','444-444-4444','236 W Reade Ave, Upland, IN 46989','test4@exmple.com'),(5,'testVendor5','555-555-5555','220 W Walnut St, Kokomo, IN 46901','test5@example.org');
/*!40000 ALTER TABLE `vendor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-28 11:20:49
