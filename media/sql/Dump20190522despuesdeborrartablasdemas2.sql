-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mpod
-- ------------------------------------------------------
-- Server version	5.6.39-log

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Administrators'),(3,'Frontend user'),(4,'Publishing'),(2,'Users');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_425ae3c4` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_5886d21f` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,1,16),(17,1,17),(18,1,18);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `message` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_1bb8f392` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '0',
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (0,'Anyone','','','','pbkdf2_sha256$10000$7BfA1wK9wSuN$/HLFLzy/PHVyMZgju80XJ/4KFO59hwSgnH01omJSNrc=',0,0,0,'2017-08-26 21:56:12','2017-08-26 21:56:12'),(1,'admin','','','chvo21181@hotmail.com','pbkdf2_sha256$10000$tcLcLKt6ldqV$Sq9egkAk6Fvdgpp2VYhwOvZiBNnBKixtk+DaGgSqk5I=',1,1,1,'2019-05-17 23:31:37','2017-08-14 00:20:38'),(2,'mpod_admin','','','mpod@cimav.edu.mx','pbkdf2_sha256$10000$xDwyiUKMWUbC$zXaxSh9+9G135u3MHzDVdR5eylf6QzLztyqYo/25rhw=',1,1,1,'2017-08-14 02:42:56','2017-08-14 00:21:39'),(5,'d','Adriana ','Ramos','chvo21181@hotmail.com','pbkdf2_sha256$10000$boIbU7sG6UjI$R+Y5EQ5zbfNcE3V6njz3DaRdwVjRE1OG/4WJNnwDgrU=',0,1,0,'2019-05-19 07:49:27','2017-08-14 00:27:42'),(14,'editor','','','','pbkdf2_sha256$10000$TnFQxR82MVrt$gjWbCIZDfluuYsoSnmhb+e0gCaPdywBZRYDRIfItDjY=',1,1,0,'2018-10-16 02:26:08','2018-10-03 15:36:51'),(15,'publisher','Luis','Fuentes-Cobas','luis.fuentes@cimav.edu.mx','pbkdf2_sha256$10000$E0Yp6pl33vDC$TvbPUTbJbmy8aj9BrPtHLovaybHg/aB8fI33UbFmR14=',1,1,1,'2019-03-21 17:18:22','2018-10-03 15:37:09'),(16,'Adry69','Adriana ','Ramos Palomino','adriana.ramosp@gmail.com','pbkdf2_sha256$10000$5DAwnphu8maE$3zP+DSyw1rJRjeAE+gSamNLkMTNo+rQEBBeE/rJ1C0w=',0,1,0,'2019-04-26 21:20:29','2019-02-01 19:35:59'),(41,'g','g','g','jorgta@gmail.com','pbkdf2_sha256$10000$yONxq8tjRJ8B$anugD3TKSuehK+gV7vTnYPOn2kTI9loC6VUfD1X8yoQ=',0,1,0,'2019-03-24 22:10:38','2019-03-24 22:10:16'),(42,'Manf','Miguel Angel','Neri','miguel.neri@cimav.edu.mx','pbkdf2_sha256$10000$V224Wy8J3wov$sbDgAsFhULtQ9x4gPg6B4uttim7gN041/gF3r/f2Yjw=',0,1,0,'2019-04-26 20:47:29','2019-04-26 20:46:53');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_403f60f` (`user_id`),
  KEY `auth_user_groups_425ae3c4` (`group_id`),
  CONSTRAINT `group_id_refs_id_f116770` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_7ceef80f` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (8,0,3),(6,1,1),(2,2,1),(14,14,4),(16,15,1);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_403f60f` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_dfbab7d` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `captcha_captchastore`
--

DROP TABLE IF EXISTS `captcha_captchastore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `captcha_captchastore` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `challenge` varchar(32) NOT NULL,
  `response` varchar(32) NOT NULL,
  `hashkey` varchar(40) NOT NULL,
  `expiration` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hashkey` (`hashkey`)
) ENGINE=MyISAM AUTO_INCREMENT=60 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `captcha_captchastore`
--

LOCK TABLES `captcha_captchastore` WRITE;
/*!40000 ALTER TABLE `captcha_captchastore` DISABLE KEYS */;
INSERT INTO `captcha_captchastore` VALUES (1,'ANQA','anqa','30c22faec9b765aaea6feca97915c1cfcdfec9ab','2014-06-25 04:10:56'),(2,'VCCT','vcct','3d3d3d0a0c8e352a7e7533db47dcc9eadf98ad27','2014-06-25 15:31:04'),(3,'VJDS','vjds','1b2df9c16df66df0c72a5a1ff67084e1f8f750ef','2014-06-25 23:18:11'),(4,'JVUX','jvux','1d92f7a1c13af763aa644e9e56005bba7e5081a2','2014-06-25 23:18:50'),(5,'JMNE','jmne','d0d1d245daa47337acb9ace8cfb8c45322594444','2014-06-25 23:20:21'),(6,'TNCG','tncg','0690052dd37362f5c9e9bb2586009c1deed8a0a2','2014-06-25 23:43:41'),(7,'PCMD','pcmd','585098d899c13936ff13f857cc60fd893230892e','2014-06-27 11:26:36'),(8,'ENIF','enif','d7a57ae75b5245a084d508a77a13d9e036b0a79a','2014-07-01 02:14:01'),(9,'XDMC','xdmc','2967b943d46b818aa7f993749958bc9b4b29766e','2014-07-01 11:08:32'),(10,'WINA','wina','98b3146ef214e954d8b1865d1f61e821d093813b','2014-07-03 07:30:01'),(11,'IZHL','izhl','e3e738e972129108cae11069c288e25ea4d69b6f','2014-07-04 02:27:04'),(12,'YBPF','ybpf','7fa8be9f4e9251c6e719826615326f1a9f0b9ce5','2014-07-05 11:04:13'),(13,'YNMC','ynmc','62295fcd97f3cff270f9da4a5dec31d335a8bfe9','2014-07-10 12:58:43'),(14,'MXQF','mxqf','cb301971ec18f933ef5fe18a9f3f1feb6fbefc7e','2014-07-10 16:40:52'),(15,'JZSH','jzsh','09a3aac77d43ce88668c873392dc0396676777df','2014-07-12 00:35:02'),(16,'LRRZ','lrrz','5de21a24c09a2281515e340c696779f304639f90','2014-07-12 05:48:17'),(17,'SMCU','smcu','1c5de468a09bb3a77d07ddf7d193053c4cf8893d','2014-07-12 15:24:06'),(18,'REHR','rehr','8bdeb7c9a5f03be11228364517290868486b0954','2014-07-16 15:10:22'),(19,'XIFT','xift','7b3cb7f09893d8446710b5bd0521e9f88d21cfec','2014-07-17 14:30:18'),(20,'DUSW','dusw','9ef8e24821ed53ec834f68dc58366ece99ec64b6','2014-07-18 00:34:46'),(21,'DODX','dodx','0bbfdf7e5c6e270b831ca180f5e78d537206b8c7','2014-07-18 21:21:14'),(22,'LGDH','lgdh','6c25f58471303f6e58936f8166ac1e0e9f3bf8bf','2014-07-19 01:45:13'),(23,'UEGI','uegi','d7b09a9470ebaacb62d6e22ee267d2b25c2ca4bf','2014-07-19 10:33:11'),(24,'VZYP','vzyp','4026a4a84a00b604ac17a6517aa355e550df3739','2014-07-21 17:16:44'),(25,'WBPM','wbpm','e3e5255ad0195c302f0fb4045bdfc23a6476aa19','2014-07-22 09:01:14'),(26,'YHXI','yhxi','831aa534d6849740d1fc8f05276825fc680cc239','2014-07-23 20:25:07'),(27,'LZUZ','lzuz','38e69693ee45a96a5d392075d4f1212c4bd31a02','2014-07-27 19:27:02'),(28,'IZOZ','izoz','8b95c4c640268e6d899631a9a5a7900f81bd958b','2014-08-01 16:24:28'),(29,'HSSW','hssw','936e8f6603ac3ee3e3c92d92597e40970aacfc0f','2014-08-01 16:24:30'),(30,'UPIH','upih','a29993107ba3b6f6b6da7fbd1d5789ef937d4148','2014-08-01 23:28:33'),(31,'UJDX','ujdx','233be6a69135fd20f2ab3e90802bbac2d2e455e6','2014-08-03 12:38:01'),(32,'DDXH','ddxh','b18c9b452457317284b6d9929e25acbb28104cf9','2014-08-03 14:11:46'),(33,'VBUK','vbuk','a5437b509b72f8a9b8728ee03261d5bdc814bcdb','2014-08-04 21:52:03'),(34,'MSBH','msbh','8218745c6863bfa6a3719f002c07970d780c094c','2014-08-12 03:46:33'),(35,'EFJZ','efjz','34fb9f6eeaabd6f6a7b2f2396bd11797e57ea97d','2014-08-23 05:01:40'),(36,'OPSF','opsf','e0fb2d9d234ee49fc5bb71f3a698d7d3f714c3ef','2014-08-28 22:51:36'),(37,'TGLU','tglu','a2ceafa4a1dce1ed8c0d837d2e7ddb252e7da021','2014-08-28 22:51:38'),(38,'SQMD','sqmd','b4b6d80b51cf98580a8bbcf65e2fc3a61c9f7a2b','2014-08-29 03:13:06'),(39,'EWGI','ewgi','316a167ee5c4084471c1f78e027ac60dfb46e951','2014-08-29 11:08:16'),(40,'KPRC','kprc','2a284c08094d7010b5113fb093c58277b9fcb21b','2014-08-29 12:29:42'),(41,'AVJI','avji','b3097381a0e4b52c6d20675d41ff47731a4489d3','2014-08-31 08:28:20'),(42,'ZFPA','zfpa','01748950aa4bb0c41cb5e8ca325ba67edc52a3a6','2014-09-02 03:17:16'),(43,'CLXQ','clxq','830c67c4ca6581a140e49cd78bf778b77c220312','2014-09-06 02:44:24'),(44,'KCEC','kcec','aa7205dec8642f2a6805b9512f3d81ac31a2c057','2014-09-07 15:10:05'),(45,'RWLN','rwln','443da5ff13f49c325e02b8627256f1b0894f85e3','2014-09-11 14:56:41'),(46,'PMNO','pmno','c025a051b057a1479329d27d1486080920249b01','2014-09-11 17:04:50'),(47,'QQGQ','qqgq','35c3fdaf8e26c9e0c300ff31a96c35da6dbb92ca','2014-09-13 15:13:17'),(48,'WSZR','wszr','423bff67b0f24fd134b232597c33a393962db657','2014-09-15 05:21:05'),(49,'VBOK','vbok','41bc81e994b84fa556734a7e10e4eb36204b8d2e','2014-09-17 15:20:36'),(50,'WFHE','wfhe','30df3bdb2d5bc6814e8f5ae2d44cbeb60483a852','2014-09-20 09:12:33'),(51,'JTUR','jtur','202fcfa43a8cbbfa6b983211e16fee4710373471','2014-09-21 06:10:42'),(52,'MWZN','mwzn','e6619d567baae163b9c8061615d5a20398cd89df','2014-09-22 10:19:14'),(53,'STHJ','sthj','2658036ea717487dc1bfbd903a9c3c5ea64989c5','2014-09-28 23:10:04'),(54,'PJWB','pjwb','da8747569b058ada1da81b378643c20f79f12f0c','2014-10-01 22:33:42'),(55,'XJTI','xjti','2a9f163c7feec9b42f98c41b790010e7efe4211c','2014-10-03 01:13:26'),(56,'LMRS','lmrs','687c06e06c2c3bdb30befd1a28f9291e1396fdbf','2014-10-03 03:27:47'),(57,'PZGP','pzgp','43bc563477f4c803722b9b43a2de60441a8927bb','2014-10-03 10:58:47'),(58,'OCHR','ochr','9e99e3d29aad375a7acc3a3f7b1ab244749d65ff','2014-10-03 15:12:24'),(59,'TFYJ','tfyj','a9354bac7f88808f1543a321691665df1146ead3','2014-10-10 01:40:50');
/*!40000 ALTER TABLE `captcha_captchastore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalog_axis`
--

DROP TABLE IF EXISTS `catalog_axis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalog_axis` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(511) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalog_axis`
--

LOCK TABLES `catalog_axis` WRITE;
/*!40000 ALTER TABLE `catalog_axis` DISABLE KEYS */;
INSERT INTO `catalog_axis` VALUES (4,'None',' '),(1,'x1',' '),(2,'x2',' '),(3,'x3',' ');
/*!40000 ALTER TABLE `catalog_axis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalog_chemical`
--

DROP TABLE IF EXISTS `catalog_chemical`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalog_chemical` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `definition` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalog_chemical`
--

LOCK TABLES `catalog_chemical` WRITE;
/*!40000 ALTER TABLE `catalog_chemical` DISABLE KEYS */;
INSERT INTO `catalog_chemical` VALUES (1,'_chemical_formula','chemical formula',NULL),(2,'_chemical_formula_sum','chemical formula sum',NULL);
/*!40000 ALTER TABLE `catalog_chemical` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalog_crystal_system`
--

DROP TABLE IF EXISTS `catalog_crystal_system`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalog_crystal_system` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(511) NOT NULL,
  `catalogproperty_id` int(11) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalog_crystal_system`
--

LOCK TABLES `catalog_crystal_system` WRITE;
/*!40000 ALTER TABLE `catalog_crystal_system` DISABLE KEYS */;
INSERT INTO `catalog_crystal_system` VALUES (1,'tc','Triclinic',1,1),(2,'m','Monoclinic',1,1),(3,'o','Orthorhombic',1,1),(4,'c','Cubic',1,1),(5,'te','Tetragonal',1,1),(6,'tg','Trigonal -  Rombohedric',1,1),(7,'iso','Isotropic',1,1),(8,'h','Hexagonal',1,1),(9,'tc','Triclinic',2,1),(10,'m','Monoclinic',2,1),(11,'o','Orthorhombic',2,1),(12,'c','Cubic',2,1),(13,'te','Tetragonal',2,1),(14,'tg','Trigonal -  Rombohedric',2,1),(15,'h','Hexagonal',2,1),(16,'tc','Triclinic',3,1),(17,'m','Monoclinic',3,1),(18,'o','Orthorhombic',3,1),(19,'c','Cubic',3,1),(20,'u','Uniaxial',3,1),(25,'tc','Triclinico Test',8,1),(26,'te','Tetragonal',3,1);
/*!40000 ALTER TABLE `catalog_crystal_system` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalog_point_group`
--

DROP TABLE IF EXISTS `catalog_point_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalog_point_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `description` varchar(511) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=91 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalog_point_group`
--

LOCK TABLES `catalog_point_group` WRITE;
/*!40000 ALTER TABLE `catalog_point_group` DISABLE KEYS */;
INSERT INTO `catalog_point_group` VALUES (1,'4',''),(2,'-4',''),(3,'4/m',''),(4,'422',''),(5,'4mm',''),(6,'-42m',''),(7,'4/mmm',''),(8,'3',''),(9,'-3',''),(10,'32',''),(11,'3m',''),(12,'-3m',''),(13,'2',''),(14,'m',''),(15,'2/m',''),(16,'222',''),(17,'2mm',''),(18,'mmm',''),(19,'23',''),(20,'m3',''),(21,'432',''),(22,'-43m',''),(23,'m3m',''),(24,'6',''),(25,'-6',''),(26,'6/m',''),(27,'6mm',''),(28,'622',''),(29,'-6m2',''),(30,'6/mmm',''),(38,'infinfm',NULL),(37,'infinf',NULL),(45,'None',NULL),(35,'1',NULL),(36,'-1',NULL),(40,'inf','inf'),(41,'infm','infm'),(42,'inf/m','inf/m'),(43,'inf2','inf2'),(44,'inf/mm','inf/mm'),(46,'-1*','-1*'),(47,'m*','m*'),(48,'4*/m*','4*/m*'),(49,'2/m*','2/m*'),(50,'2*','2*'),(51,'2*/m','2*/m'),(52,'m*m*2','m*m*2'),(53,'m*m*m*','m*m*m*'),(54,'22*2*','22*2*'),(55,'m*m2*','m*m2*'),(56,'m*mm','m*mm'),(57,'-3*','-3*'),(58,'-4*','-4*'),(59,'4/m*','4/m*'),(60,'-6*','-6*'),(61,'6/m*','6/m*'),(62,'infm*','infm*'),(63,'4*','4*'),(64,'3m*','3m*'),(65,'-3*m*','-3*m*'),(66,'4m*m*','4m*m*'),(67,'4/m*m*m*','4/m*m*m*'),(68,'6m*m*','6m*m*'),(69,'-6*m*2','-6*m*2'),(70,'4*22','4*22'),(71,'4*mm*','4*mm*'),(72,'-42*m*','-42*m*'),(73,'4*/m*mm*','4*/m*mm*'),(74,'32*','32*'),(75,'-3m*','-3m*'),(76,'42*2*','42*2*'),(77,'4/m*mm','4/m*mm'),(78,'62*2*','62*2*'),(79,'-6*m2*','-6*m2*'),(80,'6/m*mm','6/m*mm'),(81,'inf2*','inf2*'),(82,'inf/m*m','inf/m*m'),(83,'m*3','m*3'),(84,'-4*3m*','-4*3m*'),(85,'m*3m*','m*3m*'),(86,'-4*2m*','-4*2m*'),(87,'6/m*m*m*','6/m*m*m*'),(88,'inf/m*m*','inf/m*m*'),(89,'-3*m','-3*m'),(90,'-4*2*m','-4*2*m');
/*!40000 ALTER TABLE `catalog_point_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalog_property_detail`
--

DROP TABLE IF EXISTS `catalog_property_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalog_property_detail` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(511) DEFAULT NULL,
  `type_id` int(11) NOT NULL,
  `crystalsystem_id` int(11) NOT NULL,
  `catalogaxis_id` int(11) DEFAULT NULL,
  `catalogpointgroup_id` int(11) DEFAULT NULL,
  `pointgroupnames_id` int(11) DEFAULT NULL,
  `dataproperty_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3261 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalog_property_detail`
--

LOCK TABLES `catalog_property_detail` WRITE;
/*!40000 ALTER TABLE `catalog_property_detail` DISABLE KEYS */;
INSERT INTO `catalog_property_detail` VALUES (865,'c11','',1,1,4,45,20,10),(864,'c12','',1,1,4,45,20,10),(863,'c13','',1,1,4,45,20,10),(862,'c14','',1,1,4,45,20,10),(861,'c15','',1,1,4,45,20,10),(860,'c16','',1,1,4,45,20,10),(859,'c22','',1,1,4,45,20,10),(858,'c23','',1,1,4,45,20,10),(857,'c24','',1,1,4,45,20,10),(856,'c25','',1,1,4,45,20,10),(855,'c26','',1,1,4,45,20,10),(854,'c33','',1,1,4,45,20,10),(853,'c34','',1,1,4,45,20,10),(852,'c35','',1,1,4,45,20,10),(851,'c36','',1,1,4,45,20,10),(850,'c44','',1,1,4,45,20,10),(849,'c45','',1,1,4,45,20,10),(848,'c46','',1,1,4,45,20,10),(847,'c55','',1,1,4,45,20,10),(846,'c56','',1,1,4,45,20,10),(845,'c66','',1,1,4,45,20,10),(844,'s11','',2,1,4,45,20,7),(843,'s12','',2,1,4,45,20,7),(842,'s13','',2,1,4,45,20,7),(841,'s14','',2,1,4,45,20,7),(840,'s15','',2,1,4,45,20,7),(839,'s16','',2,1,4,45,20,7),(838,'s22','',2,1,4,45,20,7),(837,'s23','',2,1,4,45,20,7),(836,'s24','',2,1,4,45,20,7),(835,'s25','',2,1,4,45,20,7),(834,'s26','',2,1,4,45,20,7),(833,'s33','',2,1,4,45,20,7),(832,'s34','',2,1,4,45,20,7),(831,'s35','',2,1,4,45,20,7),(830,'s36','',2,1,4,45,20,7),(829,'s44','',2,1,4,45,20,7),(828,'s45','',2,1,4,45,20,7),(827,'s46','',2,1,4,45,20,7),(826,'s55','',2,1,4,45,20,7),(825,'s56','',2,1,4,45,20,7),(824,'s66','',2,1,4,45,20,7),(866,'s66','',2,2,2,45,19,7),(867,'s55','',2,2,2,45,19,7),(868,'s46','',2,2,2,45,19,7),(869,'s44','',2,2,2,45,19,7),(870,'s35','',2,2,2,45,19,7),(871,'s33','',2,2,2,45,19,7),(872,'s25','',2,2,2,45,19,7),(873,'s23','',2,2,2,45,19,7),(874,'s22','',2,2,2,45,19,7),(875,'s15','',2,2,2,45,19,7),(876,'s13','',2,2,2,45,19,7),(877,'s12','',2,2,2,45,19,7),(878,'s11','',2,2,2,45,19,7),(879,'s66','',2,2,3,45,19,7),(880,'s55','',2,2,3,45,19,7),(881,'s45','',2,2,3,45,19,7),(882,'s44','',2,2,3,45,19,7),(883,'s36','',2,2,3,45,19,7),(884,'s33','',2,2,3,45,19,7),(885,'s26','',2,2,3,45,19,7),(886,'s23','',2,2,3,45,19,7),(887,'s22','',2,2,3,45,19,7),(888,'s16','',2,2,3,45,19,7),(889,'s13','',2,2,3,45,19,7),(890,'s12','',2,2,3,45,19,7),(891,'s11','',2,2,3,45,19,7),(892,'s66','',2,3,4,45,18,7),(893,'s55','',2,3,4,45,18,7),(894,'s44','',2,3,4,45,18,7),(895,'s33','',2,3,4,45,18,7),(896,'s23','',2,3,4,45,18,7),(897,'s22','',2,3,4,45,18,7),(898,'s13','',2,3,4,45,18,7),(899,'s12','',2,3,4,45,18,7),(900,'s11','',2,3,4,45,18,7),(901,'s44','',2,4,4,45,16,7),(902,'s12','',2,4,4,45,16,7),(903,'s11','',2,4,4,45,16,7),(904,'s66','',2,5,4,45,2,7),(905,'s44','',2,5,4,45,2,7),(906,'s33','',2,5,4,45,2,7),(907,'s16','',2,5,4,45,2,7),(908,'s13','',2,5,4,45,2,7),(909,'s12','',2,5,4,45,2,7),(910,'s11','',2,5,4,45,2,7),(911,'s66','',2,5,4,45,1,7),(912,'s44','',2,5,4,45,1,7),(913,'s33','',2,5,4,45,1,7),(914,'s13','',2,5,4,45,1,7),(915,'s12','',2,5,4,45,1,7),(916,'s11','',2,5,4,45,1,7),(917,'s44','',2,6,4,45,4,7),(918,'s33','',2,6,4,45,4,7),(919,'s25','',2,6,4,45,4,7),(920,'s14','',2,6,4,45,4,7),(921,'s13','',2,6,4,45,4,7),(922,'s12','',2,6,4,45,4,7),(923,'s11','',2,6,4,45,4,7),(924,'s44','',2,6,4,45,3,7),(925,'s33','',2,6,4,45,3,7),(926,'s14','',2,6,4,45,3,7),(927,'s13','',2,6,4,45,3,7),(928,'s12','',2,6,4,45,3,7),(929,'s11','',2,6,4,45,3,7),(930,'s12','',2,7,4,45,15,7),(931,'s11','',2,7,4,45,15,7),(932,'s66E','',2,1,4,45,20,9),(933,'s56E','',2,1,4,45,20,9),(934,'s55E','',2,1,4,45,20,9),(935,'s46E','',2,1,4,45,20,9),(936,'s45E','',2,1,4,45,20,9),(937,'s44E','',2,1,4,45,20,9),(938,'s36E','',2,1,4,45,20,9),(939,'s35E','',2,1,4,45,20,9),(940,'s34E','',2,1,4,45,20,9),(941,'s33E','',2,1,4,45,20,9),(942,'s26E','',2,1,4,45,20,9),(943,'s25E','',2,1,4,45,20,9),(944,'s24E','',2,1,4,45,20,9),(945,'s23E','',2,1,4,45,20,9),(946,'s22E','',2,1,4,45,20,9),(947,'s16E','',2,1,4,45,20,9),(948,'s15E','',2,1,4,45,20,9),(949,'s14E','',2,1,4,45,20,9),(950,'s13E','',2,1,4,45,20,9),(951,'s12E','',2,1,4,45,20,9),(952,'s11E','',2,1,4,45,20,9),(953,'s66E','',2,2,2,45,19,9),(954,'s55E','',2,2,2,45,19,9),(955,'s46E','',2,2,2,45,19,9),(956,'s44E','',2,2,2,45,19,9),(957,'s35E','',2,2,2,45,19,9),(958,'s33E','',2,2,2,45,19,9),(959,'s25E','',2,2,2,45,19,9),(960,'s23E','',2,2,2,45,19,9),(961,'s22E','',2,2,2,45,19,9),(962,'s15E','',2,2,2,45,19,9),(963,'s13E','',2,2,2,45,19,9),(964,'s12E','',2,2,2,45,19,9),(965,'s11E','',2,2,2,45,19,9),(966,'s66E','',2,2,3,45,19,9),(967,'s55E','',2,2,3,45,19,9),(968,'s45E','',2,2,3,45,19,9),(969,'s44E','',2,2,3,45,19,9),(970,'s36E','',2,2,3,45,19,9),(971,'s33E','',2,2,3,45,19,9),(972,'s26E','',2,2,3,45,19,9),(973,'s23E','',2,2,3,45,19,9),(974,'s22E','',2,2,3,45,19,9),(975,'s16E','',2,2,3,45,19,9),(976,'s13E','',2,2,3,45,19,9),(977,'s12E','',2,2,3,45,19,9),(978,'s11E','',2,2,3,45,19,9),(979,'s66E','',2,3,4,45,18,9),(980,'s55E','',2,3,4,45,18,9),(981,'s44E','',2,3,4,45,18,9),(982,'s33E','',2,3,4,45,18,9),(983,'s23E','',2,3,4,45,18,9),(984,'s22E','',2,3,4,45,18,9),(985,'s13E','',2,3,4,45,18,9),(986,'s12E','',2,3,4,45,18,9),(987,'s11E','',2,3,4,45,18,9),(988,'s44E','',2,4,4,45,16,9),(989,'s12E','',2,4,4,45,16,9),(990,'s11E','',2,4,4,45,16,9),(991,'s66E','',2,5,4,45,2,9),(992,'s44E','',2,5,4,45,2,9),(993,'s33E','',2,5,4,45,2,9),(994,'s16E','',2,5,4,45,2,9),(995,'s13E','',2,5,4,45,2,9),(996,'s12E','',2,5,4,45,2,9),(997,'s11E','',2,5,4,45,2,9),(998,'s66E','',2,5,4,45,1,9),(999,'s44E','',2,5,4,45,1,9),(1000,'s33E','',2,5,4,45,1,9),(1001,'s13E','',2,5,4,45,1,9),(1002,'s12E','',2,5,4,45,1,9),(1003,'s11E','',2,5,4,45,1,9),(1004,'s44E','',2,6,4,45,4,9),(1005,'s33E','',2,6,4,45,4,9),(1006,'s25E','',2,6,4,45,4,9),(1007,'s14E','',2,6,4,45,4,9),(1008,'s13E','',2,6,4,45,4,9),(1009,'s12E','',2,6,4,45,4,9),(1010,'s11E','',2,6,4,45,4,9),(1011,'s44E','',2,6,4,45,3,9),(1012,'s33E','',2,6,4,45,3,9),(1013,'s14E','',2,6,4,45,3,9),(1014,'s13E','',2,6,4,45,3,9),(1015,'s12E','',2,6,4,45,3,9),(1016,'s11E','',2,6,4,45,3,9),(1017,'s12E','',2,7,4,45,15,9),(1018,'s11E','',2,7,4,45,15,9),(1019,'s44E','',2,8,4,45,17,9),(1020,'s33E','',2,8,4,45,17,9),(1021,'s13E','',2,8,4,45,17,9),(1022,'s12E','',2,8,4,45,17,9),(1023,'s11E','',2,8,4,45,17,9),(1024,'s66D','',2,1,4,45,20,8),(1025,'s56D','',2,1,4,45,20,8),(1026,'s55D','',2,1,4,45,20,8),(1027,'s46D','',2,1,4,45,20,8),(1028,'s45D','',2,1,4,45,20,8),(1029,'s44D','',2,1,4,45,20,8),(1030,'s36D','',2,1,4,45,20,8),(1031,'s35D','',2,1,4,45,20,8),(1032,'s34D','',2,1,4,45,20,8),(1033,'s33D','',2,1,4,45,20,8),(1034,'s26D','',2,1,4,45,20,8),(1035,'s25D','',2,1,4,45,20,8),(1036,'s24D','',2,1,4,45,20,8),(1037,'s23D','',2,1,4,45,20,8),(1038,'s22D','',2,1,4,45,20,8),(1039,'s16D','',2,1,4,45,20,8),(1040,'s15D','',2,1,4,45,20,8),(1041,'s14D','',2,1,4,45,20,8),(1042,'s13D','',2,1,4,45,20,8),(1043,'s12D','',2,1,4,45,20,8),(1044,'s11D','',2,1,4,45,20,8),(1045,'s66D','',2,2,2,45,19,8),(1046,'s55D','',2,2,2,45,19,8),(1047,'s46D','',2,2,2,45,19,8),(1048,'s44D','',2,2,2,45,19,8),(1049,'s35D','',2,2,2,45,19,8),(1050,'s33D','',2,2,2,45,19,8),(1051,'s25D','',2,2,2,45,19,8),(1052,'s23D','',2,2,2,45,19,8),(1053,'s22D','',2,2,2,45,19,8),(1054,'s15D','',2,2,2,45,19,8),(1055,'s13D','',2,2,2,45,19,8),(1056,'s12D','',2,2,2,45,19,8),(1057,'s11D','',2,2,2,45,19,8),(1058,'s66D','',2,2,3,45,19,8),(1059,'s55D','',2,2,3,45,19,8),(1060,'s45D','',2,2,3,45,19,8),(1061,'s44D','',2,2,3,45,19,8),(1062,'s36D','',2,2,3,45,19,8),(1063,'s33D','',2,2,3,45,19,8),(1064,'s26D','',2,2,3,45,19,8),(1065,'s23D','',2,2,3,45,19,8),(1066,'s22D','',2,2,3,45,19,8),(1067,'s16D','',2,2,3,45,19,8),(1068,'s13D','',2,2,3,45,19,8),(1069,'s12D','',2,2,3,45,19,8),(1070,'s11D','',2,2,3,45,19,8),(1071,'s66D','',2,3,4,45,18,8),(1072,'s55D','',2,3,4,45,18,8),(1073,'s44D','',2,3,4,45,18,8),(1074,'s33D','',2,3,4,45,18,8),(1075,'s23D','',2,3,4,45,18,8),(1076,'s22D','',2,3,4,45,18,8),(1077,'s13D','',2,3,4,45,18,8),(1078,'s12D','',2,3,4,45,18,8),(1079,'s11D','',2,3,4,45,18,8),(1080,'s44D','',2,4,4,45,16,8),(1081,'s12D','',2,4,4,45,16,8),(1082,'s11D','',2,4,4,45,16,8),(1083,'s66D','',2,5,4,45,2,8),(1084,'s44D','',2,5,4,45,2,8),(1085,'s33D','',2,5,4,45,2,8),(1086,'s16D','',2,5,4,45,2,8),(1087,'s13D','',2,5,4,45,2,8),(1088,'s12D','',2,5,4,45,2,8),(1089,'s11D','',2,5,4,45,2,8),(1090,'s66D','',2,5,4,45,1,8),(1091,'s44D','',2,5,4,45,1,8),(1092,'s33D','',2,5,4,45,1,8),(1093,'s13D','',2,5,4,45,1,8),(1094,'s12D','',2,5,4,45,1,8),(1095,'s11D','',2,5,4,45,1,8),(1096,'s44D','',2,6,4,45,4,8),(1097,'s33D','',2,6,4,45,4,8),(1098,'s25D','',2,6,4,45,4,8),(1099,'s14D','',2,6,4,45,4,8),(1100,'s13D','',2,6,4,45,4,8),(1101,'s12D','',2,6,4,45,4,8),(1102,'s11D','',2,6,4,45,4,8),(1103,'s44D','',2,6,4,45,3,8),(1104,'s33D','',2,6,4,45,3,8),(1105,'s14D','',2,6,4,45,3,8),(1106,'s13D','',2,6,4,45,3,8),(1107,'s12D','',2,6,4,45,3,8),(1108,'s11D','',2,6,4,45,3,8),(1109,'s12D','',2,7,4,45,15,8),(1110,'s11D','',2,7,4,45,15,8),(1111,'s44D','',2,8,4,45,17,8),(1112,'s33D','',2,8,4,45,17,8),(1113,'s13D','',2,8,4,45,17,8),(1114,'s12D','',2,8,4,45,17,8),(1115,'s11D','',2,8,4,45,17,8),(1116,'s661T','',2,1,4,45,20,57),(1117,'s561T','',2,1,4,45,20,57),(1118,'s551T','',2,1,4,45,20,57),(1119,'s461T','',2,1,4,45,20,57),(1120,'s451T','',2,1,4,45,20,57),(1121,'s441T','',2,1,4,45,20,57),(1122,'s361T','',2,1,4,45,20,57),(1123,'s351T','',2,1,4,45,20,57),(1124,'s341T','',2,1,4,45,20,57),(1125,'s331T','',2,1,4,45,20,57),(1126,'s261T','',2,1,4,45,20,57),(1127,'s251T','',2,1,4,45,20,57),(1128,'s241T','',2,1,4,45,20,57),(1129,'s231T','',2,1,4,45,20,57),(1130,'s221T','',2,1,4,45,20,57),(1131,'s161T','',2,1,4,45,20,57),(1132,'s151T','',2,1,4,45,20,57),(1133,'s141T','',2,1,4,45,20,57),(1134,'s131T','',2,1,4,45,20,57),(1135,'s121T','',2,1,4,45,20,57),(1136,'s111T','',2,1,4,45,20,57),(1137,'s661T','',2,2,2,45,19,57),(1138,'s551T','',2,2,2,45,19,57),(1139,'s461T','',2,2,2,45,19,57),(1140,'s441T','',2,2,2,45,19,57),(1141,'s351T','',2,2,2,45,19,57),(1142,'s331T','',2,2,2,45,19,57),(1143,'s251T','',2,2,2,45,19,57),(1144,'s231T','',2,2,2,45,19,57),(1145,'s221T','',2,2,2,45,19,57),(1146,'s151T','',2,2,2,45,19,57),(1147,'s131T','',2,2,2,45,19,57),(1148,'s121T','',2,2,2,45,19,57),(1149,'s111T','',2,2,2,45,19,57),(1150,'s661T','',2,2,3,45,19,57),(1151,'s551T','',2,2,3,45,19,57),(1152,'s451T','',2,2,3,45,19,57),(1153,'s441T','',2,2,3,45,19,57),(1154,'s361T','',2,2,3,45,19,57),(1155,'s331T','',2,2,3,45,19,57),(1156,'s261T','',2,2,3,45,19,57),(1157,'s231T','',2,2,3,45,19,57),(1158,'s221T','',2,2,3,45,19,57),(1159,'s161T','',2,2,3,45,19,57),(1160,'s131T','',2,2,3,45,19,57),(1161,'s121T','',2,2,3,45,19,57),(1162,'s111T','',2,2,3,45,19,57),(1163,'s661T','',2,3,4,45,18,57),(1164,'s551T','',2,3,4,45,18,57),(1165,'s441T','',2,3,4,45,18,57),(1166,'s331T','',2,3,4,45,18,57),(1167,'s231T','',2,3,4,45,18,57),(1168,'s221T','',2,3,4,45,18,57),(1169,'s131T','',2,3,4,45,18,57),(1170,'s121T','',2,3,4,45,18,57),(1171,'s111T','',2,3,4,45,18,57),(1172,'s121T','',2,4,4,45,16,57),(1173,'s111T','',2,4,4,45,16,57),(1174,'s661T','',2,5,4,45,2,57),(1175,'s441T','',2,5,4,45,2,57),(1176,'s331T','',2,5,4,45,2,57),(1177,'s161T','',2,5,4,45,2,57),(1178,'s131T','',2,5,4,45,2,57),(1179,'s121T','',2,5,4,45,2,57),(1180,'s111T','',2,5,4,45,2,57),(1181,'s661T','',2,5,4,45,1,57),(1182,'s441T','',2,5,4,45,1,57),(1183,'s331T','',2,5,4,45,1,57),(1184,'s131T','',2,5,4,45,1,57),(1185,'s121T','',2,5,4,45,1,57),(1186,'s111T','',2,5,4,45,1,57),(1187,'s441T','',2,6,4,45,4,57),(1188,'s331T','',2,6,4,45,4,57),(1189,'s251T','',2,6,4,45,4,57),(1190,'s141T','',2,6,4,45,4,57),(1191,'s131T','',2,6,4,45,4,57),(1192,'s121T','',2,6,4,45,4,57),(1193,'s111T','',2,6,4,45,4,57),(1194,'s441T','',2,6,4,45,3,57),(1195,'s331T','',2,6,4,45,3,57),(1196,'s141T','',2,6,4,45,3,57),(1197,'s131T','',2,6,4,45,3,57),(1198,'s121T','',2,6,4,45,3,57),(1199,'s111T','',2,6,4,45,3,57),(1200,'s121T','',2,7,4,45,15,57),(1201,'s111T','',2,7,4,45,15,57),(1202,'s441T','',2,8,4,45,17,57),(1203,'s331T','',2,8,4,45,17,57),(1204,'s131T','',2,8,4,45,17,57),(1205,'s121T','',2,8,4,45,17,57),(1206,'s111T','',2,8,4,45,17,57),(1207,'s662T','',2,1,4,45,20,58),(1208,'s562T','',2,1,4,45,20,58),(1209,'s552T','',2,1,4,45,20,58),(1210,'s462T','',2,1,4,45,20,58),(1211,'s452T','',2,1,4,45,20,58),(1212,'s442T','',2,1,4,45,20,58),(1213,'s362T','',2,1,4,45,20,58),(1214,'s352T','',2,1,4,45,20,58),(1215,'s342T','',2,1,4,45,20,58),(1216,'s332T','',2,1,4,45,20,58),(1217,'s262T','',2,1,4,45,20,58),(1218,'s252T','',2,1,4,45,20,58),(1219,'s242T','',2,1,4,45,20,58),(1220,'s232T','',2,1,4,45,20,58),(1221,'s222T','',2,1,4,45,20,58),(1222,'s162T','',2,1,4,45,20,58),(1223,'s152T','',2,1,4,45,20,58),(1224,'s142T','',2,1,4,45,20,58),(1225,'s132T','',2,1,4,45,20,58),(1226,'s122T','',2,1,4,45,20,58),(1227,'s112T','',2,1,4,45,20,58),(1228,'s662T','',2,2,2,45,19,58),(1229,'s552T','',2,2,2,45,19,58),(1230,'s462T','',2,2,2,45,19,58),(1231,'s442T','',2,2,2,45,19,58),(1232,'s352T','',2,2,2,45,19,58),(1233,'s332T','',2,2,2,45,19,58),(1234,'s252T','',2,2,2,45,19,58),(1235,'s232T','',2,2,2,45,19,58),(1236,'s222T','',2,2,2,45,19,58),(1237,'s152T','',2,2,2,45,19,58),(1238,'s132T','',2,2,2,45,19,58),(1239,'s122T','',2,2,2,45,19,58),(1240,'s112T','',2,2,2,45,19,58),(1241,'s662T','',2,2,3,45,19,58),(1242,'s552T','',2,2,3,45,19,58),(1243,'s452T','',2,2,3,45,19,58),(1244,'s442T','',2,2,3,45,19,58),(1245,'s362T','',2,2,3,45,19,58),(1246,'s332T','',2,2,3,45,19,58),(1247,'s262T','',2,2,3,45,19,58),(1248,'s232T','',2,2,3,45,19,58),(1249,'s222T','',2,2,3,45,19,58),(1250,'s162T','',2,2,3,45,19,58),(1251,'s132T','',2,2,3,45,19,58),(1252,'s122T','',2,2,3,45,19,58),(1253,'s112T','',2,2,3,45,19,58),(1254,'s662T','',2,3,4,45,18,58),(1255,'s552T','',2,3,4,45,18,58),(1256,'s442T','',2,3,4,45,18,58),(1257,'s332T','',2,3,4,45,18,58),(1258,'s232T','',2,3,4,45,18,58),(1259,'s222T','',2,3,4,45,18,58),(1260,'s132T','',2,3,4,45,18,58),(1261,'s122T','',2,3,4,45,18,58),(1262,'s112T','',2,3,4,45,18,58),(1263,'s442T','',2,4,4,45,16,58),(1264,'s122T','',2,4,4,45,16,58),(1265,'s112T','',2,4,4,45,16,58),(1266,'s662T','',2,5,4,45,2,58),(1267,'s442T','',2,5,4,45,2,58),(1268,'s332T','',2,5,4,45,2,58),(1269,'s162T','',2,5,4,45,2,58),(1270,'s132T','',2,5,4,45,2,58),(1271,'s122T','',2,5,4,45,2,58),(1272,'s112T','',2,5,4,45,2,58),(1273,'s662T','',2,5,4,45,1,58),(1274,'s442T','',2,5,4,45,1,58),(1275,'s332T','',2,5,4,45,1,58),(1276,'s132T','',2,5,4,45,1,58),(1277,'s122T','',2,5,4,45,1,58),(1278,'s112T','',2,5,4,45,1,58),(1279,'s442T','',2,6,4,45,4,58),(1280,'s332T','',2,6,4,45,4,58),(1281,'s252T','',2,6,4,45,4,58),(1282,'s142T','',2,6,4,45,4,58),(1283,'s132T','',2,6,4,45,4,58),(1284,'s122T','',2,6,4,45,4,58),(1285,'s112T','',2,6,4,45,4,58),(1286,'s442T','',2,6,4,45,3,58),(1287,'s332T','',2,6,4,45,3,58),(1288,'s142T','',2,6,4,45,3,58),(1289,'s132T','',2,6,4,45,3,58),(1290,'s122T','',2,6,4,45,3,58),(1291,'s112T','',2,6,4,45,3,58),(1292,'s122T','',2,7,4,45,15,58),(1293,'s112T','',2,7,4,45,15,58),(1294,'s442T','',2,8,4,45,17,58),(1295,'s332T','',2,8,4,45,17,58),(1296,'s132T','',2,8,4,45,17,58),(1297,'s122T','',2,8,4,45,17,58),(1298,'s112T','',2,8,4,45,17,58),(1299,'s663T','',2,1,4,45,20,59),(1300,'s563T','',2,1,4,45,20,59),(1301,'s553T','',2,1,4,45,20,59),(1302,'s463T','',2,1,4,45,20,59),(1303,'s453T','',2,1,4,45,20,59),(1304,'s443T','',2,1,4,45,20,59),(1305,'s363T','',2,1,4,45,20,59),(1306,'s353T','',2,1,4,45,20,59),(1307,'s343T','',2,1,4,45,20,59),(1308,'s333T','',2,1,4,45,20,59),(1309,'s263T','',2,1,4,45,20,59),(1310,'s253T','',2,1,4,45,20,59),(1311,'s243T','',2,1,4,45,20,59),(1312,'s233T','',2,1,4,45,20,59),(1313,'s223T','',2,1,4,45,20,59),(1314,'s163T','',2,1,4,45,20,59),(1315,'s153T','',2,1,4,45,20,59),(1316,'s143T','',2,1,4,45,20,59),(1317,'s133T','',2,1,4,45,20,59),(1318,'s123T','',2,1,4,45,20,59),(1319,'s113T','',2,1,4,45,20,59),(1320,'s663T','',2,2,2,45,19,59),(1321,'s553T','',2,2,2,45,19,59),(1322,'s463T','',2,2,2,45,19,59),(1323,'s443T','',2,2,2,45,19,59),(1324,'s353T','',2,2,2,45,19,59),(1325,'s333T','',2,2,2,45,19,59),(1326,'s253T','',2,2,2,45,19,59),(1327,'s233T','',2,2,2,45,19,59),(1328,'s223T','',2,2,2,45,19,59),(1329,'s153T','',2,2,2,45,19,59),(1330,'s133T','',2,2,2,45,19,59),(1331,'s123T','',2,2,2,45,19,59),(1332,'s113T','',2,2,2,45,19,59),(1333,'s663T','',2,2,3,45,19,59),(1334,'s553T','',2,2,3,45,19,59),(1335,'s453T','',2,2,3,45,19,59),(1336,'s443T','',2,2,3,45,19,59),(1337,'s363T','',2,2,3,45,19,59),(1338,'s333T','',2,2,3,45,19,59),(1339,'s263T','',2,2,3,45,19,59),(1340,'s233T','',2,2,3,45,19,59),(1341,'s223T','',2,2,3,45,19,59),(1342,'s163T','',2,2,3,45,19,59),(1343,'s133T','',2,2,3,45,19,59),(1344,'s123T','',2,2,3,45,19,59),(1345,'s113T','',2,2,3,45,19,59),(1346,'s663T','',2,3,4,45,18,59),(1347,'s553T','',2,3,4,45,18,59),(1348,'s443T','',2,3,4,45,18,59),(1349,'s333T','',2,3,4,45,18,59),(1350,'s233T','',2,3,4,45,18,59),(1351,'s223T','',2,3,4,45,18,59),(1352,'s133T','',2,3,4,45,18,59),(1353,'s123T','',2,3,4,45,18,59),(1354,'s113T','',2,3,4,45,18,59),(1355,'s443T','',2,4,4,45,16,59),(1356,'s123T','',2,4,4,45,16,59),(1357,'s113T','',2,4,4,45,16,59),(1358,'s663T','',2,5,4,45,2,59),(1359,'s443T','',2,5,4,45,2,59),(1360,'s333T','',2,5,4,45,2,59),(1361,'s163T','',2,5,4,45,2,59),(1362,'s133T','',2,5,4,45,2,59),(1363,'s123T','',2,5,4,45,2,59),(1364,'s113T','',2,5,4,45,2,59),(1365,'s663T','',2,5,4,45,1,59),(1366,'s443T','',2,5,4,45,1,59),(1367,'s333T','',2,5,4,45,1,59),(1368,'s133T','',2,5,4,45,1,59),(1369,'s123T','',2,5,4,45,1,59),(1370,'s113T','',2,5,4,45,1,59),(1371,'s443T','',2,6,4,45,4,59),(1372,'s333T','',2,6,4,45,4,59),(1373,'s253T','',2,6,4,45,4,59),(1374,'s143T','',2,6,4,45,4,59),(1375,'s133T','',2,6,4,45,4,59),(1376,'s123T','',2,6,4,45,4,59),(1377,'s113T','',2,6,4,45,4,59),(1378,'s443T','',2,6,4,45,3,59),(1379,'s333T','',2,6,4,45,3,59),(1380,'s143T','',2,6,4,45,3,59),(1381,'s133T','',2,6,4,45,3,59),(1382,'s123T','',2,6,4,45,3,59),(1383,'s113T','',2,6,4,45,3,59),(1384,'s123T','',2,7,4,45,15,59),(1385,'s113T','',2,7,4,45,15,59),(1386,'s443T','',2,8,4,45,17,59),(1387,'s333T','',2,8,4,45,17,59),(1388,'s133T','',2,8,4,45,17,59),(1389,'s123T','',2,8,4,45,17,59),(1390,'s113T','',2,8,4,45,17,59),(1391,'s66S','',2,1,4,45,20,63),(1392,'s56S','',2,1,4,45,20,63),(1393,'s55S','',2,1,4,45,20,63),(1394,'s46S','',2,1,4,45,20,63),(1395,'s45S','',2,1,4,45,20,63),(1396,'s44S','',2,1,4,45,20,63),(1397,'s36S','',2,1,4,45,20,63),(1398,'s35S','',2,1,4,45,20,63),(1399,'s34S','',2,1,4,45,20,63),(1400,'s33S','',2,1,4,45,20,63),(1401,'s26S','',2,1,4,45,20,63),(1402,'s25S','',2,1,4,45,20,63),(1403,'s24S','',2,1,4,45,20,63),(1404,'s23S','',2,1,4,45,20,63),(1405,'s22S','',2,1,4,45,20,63),(1406,'s16S','',2,1,4,45,20,63),(1407,'s15S','',2,1,4,45,20,63),(1408,'s14S','',2,1,4,45,20,63),(1409,'s13S','',2,1,4,45,20,63),(1410,'s12S','',2,1,4,45,20,63),(1411,'s11S','',2,1,4,45,20,63),(1412,'s66S','',2,2,2,45,19,63),(1413,'s55S','',2,2,2,45,19,63),(1414,'s46S','',2,2,2,45,19,63),(1415,'s44S','',2,2,2,45,19,63),(1416,'s35S','',2,2,2,45,19,63),(1417,'s33S','',2,2,2,45,19,63),(1418,'s25S','',2,2,2,45,19,63),(1419,'s23S','',2,2,2,45,19,63),(1420,'s22S','',2,2,2,45,19,63),(1421,'s15S','',2,2,2,45,19,63),(1422,'s13S','',2,2,2,45,19,63),(1423,'s12S','',2,2,2,45,19,63),(1424,'s11S','',2,2,2,45,19,63),(1425,'s66S','',2,2,3,45,19,63),(1426,'s55S','',2,2,3,45,19,63),(1427,'s45S','',2,2,3,45,19,63),(1428,'s44S','',2,2,3,45,19,63),(1429,'s36S','',2,2,3,45,19,63),(1430,'s33S','',2,2,3,45,19,63),(1431,'s26S','',2,2,3,45,19,63),(1432,'s23S','',2,2,3,45,19,63),(1433,'s22S','',2,2,3,45,19,63),(1434,'s16S','',2,2,3,45,19,63),(1435,'s13S','',2,2,3,45,19,63),(1436,'s12S','',2,2,3,45,19,63),(1437,'s11S','',2,2,3,45,19,63),(1438,'s66S','',2,3,4,45,18,63),(1439,'s55S','',2,3,4,45,18,63),(1440,'s44S','',2,3,4,45,18,63),(1441,'s33S','',2,3,4,45,18,63),(1442,'s23S','',2,3,4,45,18,63),(1443,'s22S','',2,3,4,45,18,63),(1444,'s13S','',2,3,4,45,18,63),(1445,'s12S','',2,3,4,45,18,63),(1446,'s11S','',2,3,4,45,18,63),(1447,'s44S','',2,4,4,45,16,63),(1448,'s12S','',2,4,4,45,16,63),(1449,'s11S','',2,4,4,45,16,63),(1450,'s66S','',2,5,4,45,2,63),(1451,'s44S','',2,5,4,45,2,63),(1452,'s33S','',2,5,4,45,2,63),(1453,'s16S','',2,5,4,45,2,63),(1454,'s13S','',2,5,4,45,2,63),(1455,'s12S','',2,5,4,45,2,63),(1456,'s11S','',2,5,4,45,2,63),(1457,'s66S','',2,5,4,45,1,63),(1458,'s44S','',2,5,4,45,1,63),(1459,'s33S','',2,5,4,45,1,63),(1460,'s13S','',2,5,4,45,1,63),(1461,'s12S','',2,5,4,45,1,63),(1462,'s11S','',2,5,4,45,1,63),(1463,'s44S','',2,6,4,45,4,63),(1464,'s33S','',2,6,4,45,4,63),(1465,'s25S','',2,6,4,45,4,63),(1466,'s14S','',2,6,4,45,4,63),(1467,'s13S','',2,6,4,45,4,63),(1468,'s12S','',2,6,4,45,4,63),(1469,'s11S','',2,6,4,45,4,63),(1470,'s44S','',2,6,4,45,3,63),(1471,'s33S','',2,6,4,45,3,63),(1472,'s14S','',2,6,4,45,3,63),(1473,'s13S','',2,6,4,45,3,63),(1474,'s12S','',2,6,4,45,3,63),(1475,'s11S','',2,6,4,45,3,63),(1476,'s12S','',2,7,4,45,15,63),(1477,'s11S','',2,7,4,45,15,63),(1478,'s44S','',2,8,4,45,17,63),(1479,'s33S','',2,8,4,45,17,63),(1480,'s13S','',2,8,4,45,17,63),(1481,'s12S','',2,8,4,45,17,63),(1482,'s11S','',2,8,4,45,17,63),(1524,'c22','',1,2,3,45,19,10),(1523,'c23','',1,2,3,45,19,10),(1522,'c26','',1,2,3,45,19,10),(1521,'c33','',1,2,3,45,19,10),(1520,'c36','',1,2,3,45,19,10),(1519,'c44','',1,2,3,45,19,10),(1518,'c45','',1,2,3,45,19,10),(1517,'c55','',1,2,3,45,19,10),(1516,'c66','',1,2,3,45,19,10),(1515,'c11','',1,2,2,45,19,10),(1514,'c12','',1,2,2,45,19,10),(1513,'c13','',1,2,2,45,19,10),(1512,'c15','',1,2,2,45,19,10),(1511,'c22','',1,2,2,45,19,10),(1510,'c23','',1,2,2,45,19,10),(1509,'c25','',1,2,2,45,19,10),(1508,'c33','',1,2,2,45,19,10),(1507,'c35','',1,2,2,45,19,10),(1506,'c44','',1,2,2,45,19,10),(1505,'c55','',1,2,2,45,19,10),(1504,'c66','',1,2,2,45,19,10),(1525,'c16','',1,2,3,45,19,10),(1526,'c13','',1,2,3,45,19,10),(1527,'c12','',1,2,3,45,19,10),(1528,'c11','',1,2,3,45,19,10),(1529,'c66','',1,3,4,45,18,10),(1530,'c55','',1,3,4,45,18,10),(1531,'c44','',1,3,4,45,18,10),(1532,'c33','',1,3,4,45,18,10),(1533,'c23','',1,3,4,45,18,10),(1534,'c22','',1,3,4,45,18,10),(1535,'c13','',1,3,4,45,18,10),(1536,'c12','',1,3,4,45,18,10),(1537,'c11','',1,3,4,45,18,10),(1538,'c44','',1,4,4,45,16,10),(1539,'c12','',1,4,4,45,16,10),(1540,'c11','',1,4,4,45,16,10),(1541,'c66','',1,5,4,45,2,10),(1542,'c44','',1,5,4,45,2,10),(1543,'c33','',1,5,4,45,2,10),(1544,'c16','',1,5,4,45,2,10),(1545,'c13','',1,5,4,45,2,10),(1546,'c12','',1,5,4,45,2,10),(1547,'c11','',1,5,4,45,2,10),(1548,'c66','',1,5,4,45,1,10),(1549,'c44','',1,5,4,45,1,10),(1550,'c33','',1,5,4,45,1,10),(1551,'c13','',1,5,4,45,1,10),(1552,'c12','',1,5,4,45,1,10),(1553,'c11','',1,5,4,45,1,10),(1554,'c44','',1,6,4,45,4,10),(1555,'c33','',1,6,4,45,4,10),(1556,'c25','',1,6,4,45,4,10),(1557,'c14','',1,6,4,45,4,10),(1558,'c13','',1,6,4,45,4,10),(1559,'c12','',1,6,4,45,4,10),(1560,'c11','',1,6,4,45,4,10),(1561,'c44','',1,6,4,45,3,10),(1562,'c33','',1,6,4,45,3,10),(1563,'c14','',1,6,4,45,3,10),(1564,'c13','',1,6,4,45,3,10),(1565,'c12','',1,6,4,45,3,10),(1566,'c11','',1,6,4,45,3,10),(1567,'c12','',1,7,4,45,15,10),(1568,'c11','',1,7,4,45,15,10),(1569,'c44','',1,8,4,45,17,10),(1570,'c33','',1,8,4,45,17,10),(1571,'c13','',1,8,4,45,17,10),(1572,'c12','',1,8,4,45,17,10),(1573,'c11','',1,8,4,45,17,10),(1574,'c66D','',1,1,4,45,20,11),(1575,'c56D','',1,1,4,45,20,11),(1576,'c55D','',1,1,4,45,20,11),(1577,'c46D','',1,1,4,45,20,11),(1578,'c45D','',1,1,4,45,20,11),(1579,'c44D','',1,1,4,45,20,11),(1580,'c36D','',1,1,4,45,20,11),(1581,'c35D','',1,1,4,45,20,11),(1582,'c34D','',1,1,4,45,20,11),(1583,'c33D','',1,1,4,45,20,11),(1584,'c26D','',1,1,4,45,20,11),(1585,'c25D','',1,1,4,45,20,11),(1586,'c24D','',1,1,4,45,20,11),(1587,'c23D','',1,1,4,45,20,11),(1588,'c22D','',1,1,4,45,20,11),(1589,'c16D','',1,1,4,45,20,11),(1590,'c15D','',1,1,4,45,20,11),(1591,'c14D','',1,1,4,45,20,11),(1592,'c13D','',1,1,4,45,20,11),(1593,'c12D','',1,1,4,45,20,11),(1594,'c11D','',1,1,4,45,20,11),(1595,'c66D','',1,2,2,45,19,11),(1596,'c55D','',1,2,2,45,19,11),(1597,'c46D','',1,2,2,45,19,11),(1598,'c44D','',1,2,2,45,19,11),(1599,'c35D','',1,2,2,45,19,11),(1600,'c33D','',1,2,2,45,19,11),(1601,'c25D','',1,2,2,45,19,11),(1602,'c23D','',1,2,2,45,19,11),(1603,'c22D','',1,2,2,45,19,11),(1604,'c15D','',1,2,2,45,19,11),(1605,'c13D','',1,2,2,45,19,11),(1606,'c12D','',1,2,2,45,19,11),(1607,'c11D','',1,2,2,45,19,11),(1608,'c66D','',1,2,3,45,19,11),(1609,'c55D','',1,2,3,45,19,11),(1610,'c45D','',1,2,3,45,19,11),(1611,'c44D','',1,2,3,45,19,11),(1612,'c36D','',1,2,3,45,19,11),(1613,'c33D','',1,2,3,45,19,11),(1614,'c26D','',1,2,3,45,19,11),(1615,'c23D','',1,2,3,45,19,11),(1616,'c22D','',1,2,3,45,19,11),(1617,'c16D','',1,2,3,45,19,11),(1618,'c13D','',1,2,3,45,19,11),(1619,'c12D','',1,2,3,45,19,11),(1620,'c11D','',1,2,3,45,19,11),(1621,'c66D','',1,3,4,45,18,11),(1622,'c55D','',1,3,4,45,18,11),(1623,'c44D','',1,3,4,45,18,11),(1624,'c33D','',1,3,4,45,18,11),(1625,'c23D','',1,3,4,45,18,11),(1626,'c22D','',1,3,4,45,18,11),(1627,'c13D','',1,3,4,45,18,11),(1628,'c12D','',1,3,4,45,18,11),(1629,'c11D','',1,3,4,45,18,11),(1630,'c44D','',1,4,4,45,16,11),(1631,'c12D','',1,4,4,45,16,11),(1632,'c11D','',1,4,4,45,16,11),(1633,'c66D','',1,5,4,45,2,11),(1634,'c44D','',1,5,4,45,2,11),(1635,'c33D','',1,5,4,45,2,11),(1636,'c16D','',1,5,4,45,2,11),(1637,'c13D','',1,5,4,45,2,11),(1638,'c12D','',1,5,4,45,2,11),(1639,'c11D','',1,5,4,45,2,11),(1640,'c66D','',1,5,4,45,1,11),(1641,'c44D','',1,5,4,45,1,11),(1642,'c33D','',1,5,4,45,1,11),(1643,'c13D','',1,5,4,45,1,11),(1644,'c12D','',1,5,4,45,1,11),(1645,'c11D','',1,5,4,45,1,11),(1646,'c44D','',1,6,4,45,4,11),(1647,'c33D','',1,6,4,45,4,11),(1648,'c25D','',1,6,4,45,4,11),(1649,'c14D','',1,6,4,45,4,11),(1650,'c13D','',1,6,4,45,4,11),(1651,'c12D','',1,6,4,45,4,11),(1652,'c11D','',1,6,4,45,4,11),(1653,'c44D','',1,6,4,45,3,11),(1654,'c33D','',1,6,4,45,3,11),(1655,'c14D','',1,6,4,45,3,11),(1656,'c13D','',1,6,4,45,3,11),(1657,'c12D','',1,6,4,45,3,11),(1658,'c11D','',1,6,4,45,3,11),(1659,'c12D','',1,7,4,45,15,11),(1660,'c11D','',1,7,4,45,15,11),(1661,'c44D','',1,8,4,45,17,11),(1662,'c33D','',1,8,4,45,17,11),(1663,'c13D','',1,8,4,45,17,11),(1664,'c12D','',1,8,4,45,17,11),(1665,'c11D','',1,8,4,45,17,11),(1666,'c66E','',1,1,4,45,20,12),(1667,'c56E','',1,1,4,45,20,12),(1668,'c55E','',1,1,4,45,20,12),(1669,'c46E','',1,1,4,45,20,12),(1670,'c45E','',1,1,4,45,20,12),(1671,'c44E','',1,1,4,45,20,12),(1672,'c36E','',1,1,4,45,20,12),(1673,'c35E','',1,1,4,45,20,12),(1674,'c34E','',1,1,4,45,20,12),(1675,'c33E','',1,1,4,45,20,12),(1676,'c26E','',1,1,4,45,20,12),(1677,'c25E','',1,1,4,45,20,12),(1678,'c24E','',1,1,4,45,20,12),(1679,'c23E','',1,1,4,45,20,12),(1680,'c22E','',1,1,4,45,20,12),(1681,'c16E','',1,1,4,45,20,12),(1682,'c15E','',1,1,4,45,20,12),(1683,'c14E','',1,1,4,45,20,12),(1684,'c13E','',1,1,4,45,20,12),(1685,'c12E','',1,1,4,45,20,12),(1686,'c11E','',1,1,4,45,20,12),(1687,'c66E','',1,2,2,45,19,12),(1688,'c55E','',1,2,2,45,19,12),(1689,'c46E','',1,2,2,45,19,12),(1690,'c44E','',1,2,2,45,19,12),(1691,'c35E','',1,2,2,45,19,12),(1692,'c33E','',1,2,2,45,19,12),(1693,'c25E','',1,2,2,45,19,12),(1694,'c23E','',1,2,2,45,19,12),(1695,'c22E','',1,2,2,45,19,12),(1696,'c15E','',1,2,2,45,19,12),(1697,'c13E','',1,2,2,45,19,12),(1698,'c12E','',1,2,2,45,19,12),(1699,'c11E','',1,2,2,45,19,12),(1700,'c66E','',1,2,3,45,19,12),(1701,'c55E','',1,2,3,45,19,12),(1702,'c45E','',1,2,3,45,19,12),(1703,'c44E','',1,2,3,45,19,12),(1704,'c36E','',1,2,3,45,19,12),(1705,'c33E','',1,2,3,45,19,12),(1706,'c26E','',1,2,3,45,19,12),(1707,'c23E','',1,2,3,45,19,12),(1708,'c22E','',1,2,3,45,19,12),(1709,'c16E','',1,2,3,45,19,12),(1710,'c13E','',1,2,3,45,19,12),(1711,'c12E','',1,2,3,45,19,12),(1712,'c11E','',1,2,3,45,19,12),(1713,'c66E','',1,3,4,45,18,12),(1714,'c55E','',1,3,4,45,18,12),(1715,'c44E','',1,3,4,45,18,12),(1716,'c23E','',1,3,4,45,18,12),(1717,'c22E','',1,3,4,45,18,12),(1718,'c13E','',1,3,4,45,18,12),(1719,'c12E','',1,3,4,45,18,12),(1720,'c11E','',1,3,4,45,18,12),(1721,'c44E','',1,4,4,45,16,12),(1722,'c12E','',1,4,4,45,16,12),(1723,'c11E','',1,4,4,45,16,12),(1724,'c66E','',1,5,4,45,2,12),(1725,'c44E','',1,5,4,45,2,12),(1726,'c33E','',1,5,4,45,2,12),(1727,'c16E','',1,5,4,45,2,12),(1728,'c13E','',1,5,4,45,2,12),(1729,'c12E','',1,5,4,45,2,12),(1730,'c11E','',1,5,4,45,2,12),(1731,'c66E','',1,5,4,45,1,12),(1732,'c44E','',1,5,4,45,1,12),(1733,'c33E','',1,5,4,45,1,12),(1734,'c13E','',1,5,4,45,1,12),(1735,'c12E','',1,5,4,45,1,12),(1736,'c11E','',1,5,4,45,1,12),(1737,'c44E','',1,6,4,45,4,12),(1738,'c33E','',1,6,4,45,4,12),(1739,'c25E','',1,6,4,45,4,12),(1740,'c14E','',1,6,4,45,4,12),(1741,'c13E','',1,6,4,45,4,12),(1742,'c12E','',1,6,4,45,4,12),(1743,'c11E','',1,6,4,45,4,12),(1744,'c44E','',1,6,4,45,3,12),(1745,'c33E','',1,6,4,45,3,12),(1746,'c14E','',1,6,4,45,3,12),(1747,'c13E','',1,6,4,45,3,12),(1748,'c12E','',1,6,4,45,3,12),(1749,'c11E','',1,6,4,45,3,12),(1750,'c12E','',1,7,4,45,15,12),(1751,'c11E','',1,7,4,45,15,12),(1752,'c44E','',1,8,4,45,17,12),(1753,'c33E','',1,8,4,45,17,12),(1754,'c13E','',1,8,4,45,17,12),(1755,'c12E','',1,8,4,45,17,12),(1756,'c11E','',1,8,4,45,17,12),(1757,'c66S','',1,1,4,45,20,13),(1758,'c56S','',1,1,4,45,20,13),(1759,'c55S','',1,1,4,45,20,13),(1760,'c46S','',1,1,4,45,20,13),(1761,'c45S','',1,1,4,45,20,13),(1762,'c44S','',1,1,4,45,20,13),(1763,'c36S','',1,1,4,45,20,13),(1764,'c35S','',1,1,4,45,20,13),(1765,'c34S','',1,1,4,45,20,13),(1766,'c33S','',1,1,4,45,20,13),(1767,'c26S','',1,1,4,45,20,13),(1768,'c25S','',1,1,4,45,20,13),(1769,'c24S','',1,1,4,45,20,13),(1770,'c23S','',1,1,4,45,20,13),(1771,'c22S','',1,1,4,45,20,13),(1772,'c16S','',1,1,4,45,20,13),(1773,'c15S','',1,1,4,45,20,13),(1774,'c14S','',1,1,4,45,20,13),(1775,'c13S','',1,1,4,45,20,13),(1776,'c12S','',1,1,4,45,20,13),(1777,'c11S','',1,1,4,45,20,13),(1778,'c66S','',1,2,2,45,19,13),(1779,'c55S','',1,2,2,45,19,13),(1780,'c46S','',1,2,2,45,19,13),(1781,'c44S','',1,2,2,45,19,13),(1782,'c35S','',1,2,2,45,19,13),(1783,'c33S','',1,2,2,45,19,13),(1784,'c25S','',1,2,2,45,19,13),(1785,'c23S','',1,2,2,45,19,13),(1786,'c22S','',1,2,2,45,19,13),(1787,'c15S','',1,2,2,45,19,13),(1788,'c13S','',1,2,2,45,19,13),(1789,'c12S','',1,2,2,45,19,13),(1790,'c11S','',1,2,2,45,19,13),(1791,'c66S','',1,2,3,45,19,13),(1792,'c55S','',1,2,3,45,19,13),(1793,'c45S','',1,2,3,45,19,13),(1794,'c44S','',1,2,3,45,19,13),(1795,'c36S','',1,2,3,45,19,13),(1796,'c33S','',1,2,3,45,19,13),(1797,'c26S','',1,2,3,45,19,13),(1798,'c23S','',1,2,3,45,19,13),(1799,'c22S','',1,2,3,45,19,13),(1800,'c16S','',1,2,3,45,19,13),(1801,'c13S','',1,2,3,45,19,13),(1802,'c12S','',1,2,3,45,19,13),(1803,'c11S','',1,2,3,45,19,13),(1804,'c66S','',1,3,4,45,18,13),(1805,'c55S','',1,3,4,45,18,13),(1806,'c44S','',1,3,4,45,18,13),(1807,'c33S','',1,3,4,45,18,13),(1808,'c23S','',1,3,4,45,18,13),(1809,'c22S','',1,3,4,45,18,13),(1810,'c13S','',1,3,4,45,18,13),(1811,'c12S','',1,3,4,45,18,13),(1812,'c11S','',1,3,4,45,18,13),(1813,'c44S','',1,4,4,45,16,13),(1814,'c12S','',1,4,4,45,16,13),(1815,'c11S','',1,4,4,45,16,13),(1816,'c66S','',1,5,4,45,2,13),(1817,'c44S','',1,5,4,45,2,13),(1818,'c33S','',1,5,4,45,2,13),(1819,'c16S','',1,5,4,45,2,13),(1820,'c13S','',1,5,4,45,2,13),(1821,'c12S','',1,5,4,45,2,13),(1822,'c11S','',1,5,4,45,2,13),(1823,'c66S','',1,5,4,45,1,13),(1824,'c44S','',1,5,4,45,1,13),(1825,'c33S','',1,5,4,45,1,13),(1826,'c13S','',1,5,4,45,1,13),(1827,'c12S','',1,5,4,45,1,13),(1828,'c11S','',1,5,4,45,1,13),(1829,'c44S','',1,6,4,45,4,13),(1830,'c33S','',1,6,4,45,4,13),(1831,'c25S','',1,6,4,45,4,13),(1832,'c14S','',1,6,4,45,4,13),(1833,'c13S','',1,6,4,45,4,13),(1834,'c12S','',1,6,4,45,4,13),(1835,'c11S','',1,6,4,45,4,13),(1836,'c44S','',1,6,4,45,3,13),(1837,'c33S','',1,6,4,45,3,13),(1838,'c14S','',1,6,4,45,3,13),(1839,'c13S','',1,6,4,45,3,13),(1840,'c12S','',1,6,4,45,3,13),(1841,'c11S','',1,6,4,45,3,13),(1842,'c12S','',1,7,4,45,15,13),(1843,'c11S','',1,7,4,45,15,13),(1844,'c44S','',1,8,4,45,17,13),(1845,'c33S','',1,8,4,45,17,13),(1846,'c13S','',1,8,4,45,17,13),(1847,'c12S','',1,8,4,45,17,13),(1848,'c11S','',1,8,4,45,17,13),(1849,'c661P','',1,1,4,45,20,61),(1850,'c561P','',1,1,4,45,20,61),(1851,'c551P','',1,1,4,45,20,61),(1852,'c461P','',1,1,4,45,20,61),(1853,'c451P','',1,1,4,45,20,61),(1854,'c441P','',1,1,4,45,20,61),(1855,'c361P','',1,1,4,45,20,61),(1856,'c351P','',1,1,4,45,20,61),(1857,'c341P','',1,1,4,45,20,61),(1858,'c331P','',1,1,4,45,20,61),(1859,'c261P','',1,1,4,45,20,61),(1860,'c251P','',1,1,4,45,20,61),(1861,'c241P','',1,1,4,45,20,61),(1862,'c231P','',1,1,4,45,20,61),(1863,'c221P','',1,1,4,45,20,61),(1864,'c161P','',1,1,4,45,20,61),(1865,'c151P','',1,1,4,45,20,61),(1866,'c141P','',1,1,4,45,20,61),(1867,'c131P','',1,1,4,45,20,61),(1868,'c121P','',1,1,4,45,20,61),(1869,'c111P','',1,1,4,45,20,61),(1870,'c661P','',1,2,2,45,19,61),(1871,'c551P','',1,2,2,45,19,61),(1872,'c461P','',1,2,2,45,19,61),(1873,'c441P','',1,2,2,45,19,61),(1874,'c351P','',1,2,2,45,19,61),(1875,'c331P','',1,2,2,45,19,61),(1876,'c251P','',1,2,2,45,19,61),(1877,'c231P','',1,2,2,45,19,61),(1878,'c221P','',1,2,2,45,19,61),(1879,'c151P','',1,2,2,45,19,61),(1880,'c131P','',1,2,2,45,19,61),(1881,'c121P','',1,2,2,45,19,61),(1882,'c111P','',1,2,2,45,19,61),(1883,'c661P','',1,2,3,45,19,61),(1884,'c551P','',1,2,3,45,19,61),(1885,'c451P','',1,2,3,45,19,61),(1886,'c441P','',1,2,3,45,19,61),(1887,'c361P','',1,2,3,45,19,61),(1888,'c331P','',1,2,3,45,19,61),(1889,'c261P','',1,2,3,45,19,61),(1890,'c231P','',1,2,3,45,19,61),(1891,'c221P','',1,2,3,45,19,61),(1892,'c161P','',1,2,3,45,19,61),(1893,'c131P','',1,2,3,45,19,61),(1894,'c121P','',1,2,3,45,19,61),(1895,'c111P','',1,2,3,45,19,61),(1896,'c661P','',1,3,4,45,18,61),(1897,'c551P','',1,3,4,45,18,61),(1898,'c441P','',1,3,4,45,18,61),(1899,'c331P','',1,3,4,45,18,61),(1900,'c231P','',1,3,4,45,18,61),(1901,'c221P','',1,3,4,45,18,61),(1902,'c131P','',1,3,4,45,18,61),(1903,'c121P','',1,3,4,45,18,61),(1904,'c111P','',1,3,4,45,18,61),(1905,'c441P','',1,4,4,45,16,61),(1906,'c121P','',1,4,4,45,16,61),(1907,'c111P','',1,4,4,45,16,61),(1908,'c661P','',1,5,4,45,2,61),(1909,'c441P','',1,5,4,45,2,61),(1910,'c331P','',1,5,4,45,2,61),(1911,'c161P','',1,5,4,45,2,61),(1912,'c131P','',1,5,4,45,2,61),(1913,'c121P','',1,5,4,45,2,61),(1914,'c111P','',1,5,4,45,2,61),(1915,'c661P','',1,5,4,45,1,61),(1916,'c441P','',1,5,4,45,1,61),(1917,'c331P','',1,5,4,45,1,61),(1918,'c131P','',1,5,4,45,1,61),(1919,'c121P','',1,5,4,45,1,61),(1920,'c111P','',1,5,4,45,1,61),(1921,'c441P','',1,6,4,45,4,61),(1922,'c331P','',1,6,4,45,4,61),(1923,'c251P','',1,6,4,45,4,61),(1924,'c141P','',1,6,4,45,4,61),(1925,'c131P','',1,6,4,45,4,61),(1926,'c121P','',1,6,4,45,4,61),(1927,'c111P','',1,6,4,45,4,61),(1928,'c441P','',1,6,4,45,3,61),(1929,'c331P','',1,6,4,45,3,61),(1930,'c141P','',1,6,4,45,3,61),(1931,'c131P','',1,6,4,45,3,61),(1932,'c121P','',1,6,4,45,3,61),(1933,'c111P','',1,6,4,45,3,61),(1934,'c121P','',1,7,4,45,15,61),(1935,'c111P','',1,7,4,45,15,61),(1936,'c441P','',1,8,4,45,17,61),(1937,'c331P','',1,8,4,45,17,61),(1938,'c131P','',1,8,4,45,17,61),(1939,'c121P','',1,8,4,45,17,61),(1940,'c111P','',1,8,4,45,17,61),(1941,'c662P','',1,1,4,45,20,62),(1942,'c562P','',1,1,4,45,20,62),(1943,'c552P','',1,1,4,45,20,62),(1944,'c462P','',1,1,4,45,20,62),(1945,'c452P','',1,1,4,45,20,62),(1946,'c442P','',1,1,4,45,20,62),(1947,'c362P','',1,1,4,45,20,62),(1948,'c352P','',1,1,4,45,20,62),(1949,'c342P','',1,1,4,45,20,62),(1950,'c332P','',1,1,4,45,20,62),(1951,'c262P','',1,1,4,45,20,62),(1952,'c252P','',1,1,4,45,20,62),(1953,'c242P','',1,1,4,45,20,62),(1954,'c232P','',1,1,4,45,20,62),(1955,'c222P','',1,1,4,45,20,62),(1956,'c162P','',1,1,4,45,20,62),(1957,'c152P','',1,1,4,45,20,62),(1958,'c142P','',1,1,4,45,20,62),(1959,'c132P','',1,1,4,45,20,62),(1960,'c122P','',1,1,4,45,20,62),(1961,'c112P','',1,1,4,45,20,62),(1962,'c662P','',1,2,2,45,19,62),(1963,'c552P','',1,2,2,45,19,62),(1964,'c462P','',1,2,2,45,19,62),(1965,'c442P','',1,2,2,45,19,62),(1966,'c352P','',1,2,2,45,19,62),(1967,'c332P','',1,2,2,45,19,62),(1968,'c252P','',1,2,2,45,19,62),(1969,'c232P','',1,2,2,45,19,62),(1970,'c222P','',1,2,2,45,19,62),(1971,'c152P','',1,2,2,45,19,62),(1972,'c132P','',1,2,2,45,19,62),(1973,'c122P','',1,2,2,45,19,62),(1974,'c112P','',1,2,2,45,19,62),(1975,'c662P','',1,2,3,45,19,62),(1976,'c552P','',1,2,3,45,19,62),(1977,'c452P','',1,2,3,45,19,62),(1978,'c442P','',1,2,3,45,19,62),(1979,'c362P','',1,2,3,45,19,62),(1980,'c332P','',1,2,3,45,19,62),(1981,'c262P','',1,2,3,45,19,62),(1982,'c232P','',1,2,3,45,19,62),(1983,'c222P','',1,2,3,45,19,62),(1984,'c162P','',1,2,3,45,19,62),(1985,'c132P','',1,2,3,45,19,62),(1986,'c122P','',1,2,3,45,19,62),(1987,'c112P','',1,2,3,45,19,62),(1988,'c662P','',1,3,4,45,18,62),(1989,'c552P','',1,3,4,45,18,62),(1990,'c442P','',1,3,4,45,18,62),(1991,'c332P','',1,3,4,45,18,62),(1992,'c232P','',1,3,4,45,18,62),(1993,'c222P','',1,3,4,45,18,62),(1994,'c132P','',1,3,4,45,18,62),(1995,'c122P','',1,3,4,45,18,62),(1996,'c112P','',1,3,4,45,18,62),(1997,'c442P','',1,4,4,45,16,62),(1998,'c122P','',1,4,4,45,16,62),(1999,'c112P','',1,4,4,45,16,62),(2000,'c662P','',1,5,4,45,2,62),(2001,'c442P','',1,5,4,45,2,62),(2002,'c332P','',1,5,4,45,2,62),(2003,'c162P','',1,5,4,45,2,62),(2004,'c132P','',1,5,4,45,2,62),(2005,'c122P','',1,5,4,45,2,62),(2006,'c112P','',1,5,4,45,2,62),(2007,'c662P','',1,5,4,45,1,62),(2008,'c442P','',1,5,4,45,1,62),(2009,'c332P','',1,5,4,45,1,62),(2010,'c132P','',1,5,4,45,1,62),(2011,'c122P','',1,5,4,45,1,62),(2012,'c112P','',1,5,4,45,1,62),(2013,'c442P','',1,6,4,45,3,62),(2014,'c332P','',1,6,4,45,3,62),(2027,'c122P','',1,7,4,45,15,62),(2016,'c142P','',1,6,4,45,3,62),(2017,'c132P','',1,6,4,45,3,62),(2018,'c122P','',1,6,4,45,3,62),(2019,'c112P','',1,6,4,45,3,62),(2020,'c442P','',1,6,4,45,4,62),(2021,'c332P','',1,6,4,45,4,62),(2022,'c252P','',1,6,4,45,4,62),(2023,'c142P','',1,6,4,45,4,62),(2024,'c132P','',1,6,4,45,4,62),(2025,'c122P','',1,6,4,45,4,62),(2026,'c112P','',1,6,4,45,4,62),(2028,'c112P','',1,7,4,45,15,62),(2029,'c442P','',1,8,4,45,17,62),(2030,'c332P','',1,8,4,45,17,62),(2031,'c132P','',1,8,4,45,17,62),(2032,'c122P','',1,8,4,45,17,62),(2033,'c112P','',1,8,4,45,17,62),(2034,'c66S1T','',1,1,4,45,20,71),(2035,'c56S1T','',1,1,4,45,20,71),(2036,'c55S1T','',1,1,4,45,20,71),(2037,'c46S1T','',1,1,4,45,20,71),(2038,'c45S1T','',1,1,4,45,20,71),(2039,'c44S1T','',1,1,4,45,20,71),(2040,'c36S1T','',1,1,4,45,20,71),(2041,'c35S1T','',1,1,4,45,20,71),(2042,'c34S1T','',1,1,4,45,20,71),(2043,'c33S1T','',1,1,4,45,20,71),(2044,'c26S1T','',1,1,4,45,20,71),(2045,'c25S1T','',1,1,4,45,20,71),(2046,'c24S1T','',1,1,4,45,20,71),(2047,'c23S1T','',1,1,4,45,20,71),(2048,'c22S1T','',1,1,4,45,20,71),(2049,'c16S1T','',1,1,4,45,20,71),(2050,'c15S1T','',1,1,4,45,20,71),(2051,'c14S1T','',1,1,4,45,20,71),(2052,'c13S1T','',1,1,4,45,20,71),(2053,'c12S1T','',1,1,4,45,20,71),(2054,'c11S1T','',1,1,4,45,20,71),(2055,'c66S1T','',1,2,2,45,19,71),(2056,'c55S1T','',1,2,2,45,19,71),(2057,'c46S1T','',1,2,2,45,19,71),(2058,'c44S1T','',1,2,2,45,19,71),(2059,'c35S1T','',1,2,2,45,19,71),(2060,'c33S1T','',1,2,2,45,19,71),(2061,'c25S1T','',1,2,2,45,19,71),(2062,'c23S1T','',1,2,2,45,19,71),(2063,'c22S1T','',1,2,2,45,19,71),(2064,'c15S1T','',1,2,2,45,19,71),(2065,'c13S1T','',1,2,2,45,19,71),(2066,'c12S1T','',1,2,2,45,19,71),(2067,'c11S1T','',1,2,2,45,19,71),(2068,'c66S1T','',1,2,3,45,19,71),(2069,'c55S1T','',1,2,3,45,19,71),(2070,'c45S1T','',1,2,3,45,19,71),(2071,'c44S1T','',1,2,3,45,19,71),(2072,'c36S1T','',1,2,3,45,19,71),(2073,'c33S1T','',1,2,3,45,19,71),(2074,'c26S1T','',1,2,3,45,19,71),(2075,'c23S1T','',1,2,3,45,19,71),(2076,'c22S1T','',1,2,3,45,19,71),(2077,'c16S1T','',1,2,3,45,19,71),(2078,'c13S1T','',1,2,3,45,19,71),(2079,'c12S1T','',1,2,3,45,19,71),(2080,'c11S1T','',1,2,3,45,19,71),(2081,'c66S1T','',1,3,4,45,18,71),(2082,'c55S1T','',1,3,4,45,18,71),(2083,'c44S1T','',1,3,4,45,18,71),(2084,'c33S1T','',1,3,4,45,18,71),(2085,'c23S1T','',1,3,4,45,18,71),(2086,'c22S1T','',1,3,4,45,18,71),(2087,'c13S1T','',1,3,4,45,18,71),(2088,'c12S1T','',1,3,4,45,18,71),(2089,'c11S1T','',1,3,4,45,18,71),(2090,'c44S1T','',1,4,4,45,16,71),(2091,'c12S1T','',1,4,4,45,16,71),(2092,'c11S1T','',1,4,4,45,16,71),(2093,'c66S1T','',1,5,4,45,2,71),(2094,'c44S1T','',1,5,4,45,2,71),(2095,'c33S1T','',1,5,4,45,2,71),(2096,'c16S1T','',1,5,4,45,2,71),(2097,'c13S1T','',1,5,4,45,2,71),(2098,'c12S1T','',1,5,4,45,2,71),(2099,'c11S1T','',1,5,4,45,2,71),(2100,'c66S1T','',1,5,4,45,1,71),(2101,'c44S1T','',1,5,4,45,1,71),(2102,'c33S1T','',1,5,4,45,1,71),(2103,'c13S1T','',1,5,4,45,1,71),(2104,'c12S1T','',1,5,4,45,1,71),(2105,'c11S1T','',1,5,4,45,1,71),(2106,'c44S1T','',1,6,4,45,4,71),(2107,'c33S1T','',1,6,4,45,4,71),(2108,'c25S1T','',1,6,4,45,4,71),(2109,'c14S1T','',1,6,4,45,4,71),(2110,'c13S1T','',1,6,4,45,4,71),(2111,'c12S1T','',1,6,4,45,4,71),(2112,'c11S1T','',1,6,4,45,4,71),(2113,'c44S1T','',1,6,4,45,3,71),(2114,'c33S1T','',1,6,4,45,3,71),(2115,'c14S1T','',1,6,4,45,3,71),(2116,'c13S1T','',1,6,4,45,3,71),(2117,'c12S1T','',1,6,4,45,3,71),(2118,'c11S1T','',1,6,4,45,3,71),(2119,'c12S1T','',1,7,4,45,15,71),(2120,'c11S1T','',1,7,4,45,15,71),(2121,'c44S1T','',1,8,4,45,17,71),(2122,'c33S1T','',1,8,4,45,17,71),(2123,'c13S1T','',1,8,4,45,17,71),(2124,'c12S1T','',1,8,4,45,17,71),(2125,'c11S1T','',1,8,4,45,17,71),(2126,'c66S2T','',1,1,4,45,20,72),(2127,'c56S2T','',1,1,4,45,20,72),(2128,'c55S2T','',1,1,4,45,20,72),(2129,'c46S2T','',1,1,4,45,20,72),(2130,'c45S2T','',1,1,4,45,20,72),(2131,'c44S2T','',1,1,4,45,20,72),(2132,'c35S2T','',1,1,4,45,20,72),(2133,'c36S2T','',1,1,4,45,20,72),(2134,'c34S2T','',1,1,4,45,20,72),(2135,'c33S2T','',1,1,4,45,20,72),(2136,'c26S2T','',1,1,4,45,20,72),(2137,'c25S2T','',1,1,4,45,20,72),(2138,'c24S2T','',1,1,4,45,20,72),(2139,'c23S2T','',1,1,4,45,20,72),(2140,'c22S2T','',1,1,4,45,20,72),(2141,'c16S2T','',1,1,4,45,20,72),(2142,'c15S2T','',1,1,4,45,20,72),(2143,'c14S2T','',1,1,4,45,20,72),(2144,'c13S2T','',1,1,4,45,20,72),(2145,'c12S2T','',1,1,4,45,20,72),(2146,'c11S2T','',1,1,4,45,20,72),(2147,'c66S2T','',1,2,2,45,19,72),(2148,'c55S2T','',1,2,2,45,19,72),(2149,'c46S2T','',1,2,2,45,19,72),(2150,'c44S2T','',1,2,2,45,19,72),(2151,'c35S2T','',1,2,2,45,19,72),(2152,'c33S2T','',1,2,2,45,19,72),(2153,'c25S2T','',1,2,2,45,19,72),(2154,'c23S2T','',1,2,2,45,19,72),(2155,'c22S2T','',1,2,2,45,19,72),(2156,'c15S2T','',1,2,2,45,19,72),(2157,'c13S2T','',1,2,2,45,19,72),(2158,'c12S2T','',1,2,2,45,19,72),(2159,'c11S2T','',1,2,2,45,19,72),(2160,'c66S2T','',1,2,3,45,19,72),(2161,'c55S2T','',1,2,3,45,19,72),(2162,'c45S2T','',1,2,3,45,19,72),(2163,'c44S2T','',1,2,3,45,19,72),(2164,'c36S2T','',1,2,3,45,19,72),(2165,'c33S2T','',1,2,3,45,19,72),(2166,'c26S2T','',1,2,3,45,19,72),(2167,'c23S2T','',1,2,3,45,19,72),(2168,'c22S2T','',1,2,3,45,19,72),(2169,'c16S2T','',1,2,3,45,19,72),(2170,'c13S2T','',1,2,3,45,19,72),(2171,'c12S2T','',1,2,3,45,19,72),(2172,'c11S2T','',1,2,3,45,19,72),(2173,'c66S2T','',1,3,4,45,18,72),(2174,'c55S2T','',1,3,4,45,18,72),(2175,'c44S2T','',1,3,4,45,18,72),(2176,'c33S2T','',1,3,4,45,18,72),(2177,'c23S2T','',1,3,4,45,18,72),(2178,'c22S2T','',1,3,4,45,18,72),(2179,'c13S2T','',1,3,4,45,18,72),(2180,'c12S2T','',1,3,4,45,18,72),(2181,'c11S2T','',1,3,4,45,18,72),(2182,'c44S2T','',1,4,4,45,16,72),(2183,'c12S2T','',1,4,4,45,16,72),(2184,'c11S2T','',1,4,4,45,16,72),(2185,'c66S2T','',1,5,4,45,2,72),(2186,'c44S2T','',1,5,4,45,2,72),(2187,'c33S2T','',1,5,4,45,2,72),(2188,'c16S2T','',1,5,4,45,2,72),(2189,'c13S2T','',1,5,4,45,2,72),(2190,'c12S2T','',1,5,4,45,2,72),(2191,'c11S2T','',1,5,4,45,2,72),(2192,'c66S2T','',1,5,4,45,1,72),(2193,'c44S2T','',1,5,4,45,1,72),(2194,'c33S2T','',1,5,4,45,1,72),(2195,'c13S2T','',1,5,4,45,1,72),(2196,'c12S2T','',1,5,4,45,1,72),(2197,'c11S2T','',1,5,4,45,1,72),(2198,'c44S2T','',1,6,4,45,4,72),(2199,'c33S2T','',1,6,4,45,4,72),(2200,'c25S2T','',1,6,4,45,4,72),(2201,'c14S2T','',1,6,4,45,4,72),(2202,'c13S2T','',1,6,4,45,4,72),(2203,'c12S2T','',1,6,4,45,4,72),(2204,'c11S2T','',1,6,4,45,4,72),(2205,'c44S2T','',1,6,4,45,3,72),(2206,'c33S2T','',1,6,4,45,3,72),(2207,'c14S2T','',1,6,4,45,3,72),(2208,'c13S2T','',1,6,4,45,3,72),(2209,'c12S2T','',1,6,4,45,3,72),(2210,'c11S2T','',1,6,4,45,3,72),(2211,'c12S2T','',1,7,4,45,15,72),(2212,'c11S2T','',1,7,4,45,15,72),(2213,'c44S2T','',1,8,4,45,17,72),(2214,'c33S2T','',1,8,4,45,17,72),(2215,'c13S2T','',1,8,4,45,17,72),(2216,'c12S2T','',1,8,4,45,17,72),(2217,'c11S2T','',1,8,4,45,17,72),(2218,'d35','',3,9,4,35,21,33),(2219,'d36','',3,9,4,35,21,33),(2220,'d34','',3,9,4,35,21,33),(2221,'d33','',3,9,4,35,21,33),(2222,'d32','',3,9,4,35,21,33),(2223,'d31','',3,9,4,35,21,33),(2224,'d26','',3,9,4,35,21,33),(2225,'d25','',3,9,4,35,21,33),(2226,'d24','',3,9,4,35,21,33),(2227,'d23','',3,9,4,35,21,33),(2228,'d22','',3,9,4,35,21,33),(2229,'d21','',3,9,4,35,21,33),(2230,'d16','',3,9,4,35,21,33),(2231,'d15','',3,9,4,35,21,33),(2232,'d14','',3,9,4,35,21,33),(2233,'d13','',3,9,4,35,21,33),(2234,'d12','',3,9,4,35,21,33),(2235,'d11','',3,9,4,35,21,33),(2236,'d36','',3,10,3,13,21,33),(2237,'d33','',3,10,3,13,21,33),(2238,'d32','',3,10,3,13,21,33),(2239,'d31','',3,10,3,13,21,33),(2240,'d25','',3,10,3,13,21,33),(2241,'d24','',3,10,3,13,21,33),(2242,'d15','',3,10,3,13,21,33),(2243,'d14','',3,10,3,13,21,33),(2244,'d36','',3,10,2,13,21,33),(2245,'d34','',3,10,2,13,21,33),(2246,'d25','',3,10,2,13,21,33),(2247,'d23','',3,10,2,13,21,33),(2248,'d22','',3,10,2,13,21,33),(2249,'d21','',3,10,2,13,21,33),(2250,'d16','',3,10,2,13,21,33),(2251,'d14','',3,10,2,13,21,33),(2252,'d35','',3,10,2,14,21,33),(2253,'d33','',3,10,2,14,21,33),(2254,'d32','',3,10,2,14,21,33),(2255,'d31','',3,10,2,14,21,33),(2256,'d26','',3,10,2,14,21,33),(2257,'d24','',3,10,2,14,21,33),(2258,'d15','',3,10,2,14,21,33),(2259,'d13','',3,10,2,14,21,33),(2260,'d12','',3,10,2,14,21,33),(2261,'d11','',3,10,2,14,21,33),(2262,'d35','',3,10,3,14,21,33),(2263,'d34','',3,10,3,14,21,33),(2264,'d26','',3,10,3,14,21,33),(2265,'d23','',3,10,3,14,21,33),(2266,'d22','',3,10,3,14,21,33),(2267,'d21','',3,10,3,14,21,33),(2268,'d16','',3,10,3,14,21,33),(2269,'d13','',3,10,3,14,21,33),(2270,'d12','',3,10,3,14,21,33),(2271,'d11','',3,10,3,14,21,33),(3086,'d14','',3,14,4,10,21,33),(3087,'d11','',3,14,4,10,21,33),(2277,'d36','',3,11,4,16,21,33),(2278,'d25','',3,11,4,16,21,33),(2279,'d14','',3,11,4,16,21,33),(2280,'d14','',3,12,4,45,8,33),(2281,'d36','',3,13,4,6,21,33),(2282,'d14','',3,13,4,6,21,33),(2283,'d33','',3,13,4,5,21,33),(2284,'d31','',3,13,4,5,21,33),(2285,'d15','',3,13,4,5,21,33),(2286,'d14','',3,13,4,4,21,33),(2287,'d36','',3,13,4,2,21,33),(2288,'d31','',3,13,4,2,21,33),(2289,'d15','',3,13,4,2,21,33),(2290,'d14','',3,13,4,2,21,33),(2291,'d33','',3,13,4,1,21,33),(2292,'d31','',3,13,4,1,21,33),(2293,'d15','',3,13,4,1,21,33),(2294,'d14','',3,13,4,1,21,33),(2295,'e14','',7,13,4,1,21,34),(2296,'e15','',7,13,4,1,21,34),(2297,'e31','',7,13,4,1,21,34),(2298,'e33','',7,13,4,1,21,34),(2299,'e14','',7,13,4,2,21,34),(2300,'e31','',7,13,4,2,21,34),(2301,'e15','',7,13,4,2,21,34),(2302,'e36','',7,13,4,2,21,34),(2303,'e15','',7,13,4,5,21,34),(2304,'e14','',7,13,4,4,21,34),(2305,'e31','',7,13,4,5,21,34),(2306,'e14','',7,13,4,6,21,34),(2307,'e33','',7,13,4,5,21,34),(2308,'e36','',7,13,4,6,21,34),(2309,'e14','',7,11,4,16,21,34),(2310,'e14','',7,12,4,45,8,34),(2311,'e25','',7,11,4,16,21,34),(2312,'e36','',7,11,4,16,21,34),(3099,'g11','',3,14,4,10,21,35),(2318,'e11','',7,10,3,14,21,34),(2319,'e12','',7,10,3,14,21,34),(2320,'e13','',7,10,3,14,21,34),(2321,'e16','',7,10,3,14,21,34),(2322,'e21','',7,10,3,14,21,34),(2323,'e22','',7,10,3,14,21,34),(2324,'e23','',7,10,3,14,21,34),(2325,'e26','',7,10,3,14,21,34),(2326,'e34','',7,10,3,14,21,34),(2327,'e35','',7,10,3,14,21,34),(2328,'e11','',7,10,2,14,21,34),(2329,'d12','',3,10,2,14,21,33),(2330,'e13','',7,10,2,14,21,34),(2331,'e15','',7,10,2,14,21,34),(2332,'e24','',7,10,2,14,21,34),(2333,'e26','',7,10,2,14,21,34),(2334,'e31','',7,10,2,14,21,34),(2335,'e32','',7,10,2,14,21,34),(2336,'e33','',7,10,2,14,21,34),(2337,'e35','',7,10,2,14,21,34),(2338,'e14','',7,10,2,13,21,34),(2339,'e16','',7,10,2,13,21,34),(2340,'e21','',7,10,2,13,21,34),(2341,'e22','',7,10,2,13,21,34),(2342,'e23','',7,10,2,13,21,34),(2343,'e25','',7,10,2,13,21,34),(2344,'e34','',7,10,2,13,21,34),(2345,'e36','',7,10,2,13,21,34),(2346,'e14','',7,10,3,13,21,34),(2347,'e15','',7,10,3,13,21,34),(2348,'e24','',7,10,3,13,21,34),(2349,'e25','',7,10,3,13,21,34),(2350,'e31','',7,10,3,13,21,34),(2351,'e32','',7,10,3,13,21,34),(2352,'e33','',7,10,3,13,21,34),(2353,'e36','',7,10,3,13,21,34),(2354,'e11','',7,9,4,35,21,34),(2355,'e12','',7,9,4,35,21,34),(2356,'e13','',7,9,4,35,21,34),(2357,'e14','',7,9,4,35,21,34),(2358,'e15','',7,9,4,35,21,34),(2359,'e16','',7,9,4,35,21,34),(2360,'e21','',7,9,4,35,21,34),(2361,'e23','',7,9,4,35,21,34),(2362,'e22','',7,9,4,35,21,34),(2363,'e24','',7,9,4,35,21,34),(2364,'e25','',7,9,4,35,21,34),(2365,'e26','',7,9,4,35,21,34),(2366,'e31','',7,9,4,35,21,34),(2367,'e32','',7,9,4,35,21,34),(2368,'e33','',7,9,4,35,21,34),(2369,'e34','',7,9,4,35,21,34),(2370,'e36','',7,9,4,35,21,34),(2371,'e35','',7,9,4,35,21,34),(2372,'g14','',3,13,4,1,21,35),(2373,'g15','',3,13,4,1,21,35),(2374,'g31','',3,13,4,1,21,35),(2375,'g33','',3,13,4,1,21,35),(2376,'g14','',3,13,4,2,21,35),(2377,'g31','',3,13,4,2,21,35),(2378,'g15','',3,13,4,2,21,35),(2379,'g36','',3,13,4,2,21,35),(2380,'g15','',3,13,4,5,21,35),(2381,'g14','',3,13,4,4,21,35),(2382,'g31','',3,13,4,5,21,35),(2383,'g14','',3,13,4,6,21,35),(2384,'g33','',3,13,4,5,21,35),(2385,'g36','',3,13,4,6,21,35),(2386,'g14','',3,11,4,16,21,35),(2387,'g14','',3,12,4,45,8,35),(2388,'g25','',3,11,4,16,21,35),(2389,'g36','',3,11,4,16,21,35),(3098,'g14','',3,14,4,10,21,35),(2395,'g11','',3,10,3,14,21,35),(2396,'g12','',3,10,3,14,21,35),(2397,'g13','',3,10,3,14,21,35),(2398,'g16','',3,10,3,14,21,35),(2399,'g21','',3,10,3,14,21,35),(2400,'g22','',3,10,3,14,21,35),(2401,'g23','',3,10,3,14,21,35),(2402,'g26','',3,10,3,14,21,35),(2403,'g34','',3,10,3,14,21,35),(2404,'g35','',3,10,3,14,21,35),(2405,'g11','',3,10,2,14,21,35),(2406,'g12','',3,10,2,14,21,35),(2407,'g13','',3,10,2,14,21,35),(2408,'g15','',3,10,2,14,21,35),(2409,'g24','',3,10,2,14,21,35),(2410,'g26','',3,10,2,14,21,35),(2411,'g31','',3,10,2,14,21,35),(2412,'g32','',3,10,2,14,21,35),(2413,'g33','',3,10,2,14,21,35),(2414,'g35','',3,10,2,14,21,35),(2415,'g14','',3,10,2,13,21,35),(2416,'g16','',3,10,2,13,21,35),(2417,'g21','',3,10,2,13,21,35),(2418,'g22','',3,10,2,13,21,35),(2419,'g23','',3,10,2,13,21,35),(2420,'g25','',3,10,2,13,21,35),(2421,'g34','',3,10,2,13,21,35),(2422,'g36','',3,10,2,13,21,35),(2423,'g14','',3,10,3,13,21,35),(2424,'g15','',3,10,3,13,21,35),(2425,'g24','',3,10,3,13,21,35),(2426,'g25','',3,10,3,13,21,35),(2427,'g31','',3,10,3,13,21,35),(2428,'g32','',3,10,3,13,21,35),(2429,'g33','',3,10,3,13,21,35),(2430,'g36','',3,10,3,13,21,35),(2431,'g11','',3,9,4,35,21,35),(2432,'g12','',3,9,4,35,21,35),(2433,'g13','',3,9,4,35,21,35),(2434,'g14','',3,9,4,35,21,35),(2435,'g15','',3,9,4,35,21,35),(2436,'g16','',3,9,4,35,21,35),(2437,'g21','',3,9,4,35,21,35),(2438,'g23','',3,9,4,35,21,35),(2439,'g22','',3,9,4,35,21,35),(2440,'g24','',3,9,4,35,21,35),(2441,'g25','',3,9,4,35,21,35),(2442,'g26','',3,9,4,35,21,35),(2443,'g31','',3,9,4,35,21,35),(2444,'g32','',3,9,4,35,21,35),(2445,'g33','',3,9,4,35,21,35),(2446,'g34','',3,9,4,35,21,35),(2447,'g36','',3,9,4,35,21,35),(2448,'g35','',3,9,4,35,21,35),(2449,'h14','',7,13,4,1,21,36),(2450,'h15','',7,13,4,1,21,36),(2451,'h31','',7,13,4,1,21,36),(2452,'h33','',7,13,4,1,21,36),(2453,'h14','',7,13,4,2,21,36),(2454,'h31','',7,13,4,2,21,36),(2455,'h15','',7,13,4,2,21,36),(2456,'h36','',7,13,4,2,21,36),(2457,'h15','',7,13,4,5,21,36),(2458,'h14','',7,13,4,4,21,36),(2459,'h31','',7,13,4,5,21,36),(2460,'h14','',7,13,4,6,21,36),(2461,'h33','',7,13,4,5,21,36),(2462,'h36','',7,13,4,6,21,36),(2463,'h14','',7,11,4,16,21,36),(2464,'h14','',7,12,4,45,8,36),(2465,'h25','',7,11,4,16,21,36),(2466,'h36','',7,11,4,16,21,36),(2472,'h11','',7,10,3,14,21,36),(2473,'h12','',7,10,3,14,21,36),(2474,'h13','',7,10,3,14,21,36),(2475,'h16','',7,10,3,14,21,36),(2476,'h21','',7,10,3,14,21,36),(2477,'h22','',7,10,3,14,21,36),(2478,'h23','',7,10,3,14,21,36),(2479,'h26','',7,10,3,14,21,36),(2480,'h34','',7,10,3,14,21,36),(2481,'h35','',7,10,3,14,21,36),(2482,'h11','',7,10,2,14,21,36),(2483,'h12','',7,10,2,14,21,36),(2484,'h13','',7,10,2,14,21,36),(2485,'h15','',7,10,2,14,21,36),(2486,'h24','',7,10,2,14,21,36),(2487,'h26','',7,10,2,14,21,36),(2488,'h31','',7,10,2,14,21,36),(2489,'h32','',7,10,2,14,21,36),(2490,'h33','',7,10,2,14,21,36),(2491,'h35','',7,10,2,14,21,36),(2492,'h14','',7,10,2,13,21,36),(2493,'h16','',7,10,2,13,21,36),(2494,'h21','',7,10,2,13,21,36),(2495,'h22','',7,10,2,13,21,36),(2496,'h23','',7,10,2,13,21,36),(2497,'h25','',7,10,2,13,21,36),(2498,'h34','',7,10,2,13,21,36),(2499,'h36','',7,10,2,13,21,36),(2500,'h14','',7,10,3,13,21,36),(2501,'h15','',7,10,3,13,21,36),(2502,'h24','',7,10,3,13,21,36),(2503,'h25','',7,10,3,13,21,36),(2504,'h31','',7,10,3,13,21,36),(2505,'h32','',7,10,3,13,21,36),(2506,'h33','',7,10,3,13,21,36),(2507,'h36','',7,10,3,13,21,36),(2508,'h11','',7,9,4,35,21,36),(2509,'h12','',7,9,4,35,21,36),(2510,'h13','',7,9,4,35,21,36),(2511,'h14','',7,9,4,35,21,36),(2512,'h15','',7,9,4,35,21,36),(2513,'h16','',7,9,4,35,21,36),(2514,'h21','',7,9,4,35,21,36),(2515,'h23','',7,9,4,35,21,36),(2516,'h22','',7,9,4,35,21,36),(2517,'h24','',7,9,4,35,21,36),(2518,'h25','',7,9,4,35,21,36),(2519,'h26','',7,9,4,35,21,36),(2520,'h31','',7,9,4,35,21,36),(2521,'h32','',7,9,4,35,21,36),(2522,'h33','',7,9,4,35,21,36),(2523,'h34','',7,9,4,35,21,36),(2524,'h36','',7,9,4,35,21,36),(2525,'h35','',7,9,4,35,21,36),(2526,'k14','',3,13,4,1,21,18),(2527,'k15','',3,13,4,1,21,18),(2528,'k31','',3,13,4,1,21,18),(2529,'k33','',3,13,4,1,21,18),(2530,'k14','',3,13,4,2,21,18),(2531,'k31','',3,13,4,2,21,18),(2532,'k15','',3,13,4,2,21,18),(2533,'k36','',3,13,4,2,21,18),(2534,'k15','',3,13,4,5,21,18),(2535,'k14','',3,13,4,4,21,18),(2536,'k31','',3,13,4,5,21,18),(2537,'k14','',3,13,4,6,21,18),(2538,'k33','',3,13,4,5,21,18),(2539,'k36','',3,13,4,6,21,18),(2540,'k14','',3,11,4,16,21,18),(2541,'k14','',3,12,4,45,8,18),(2542,'k25','',3,11,4,16,21,18),(2543,'k36','',3,11,4,16,21,18),(3092,'e14','',7,14,4,10,21,34),(2549,'k11','',3,10,3,14,21,18),(2550,'k12','',3,10,3,14,21,18),(2551,'k13','',3,10,3,14,21,18),(2552,'k16','',3,10,3,14,21,18),(2553,'k21','',3,10,3,14,21,18),(2554,'k22','',3,10,3,14,21,18),(2555,'k23','',3,10,3,14,21,18),(2556,'k26','',3,10,3,14,21,18),(2557,'k34','',3,10,3,14,21,18),(2558,'k35','',3,10,3,14,21,18),(2559,'k11','',3,10,2,14,21,18),(2560,'k12','',3,10,2,14,21,18),(2561,'k13','',3,10,2,14,21,18),(2562,'k15','',3,10,2,14,21,18),(2563,'k24','',3,10,2,14,21,18),(2564,'k26','',3,10,2,14,21,18),(2565,'k31','',3,10,2,14,21,18),(2566,'k32','',3,10,2,14,21,18),(2567,'k33','',3,10,2,14,21,18),(2568,'k35','',3,10,2,14,21,18),(2569,'k14','',3,10,2,13,21,18),(2570,'k16','',3,10,2,13,21,18),(2571,'k21','',3,10,2,13,21,18),(2572,'k22','',3,10,2,13,21,18),(2573,'k23','',3,10,2,13,21,18),(2574,'k25','',3,10,2,13,21,18),(2575,'k34','',3,10,2,13,21,18),(2576,'k36','',3,10,2,13,21,18),(2577,'k14','',3,10,3,13,21,18),(2578,'k15','',3,10,3,13,21,18),(2579,'k24','',3,10,3,13,21,18),(2580,'k25','',3,10,3,13,21,18),(2581,'k31','',3,10,3,13,21,18),(2582,'k32','',3,10,3,13,21,18),(2583,'k33','',3,10,3,13,21,18),(2584,'k36','',3,10,3,13,21,18),(2585,'k11','',3,9,4,35,21,18),(2586,'k12','',3,9,4,35,21,18),(2587,'k13','',3,9,4,35,21,18),(2588,'k14','',3,9,4,35,21,18),(2589,'k15','',3,9,4,35,21,18),(2590,'k16','',3,9,4,35,21,18),(2591,'k21','',3,9,4,35,21,18),(2592,'k23','',3,9,4,35,21,18),(2593,'k22','',3,9,4,35,21,18),(2594,'k24','',3,9,4,35,21,18),(2595,'k25','',3,9,4,35,21,18),(2596,'k26','',3,9,4,35,21,18),(2597,'k31','',3,9,4,35,21,18),(2598,'k32','',3,9,4,35,21,18),(2599,'k33','',3,9,4,35,21,18),(2600,'k34','',3,9,4,35,21,18),(2601,'k36','',3,9,4,35,21,18),(2602,'k35','',3,9,4,35,21,18),(2603,'d33','',3,14,4,8,21,33),(2604,'d31','',3,14,4,8,21,33),(2605,'d22','',3,14,4,8,21,33),(2606,'d15','',3,14,4,8,21,33),(2607,'d14','',3,14,4,8,21,33),(2612,'d33','',3,14,2,11,21,33),(2609,'d11','',3,14,4,8,21,33),(2613,'d31','',3,14,2,11,21,33),(2614,'d15','',3,14,2,11,21,33),(2615,'d14','',3,14,2,11,21,33),(2616,'d11','',3,14,2,11,21,33),(2617,'d33','',3,14,1,11,21,33),(2618,'d31','',3,14,1,11,21,33),(2619,'d22','',3,14,1,11,21,33),(2620,'d15','',3,14,1,11,21,33),(2621,'d14','',3,14,1,11,21,33),(2622,'e33','',7,14,4,8,21,34),(2623,'e31','',7,14,4,8,21,34),(2624,'e22','',7,14,4,8,21,34),(2625,'e15','',7,14,4,8,21,34),(2626,'e14','',7,14,4,8,21,34),(2627,'e33','',7,14,2,11,21,34),(2628,'e11','',7,14,4,8,21,34),(2630,'e11','',7,14,4,10,21,34),(2631,'e31','',7,14,2,11,21,34),(2632,'e15','',7,14,2,11,21,34),(2633,'e14','',7,14,2,11,21,34),(2634,'e11','',7,14,2,11,21,34),(2635,'e33','',7,14,1,11,21,34),(2636,'e31','',7,14,1,11,21,34),(2637,'e22','',7,14,1,11,21,34),(2638,'e15','',7,14,1,11,21,34),(2639,'e14','',7,14,1,11,21,34),(2640,'g33','',3,14,4,8,21,35),(2641,'g31','',3,14,4,8,21,35),(2642,'g22','',3,14,4,8,21,35),(2643,'g15','',3,14,4,8,21,35),(2644,'g14','',3,14,4,8,21,35),(2645,'g33','',3,14,2,11,21,35),(2646,'g11','',3,14,4,8,21,35),(2649,'g31','',3,14,2,11,21,35),(2650,'g15','',3,14,2,11,21,35),(2651,'g14','',3,14,2,11,21,35),(2652,'g11','',3,14,2,11,21,35),(2653,'g33','',3,14,1,11,21,35),(2654,'g31','',3,14,1,11,21,35),(2655,'g22','',3,14,1,11,21,35),(2656,'g15','',3,14,1,11,21,35),(2657,'g14','',3,14,1,11,21,35),(2658,'h33','',7,14,4,8,21,36),(2659,'h31','',7,14,4,8,21,36),(2660,'h22','',7,14,4,8,21,36),(2661,'h15','',7,14,4,8,21,36),(2662,'h14','',7,14,4,8,21,36),(2663,'h33','',7,14,2,11,21,36),(2664,'h11','',7,14,4,8,21,36),(2667,'h31','',7,14,2,11,21,36),(2668,'h15','',7,14,2,11,21,36),(2669,'h14','',7,14,2,11,21,36),(2670,'h11','',7,14,2,11,21,36),(2671,'h33','',7,14,1,11,21,36),(2672,'h31','',7,14,1,11,21,36),(2673,'h22','',7,14,1,11,21,36),(2674,'h15','',7,14,1,11,21,36),(2675,'h14','',7,14,1,11,21,36),(2676,'k33','',3,14,4,8,21,18),(2677,'k31','',3,14,4,8,21,18),(2678,'k22','',3,14,4,8,21,18),(2679,'k15','',3,14,4,8,21,18),(2680,'k14','',3,14,4,8,21,18),(2681,'k33','',3,14,2,11,21,18),(2682,'k11','',3,14,4,8,21,18),(2685,'k31','',3,14,2,11,21,18),(2686,'k15','',3,14,2,11,21,18),(2687,'k14','',3,14,2,11,21,18),(2688,'k11','',3,14,2,11,21,18),(2689,'k33','',3,14,1,11,21,18),(2690,'k31','',3,14,1,11,21,18),(2691,'k22','',3,14,1,11,21,18),(2692,'k15','',3,14,1,11,21,18),(2693,'k14','',3,14,1,11,21,18),(2694,'d11','',3,15,2,29,21,33),(2695,'d22','',3,15,1,29,21,33),(2696,'d22','',3,15,4,25,21,33),(2697,'d11','',3,15,4,25,21,33),(2698,'d14','',3,15,4,28,21,33),(2699,'d33','',3,15,4,27,21,33),(2700,'d31','',3,15,4,27,21,33),(2701,'d15','',3,15,4,27,21,33),(2702,'d33','',3,15,4,24,21,33),(2703,'d31','',3,15,4,24,21,33),(2704,'d15','',3,15,4,24,21,33),(2705,'d14','',3,15,4,24,21,33),(2706,'---',' ',7,15,4,30,21,34),(2707,'---',' ',7,15,4,26,21,34),(2708,'e11','',7,15,2,29,21,34),(2709,'e22','',7,15,1,29,21,34),(2710,'e22','',7,15,4,25,21,34),(2711,'e11','',7,15,4,25,21,34),(2712,'e14','',7,15,4,28,21,34),(2713,'e33','',7,15,4,27,21,34),(2714,'e31','',7,15,4,27,21,34),(2715,'e15','',7,15,4,27,21,34),(2716,'e33','',7,15,4,24,21,34),(2717,'e31','',7,15,4,24,21,34),(2718,'e15','',7,15,4,24,21,34),(2719,'e14','',7,15,4,24,21,34),(2720,'---',' ',7,15,4,30,21,34),(2721,'---',' ',7,15,4,26,21,34),(2722,'g11','',3,15,2,29,21,35),(2723,'g22','',3,15,1,29,21,35),(2724,'g22','',3,15,4,25,21,35),(2725,'g11','',3,15,4,25,21,35),(2726,'g14','',3,15,4,28,21,35),(2727,'g33','',3,15,4,27,21,35),(2728,'g31','',3,15,4,27,21,35),(2729,'g15','',3,15,4,27,21,35),(2730,'g33','',3,15,4,24,21,35),(2731,'g31','',3,15,4,24,21,35),(2732,'g15','',3,15,4,24,21,35),(2733,'g14','',3,15,4,24,21,35),(2734,'---',' ',7,15,4,30,21,34),(2735,'---',' ',7,15,4,26,21,34),(2736,'h11','',7,15,2,29,21,36),(2737,'h22','',7,15,1,29,21,36),(2738,'h22','',7,15,4,25,21,36),(2739,'h11','',7,15,4,25,21,36),(2740,'h14','',7,15,4,28,21,36),(2741,'h33','',7,15,4,27,21,36),(2742,'h31','',7,15,4,27,21,36),(2743,'h15','',7,15,4,27,21,36),(2744,'h33','',7,15,4,24,21,36),(2745,'h31','',7,15,4,24,21,36),(2746,'h15','',7,15,4,24,21,36),(2747,'h14','',7,15,4,24,21,36),(2748,'---',' ',7,15,4,30,21,34),(2749,'---',' ',7,15,4,26,21,34),(2750,'k11','',3,15,2,29,21,18),(2751,'k22','',3,15,1,29,21,18),(2752,'k22','',3,15,4,25,21,18),(2753,'k11','',3,15,4,25,21,18),(2754,'k14','',3,15,4,28,21,18),(2755,'k33','',3,15,4,27,21,18),(2756,'k31','',3,15,4,27,21,18),(2757,'k15','',3,15,4,27,21,18),(2758,'k33','',3,15,4,24,21,18),(2759,'k31','',3,15,4,24,21,18),(2760,'k15','',3,15,4,24,21,18),(2761,'k14','',3,15,4,24,21,18),(2762,'---',' ',7,15,4,30,21,34),(2763,'---',' ',7,15,4,26,21,34),(2840,'epsr23S','k23',4,16,4,45,20,2),(2839,'epsr22S','k22',4,16,4,45,20,2),(2838,'epsr13S','k13',4,16,4,45,20,2),(2837,'epsr12S','k12',4,16,4,45,20,2),(2836,'epsr11S','k11',4,16,4,45,20,2),(2835,'epsr33S','k33',4,17,4,45,19,2),(2834,'epsr13S','k13',4,17,4,45,19,2),(2833,'epsr22S','k22',4,17,4,45,19,2),(2832,'epsr11S','k11',4,17,4,45,19,2),(2831,'epsr11','k11',4,19,4,45,15,1),(2830,'epsr11','k11',4,19,4,45,16,1),(2829,'epsr11','k11',4,20,4,45,38,1),(2828,'epsr33','k33',4,20,4,45,38,1),(2827,'epsr33','k33',4,18,4,45,18,1),(2826,'epsr22','k22',4,18,4,45,18,1),(2825,'epsr11','k11',4,18,4,45,18,1),(2824,'epsr33','k33',4,16,4,45,20,1),(2823,'epsr23','k23',4,16,4,45,20,1),(2822,'epsr22','k22',4,16,4,45,20,1),(2821,'epsr13','k13',4,16,4,45,20,1),(2820,'epsr12','k12',4,16,4,45,20,1),(2819,'epsr11','k11',4,16,4,45,20,1),(2818,'epsr33','k33',4,17,4,45,19,1),(2817,'epsr13','k13',4,17,4,45,19,1),(2816,'epsr22','k22',4,17,4,45,19,1),(2815,'epsr11','k11',4,17,4,45,19,1),(2841,'epsr33S','k33',4,16,4,45,20,2),(2842,'epsr11S','k11',4,18,4,45,18,2),(2843,'epsr22S','k22',4,18,4,45,18,2),(2844,'epsr33S','k33',4,18,4,45,18,2),(2845,'epsr33S','k33',4,20,4,45,38,2),(2846,'epsr11S','k11',4,20,4,45,38,2),(2847,'epsr11S','k11',4,19,4,45,16,2),(2848,'epsr11S','k11',4,19,4,45,15,2),(2849,'epsr11T','k11',4,17,4,45,19,3),(2850,'epsr22T','k22',4,17,4,45,19,3),(2851,'epsr13T','k13',4,17,4,45,19,3),(2852,'epsr33T','k33',4,17,4,45,19,3),(2853,'epsr11T','k11',4,16,4,45,20,3),(2854,'epsr12T','k12',4,16,4,45,20,3),(2855,'epsr13T','k13',4,16,4,45,20,3),(2856,'epsr22T','k22',4,16,4,45,20,3),(2857,'epsr23T','k23',4,16,4,45,20,3),(2858,'epsr33T','k33',4,16,4,45,20,3),(2859,'epsr11T','k11',4,18,4,45,18,3),(2860,'epsr22T','k22',4,18,4,45,18,3),(2861,'epsr33T','k33',4,18,4,45,18,3),(2862,'epsr33T','k33',4,20,4,45,38,3),(2863,'epsr11T','k11',4,20,4,45,38,3),(2864,'epsr11T','k11',4,19,4,45,16,3),(2865,'epsr11T','k11',4,19,4,45,15,3),(2866,'betr11S','k11',4,17,4,45,19,4),(2867,'betr22S','k22',4,17,4,45,19,4),(2868,'betr13S','k13',4,17,4,45,19,4),(2869,'betr33S','k33',4,17,4,45,19,4),(2870,'betr11S','k11',4,16,4,45,20,4),(2871,'betr12S','k12',4,16,4,45,20,4),(2872,'betr13S','k13',4,16,4,45,20,4),(2873,'betr22S','k22',4,16,4,45,20,4),(2874,'betr23S','k23',4,16,4,45,20,4),(2875,'betr33S','k33',4,16,4,45,20,4),(2876,'betr11S','k11',4,18,4,45,18,4),(2877,'betr22S','k22',4,18,4,45,18,4),(2878,'betr33S','k33',4,18,4,45,18,4),(2879,'betr33S','k33',4,20,4,45,38,4),(2880,'betr11S','k11',4,20,4,45,38,4),(2881,'betr11S','k11',4,19,4,45,16,4),(2882,'betr11S','k11',4,19,4,45,15,4),(2883,'betr11T','k11',4,17,4,45,19,5),(2884,'betr22T','k22',4,17,4,45,19,5),(2885,'betr13T','k13',4,17,4,45,19,5),(2886,'betr33T','k33',4,17,4,45,19,5),(2887,'betr11T','k11',4,16,4,45,20,5),(2888,'betr12T','k12',4,16,4,45,20,5),(2889,'betr13T','k13',4,16,4,45,20,5),(2890,'betr22T','k22',4,16,4,45,20,5),(2891,'betr23T','k23',4,16,4,45,20,5),(2892,'betr33T','k33',4,16,4,45,20,5),(2893,'betr11T','k11',4,18,4,45,18,5),(2894,'betr22T','k22',4,18,4,45,18,5),(2895,'betr33T','k33',4,18,4,45,18,5),(2896,'betr33T','k33',4,20,4,45,38,5),(2897,'betr11T','k11',4,20,4,45,38,5),(2898,'betr11T','k11',4,19,4,45,16,5),(2899,'betr11T','k11',4,19,4,45,15,5),(2900,'rhoe11','k11',4,17,4,45,19,17),(2901,'rhoe22','k22',4,17,4,45,19,17),(2902,'rhoe13','k13',4,17,4,45,19,17),(2903,'rhoe33','k33',4,17,4,45,19,17),(2904,'rhoe11','k11',4,16,4,45,20,17),(2905,'rhoe12','k12',4,16,4,45,20,17),(2906,'rhoe13','k13',4,16,4,45,20,17),(2907,'rhoe22','k22',4,16,4,45,20,17),(2908,'rhoe23','k23',4,16,4,45,20,17),(2909,'rhoe33','k33',4,16,4,45,20,17),(2910,'rhoe11','k11',4,18,4,45,18,17),(2911,'rhoe22','k22',4,18,4,45,18,17),(2912,'rhoe33','k33',4,18,4,45,18,17),(2913,'rhoe33','k33',4,20,4,45,38,17),(2914,'rhoe11','k11',4,20,4,45,38,17),(2915,'rhoe11','k11',4,19,4,45,16,17),(2916,'rhoe11','k11',4,19,4,45,15,17),(2917,'kappa11','k11',4,17,4,45,19,53),(2918,'kappa22','k22',4,17,4,45,19,53),(2919,'kappa13','k13',4,17,4,45,19,53),(2920,'kappa33','k33',4,17,4,45,19,53),(2921,'kappa11','k11',4,16,4,45,20,53),(2922,'kappa12','k12',4,16,4,45,20,53),(2923,'kappa13','k13',4,16,4,45,20,53),(2924,'kappa22','k22',4,16,4,45,20,53),(2925,'kappa23','k23',4,16,4,45,20,53),(2926,'kappa33','k33',4,16,4,45,20,53),(2927,'kappa11','k11',4,18,4,45,18,53),(2928,'kappa22','k22',4,18,4,45,18,53),(2929,'kappa33','k33',4,18,4,45,18,53),(2930,'kappa33','k33',4,20,4,45,38,53),(2931,'kappa11','k11',4,20,4,45,38,53),(2932,'kappa11','k11',4,19,4,45,16,53),(2933,'kappa11','k11',4,19,4,45,15,53),(2934,'kappad11','k11',4,17,4,45,19,54),(2935,'kappad22','k22',4,17,4,45,19,54),(2936,'kappad13','k13',4,17,4,45,19,54),(2937,'kappad33','k33',4,17,4,45,19,54),(2938,'kappad11','k11',4,16,4,45,20,54),(2939,'kappad12','k12',4,16,4,45,20,54),(2940,'kappad13','k13',4,16,4,45,20,54),(2941,'kappad22','k22',4,16,4,45,20,54),(2942,'kappad23','k23',4,16,4,45,20,54),(2943,'kappad33','k33',4,16,4,45,20,54),(2944,'kappad11','k11',4,18,4,45,18,54),(2945,'kappad22','k22',4,18,4,45,18,54),(2946,'kappad33','k33',4,18,4,45,18,54),(2947,'kappad33','k33',4,20,4,45,38,54),(2948,'kappad11','k11',4,20,4,45,38,54),(2949,'kappad11','k11',4,19,4,45,16,54),(2950,'kappad11','k11',4,19,4,45,15,54),(2951,'alpha11','k11',4,17,4,45,19,56),(2952,'alpha22','k22',4,17,4,45,19,56),(2953,'alpha13','k13',4,17,4,45,19,56),(2954,'alpha33','k33',4,17,4,45,19,56),(2955,'alpha11','k11',4,16,4,45,20,56),(2956,'alpha12','k12',4,16,4,45,20,56),(2957,'alpha13','k13',4,16,4,45,20,56),(2958,'alpha22','k22',4,16,4,45,20,56),(2959,'alpha23','k23',4,16,4,45,20,56),(2960,'alpha33','k33',4,16,4,45,20,56),(2961,'alpha11','k11',4,18,4,45,18,56),(2962,'alpha22','k22',4,18,4,45,18,56),(2963,'alpha33','k33',4,18,4,45,18,56),(2964,'alpha33','k33',4,20,4,45,38,56),(2965,'alpha11','k11',4,20,4,45,38,56),(2966,'alpha11','k11',4,19,4,45,16,56),(2967,'alpha11','k11',4,19,4,45,15,56),(2968,'Se11','k11',4,17,4,45,19,60),(2969,'Se22','k22',4,17,4,45,19,60),(2970,'Se13','k13',4,17,4,45,19,60),(2971,'Se33','k33',4,17,4,45,19,60),(2972,'Se11','k11',4,16,4,45,20,60),(2973,'Se12','k12',4,16,4,45,20,60),(2974,'Se13','k13',4,16,4,45,20,60),(2975,'Se22','k22',4,16,4,45,20,60),(2976,'Se23','k23',4,16,4,45,20,60),(2977,'Se33','k33',4,16,4,45,20,60),(2978,'Se11','k11',4,18,4,45,18,60),(2979,'Se22','k22',4,18,4,45,18,60),(2980,'Se33','k33',4,18,4,45,18,60),(2981,'Se33','k33',4,20,4,45,38,60),(2982,'Se11','k11',4,20,4,45,38,60),(2983,'Se11','k11',4,19,4,45,16,60),(2984,'Se11','k11',4,19,4,45,15,60),(3163,'MEalpha11','',11,17,4,45,43,76),(3162,'MEalpha13','',11,17,4,45,43,76),(3161,'MEalpha22','',11,17,4,45,43,76),(3159,'MEalpha33','',11,17,4,45,43,76),(3158,'MEalpha11','',11,16,4,45,39,76),(3157,'MEalpha12','',11,16,4,45,39,76),(3156,'MEalpha13','',11,16,4,45,39,76),(3154,'MEalpha22','',11,16,4,45,39,76),(3153,'MEalpha23','',11,16,4,45,39,76),(3150,'MEalpha33','',11,16,4,45,39,76),(3187,'alpha22T0','',4,16,4,45,20,74),(3186,'alpha23T0','',4,16,4,45,20,74),(3185,'alpha33T0','',4,16,4,45,20,74),(3002,'s44','',2,8,4,45,17,7),(3003,'s33','',2,8,4,45,17,7),(3004,'s13','',2,8,4,45,17,7),(3005,'s12','',2,8,4,45,17,7),(3006,'s11','',2,8,4,45,17,7),(3061,'e24','',7,11,4,17,21,34),(3060,'e15','',7,11,4,17,21,34),(3059,'d15','',3,11,4,17,21,33),(3058,'d24','',3,11,4,17,21,33),(3057,'d31','',3,11,4,17,21,33),(3111,'k11','',3,14,4,10,21,18),(3110,'k14','',3,14,4,10,21,18),(3018,'c46','',1,2,2,45,19,10),(3105,'h11','',7,14,4,10,21,36),(3104,'h14','',7,14,4,10,21,36),(3079,'h33',' ',7,11,4,17,21,36),(3080,'k32',' ',3,11,4,17,21,18),(3081,'k33',' ',3,11,4,17,21,18),(3075,'e33',' ',7,11,4,17,21,34),(3076,'g32',' ',3,11,4,17,21,35),(3077,'g33',' ',3,11,4,17,21,35),(3078,'h32',' ',7,11,4,17,21,36),(3071,'k31','',3,11,4,17,21,18),(3072,'d32',' ',3,11,4,17,21,33),(3073,'d33',' ',3,11,4,17,21,33),(3074,'e32',' ',7,11,4,17,21,34),(3067,'h24','',7,11,4,17,21,36),(3068,'h31','',7,11,4,17,21,36),(3069,'k15','',3,11,4,17,21,18),(3070,'k24','',3,11,4,17,21,18),(3062,'e31','',7,11,4,17,21,34),(3063,'g15','',3,11,4,17,21,35),(3064,'g24','',3,11,4,17,21,35),(3065,'g31','',3,11,4,17,21,35),(3066,'h15','',7,11,4,17,21,36),(3118,'e33','',7,14,4,11,21,34),(3119,'e31','',7,14,4,11,21,34),(3120,'e22','',7,14,4,11,21,34),(3121,'e15','',7,14,4,11,21,34),(3122,'e14','',7,14,4,11,21,34),(3123,'e11','',7,14,4,11,21,34),(3124,'g33','',3,14,4,11,21,35),(3125,'g31','',3,14,4,11,21,35),(3126,'g22','',3,14,4,11,21,35),(3127,'g15','',3,14,4,11,21,35),(3128,'g14','',3,14,4,11,21,35),(3129,'g11','',3,14,4,11,21,35),(3130,'h33','',7,14,4,11,21,36),(3131,'h31','',7,14,4,11,21,36),(3132,'h22','',7,14,4,11,21,36),(3133,'h15','',7,14,4,11,21,36),(3134,'h14','',7,14,4,11,21,36),(3135,'h11','',7,14,4,11,21,36),(3136,'k33','',3,14,4,11,21,18),(3137,'k31','',3,14,4,11,21,18),(3138,'k22','',3,14,4,11,21,18),(3139,'k15','',3,14,4,11,21,18),(3140,'k14','',3,14,4,11,21,18),(3141,'k11','',3,14,4,11,21,18),(3165,'MEalpha23','',11,17,4,45,44,76),(3167,'MEalpha12','',11,17,4,45,44,76),(3168,'MEalpha33','',11,18,4,45,45,76),(3169,'MEalpha22','',11,18,4,45,45,76),(3170,'MEalpha11','',11,18,4,45,45,76),(3172,'MEalpha23','',11,18,4,45,46,76),(3173,'MEalpha33','',11,20,4,45,47,76),(3188,'alpha13T0','',4,16,4,45,20,74),(3175,'MEalpha12','',11,20,4,45,47,76),(3176,'MEalpha11','',11,20,4,45,47,76),(3177,'MEalpha33','',11,20,4,45,49,76),(3178,'MEalpha11','',11,20,4,45,49,76),(3179,'MEalpha12','',11,20,4,45,51,76),(3189,'alpha12T0','',4,16,4,45,20,74),(3181,'MEalpha12','',11,26,4,45,48,76),(3182,'MEalpha11','',11,26,4,45,48,76),(3183,'MEalpha11','',11,26,4,45,50,76),(3184,'MEalpha11','',11,19,4,45,52,76),(3190,'alpha11T0','',4,16,4,45,20,74),(3191,'alpha33T','',4,16,4,45,20,75),(3192,'alpha23T','',4,16,4,45,20,75),(3193,'alpha22T','',4,16,4,45,20,75),(3194,'alpha13T','',4,16,4,45,20,75),(3195,'alpha12T','',4,16,4,45,20,75),(3196,'alpha11T','',4,16,4,45,20,75),(3197,'alpha33T0','',4,17,4,45,19,74),(3198,'alpha22T0','',4,17,4,45,19,74),(3199,'alpha13T0','',4,17,4,45,19,74),(3200,'alpha11T0','',4,17,4,45,19,74),(3201,'alpha33T','',4,17,4,45,19,75),(3202,'alpha22T','',4,17,4,45,19,75),(3203,'alpha13T','',4,17,4,45,19,75),(3204,'alpha11T','',4,17,4,45,19,75),(3205,'alpha33T0','',4,18,4,45,18,74),(3206,'alpha22T0','',4,18,4,45,18,74),(3207,'alpha11T0','',4,18,4,45,18,74),(3208,'alpha33T','',4,18,4,45,18,75),(3209,'alpha22T','',4,18,4,45,18,75),(3210,'alpha11T','',4,18,4,45,18,75),(3211,'alpha11T0','',4,19,4,45,15,74),(3212,'alpha11T','',4,19,4,45,15,75),(3213,'alpha33T','',4,20,4,45,38,75),(3214,'alpha11T','',4,20,4,45,38,75),(3215,'alpha33T0','',4,20,4,45,38,74),(3216,'alpha11T0','',4,20,4,45,38,74),(3217,'s441T','',2,4,4,45,16,57),(3218,'e36','',7,10,4,45,19,34),(3219,'e34','',7,10,4,45,19,34),(3220,'e25','',7,10,4,45,19,34),(3221,'e23','',7,10,4,45,19,34),(3222,'e22','',7,10,4,45,19,34),(3223,'e21','',7,10,4,45,19,34),(3224,'e16','',7,10,4,45,19,34),(3225,'e14','',7,10,4,45,19,34),(3226,'e36','',7,10,2,45,19,34),(3227,'e34','',7,10,2,45,19,34),(3228,'e25','',7,10,2,45,19,34),(3229,'e23','',7,10,2,45,19,34),(3230,'e22','',7,10,2,45,19,34),(3231,'e21','',7,10,2,45,19,34),(3232,'e16','',7,10,2,45,19,34),(3233,'e14','',7,10,2,45,19,34),(3234,'e36','',7,10,3,45,19,34),(3235,'e34','',7,10,3,45,19,34),(3236,'e25','',7,10,3,45,19,34),(3237,'e23','',7,10,3,45,19,34),(3238,'e22','',7,10,3,45,19,34),(3239,'e21','',7,10,3,45,19,34),(3240,'e16','',7,10,3,45,19,34),(3241,'e14','',7,10,3,45,19,34),(3242,'h36','',7,10,2,45,19,36),(3243,'h34','',7,10,2,45,19,36),(3244,'h25','',7,10,2,45,19,36),(3245,'h23','',7,10,2,45,19,36),(3246,'h22','',7,10,2,45,19,36),(3247,'h21','',7,10,2,45,19,36),(3248,'h16','',7,10,2,45,19,36),(3249,'h14','',7,10,2,45,19,36),(3250,'h36','',7,10,3,45,19,36),(3251,'h34','',7,10,3,45,19,36),(3252,'h25','',7,10,3,45,19,36),(3253,'h23','',7,10,3,45,19,36),(3254,'h22','',7,10,3,45,19,36),(3255,'h21','',7,10,3,45,19,36),(3256,'h16','',7,10,3,45,19,36),(3257,'h14','',7,10,3,45,19,36),(3258,'e12','',7,10,2,14,21,34),(3259,'alpha11T0','',4,19,4,45,16,74),(3260,'alpha11T','',4,19,4,45,16,75);
/*!40000 ALTER TABLE `catalog_property_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalog_property_detail_old`
--

DROP TABLE IF EXISTS `catalog_property_detail_old`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalog_property_detail_old` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(511) DEFAULT NULL,
  `type_id` int(11) NOT NULL,
  `crystalsystem_id` int(11) NOT NULL,
  `catalogaxis_id` int(11) DEFAULT NULL,
  `catalogpointgroup_id` int(11) DEFAULT NULL,
  `puntualgroupnames_id` int(11) DEFAULT NULL,
  `dataproperty_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=782 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalog_property_detail_old`
--

LOCK TABLES `catalog_property_detail_old` WRITE;
/*!40000 ALTER TABLE `catalog_property_detail_old` DISABLE KEYS */;
INSERT INTO `catalog_property_detail_old` VALUES (163,'s44','',2,4,4,45,16,NULL),(162,'s12','',2,4,4,45,16,NULL),(161,'s11','',2,4,4,45,16,NULL),(160,'c44','',1,4,4,45,16,NULL),(159,'c12','',1,4,4,45,16,NULL),(158,'c11','',1,4,4,45,16,NULL),(157,'s12','',2,7,4,45,15,NULL),(156,'s11','',2,7,4,45,15,NULL),(155,'c12','',1,7,4,45,15,NULL),(154,'c11','',1,7,4,45,15,NULL),(153,'s66','',2,1,4,45,20,7),(152,'s56','',2,1,4,45,20,7),(151,'s55','',2,1,4,45,20,7),(150,'s46','',2,1,4,45,20,7),(149,'s45','',2,1,4,45,20,7),(148,'s44','',2,1,4,45,20,7),(147,'s36','',2,1,4,45,20,7),(146,'s35','',2,1,4,45,20,7),(145,'s34','',2,1,4,45,20,7),(144,'s33','',2,1,4,45,20,7),(143,'s26','',2,1,4,45,20,7),(142,'s25','',2,1,4,45,20,7),(141,'s24','',2,1,4,45,20,7),(140,'s23','',2,1,4,45,20,7),(139,'s22','',2,1,4,45,20,7),(138,'s16','',2,1,4,45,20,7),(137,'s15','',2,1,4,45,20,7),(136,'s14','',2,1,4,45,20,7),(135,'s13','',2,1,4,45,20,7),(134,'s12','',2,1,4,45,20,7),(133,'s11','',2,1,4,45,20,7),(132,'c66','',1,1,4,45,20,10),(131,'c56','',1,1,4,45,20,10),(130,'c55','',1,1,4,45,20,10),(129,'c46','',1,1,4,45,20,10),(128,'c45','',1,1,4,45,20,10),(127,'c44','',1,1,4,45,20,10),(126,'c36','',1,1,4,45,20,10),(125,'c35','',1,1,4,45,20,10),(124,'c34','',1,1,4,45,20,10),(123,'c33','',1,1,4,45,20,10),(122,'c26','',1,1,4,45,20,10),(121,'c25','',1,1,4,45,20,10),(120,'c24','',1,1,4,45,20,10),(119,'c23','',1,1,4,45,20,10),(118,'c22','',1,1,4,45,20,10),(117,'c16','',1,1,4,45,20,10),(116,'c15','',1,1,4,45,20,10),(115,'c14','',1,1,4,45,20,10),(114,'c13','',1,1,4,45,20,10),(113,'c12','',1,1,4,45,20,10),(112,'c11','',1,1,4,45,20,10),(215,'s66','',2,2,2,45,19,NULL),(214,'s55','',2,2,2,45,19,NULL),(213,'s46','',2,2,2,45,19,NULL),(212,'s44','',2,2,2,45,19,NULL),(211,'s35','',2,2,2,45,19,NULL),(210,'s33','',2,2,2,45,19,NULL),(209,'s25','',2,2,2,45,19,NULL),(208,'s23','',2,2,2,45,19,NULL),(207,'s22','',2,2,2,45,19,NULL),(206,'s15','',2,2,2,45,19,NULL),(205,'s13','',2,2,2,45,19,NULL),(204,'s12','',2,2,2,45,19,NULL),(203,'s11','',2,2,2,45,19,NULL),(202,'c66','',1,2,2,45,19,NULL),(201,'c55','',1,2,2,45,19,NULL),(200,'c46','',1,2,2,45,19,NULL),(199,'c44','',1,2,2,45,19,NULL),(198,'c35','',1,2,2,45,19,NULL),(197,'c33','',1,2,2,45,19,NULL),(196,'c25','',1,2,2,45,19,NULL),(195,'c23','',1,2,2,45,19,NULL),(194,'c22','',1,2,2,45,19,NULL),(193,'c15','',1,2,2,45,19,NULL),(192,'c13','',1,2,2,45,19,NULL),(191,'c12','',1,2,2,45,19,NULL),(190,'c11','',1,2,2,45,19,NULL),(216,'c11','',1,3,4,45,18,NULL),(217,'c12','',1,3,4,45,18,NULL),(218,'c13','',1,3,4,45,18,NULL),(219,'c22','',1,3,4,45,18,NULL),(220,'c23','',1,3,4,45,18,NULL),(221,'c33','',1,3,4,45,18,NULL),(222,'c44','',1,3,4,45,18,NULL),(223,'c55','',1,3,4,45,18,NULL),(224,'c66','',1,3,4,45,18,NULL),(225,'s11','',2,3,4,45,18,NULL),(226,'s12','',2,3,4,45,18,NULL),(227,'s13','',2,3,4,45,18,NULL),(228,'s22','',2,3,4,45,18,NULL),(229,'s23','',2,3,4,45,18,NULL),(230,'s33','',2,3,4,45,18,NULL),(231,'s44','',2,3,4,45,18,NULL),(232,'s55','',2,3,4,45,18,NULL),(233,'s66','',2,3,4,45,18,NULL),(693,'d25','',3,10,3,13,21,NULL),(596,'d15','',3,10,2,14,21,NULL),(692,'d24','',3,10,3,13,21,NULL),(595,'d13','',3,10,2,14,21,NULL),(691,'d15','',3,10,3,13,21,NULL),(594,'d12','',3,10,2,14,21,NULL),(690,'d14','',3,10,3,13,21,NULL),(593,'d11','',3,10,2,14,21,NULL),(695,'d32','',3,10,3,13,21,NULL),(592,'d36','',3,10,2,13,21,NULL),(694,'d31','',3,10,3,13,21,NULL),(591,'d34','',3,10,2,13,21,NULL),(590,'d25','',3,10,2,13,21,NULL),(589,'d23','',3,10,2,13,21,NULL),(588,'d22','',3,10,2,13,21,NULL),(587,'d21','',3,10,2,13,21,NULL),(586,'d16','',3,10,2,13,21,NULL),(585,'d14','',3,10,2,13,21,NULL),(258,'c11','',1,8,4,45,17,NULL),(259,'c12','',1,8,4,45,17,NULL),(260,'c13','',1,8,4,45,17,NULL),(261,'c33','',1,8,4,45,17,NULL),(262,'c44','',1,8,4,45,17,NULL),(263,'s11','',2,8,4,45,17,NULL),(264,'s12','',2,8,4,45,17,NULL),(265,'s13','',2,8,4,45,17,NULL),(266,'s33','',2,8,4,45,17,NULL),(267,'s44','',2,8,4,45,17,NULL),(268,'s11','',2,2,3,45,19,NULL),(269,'s12','',2,2,3,45,19,NULL),(270,'s13','',2,2,3,45,19,NULL),(271,'s16','',2,2,3,45,19,NULL),(272,'s22','',2,2,3,45,19,NULL),(273,'s23','',2,2,3,45,19,NULL),(274,'s26','',2,2,3,45,19,NULL),(275,'s33','',2,2,3,45,19,NULL),(276,'s36','',2,2,3,45,19,NULL),(277,'s44','',2,2,3,45,19,NULL),(278,'s45','',2,2,3,45,19,NULL),(279,'s55','',2,2,3,45,19,NULL),(280,'s66','',2,2,3,45,19,NULL),(281,'c11','',1,2,3,45,19,NULL),(282,'c12','',1,2,3,45,19,NULL),(283,'c13','',1,2,3,45,19,NULL),(284,'c16','',1,2,3,45,19,NULL),(285,'c22','',1,2,3,45,19,NULL),(286,'c23','',1,2,3,45,19,NULL),(287,'c26','',1,2,3,45,19,NULL),(288,'c33','',1,2,3,45,19,NULL),(289,'c36','',1,2,3,45,19,NULL),(290,'c44','',1,2,3,45,19,NULL),(291,'c45','',1,2,3,45,19,NULL),(292,'c55','',1,2,3,45,19,NULL),(293,'c66','',1,2,3,45,19,NULL),(762,'---',' ',3,15,4,26,21,NULL),(761,'---',' ',3,15,4,30,21,NULL),(760,'---',' ',3,14,4,12,21,NULL),(759,'---',' ',3,14,4,9,21,NULL),(758,'---',' ',3,12,4,45,9,NULL),(566,'s44','',2,6,4,45,4,NULL),(565,'s33','',2,6,4,45,4,NULL),(564,'s25','',2,6,4,45,4,NULL),(563,'s14','',2,6,4,45,4,NULL),(562,'s13','',2,6,4,45,4,NULL),(561,'s12','',2,6,4,45,4,NULL),(560,'s11','',2,6,4,45,4,NULL),(559,'c44','',1,6,4,45,4,NULL),(558,'c33','',1,6,4,45,4,NULL),(557,'c25','',1,6,4,45,4,NULL),(556,'c14','',1,6,4,45,4,NULL),(555,'c13','',1,6,4,45,4,NULL),(554,'c12','',1,6,4,45,4,NULL),(553,'c11','',1,6,4,45,4,NULL),(552,'s44','',2,6,4,45,3,NULL),(551,'s33','',2,6,4,45,3,NULL),(550,'s14','',2,6,4,45,3,NULL),(549,'s13','',2,6,4,45,3,NULL),(548,'s12','',2,6,4,45,3,NULL),(547,'s11','',2,6,4,45,3,NULL),(546,'c44','',1,6,4,45,3,NULL),(545,'c33','',1,6,4,45,3,NULL),(544,'c14','',1,6,4,45,3,NULL),(543,'c13','',1,6,4,45,3,NULL),(542,'c12','',1,6,4,45,3,NULL),(541,'c11','',1,6,4,45,3,NULL),(397,'s66','',2,5,4,45,2,NULL),(396,'s44','',2,5,4,45,2,NULL),(395,'s33','',2,5,4,45,2,NULL),(394,'s16','',2,5,4,45,2,NULL),(393,'s13','',2,5,4,45,2,NULL),(392,'s12','',2,5,4,45,2,NULL),(391,'s11','',2,5,4,45,2,NULL),(754,'c66','',1,5,4,45,2,NULL),(389,'c44','',1,5,4,45,2,NULL),(388,'c33','',1,5,4,45,2,NULL),(387,'c16','',1,5,4,45,2,NULL),(386,'c13','',1,5,4,45,2,NULL),(385,'c12','',1,5,4,45,2,NULL),(384,'c11','',1,5,4,45,2,NULL),(383,'s66','',2,5,4,45,1,NULL),(382,'s44','',2,5,4,45,1,NULL),(381,'s33','',2,5,4,45,1,NULL),(380,'s13','',2,5,4,45,1,NULL),(379,'s12','',2,5,4,45,1,NULL),(378,'s11','',2,5,4,45,1,NULL),(377,'c66','',1,5,4,45,1,NULL),(376,'c44','',1,5,4,45,1,NULL),(375,'c33','',1,5,4,45,1,NULL),(374,'c13','',1,5,4,45,1,NULL),(373,'c12','',1,5,4,45,1,NULL),(372,'c11','',1,5,4,45,1,NULL),(597,'d24','',3,10,2,14,21,NULL),(598,'d26','',3,10,2,14,21,NULL),(599,'d31','',3,10,2,14,21,NULL),(600,'d32','',3,10,2,14,21,NULL),(601,'d33','',3,10,2,14,21,NULL),(602,'d35','',3,10,2,14,21,NULL),(662,'d15','',3,14,4,8,21,NULL),(661,'d14','',3,14,4,8,21,NULL),(660,'d11','',3,14,4,8,21,NULL),(659,'d14','',3,12,4,45,8,NULL),(658,'d36','',3,13,4,6,21,NULL),(657,'d14','',3,13,4,6,21,NULL),(656,'d33','',3,13,4,5,21,NULL),(655,'d31','',3,13,4,5,21,NULL),(654,'d15','',3,13,4,5,21,NULL),(653,'d14','',3,13,4,4,21,NULL),(652,'d36','',3,13,4,2,21,NULL),(651,'d31','',3,13,4,2,21,NULL),(650,'d15','',3,13,4,2,21,NULL),(649,'d14','',3,13,4,2,21,NULL),(648,'d33','',3,13,4,1,21,NULL),(647,'d31','',3,13,4,1,21,NULL),(646,'d15','',3,13,4,1,21,NULL),(645,'d14','',3,13,4,1,21,NULL),(644,'d33','',3,11,4,17,21,NULL),(643,'d32','',3,11,4,17,21,NULL),(642,'d31','',3,11,4,17,21,NULL),(641,'d24','',3,11,4,17,21,NULL),(640,'d15','',3,11,4,17,21,NULL),(639,'d36','',3,11,4,16,21,NULL),(638,'d25','',3,11,4,16,21,NULL),(637,'d14','',3,11,4,16,21,NULL),(663,'d22','',3,14,4,8,21,NULL),(664,'d31','',3,14,4,8,21,NULL),(665,'d33','',3,14,4,8,21,NULL),(666,'d11','',3,14,4,10,21,NULL),(667,'d14','',3,14,4,10,21,NULL),(668,'d14','',3,14,1,11,21,NULL),(669,'d15','',3,14,1,11,21,NULL),(670,'d22','',3,14,1,11,21,NULL),(671,'d31','',3,14,1,11,21,NULL),(672,'d33','',3,14,1,11,21,NULL),(673,'d11','',3,14,2,11,21,NULL),(674,'d14','',3,14,2,11,21,NULL),(675,'d15','',3,14,2,11,21,NULL),(676,'d31','',3,14,2,11,21,NULL),(677,'d33','',3,14,2,11,21,NULL),(678,'d14','',3,15,4,24,21,NULL),(679,'d15','',3,15,4,24,21,NULL),(680,'d31','',3,15,4,24,21,NULL),(681,'d33','',3,15,4,24,21,NULL),(682,'d15','',3,15,4,27,21,NULL),(683,'d31','',3,15,4,27,21,NULL),(684,'d33','',3,15,4,27,21,NULL),(685,'d14','',3,15,4,28,21,NULL),(686,'d11','',3,15,4,25,21,NULL),(687,'d22','',3,15,4,25,21,NULL),(688,'d22','',3,15,1,29,21,NULL),(689,'d11','',3,15,2,29,21,NULL),(696,'d33','',3,10,3,13,21,NULL),(697,'d36','',3,10,3,13,21,NULL),(698,'d11','',3,10,3,14,21,NULL),(699,'d12','',3,10,3,14,21,NULL),(700,'d13','',3,10,3,14,21,NULL),(701,'d16','',3,10,3,14,21,NULL),(702,'d21','',3,10,3,14,21,NULL),(703,'d22','',3,10,3,14,21,NULL),(704,'d23','',3,10,3,14,21,NULL),(705,'d26','',3,10,3,14,21,NULL),(706,'d34','',3,10,3,14,21,NULL),(707,'d35','',3,10,3,14,21,NULL),(722,'d11','',3,9,4,35,21,NULL),(723,'d12','',3,9,4,35,21,NULL),(724,'d13','',3,9,4,35,21,NULL),(725,'d14','',3,9,4,35,21,NULL),(726,'d15','',3,9,4,35,21,NULL),(727,'d16','',3,9,4,35,21,NULL),(728,'d21','',3,9,4,35,21,NULL),(729,'d22','',3,9,4,35,21,NULL),(730,'d23','',3,9,4,35,21,NULL),(731,'d24','',3,9,4,35,21,NULL),(732,'d25','',3,9,4,35,21,NULL),(733,'d26','',3,9,4,35,21,NULL),(734,'d31','',3,9,4,35,21,NULL),(735,'d32','',3,9,4,35,21,NULL),(736,'d33','',3,9,4,35,21,NULL),(737,'d34','',3,9,4,35,21,NULL),(738,'d35','',3,9,4,35,21,NULL),(739,'d36','',3,9,4,35,21,NULL),(757,'---',' ',3,13,4,3,21,NULL),(755,'---',' ',3,11,4,18,21,NULL),(756,'---',' ',3,13,4,7,21,NULL),(741,'---',' ',3,10,4,15,21,NULL),(740,'---',' ',3,9,4,36,21,NULL),(763,'epsr11','k11',4,17,4,45,19,1),(764,'epsr22','k22',4,17,4,45,19,1),(765,'epsr13','k13',4,17,4,45,19,1),(766,'epsr33','k33',4,17,4,45,19,1),(767,'epsr11','k11',4,16,4,45,20,1),(768,'epsr12','k12',4,16,4,45,20,1),(769,'epsr13','k13',4,16,4,45,20,1),(770,'epsr22','k22',4,16,4,45,20,1),(771,'epsr23','k23',4,16,4,45,20,1),(772,'epsr33','k33',4,16,4,45,20,1),(773,'epsr11','k11',4,18,4,45,18,1),(774,'epsr22','k22',4,18,4,45,18,1),(775,'epsr33','k33',4,18,4,45,18,1),(779,'epsr33','k33',4,20,4,45,38,1),(778,'epsr11','k11',4,20,4,45,38,1),(780,'epsr11','k11',4,19,4,45,16,1),(781,'epsr11','k11',4,19,4,45,15,1);
/*!40000 ALTER TABLE `catalog_property_detail_old` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalog_property_detail_temp`
--

DROP TABLE IF EXISTS `catalog_property_detail_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalog_property_detail_temp` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(511) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `crystalsystem_id` int(11) DEFAULT NULL,
  `catalogaxis_id` int(11) DEFAULT NULL,
  `catalogpointgroup_id` int(11) DEFAULT NULL,
  `pointgroupnames_id` int(11) DEFAULT NULL,
  `dataproperty_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=22723 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalog_property_detail_temp`
--

LOCK TABLES `catalog_property_detail_temp` WRITE;
/*!40000 ALTER TABLE `catalog_property_detail_temp` DISABLE KEYS */;
INSERT INTO `catalog_property_detail_temp` VALUES (22722,'s66','',NULL,NULL,NULL,NULL,NULL,NULL),(22721,'s56','',NULL,NULL,NULL,NULL,NULL,NULL),(22720,'s55','',NULL,NULL,NULL,NULL,NULL,NULL),(22719,'s46','',NULL,NULL,NULL,NULL,NULL,NULL),(22718,'s45','',NULL,NULL,NULL,NULL,NULL,NULL),(22717,'s44','',NULL,NULL,NULL,NULL,NULL,NULL),(22716,'s36','',NULL,NULL,NULL,NULL,NULL,NULL),(22715,'s35','',NULL,NULL,NULL,NULL,NULL,NULL),(22714,'s34','',NULL,NULL,NULL,NULL,NULL,NULL),(22713,'s33','',NULL,NULL,NULL,NULL,NULL,NULL),(22712,'s26','',NULL,NULL,NULL,NULL,NULL,NULL),(22711,'s25','',NULL,NULL,NULL,NULL,NULL,NULL),(22710,'s24','',NULL,NULL,NULL,NULL,NULL,NULL),(22709,'s23','',NULL,NULL,NULL,NULL,NULL,NULL),(22708,'s22','',NULL,NULL,NULL,NULL,NULL,NULL),(22707,'s16','',NULL,NULL,NULL,NULL,NULL,NULL),(22706,'s15','',NULL,NULL,NULL,NULL,NULL,NULL),(22705,'s14','',NULL,NULL,NULL,NULL,NULL,NULL),(22704,'s13','',NULL,NULL,NULL,NULL,NULL,NULL),(22703,'s12','',NULL,NULL,NULL,NULL,NULL,NULL),(22702,'s11','',NULL,NULL,NULL,NULL,NULL,NULL),(22701,'s65','',NULL,NULL,NULL,NULL,NULL,NULL),(22700,'s64','',NULL,NULL,NULL,NULL,NULL,NULL),(22699,'s63','',NULL,NULL,NULL,NULL,NULL,NULL),(22698,'s62','',NULL,NULL,NULL,NULL,NULL,NULL),(22697,'s61','',NULL,NULL,NULL,NULL,NULL,NULL),(22696,'s54','',NULL,NULL,NULL,NULL,NULL,NULL),(22695,'s53','',NULL,NULL,NULL,NULL,NULL,NULL),(22694,'s52','',NULL,NULL,NULL,NULL,NULL,NULL),(22693,'s51','',NULL,NULL,NULL,NULL,NULL,NULL),(22692,'s43','',NULL,NULL,NULL,NULL,NULL,NULL),(22691,'s42','',NULL,NULL,NULL,NULL,NULL,NULL),(22690,'s41','',NULL,NULL,NULL,NULL,NULL,NULL),(22689,'s32','',NULL,NULL,NULL,NULL,NULL,NULL),(22688,'s31','',NULL,NULL,NULL,NULL,NULL,NULL),(22687,'s21','',NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `catalog_property_detail_temp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogproperty_dictionary`
--

DROP TABLE IF EXISTS `catalogproperty_dictionary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogproperty_dictionary` (
  `id` int(11) NOT NULL,
  `catalogproperty_id` int(11) DEFAULT NULL,
  `dictionary_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogproperty_dictionary`
--

LOCK TABLES `catalogproperty_dictionary` WRITE;
/*!40000 ALTER TABLE `catalogproperty_dictionary` DISABLE KEYS */;
INSERT INTO `catalogproperty_dictionary` VALUES (1,1,59),(2,1,60),(3,2,61),(4,1,62),(5,1,63),(6,1,64),(7,1,65),(8,1,66),(9,1,67),(10,1,68),(11,2,69),(12,2,70),(13,2,71);
/*!40000 ALTER TABLE `catalogproperty_dictionary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'category_overview','Category Overview'),(2,'book','Book'),(3,'journal','Journal'),(4,'phase','Phase'),(5,'cod','cod'),(6,'symmetry_point_group_name_H-M','Symmetry Point Group Name H-M'),(7,'structure','Structure'),(8,'chemical','Chemical'),(9,'prop','Property'),(10,'symmetry','Property Symmetry'),(11,'phasecharacteristics','Phase Characteristics'),(12,'propmeasurement','Measurement');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category_tag`
--

DROP TABLE IF EXISTS `category_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_tag`
--

LOCK TABLES `category_tag` WRITE;
/*!40000 ALTER TABLE `category_tag` DISABLE KEYS */;
INSERT INTO `category_tag` VALUES (1,'conditions','Conditions'),(2,'properties','Properties'),(3,'article','Article'),(4,'material','Material'),(5,'general','General Tags'),(6,'None','None');
/*!40000 ALTER TABLE `category_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configuration_message`
--

DROP TABLE IF EXISTS `configuration_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configuration_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) NOT NULL,
  `message_id` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`,`account_id`,`message_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuration_message`
--

LOCK TABLES `configuration_message` WRITE;
/*!40000 ALTER TABLE `configuration_message` DISABLE KEYS */;
INSERT INTO `configuration_message` VALUES (1,1,1,1),(2,1,5,0),(3,1,6,0),(4,1,7,0);
/*!40000 ALTER TABLE `configuration_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crystalsystem_axis`
--

DROP TABLE IF EXISTS `crystalsystem_axis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crystalsystem_axis` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `catalogcrystalsystem_id` int(11) DEFAULT NULL,
  `axis_id` int(11) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `catalogpointgroup_id` int(11) DEFAULT NULL,
  `pointgroupnames_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crystalsystem_axis`
--

LOCK TABLES `crystalsystem_axis` WRITE;
/*!40000 ALTER TABLE `crystalsystem_axis` DISABLE KEYS */;
INSERT INTO `crystalsystem_axis` VALUES (21,10,3,3,1,13,21),(24,2,2,1,1,45,19),(23,2,3,2,1,45,19),(22,2,2,2,1,45,19),(20,10,2,3,1,13,21),(18,15,1,3,1,29,21),(19,15,2,3,1,29,21),(25,2,3,1,1,45,19),(26,10,3,3,1,14,21),(27,10,2,3,1,14,21),(28,10,2,7,1,45,19),(29,10,3,7,1,45,19),(30,10,2,7,1,13,21),(31,10,3,7,1,13,21),(32,10,2,7,1,14,21),(33,10,3,7,1,14,21),(34,14,2,3,1,11,21),(35,14,1,3,1,11,21),(36,14,1,7,1,11,21),(37,14,2,7,1,11,21),(38,15,1,7,1,24,21),(39,15,2,7,1,24,21),(40,15,1,7,1,29,21),(41,15,2,7,1,29,21);
/*!40000 ALTER TABLE `crystalsystem_axis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crystalsystem_point_group`
--

DROP TABLE IF EXISTS `crystalsystem_point_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crystalsystem_point_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `catalogcrystalsystem_id` int(11) NOT NULL DEFAULT '0',
  `catalogpointgroup_id` int(11) NOT NULL DEFAULT '0',
  `type_id` int(11) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`,`catalogcrystalsystem_id`,`catalogpointgroup_id`)
) ENGINE=MyISAM AUTO_INCREMENT=83 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crystalsystem_point_group`
--

LOCK TABLES `crystalsystem_point_group` WRITE;
/*!40000 ALTER TABLE `crystalsystem_point_group` DISABLE KEYS */;
INSERT INTO `crystalsystem_point_group` VALUES (1,9,35,3,1),(2,9,36,3,1),(3,10,13,3,1),(4,10,14,3,1),(5,10,15,3,1),(6,11,18,3,1),(7,11,16,3,1),(8,11,17,3,1),(9,13,1,3,1),(10,13,2,3,1),(11,13,3,3,1),(12,13,4,3,1),(13,13,5,3,1),(14,13,6,3,1),(15,13,7,3,1),(16,14,8,3,1),(17,14,9,3,1),(18,14,10,3,1),(19,14,11,3,1),(20,14,12,3,1),(21,15,24,3,1),(22,15,25,3,1),(23,15,26,3,1),(24,15,27,3,1),(25,15,28,3,1),(26,15,29,3,1),(27,15,30,3,1),(29,9,35,7,1),(30,9,36,7,1),(31,10,13,7,1),(32,10,14,7,1),(33,10,15,7,1),(34,11,18,7,1),(35,11,16,7,1),(36,11,17,7,1),(37,13,1,7,1),(38,13,2,7,1),(39,13,3,7,1),(40,13,4,7,1),(41,13,5,7,1),(42,13,6,7,1),(43,13,7,7,1),(44,14,8,7,1),(45,14,9,7,1),(46,14,10,7,1),(47,14,11,7,1),(48,14,12,7,1),(49,15,24,7,1),(50,15,25,7,1),(51,15,26,7,1),(52,15,27,7,1),(53,15,28,7,1),(54,15,29,7,1),(55,15,30,7,1);
/*!40000 ALTER TABLE `crystalsystem_point_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crystalsystem_pointgroupnames`
--

DROP TABLE IF EXISTS `crystalsystem_pointgroupnames`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crystalsystem_pointgroupnames` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `catalogcrystalsystem_id` int(11) DEFAULT NULL,
  `pointgroupnames_id` int(11) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crystalsystem_pointgroupnames`
--

LOCK TABLES `crystalsystem_pointgroupnames` WRITE;
/*!40000 ALTER TABLE `crystalsystem_pointgroupnames` DISABLE KEYS */;
INSERT INTO `crystalsystem_pointgroupnames` VALUES (1,1,20,1,1),(3,16,20,4,1),(4,16,39,11,1),(7,20,38,4,1),(9,1,20,2,1),(11,2,19,2,1),(12,2,19,1,1),(13,3,18,1,1),(14,3,18,2,1),(21,6,4,2,1),(22,6,3,2,1),(23,6,4,1,1),(24,6,3,1,1),(25,7,15,2,1),(26,7,15,1,1),(27,8,17,2,1),(28,8,17,1,1),(36,17,43,11,1),(39,17,44,11,1),(40,17,19,4,1),(41,18,45,11,1),(43,18,46,11,1),(44,18,18,4,1),(45,20,47,11,1),(46,20,49,11,1),(47,20,51,11,1),(48,26,48,11,1),(49,26,50,11,1),(50,19,52,11,1),(52,4,16,2,1),(53,4,16,1,1),(54,5,1,1,1),(55,5,1,2,1),(56,5,2,2,1),(57,5,2,1,1),(58,12,8,3,1),(59,12,9,3,1),(60,19,16,4,1),(61,19,15,4,1),(62,12,8,7,1),(63,12,9,7,1),(64,10,19,7,0);
/*!40000 ALTER TABLE `crystalsystem_pointgroupnames` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crystalsystem_type`
--

DROP TABLE IF EXISTS `crystalsystem_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crystalsystem_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `catalogcrystalsystem_id` int(11) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=84 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crystalsystem_type`
--

LOCK TABLES `crystalsystem_type` WRITE;
/*!40000 ALTER TABLE `crystalsystem_type` DISABLE KEYS */;
INSERT INTO `crystalsystem_type` VALUES (42,26,4,0),(43,26,11,1),(44,5,2,1),(45,5,1,1),(46,4,2,1),(47,4,1,1),(48,20,4,1),(49,20,11,1),(50,19,4,1),(51,19,11,1),(52,18,4,1),(53,18,11,1),(54,17,4,1),(55,17,11,1),(56,16,4,1),(57,16,11,1),(58,8,2,1),(59,8,1,1),(60,7,2,1),(61,7,1,1),(62,6,2,1),(63,6,1,1),(64,3,2,1),(65,3,1,1),(66,2,2,1),(67,2,1,1),(68,1,2,1),(69,1,1,1),(70,15,3,1),(71,15,7,1),(72,14,3,1),(73,14,7,1),(74,13,3,1),(75,12,3,1),(76,12,7,1),(77,11,3,1),(78,11,7,1),(79,10,3,1),(80,9,3,1),(81,9,7,1),(82,13,7,1),(83,10,7,1);
/*!40000 ALTER TABLE `crystalsystem_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_catalogproperty`
--

DROP TABLE IF EXISTS `data_catalogproperty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_catalogproperty` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(511) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_catalogproperty`
--

LOCK TABLES `data_catalogproperty` WRITE;
/*!40000 ALTER TABLE `data_catalogproperty` DISABLE KEYS */;
INSERT INTO `data_catalogproperty` VALUES (1,'e','Elasticity',1),(2,'p','Piezoelectricity',1),(3,'2nd','2nd-rank tensor',1),(4,'4th','4th-rank ranktensor',0),(8,'Test1','Test1',0);
/*!40000 ALTER TABLE `data_catalogproperty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_chemical`
--

DROP TABLE IF EXISTS `data_chemical`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_chemical` (
  `id` int(11) NOT NULL,
  `description` varchar(511) NOT NULL,
  `name` varchar(511) NOT NULL,
  `active` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_chemical`
--

LOCK TABLES `data_chemical` WRITE;
/*!40000 ALTER TABLE `data_chemical` DISABLE KEYS */;
INSERT INTO `data_chemical` VALUES (1,'chemical formula','_chemical_formula',1),(2,'chemical formula sum','_chemical_formula_sum',0);
/*!40000 ALTER TABLE `data_chemical` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_datafile`
--

DROP TABLE IF EXISTS `data_datafile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_datafile` (
  `code` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(13) NOT NULL,
  `cod_code` int(11) DEFAULT NULL,
  `phase_generic` varchar(255) DEFAULT NULL,
  `phase_name` varchar(255) NOT NULL,
  `chemical_formula` varchar(255) NOT NULL,
  `publication_id` int(11) NOT NULL,
  PRIMARY KEY (`code`)
) ENGINE=MyISAM AUTO_INCREMENT=1000393 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_datafile`
--

LOCK TABLES `data_datafile` WRITE;
/*!40000 ALTER TABLE `data_datafile` DISABLE KEYS */;
INSERT INTO `data_datafile` VALUES (1000001,'1000001.mpod',NULL,NULL,'Al72Ni16Co8','Al72 Ni16 Co8',1),(1000002,'1000002.mpod',9008460,NULL,'aluminum','Al',2),(1000003,'1000003.mpod',9008460,NULL,'aluminum','Al',3),(1000004,'1000004.mpod',9011635,NULL,'argon','Ar',4),(1000005,'1000005.mpod',9012729,NULL,'barium','Ba',5),(1000006,'1000006.mpod',9008488,NULL,'alpha-beryllium','Be',5),(1000007,'1000007.mpod',9008490,NULL,'cadmium','Cd',5),(1000008,'1000008.mpod',2100189,NULL,'calcite','Ca C O3',3),(1000009,'1000009.mpod',9011033,NULL,'calcium','Ca',6),(1000010,'1000010.mpod',9008465,NULL,'gamma-cerium','Ce',7),(1000011,'1000011.mpod',9011011,NULL,'cesium','Cs',8),(1000012,'1000012.mpod',5000220,NULL,'chromium','Cr',9),(1000013,'1000013.mpod',9008492,NULL,'alpha-cobalt','Co',10),(1000014,'1000014.mpod',9008466,NULL,'beta-cobalt','Co',11),(1000015,'1000015.mpod',9013014,NULL,'copper','Cu',12),(1000016,'1000016.mpod',9013014,NULL,'copper','Cu',3),(1000017,'1000017.mpod',2101499,NULL,'diamond','C',13),(1000018,'1000018.mpod',9008567,NULL,'germanium','Ge',5),(1000019,'1000019.mpod',9013035,NULL,'gold','Au',5),(1000020,'1000020.mpod',9013035,NULL,'gold','Au',3),(1000021,'1000021.mpod',1200017,NULL,'graphite','C',14),(1000022,'1000022.mpod',1200017,NULL,'graphite','C',3),(1000023,'1000023.mpod',5000217,NULL,'alpha-iron','Fe',5),(1000024,'1000024.mpod',9012706,NULL,'gamma-iron','Fe',5),(1000025,'1000025.mpod',NULL,NULL,'iron(34at%)-palladium','Fe(0.34)-Pd',15),(1000026,'1000026.mpod',NULL,'KTA','KTiOAsO4','K Ti As O5',16),(1000027,'1000027.mpod',9012795,NULL,'langasite','La3 Ga5 Si O14',17),(1000028,'1000028.mpod',9008477,NULL,'lead','Pb',5),(1000029,'1000029.mpod',2101845,NULL,'LiNbO3','Li Nb O3',18),(1000030,'1000030.mpod',2101845,NULL,'LiNbO3','Li Nb O3',19),(1000031,'1000031.mpod',2101845,NULL,'LiNbO3','Li Nb O3',20),(1000032,'1000032.mpod',2101845,NULL,'LiNbO3','Li Nb O3.07 Mg0.07',19),(1000033,'1000033.mpod',2101845,NULL,'LiNbO3','Li Nb O3.07 Mg0.07',20),(1000034,'1000034.mpod',9008506,NULL,'magnesium','Mg',5),(1000035,'1000035.mpod',9008543,NULL,'molybdenum','Mo',5),(1000036,'1000036.mpod',9008508,NULL,'neodymium','Nd',5),(1000037,'1000037.mpod',9008476,NULL,'nickel','Ni',5),(1000038,'1000038.mpod',9008546,NULL,'niobium','Nb',5),(1000039,'1000039.mpod',9008478,NULL,'palladium','Pd',5),(1000040,'1000040.mpod',9009088,NULL,'alpha-TeO2','Te O2',21),(1000041,'1000041.mpod',NULL,'PIN-PMN-PT','Pb(In1/2Nb1/2)O3(0.26)-Pb(Mg1/3Nb2/3)O3(0.46)-PbTiO3(0.28)','Pb In0.13 Nb0.436 Mg0.153 Ti0.28 O3',22),(1000042,'1000042.mpod',NULL,'PIN-PMN-PT','Pb(In1/2Nb1/2)O3(0.33)-Pb(Mg1/3Nb2/3)O3(0.35)-PbTiO3(0.32)','Pb In0.165 Nb0.398 Mg0.167 Ti0.32 O3',23),(1000043,'1000043.mpod',NULL,'PMN-PT','Pb(Mg1/3Nb2/3)O3-PbTiO3(0.28)','Pb Nb0.48 Mg0.24 Ti0.28 O3',24),(1000044,'1000044.mpod',NULL,'PMN-PT','Pb(Mg1/3Nb2/3)O3-PbTiO3(0.29)','Pb Nb0.473 Mg0.237 Ti0.29 O3',25),(1000045,'1000045.mpod',NULL,'PMN-PT','Pb(Mg1/3Nb2/3)O3-PbTiO3(0.30)','Pb Nb0.467 Mg0.233 Ti0.30 O3',24),(1000046,'1000046.mpod',NULL,'PMN-PT','Pb(Mg1/3Nb2/3)O3-PbTiO3(0.32)','Pb Nb0.453 Mg0.227 Ti0.32 O3',24),(1000047,'1000047.mpod',NULL,'PMN-PT','Pb(Mg1/3Nb2/3)O3-PbTiO3(0.33)','Pb Nb0.447 Mg0.223 Ti0.33 O3',26),(1000048,'1000048.mpod',NULL,'PMN-PT','Pb(Mg1/3Nb2/3)O3-PbTiO3(0.33)','Pb Nb0.447 Mg0.223 Ti0.33 O3',27),(1000049,'1000049.mpod',NULL,'PZN-PT','Pb(Zn1/3Nb2/3)O3-PbTiO3(0.045)','Pb Nb0.637 Zn0.318 Ti0.07 O3',28),(1000050,'1000050.mpod',NULL,'PZN-PT','Pb(Zn1/3Nb2/3)O3-PbTiO3(0.07)','Pb Nb0.62 Zn0.31 Ti0.07 O3',28),(1000051,'1000051.mpod',NULL,'PZN-PT','Pb(Zn1/3Nb2/3)O3-PbTiO3(0.07)','Pb Nb0.62 Zn0.31 Ti0.07 O3',29),(1000052,'1000052.mpod',NULL,'PZN-PT','Pb(Zn1/3Nb2/3)O3-PbTiO3(0.08)','Pb Nb0.613 Zn0.307 Ti0.08 O3',28),(1000053,'1000053.mpod',9000490,NULL,'magnesium oxide','Mg O',30),(1000054,'1000054.mpod',9008480,NULL,'platinum','Pt',5),(1000055,'1000055.mpod',5000035,NULL,'alpha-Quartz','Si O2',31),(1000056,'1000056.mpod',5000035,NULL,'alpha-Quartz','Si O2',3),(1000057,'1000057.mpod',9008512,NULL,'rhenium','Re',5),(1000058,'1000058.mpod',9008513,NULL,'ruthenium','Ru',5),(1000059,'1000059.mpod',9008565,NULL,'silicon','Si',32),(1000060,'1000060.mpod',9013045,NULL,'silver','Ag',5),(1000061,'1000061.mpod',9008517,NULL,'alpha-Titanium','Ti',33),(1000062,'1000062.mpod',9008554,NULL,'beta-Titanium','Ti',34),(1000063,'1000063.mpod',9006486,NULL,'tungsten','W',5),(1000064,'1000064.mpod',9008557,NULL,'vanadium','V',5),(1000065,'1000065.mpod',9008522,NULL,'zinc','Zn',5),(1000066,'1000066.mpod',1010298,NULL,'Nd:SGGM','Nd0.0136 Sr0.92 Gd1.01 Ga2.88 O7',35),(1000067,'1000067.mpod',1010298,NULL,'iron selenide','Fe1.03 Se',36),(1000068,'1000068.mpod',1009000,NULL,'gallium arsenate','Ga As O4',37),(1000069,'1000069.mpod',1010458,NULL,'KDP, Mn-doped potassium dihydrogen phosphate','K H2 P O4 Mn0.009',38),(1000070,'1000070.mpod',1010458,NULL,'KDP, potassium dihydrogen phosphate','K H2 P O4',38),(1000071,'1000071.mpod',NULL,NULL,'pentaerythritol tetranitrate','?',39),(1000072,'1000072.mpod',NULL,NULL,'Sodium trisilicate glass','Na2 Si3 O7',40),(1000073,'1000073.mpod',NULL,NULL,'Sodium aluminosilicate glass','Nax Aly Siz O2',40),(1000074,'1000074.mpod',2102560,NULL,'KMnF3','K Mn F3',41),(1000075,'1000075.mpod',5910053,NULL,'Copper-Gold alloy','Cu3 Au',42),(1000076,'1000076.mpod',9008814,NULL,'Brass','Cu0.72 Zn0.28',43),(1000077,'1000077.mpod',9006486,NULL,'Tungsten','K',44),(1000078,'1000078.mpod',9006486,NULL,'Tungsten','K',45),(1000079,'1000079.mpod',9008545,NULL,'Sodium','Na',46),(1000080,'1000080.mpod',9013045,NULL,'Silver','Ag',47),(1000081,'1000081.mpod',9008540,NULL,'Potassium','K',48),(1000082,'1000082.mpod',9008477,NULL,'Lead','Pb',49),(1000083,'1000083.mpod',9008477,NULL,'Lead','Pb',50),(1000084,'1000084.mpod',5000217,NULL,'alpha-Iron','Fe',48),(1000085,'1000085.mpod',5000217,NULL,'alpha-Iron','Fe',51),(1000086,'1000086.mpod',5000217,NULL,'alpha-Iron','Fe',51),(1000087,'1000087.mpod',5000217,NULL,'alpha-Iron','Fe',52),(1000088,'1000088.mpod',9013035,NULL,'Gold','Au',48),(1000089,'1000089.mpod',9013035,NULL,'Gold','Au',50),(1000090,'1000090.mpod',9013035,NULL,'Gold','Au',47),(1000091,'1000091.mpod',9013014,NULL,'Copper','Cu',50),(1000092,'1000092.mpod',9013014,NULL,'Copper','Cu',53),(1000093,'1000093.mpod',9008460,NULL,'Aluminum','Al',54),(1000094,'1000094.mpod',9008860,NULL,'Aluminum nitride','Al N',55),(1000095,'1000095.mpod',NULL,'PIN-PMN-PT','Pb(In1/2Nb1/2)O3(0.33)-Pb(Mg1/3Nb2/3)O3(0.35)-PbTiO3(0.32)','Pb In0.165 Nb0.398 Mg0.167 Ti0.32 O3',56),(1000096,'1000096.mpod',NULL,'PIN-PMN-PT','Pb(In1/2Nb1/2)O3(0.26)-Pb(Mg1/3Nb2/3)O3(0.46)-PbTiO3(0.28)','Pb In0.13 Nb0.436 Mg0.153 Ti0.28 O3',56),(1000097,'1000097.mpod',9088326,NULL,'LiFeAs','Li Fe As',57),(1000098,'1000098.mpod',NULL,NULL,'Mullite 3:2','Al5 Si O9.5',58),(1000099,'1000099.mpod',NULL,NULL,'Mullite 3:2','Al6 Si2 O13',58),(1000100,'1000100.mpod',9001037,NULL,'Mullite 2:1','Al2.62 Si0.69 O5.31',59),(1000101,'1000101.mpod',2101499,NULL,'diamond','C',60),(1000102,'1000102.mpod',NULL,'?','iron arsenide','Ba Fe2 As1.3 P0.7',61),(1000103,'1000103.mpod',9008814,NULL,'beta-Brass','Cu Zn',62),(1000104,'1000104.mpod',9008814,NULL,'beta-Brass','Cu Zn',63),(1000105,'1000105.mpod',NULL,NULL,'iron selenide','K0.8 Fe2 Se2',64),(1000106,'1000106.mpod',NULL,NULL,'iron pnictide oxide',' Fe2 As2 Ca6 Al1.33 Ti2.67 O11',65),(1000107,'1000107.mpod',NULL,NULL,'YBCO','Y Ba2 Cu3 O6.915',66),(1000108,'1000108.mpod',NULL,NULL,'YBCO','Y Ba2 Cu3 O6.973',66),(1000109,'1000109.mpod',NULL,NULL,'Pr-YBCO','Y0.992 Pr0.008 Ba2 Cu3 O6.934',66),(1000110,'1000110.mpod',NULL,NULL,'Pr-YBCO','Y0.987 Pr0.013 Ba2 Cu3 O6.971',66),(1000111,'1000111.mpod',NULL,NULL,'Pr-YBCO','Y0.976 Pr0.024 Ba2 Cu3 O6.973',66),(1000112,'1000112.mpod',NULL,NULL,'?','La Ru2 P2',67),(1000113,'1000113.mpod',2104122,NULL,'chromium sesquioxide','Cr2 O3',68),(1000114,'1000114.mpod',NULL,NULL,'Iron selenide','Tl0.58 Rb0.42 Fe1.72 Se2',69),(1000115,'1000115.mpod',2104122,NULL,'chromium sesquioxide','Cr2 O3',70),(1000116,'1000116.mpod',NULL,NULL,'sodium silicon clathrate','Na8 Si46',71),(1000117,'1000117.mpod',NULL,NULL,'sodium silicon clathrate','K0.26 Zr N Cl',72),(1000118,'1000118.mpod',2101575,NULL,'KPC','K2 Pt C4 N4 Br0.3 H6 O3',73),(1000119,'1000119.mpod',NULL,'PZN-PT','Pb(Zn1/3Nb2/3)O3-PbTiO3(0.08)','Pb Nb0.613 Zn0.307 Ti0.08 O3',74),(1000120,'1000120.mpod',NULL,NULL,'Cs-doped iron selenide','Cs0.8 Fe2 Se1.96',75),(1000121,'1000121.mpod',9008460,NULL,'?',' Cu0.05 Al0.95',76),(1000122,'1000122.mpod',9013035,NULL,'?','Au0.25 Ag0.75',47),(1000123,'1000123.mpod',9013035,NULL,'?','Au0.5 Ag0.5',47),(1000124,'1000124.mpod',9013035,NULL,'?','Au0.75 Ag0.25',47),(1000125,'1000125.mpod',1100043,NULL,'zinc blende','Zn0.9364 S0.9364 Si0.02155 Fe0.0748 Al0.0748 O0.281',77),(1000126,'1000126.mpod',1000043,NULL,'fluorite','Ca F2',78),(1000127,'1000127.mpod',9003112,NULL,'potassium chlorite','K Cl',78),(1000128,'1000128.mpod',5000115,NULL,'pyrite','Fe S2',78),(1000129,'1000129.mpod',1010057,NULL,'sodium chlorate','Na Cl O2',78),(1000130,'1000130.mpod',4300180,NULL,'sodium chloride','Na Cl',78),(1000131,'1000131.mpod',1010541,NULL,'beryl','Be3 Al2 Si6 O18',78),(1000132,'1000132.mpod',2100992,NULL,'calcite','Ca C O3',78),(1000133,'1000133.mpod',2101167,NULL,'hematite','Fe2 O3',78),(1000134,'1000134.mpod',5000035,NULL,'alpha-Quartz','Si O2',78),(1000135,'1000135.mpod',6000259,NULL,'aragonite','Ca C O3',78),(1000136,'1000136.mpod',1000037,NULL,'baryte','Ba S O4',78),(1000137,'1000137.mpod',2207377,NULL,'topaz','Al2 Si O5 H F',78),(1000138,'1000138.mpod',1000043,NULL,'fluorite','Ca F2',79),(1000139,'1000139.mpod',9008667,NULL,'lithium fluoride','Li F',79),(1000140,'1000140.mpod',4300180,NULL,'sodium chloride','Na Cl',79),(1000141,'1000141.mpod',1000037,NULL,'baryte','Ba S O4',79),(1000142,'1000142.mpod',4300180,NULL,'sodium chloride','Na Cl',80),(1000143,'1000143.mpod',9000490,NULL,'magnesium oxide','Mg O',80),(1000144,'1000144.mpod',9003112,NULL,'potassium chlorite','K Cl',80),(1000145,'1000145.mpod',2102034,NULL,'potassium alum','K Al S2 O20 H24',81),(1000146,'1000146.mpod',1100043,NULL,'zinc blende','ZnS',82),(1000147,'1000147.mpod',9009734,NULL,'potassium bromide','K Br',83),(1000148,'1000148.mpod',9003112,NULL,'potassium chloride','K Cl',83),(1000149,'1000149.mpod',9009735,NULL,'potassium iodide','K I',83),(1000150,'1000150.mpod',9008677,NULL,'sodium bromide','Na Br',83),(1000151,'1000151.mpod',4300180,NULL,'sodium chloride','Na Cl',83),(1000152,'1000152.mpod',9008490,NULL,'cadmium','Cd',45),(1000153,'1000153.mpod',9008522,NULL,'zinc','Zn',45),(1000154,'1000154.mpod',5000214,NULL,'antimony','Sb',45),(1000155,'1000155.mpod',5000215,NULL,'bismuth','Bi',45),(1000156,'1000156.mpod',1011098,NULL,'tellurium','Te',45),(1000157,'1000157.mpod',9008570,NULL,'tin','Sn',45),(1000158,'1000158.mpod',9008860,NULL,'Aluminum nitride','Al N',84),(1000159,'1000159.mpod',9008860,NULL,'Aluminum nitride oxygenated','Al N O0.06',85),(1000160,'1000160.mpod',9008860,NULL,'Aluminum nitride','Al N',86),(1000161,'1000161.mpod',9008860,NULL,'Aluminum nitride','Al N',87),(1000162,'1000162.mpod',9008569,NULL,'graphite','C',88),(1000163,'1000163.mpod',9008834,NULL,'Boron nitride','B N',89),(1000164,'1000164.mpod',9008834,NULL,'Boron nitride','B N',90),(1000165,'1000165.mpod',9008834,NULL,'Boron nitride','B N',91),(1000166,'1000166.mpod',5000115,NULL,'pyrite','Fe S2',92),(1000167,'1000167.mpod',9008678,NULL,'sodium chloride','Na Cl',93),(1000168,'1000168.mpod',9008506,NULL,'Magnesium','Mg',48),(1000169,'1000169.mpod',9008506,NULL,'Magnesium','Mg',94),(1000170,'1000170.mpod',9008490,NULL,'cadmium','Cd',95),(1000171,'1000171.mpod',9008522,NULL,'zinc','Zn',95),(1000172,'1000172.mpod',9008522,NULL,'zinc','Zn',96),(1000173,'1000173.mpod',9008522,NULL,'zinc','Zn',97),(1000174,'1000174.mpod',9008522,NULL,'zinc','Zn',97),(1000175,'1000175.mpod',5000035,NULL,'alpha-Quartz','Si O2',98),(1000176,'1000176.mpod',2217854,NULL,'Rochelle salt','K Na C4 H12 O10',99),(1000177,'1000177.mpod',2217854,NULL,'Rochelle salt','K Na C4 H12 O10',100),(1000178,'1000178.mpod',2101161,NULL,'Rochelle salt','N Na C4 H16 O10',101),(1000179,'1000179.mpod',2217854,NULL,'Rochelle salt','K Na C4 H12 O10',102),(1000180,'1000180.mpod',9009049,NULL,'Uranium dioxide','U O2',103),(1000181,'1000181.mpod',9011343,NULL,'Barium nitrate','Ba N2 O6',104),(1000182,'1000182.mpod',5910007,NULL,'Lead nitrate','Pb N2 O6',104),(1000183,'1000183.mpod',5910007,NULL,'Lead nitrate','Pb N2 O6',3),(1000184,'1000184.mpod',9011343,NULL,'Barium nitrate','Ba N2 O6',3),(1000185,'1000185.mpod',NULL,NULL,'Aluminum oxynitride','Al23 N5 O27',105),(1000186,'1000186.mpod',NULL,NULL,'Aluminum oxynitride','Al23 N5 O27',106),(1000187,'1000187.mpod',9001037,NULL,'Mullite 2:1','Al4.78 Si1.22 O9.61',107),(1000188,'1000188.mpod',9001037,NULL,'Mullite 2.5:1','Al5 Si1 O9.5',108),(1000189,'1000189.mpod',9001408,NULL,'Sillimanite','Al2 Si O5',109),(1000190,'1000190.mpod',9001037,NULL,'Mullite 2:1','Al4.78 Si1.22 O9.61',110),(1000191,'1000191.mpod',9001037,NULL,'Mullite','Al4.48 Si1.52 O9.76',110),(1000192,'1000192.mpod',9001037,NULL,'Mullite','Al4.50 Si1.5 O9.75',111),(1000193,'1000193.mpod',9001408,NULL,'Sillimanite','Al2 Si O5',112),(1000194,'1000194.mpod',1501462,NULL,'iron selenide','Cs0.8 Fe2 Se1.96',113),(1000195,'1000195.mpod',1501461,NULL,'iron selenide','K0.8 Fe2 Se1.96',113),(1000196,'1000196.mpod',NULL,NULL,'iron strontium arsenide','Sr1 Fe2 As2',114),(1000197,'1000197.mpod',NULL,NULL,'thallium iron selenide','Tl1 Fe1.3 Se2',115),(1000198,'1000198.mpod',NULL,NULL,'thallium iron selenide','Tl1 Fe1.47 Se2',115),(1000199,'1000199.mpod',NULL,NULL,'thallium iron selenide','Tl1 Fe1.7 Se2',115),(1000200,'1000200.mpod',NULL,NULL,'thallium iron selenide','Tl0.64 K0.36 Fe1.83 Se2',115),(1000201,'1000201.mpod',NULL,NULL,'thallium iron selenide','Tl0.69 K0.31 Fe1.84 Se2',115),(1000202,'1000202.mpod',NULL,NULL,'thallium iron selenide','Tl0.75 K0.25 Fe1.85 Se2',115),(1000203,'1000203.mpod',9008488,NULL,' alpha-beryllium','Be1',116),(1000204,'1000204.mpod',9008490,NULL,'cadmium','Cd1',116),(1000205,'1000205.mpod',9008492,NULL,'alpha-cobalt','Co1',116),(1000206,'1000206.mpod',9008501,NULL,'hafnium','Hf1',116),(1000207,'1000207.mpod',9008506,NULL,'magnesium','Mg1',116),(1000208,'1000208.mpod',9008512,NULL,'rhenium','Re1',116),(1000209,'1000209.mpod',9008513,NULL,'ruthenium','Ru1',116),(1000210,'1000210.mpod',9008518,NULL,'thalium','Tl1',116),(1000211,'1000211.mpod',9008517,NULL,'alpha-titanium','Ti1',116),(1000212,'1000212.mpod',9010984,NULL,'yttrium','Y1',116),(1000213,'1000213.mpod',9008522,NULL,'zinc','Zn1',116),(1000214,'1000214.mpod',9008523,NULL,'zirconium','Zr1',116),(1000215,'1000215.mpod',9011344,NULL,'Strontium nitrate','Sr N2 O6',117),(1000216,'1000216.mpod',9008081,NULL,'Corundum','Al2 O3',118),(1000217,'1000217.mpod',9008678,NULL,'Sodium chloride','Na1 Cl1',119),(1000218,'1000218.mpod',9008677,NULL,'Sodium bromide','Na1 Br1',119),(1000219,'1000219.mpod',9008667,NULL,'lithium fluoride','Li1 F1',119),(1000220,'1000220.mpod',9010006,NULL,'Ammonium chloride','N1 H4 Cl1',119),(1000221,'1000221.mpod',9011300,NULL,'Ammonium bromide','N1 H4 Br1',119),(1000222,'1000222.mpod',1010057,NULL,'Sodium chlorate','Na1 Cl1 O3',119),(1000223,'1000223.mpod',1010058,NULL,'Sodium bromate','Na1 Br1 O3',119),(1000224,'1000224.mpod',5910007,NULL,'Lead nitrate','Pb1 N2 O6',119),(1000225,'1000225.mpod',9011343,NULL,'Barium nitrate','Ba N2 O6',119),(1000226,'1000226.mpod',9011344,NULL,'Strontium nitrate','Sr N2 O6',119),(1000227,'1000227.mpod',2102034,NULL,'potassium alum','K Al S2 O20 H24',119),(1000228,'1000228.mpod',9008299,NULL,'ammonium alum','N Al S2 O20 H28',119),(1000229,'1000229.mpod',NULL,NULL,'chromium alum','Cr Al S2 O20 H24',119),(1000230,'1000230.mpod',2102036,NULL,'thallium alum','Tl Al S2 O20 H24',119),(1000231,'1000231.mpod',5000115,NULL,'iron pyrite','Fe S2',119),(1000232,'1000232.mpod',9000107,NULL,'zinc blende','Zn S',119),(1000233,'1000233.mpod',9008694,NULL,'galena','Pb S',119),(1000234,'1000234.mpod',2101499,NULL,'diamond','C',119),(1000235,'1000235.mpod',1000043,NULL,'fluorite','Ca F2',119),(1000236,'1000236.mpod',2101926,NULL,'magnetite','Fe2 O3',119),(1000237,'1000237.mpod',9000490,NULL,'magnesium oxide','Mg O',119),(1000238,'1000238.mpod',2100992,NULL,'calcite','Ca C O3',119),(1000239,'1000239.mpod',9007554,NULL,'sodium nitrate','Na N O3',119),(1000240,'1000240.mpod',5000035,NULL,'alpha-Quartz','Si O2',119),(1000241,'1000241.mpod',1010541,NULL,'beryl','Be3 Al2 Si6 O18',119),(1000242,'1000242.mpod',1010541,NULL,'beryl','Be3 Al2 Si6 O18',119),(1000243,'1000243.mpod',9008081,NULL,'Corundum','Al2 O3',119),(1000244,'1000244.mpod',2223574,NULL,'sodium tartrate','Na2 C4 H4 O6',119),(1000245,'1000245.mpod',2217854,NULL,'Rochelle salt','K Na C4 H12 O10',119),(1000246,'1000246.mpod',9007483,NULL,'epsomite','Mg S H14 O11',119),(1000247,'1000247.mpod',NULL,NULL,'zinc sulphate heptahydrate','Zn S H14 O11',119),(1000248,'1000248.mpod',9008577,NULL,'sulphur','S1',119),(1000249,'1000249.mpod',1000037,NULL,'baryte','Ba S O4',119),(1000250,'1000250.mpod',9008106,NULL,'celestite','Sr1 S1 O4',119),(1000251,'1000251.mpod',NULL,NULL,'sodium thiosulfate','Na2 S2 O3',119),(1000252,'1000252.mpod',5000115,NULL,'pyrite','Fe S2',120),(1000253,'1000253.mpod',9008694,NULL,'galena','Pb S',120),(1000254,'1000254.mpod',9011343,NULL,'Barium nitrate','Ba N2 O6',121),(1000255,'1000255.mpod',NULL,NULL,'potassium iron selenide','K1 Fe2 Se2',122),(1000256,'1000256.mpod',NULL,NULL,'potassium iron selenide','K0.8 Fe2 Se2',122),(1000257,'1000257.mpod',NULL,NULL,'rubidium iron selenide','Rb0.8 Fe2 Se2',122),(1000258,'1000258.mpod',NULL,NULL,'cesium iron selenide','Cs0.8 Fe2 Se2',122),(1000259,'1000259.mpod',NULL,NULL,'thallium potassium iron selenide','Tl0.4 K0.3 Fe2 Se2',122),(1000260,'1000260.mpod',NULL,NULL,'thallium rubidium iron selenide','Tl0.4 Rb0.4 Fe2 Se2',122),(1000261,'1000261.mpod',9013529,NULL,'magnetite','Fe3 O4',123),(1000262,'1000262.mpod',9013529,NULL,'magnetite','Fe3 O4',123),(1000263,'1000263.mpod',5000115,NULL,'pyrite','Fe S2',123),(1000264,'1000264.mpod',5000115,NULL,'pyrite','Fe S2',123),(1000265,'1000265.mpod',5000115,NULL,'pyrite','Fe S2',123),(1000266,'1000266.mpod',5000115,NULL,'pyrite','Fe S2',123),(1000267,'1000267.mpod',5910349,NULL,'chromite','Fe Cr2 O4',123),(1000268,'1000268.mpod',9012754,NULL,'alpha potassium nitrate','K1 N1 O3',124),(1000269,'1000269.mpod',6000259,NULL,'aragonite','Ca C O3',124),(1000270,'1000270.mpod',2100992,NULL,'calcite','Ca C O3',124),(1000271,'1000271.mpod',9007554,NULL,'sodium nitrate','Na N O3',124),(1000272,'1000272.mpod',NULL,NULL,'BaLaCuO',' La1.85 Ba0.15 Cu O4',125),(1000273,'1000273.mpod',NULL,NULL,'YBaCuO','Y Ba2 Cu3 O7',126),(1000274,'1000274.mpod',NULL,NULL,'potassium iron selenide','K0.75 Fe1.66 Se2',127),(1000275,'1000275.mpod',NULL,NULL,'cesium iron selenide','Cs0.81 Fe1.61 Se2',127),(1000276,'1000276.mpod',NULL,NULL,'SBNN 70','Sr1.4 Ba0.6 Na Nb5 O15',128),(1000277,'1000277.mpod',NULL,NULL,'SBNN 30','Sr0.6 Ba1.4 Na Nb5 O15',128),(1000278,'1000278.mpod',NULL,NULL,'PIN-PMN-PT','Pb In0.135 Nb0.402 Mg0.133 Ti0.33 O3',129),(1000279,'1000279.mpod',NULL,NULL,'PMN-PT','Pb Nb0.387 Mg0.193 Ti0.42 O3',130),(1000280,'1000280.mpod',2101499,NULL,'diamond','C',131),(1000281,'1000281.mpod',NULL,NULL,'BNTK','Bi0.5 Na0.25 K0.25 Ti1 O3',132),(1000282,'1000282.mpod',NULL,NULL,'PZN-PT','Pb Nb0.613 Zn0.307 Ti0.08 O3',133),(1000283,'1000283.mpod',NULL,NULL,'PZN-PT','Pb Nb0.613 Zn0.307 Ti0.08 O3',133),(1000284,'1000284.mpod',2310001,NULL,'uranium dioxide','U O2',134),(1000285,'1000285.mpod',NULL,NULL,'beta-uranium','U',134),(1000286,'1000286.mpod',1000032,NULL,'corundum','Al2 O3',135),(1000287,'1000287.mpod',1000032,NULL,'corundum','Al2 O3',136),(1000288,'1000288.mpod',1000032,NULL,'corundum','Al2 O3',137),(1000289,'1000289.mpod',1000032,NULL,'corundum','Al2 O3',138),(1000290,'1000290.mpod',1000032,NULL,'corundum','Al2 O3',139),(1000291,'1000291.mpod',1000032,NULL,'corundum','Al2 O3',140),(1000292,'1000292.mpod',1000032,NULL,'corundum','Al2 O3',141),(1000293,'1000293.mpod',1000032,NULL,'corundum','Al2 O3',142),(1000294,'1000294.mpod',9011192,NULL,'PbTiO3','Pb0.99 Ti1 O3',143),(1000295,'1000295.mpod',1000032,NULL,'corundum','Al2 O3',144),(1000296,'1000296.mpod',4500649,NULL,'CTM','Cs2 Te1 Mo3 O12',145),(1000297,'1000297.mpod',9015208,'Glacier Ice','Mendenhall glacier Ice Ih','H2 O',146),(1000298,'1000298.mpod',9015208,'Lake Ice','Paddys pond lake Ice Ih','H2 O',146),(1000299,'1000299.mpod',2101499,NULL,'diamond','C1',147),(1000300,'1000300.mpod',2101499,NULL,'diamond','C1',148),(1000301,'1000301.mpod',1010275,NULL,'titanium disulfide','Ti1 S2',149),(1000302,'1000302.mpod',1508368,NULL,'titanium lithium disulfide','Li1 Ti1 S2',149),(1000303,'1000303.mpod',NULL,NULL,'s-collidine titanium disulfide','C8 H11 N1 Ti1 S2',149),(1000304,'1000304.mpod',2100858,NULL,'barium titanate','Ba1 Ti1 O3',150),(1000305,'1000305.mpod',2100862,NULL,'barium titanate','Ba1 Ti1 O3',150),(1000306,'1000306.mpod',2100858,NULL,'barium titanate','Ba1 Ti1 O3',151),(1000307,'1000307.mpod',1508402,NULL,'Lithium hydrogen selenide','Li1 H3 Se2 O6',152),(1000308,'1000308.mpod',1508502,NULL,'Lithium Dithioindate','Li1 In1 S2',153),(1000309,'1000309.mpod',1508503,NULL,'Lanthanum Aluminum Oxide','La1 Al1 O3',154),(1000310,'1000310.mpod',NULL,NULL,'beta-Ti0.7Nb0.3','Ti0.693 Nb0.307',155),(1000312,'1000312.mpod',NULL,NULL,'Nd-doped Sr3Y2(BO3)4','Nd0.005 Sr3 Y2 B4 O12',157),(1000313,'1000313.mpod',1010298,NULL,'Iron selenide','Fe Se0.963',158),(1000314,'1000314.mpod',1511976,NULL,'Bismuth selenido-telluride','Bi Se0.6 Te2.4',159),(1000315,'1000315.mpod',9000107,NULL,'zinc iron sulfide','Zn0.999984 Fe0.000016 S',160),(1000316,'1000316.mpod',9008857,NULL,'zinc selenide','Zn Se',160),(1000317,'1000317.mpod',9008858,NULL,'zinc iron telluride','Zn0.999932 Fe0.000068 Te',160),(1000318,'1000318.mpod',9008840,NULL,'cadmium telluride','Cd Te',160),(1000319,'1000319.mpod',2105478,NULL,'epsilon gallium selenide','Ga Se',161),(1000320,'1000320.mpod',NULL,NULL,'triglycine-zinc chloride','N3 H15 C6 O6 Zn1 Cl2',162),(1000321,'1000321.mpod',NULL,'PIN-PMN-PT:Mn','Pb(In1/2Nb1/2)O3(0.26)-Pb(Mg1/3Nb2/3)O3(0.42)-PbTiO3(0.32):Mn','Pb In0.13 Nb0.41 Mg0.14 Ti0.32 O3',163),(1000322,'1000322.mpod',9015208,'artificial Ice','Ice Ih','H2 O1',146),(1000323,'1000323.mpod',9015208,'sea Ice','Weddell sea Ice Ih','H2 O1',146),(1000324,'1000324.mpod',9009872,'MCCA','Dimethylammonium-bis(mu2 chloro)-chlorocuprate','C2 H8 N1 Cu1 Cl3',164),(1000325,'1000325.mpod',9009931,'','silver thiogallate','Ag1 Ga1 S2',165),(1000326,'1000326.mpod',9006864,'','strontium titanate','Sr1 Ti1 03',166),(1000327,'1000327.mpod',9002044,NULL,'magnesium aluminate','Mg1 Al2 04',30),(1000328,'1000328.mpod',9006952,NULL,'fluorapatite','Ca5 F O12 P3',167),(1000329,'1000329.mpod',9008835,NULL,'Boron Phosphide','B1 P1',168),(1000330,'1000330.mpod',1000285,'Bi-2212','Bi2Sr2CaCu2O8','Bi2 Sr2 Ca1 Cu2 O8',169),(1000331,'1000331.mpod',1000285,'Bi-2212','Bi2.1Sr1.8CaCu2O8','Bi2.1 Sr1.8 Ca1 Cu2 O8',169),(1000332,'1000332.mpod',1512396,NULL,'Iron Tetraborate','Fe1 B4',170),(1000333,'1000333.mpod',1512396,NULL,'Iron Tetraborate','Fe1 11B4',170),(1000334,'1000334.mpod',6000259,NULL,'calcium carbonate','Ca1 C1 O3',171),(1000335,'1000335.mpod',9005887,NULL,'cobalt oxyde','Co3 O4',172),(1000336,'1000336.mpod',9008618,NULL,'cobalt oxyde','Co1 O1',172),(1000337,'1000337.mpod',9006694,NULL,'calcium oxyde','Ca1 O1',173),(1000338,'1000338.mpod',9002682,NULL,'calco alumino silicate','Ca3 Al2 Si3 O12',174),(1000339,'1000339.mpod',NULL,NULL,'','Tl Ni2 Se2',175),(1000340,'1000340.mpod',1000285,'Bi-2212','Bi2Sr2CaCu2O8','Bi2 Sr2 Ca1 Cu2 O8',176),(1000341,'1000341.mpod',5000220,NULL,'Chromium','Cr',177),(1000342,'1000342.mpod',9012247,NULL,'Aluminum oxi-hydroxyde','Al1 O2 H1',178),(1000343,'1000343.mpod',2101499,NULL,'diamond','C1',3),(1000347,'1000347.mpod',9008678,NULL,'Sodium chloride','Na1 Cl1',3),(1000348,'1000348.mpod',1000032,NULL,'corundum','Al2 O3',3),(1000349,'1000349.mpod',9004141,NULL,'rutile','Ti1 O2',3),(1000350,'1000350.mpod',2217854,NULL,'Rochelle salt','K Na C4 H12 O10',3),(1000351,'1000351.mpod',1001768,NULL,'calcium hydroxide','Ca H2 O2',179),(1000352,'1000352.mpod',9008565,'P-doped silicon','silicon','Si1',180),(1000353,'1000353.mpod',9014575,'2H NbSe2','2H-NbSe2','Nb1 Se2',181),(1000378,'1000378.mpod',NULL,NULL,'Wurtzite','ZnO',293),(1000358,'1000358.mpod',9008084,NULL,'Low temperature chromium oxide','Cr2O3',183),(1000359,'1000359.mpod',9008084,NULL,'High temperature chromium oxide','Cr2O3',183),(1000360,'1000360.mpod',8103501,NULL,'lithium-cobalt double orthophosphate','LiCoPO4',184),(1000361,'1000361.mpod',0,NULL,'potasium erythrosiderite','K2[FeCl5(H2O)]',185),(1000362,'1000362.mpod',0,NULL,'rubidium erythrosiderite','Rb2[FeCl5(H2O)]',185),(1000363,'1000363.mpod',0,NULL,'cesium erythrosiderite','Cs2[FeCl5(H2O)]',185),(1000366,'1000366.mpod',NULL,NULL,'alpha-BaTeMo2O9','BaTeMo2O9',186),(1000367,'1000367.mpod',NULL,NULL,'galfenol15','Fe85Ga15',190),(1000368,'1000368.mpod',NULL,'PMN-PT','Bi2WO6','Bi2WO6',188),(1000370,'1000370.mpod',0,'0','galfenol24','Fe76Ga24',189),(1000371,'1000371.mpod',0,'0','galfenol29','Fe71Ga29',189),(1000369,'1000369.mpod',NULL,NULL,'galfenol19','Fe81Ga19',189),(1000372,'1000372.mpod',0,'0','galfenol13','Fe87Ga13',191),(1000373,'1000373.mpod',0,'0','galfenol14','Fe86Ga14',191),(1000374,'1000374.mpod',0,'0','galfenol15','Fe85Ga15',191),(1000375,'1000375.mpod',0,'0','galfenol17','Fe83Ga17',191),(1000376,'1000376.mpod',0,'0','galfenol19','Fe81Ga19',191),(1000377,'1000377.mpod',0,'0','galfenol21','Fe79Ga21',191);
/*!40000 ALTER TABLE `data_datafile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_datafile_property`
--

DROP TABLE IF EXISTS `data_datafile_property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_datafile_property` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datafile_id` int(11) NOT NULL,
  `property_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `datafile_id` (`datafile_id`,`property_id`)
) ENGINE=MyISAM AUTO_INCREMENT=960 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_datafile_property`
--

LOCK TABLES `data_datafile_property` WRITE;
/*!40000 ALTER TABLE `data_datafile_property` DISABLE KEYS */;
INSERT INTO `data_datafile_property` VALUES (1,1000001,10),(2,1000001,24),(3,1000002,10),(4,1000003,53),(5,1000003,54),(6,1000004,10),(7,1000005,10),(8,1000006,10),(9,1000007,10),(10,1000008,53),(11,1000009,10),(12,1000010,10),(13,1000011,10),(14,1000012,10),(15,1000013,10),(16,1000014,10),(17,1000015,10),(18,1000016,53),(19,1000016,54),(20,1000017,10),(21,1000018,10),(22,1000019,10),(23,1000020,53),(24,1000020,54),(25,1000021,10),(26,1000022,53),(27,1000023,10),(28,1000024,10),(29,1000025,10),(30,1000026,7),(31,1000026,10),(32,1000026,18),(33,1000026,33),(34,1000026,34),(35,1000026,1),(36,1000027,10),(37,1000028,10),(38,1000029,10),(39,1000030,7),(40,1000030,10),(41,1000030,33),(42,1000030,34),(43,1000030,1),(44,1000030,31),(45,1000031,37),(46,1000032,7),(47,1000032,10),(48,1000032,33),(49,1000032,34),(50,1000032,1),(51,1000032,31),(52,1000033,37),(53,1000034,10),(54,1000035,10),(55,1000036,10),(56,1000037,10),(57,1000038,10),(58,1000039,10),(59,1000040,10),(60,1000041,8),(61,1000041,9),(62,1000041,11),(63,1000041,12),(64,1000041,18),(65,1000041,33),(66,1000041,34),(67,1000041,35),(68,1000041,36),(69,1000041,2),(70,1000041,4),(71,1000041,3),(72,1000041,5),(73,1000042,18),(74,1000042,33),(75,1000042,35),(76,1000042,3),(77,1000043,8),(78,1000043,9),(79,1000043,11),(80,1000043,12),(81,1000043,18),(82,1000043,33),(83,1000043,34),(84,1000043,35),(85,1000043,36),(86,1000043,3),(87,1000043,5),(88,1000043,2),(89,1000043,4),(90,1000044,8),(91,1000044,9),(92,1000044,11),(93,1000044,12),(94,1000044,18),(95,1000044,33),(96,1000044,34),(97,1000044,35),(98,1000044,36),(99,1000044,2),(100,1000044,4),(101,1000044,3),(102,1000044,5),(103,1000045,8),(104,1000045,9),(105,1000045,11),(106,1000045,12),(107,1000045,18),(108,1000045,33),(109,1000045,34),(110,1000045,35),(111,1000045,36),(112,1000045,2),(113,1000045,4),(114,1000045,3),(115,1000045,5),(116,1000046,8),(117,1000046,9),(118,1000046,11),(119,1000046,12),(120,1000046,18),(121,1000046,33),(122,1000046,34),(123,1000046,35),(124,1000046,36),(125,1000046,3),(126,1000046,5),(127,1000046,2),(128,1000046,4),(129,1000047,8),(130,1000047,9),(131,1000047,11),(132,1000047,12),(133,1000047,18),(134,1000047,33),(135,1000047,34),(136,1000047,35),(137,1000047,36),(138,1000047,3),(139,1000047,5),(140,1000047,2),(141,1000047,4),(142,1000048,8),(143,1000048,9),(144,1000048,11),(145,1000048,12),(146,1000048,18),(147,1000048,33),(148,1000048,34),(149,1000048,35),(150,1000048,36),(151,1000048,2),(152,1000048,3),(153,1000048,4),(154,1000048,5),(155,1000049,8),(156,1000049,9),(157,1000049,11),(158,1000049,12),(159,1000049,18),(160,1000049,33),(161,1000049,34),(162,1000049,35),(163,1000049,36),(164,1000049,2),(165,1000049,3),(166,1000049,4),(167,1000049,5),(168,1000050,8),(169,1000050,9),(170,1000050,11),(171,1000050,12),(172,1000050,18),(173,1000050,33),(174,1000050,34),(175,1000050,35),(176,1000050,36),(177,1000050,3),(178,1000050,5),(179,1000050,2),(180,1000050,4),(181,1000051,8),(182,1000051,9),(183,1000051,11),(184,1000051,12),(185,1000051,18),(186,1000051,33),(187,1000051,34),(188,1000051,35),(189,1000051,36),(190,1000051,3),(191,1000051,5),(192,1000051,2),(193,1000051,4),(194,1000052,8),(195,1000052,9),(196,1000052,11),(197,1000052,12),(198,1000052,18),(199,1000052,33),(200,1000052,34),(201,1000052,35),(202,1000052,36),(203,1000052,3),(204,1000052,5),(205,1000052,2),(206,1000052,4),(207,1000053,10),(208,1000054,10),(209,1000055,12),(210,1000055,34),(211,1000056,53),(212,1000057,10),(213,1000058,10),(214,1000059,10),(215,1000060,10),(216,1000061,10),(217,1000062,10),(218,1000063,10),(219,1000064,10),(220,1000065,10),(221,1000066,53),(222,1000066,54),(223,1000066,56),(224,1000066,23),(225,1000066,29),(226,1000066,28),(227,1000067,46),(228,1000067,47),(229,1000067,44),(230,1000067,45),(231,1000067,48),(232,1000067,52),(233,1000067,51),(234,1000067,38),(235,1000067,39),(236,1000067,40),(237,1000067,41),(238,1000068,10),(239,1000069,33),(240,1000070,33),(241,1000071,10),(242,1000072,21),(243,1000072,22),(244,1000073,10),(245,1000073,21),(246,1000073,22),(247,1000074,21),(248,1000074,22),(249,1000075,7),(250,1000076,7),(251,1000077,7),(252,1000078,7),(253,1000079,7),(254,1000079,10),(255,1000080,7),(256,1000081,7),(257,1000082,7),(258,1000083,7),(259,1000084,7),(260,1000085,7),(261,1000086,7),(262,1000087,7),(263,1000088,7),(264,1000089,7),(265,1000090,7),(266,1000091,7),(267,1000092,7),(268,1000093,7),(269,1000094,33),(270,1000094,34),(271,1000095,12),(272,1000095,11),(273,1000095,9),(274,1000095,8),(275,1000095,33),(276,1000095,34),(277,1000095,35),(278,1000095,36),(279,1000095,18),(280,1000095,2),(281,1000095,3),(282,1000095,4),(283,1000095,5),(284,1000096,12),(285,1000096,11),(286,1000096,9),(287,1000096,8),(288,1000096,33),(289,1000096,34),(290,1000096,35),(291,1000096,36),(292,1000096,18),(293,1000096,2),(294,1000096,3),(295,1000096,4),(296,1000096,5),(297,1000097,46),(298,1000097,48),(299,1000097,52),(300,1000097,51),(301,1000097,38),(302,1000097,39),(303,1000097,40),(304,1000097,43),(305,1000097,41),(306,1000098,10),(307,1000099,56),(308,1000100,10),(309,1000100,7),(310,1000101,7),(311,1000102,43),(312,1000102,41),(313,1000102,46),(314,1000103,7),(315,1000104,7),(316,1000105,46),(317,1000105,47),(318,1000105,44),(319,1000105,45),(320,1000105,48),(321,1000105,52),(322,1000105,51),(323,1000106,46),(324,1000106,47),(325,1000106,44),(326,1000106,45),(327,1000106,48),(328,1000106,52),(329,1000106,51),(330,1000107,46),(331,1000107,47),(332,1000107,44),(333,1000107,45),(334,1000107,48),(335,1000107,52),(336,1000107,51),(337,1000107,43),(338,1000107,50),(339,1000108,46),(340,1000108,47),(341,1000108,44),(342,1000108,45),(343,1000108,48),(344,1000108,52),(345,1000108,51),(346,1000108,43),(347,1000108,50),(348,1000109,46),(349,1000109,47),(350,1000109,44),(351,1000109,45),(352,1000109,48),(353,1000109,52),(354,1000109,51),(355,1000109,43),(356,1000109,50),(357,1000110,46),(358,1000110,47),(359,1000110,44),(360,1000110,45),(361,1000110,48),(362,1000110,52),(363,1000110,51),(364,1000110,43),(365,1000110,50),(366,1000111,46),(367,1000111,47),(368,1000111,44),(369,1000111,45),(370,1000111,48),(371,1000111,52),(372,1000111,51),(373,1000111,43),(374,1000111,50),(375,1000112,17),(376,1000112,46),(377,1000112,47),(378,1000112,44),(379,1000112,45),(380,1000112,48),(381,1000112,52),(382,1000112,51),(383,1000112,43),(384,1000112,42),(385,1000112,49),(386,1000112,41),(387,1000112,50),(388,1000112,38),(389,1000112,39),(390,1000112,40),(391,1000113,1),(392,1000114,46),(393,1000114,44),(394,1000114,52),(395,1000114,43),(396,1000114,17),(397,1000115,1),(398,1000116,38),(399,1000116,39),(400,1000116,40),(401,1000116,17),(402,1000116,60),(403,1000116,53),(404,1000117,46),(405,1000118,56),(406,1000119,8),(407,1000119,9),(408,1000119,11),(409,1000119,12),(410,1000119,18),(411,1000119,33),(412,1000119,34),(413,1000119,35),(414,1000119,36),(415,1000119,3),(416,1000119,5),(417,1000119,2),(418,1000119,4),(419,1000120,46),(420,1000120,26),(421,1000120,27),(422,1000121,7),(423,1000122,7),(424,1000123,7),(425,1000124,7),(426,1000125,10),(427,1000126,7),(428,1000127,7),(429,1000128,7),(430,1000129,7),(431,1000130,7),(432,1000131,7),(433,1000132,7),(434,1000133,7),(435,1000134,7),(436,1000135,7),(437,1000136,7),(438,1000137,7),(439,1000138,7),(440,1000139,7),(441,1000140,7),(442,1000141,7),(443,1000142,7),(444,1000143,7),(445,1000144,7),(446,1000145,7),(447,1000146,7),(448,1000147,7),(449,1000148,7),(450,1000149,7),(451,1000150,7),(452,1000151,7),(453,1000152,7),(454,1000153,7),(455,1000154,7),(456,1000155,7),(457,1000156,7),(458,1000157,7),(459,1000158,10),(460,1000158,29),(461,1000158,28),(462,1000159,10),(463,1000160,10),(464,1000161,10),(465,1000162,10),(466,1000163,10),(467,1000164,10),(468,1000165,10),(469,1000166,7),(470,1000167,7),(471,1000168,7),(472,1000169,7),(473,1000170,7),(474,1000171,7),(475,1000172,7),(476,1000173,7),(477,1000174,7),(478,1000175,7),(479,1000176,10),(480,1000176,7),(481,1000176,1),(482,1000177,7),(483,1000177,10),(484,1000178,7),(485,1000179,7),(486,1000180,10),(487,1000181,31),(488,1000181,37),(489,1000182,31),(490,1000182,37),(491,1000183,10),(492,1000184,10),(493,1000185,10),(494,1000186,10),(495,1000187,10),(496,1000187,7),(497,1000187,56),(498,1000187,55),(499,1000188,10),(500,1000188,7),(501,1000188,55),(502,1000189,10),(503,1000189,7),(504,1000190,56),(505,1000191,56),(506,1000192,56),(507,1000193,56),(508,1000194,46),(509,1000195,46),(510,1000196,46),(511,1000197,25),(512,1000198,25),(513,1000199,44),(514,1000199,52),(515,1000200,44),(516,1000200,52),(517,1000201,44),(518,1000201,52),(519,1000202,44),(520,1000202,52),(521,1000203,10),(522,1000204,10),(523,1000205,10),(524,1000206,10),(525,1000207,10),(526,1000208,10),(527,1000209,10),(528,1000210,10),(529,1000211,10),(530,1000212,10),(531,1000213,10),(532,1000214,10),(533,1000215,10),(534,1000215,7),(535,1000216,10),(536,1000216,7),(537,1000217,10),(538,1000218,10),(539,1000219,10),(540,1000220,10),(541,1000221,10),(542,1000222,10),(543,1000222,7),(544,1000223,10),(545,1000224,10),(546,1000225,10),(547,1000226,10),(548,1000227,10),(549,1000228,10),(550,1000229,10),(551,1000230,10),(552,1000231,10),(553,1000231,7),(554,1000232,10),(555,1000233,10),(556,1000234,10),(557,1000235,10),(558,1000236,10),(559,1000237,10),(560,1000238,10),(561,1000239,10),(562,1000240,10),(563,1000241,10),(564,1000242,10),(565,1000243,10),(566,1000244,10),(567,1000245,10),(568,1000246,10),(569,1000247,10),(570,1000248,10),(571,1000249,10),(572,1000250,10),(573,1000251,10),(574,1000252,10),(575,1000253,10),(576,1000254,10),(577,1000255,25),(578,1000256,52),(579,1000256,46),(580,1000256,25),(581,1000257,52),(582,1000257,46),(583,1000257,25),(584,1000258,52),(585,1000258,46),(586,1000258,25),(587,1000259,52),(588,1000259,46),(589,1000259,25),(590,1000260,52),(591,1000260,46),(592,1000260,25),(593,1000261,10),(594,1000262,10),(595,1000263,10),(596,1000264,10),(597,1000265,10),(598,1000266,10),(599,1000267,10),(600,1000268,56),(601,1000269,56),(602,1000270,56),(603,1000271,56),(604,1000272,46),(605,1000273,46),(606,1000274,46),(607,1000274,52),(608,1000274,17),(609,1000274,43),(610,1000275,46),(611,1000275,52),(612,1000275,17),(613,1000275,43),(614,1000276,9),(615,1000276,12),(616,1000276,18),(617,1000276,33),(618,1000276,34),(619,1000276,3),(620,1000276,2),(621,1000277,9),(622,1000277,12),(623,1000277,18),(624,1000277,33),(625,1000277,34),(626,1000277,3),(627,1000277,2),(628,1000278,16),(629,1000278,15),(630,1000278,9),(631,1000278,8),(632,1000278,12),(633,1000278,11),(634,1000278,18),(635,1000278,33),(636,1000278,34),(637,1000278,35),(638,1000278,36),(639,1000278,3),(640,1000278,2),(641,1000278,5),(642,1000278,4),(643,1000279,16),(644,1000279,15),(645,1000279,9),(646,1000279,8),(647,1000279,12),(648,1000279,11),(649,1000279,18),(650,1000279,33),(651,1000279,34),(652,1000279,35),(653,1000279,36),(654,1000279,3),(655,1000279,2),(656,1000279,5),(657,1000279,4),(658,1000280,31),(659,1000280,37),(660,1000281,33),(661,1000281,18),(662,1000282,8),(663,1000282,9),(664,1000282,11),(665,1000282,12),(666,1000282,18),(667,1000282,33),(668,1000282,34),(669,1000282,35),(670,1000282,36),(671,1000282,3),(672,1000282,5),(673,1000282,2),(674,1000282,4),(675,1000283,8),(676,1000283,9),(677,1000283,11),(678,1000283,12),(679,1000283,18),(680,1000283,33),(681,1000283,34),(682,1000283,35),(683,1000283,36),(684,1000283,3),(685,1000283,5),(686,1000283,2),(687,1000283,4),(688,1000284,56),(689,1000285,56),(690,1000286,10),(691,1000287,10),(692,1000288,10),(693,1000289,10),(694,1000290,10),(695,1000291,10),(696,1000292,7),(697,1000293,7),(698,1000294,8),(699,1000294,9),(700,1000294,11),(701,1000294,12),(702,1000294,18),(703,1000294,33),(704,1000294,34),(705,1000294,35),(706,1000294,36),(707,1000294,3),(708,1000294,5),(709,1000294,2),(710,1000294,4),(711,1000295,10),(712,1000296,7),(713,1000296,10),(714,1000296,18),(715,1000296,33),(716,1000296,34),(717,1000296,1),(718,1000296,57),(719,1000296,58),(720,1000296,59),(721,1000297,13),(722,1000298,13),(723,1000299,10),(724,1000299,31),(725,1000300,10),(726,1000301,56),(727,1000302,56),(728,1000303,56),(729,1000304,2),(730,1000304,8),(731,1000304,9),(732,1000304,18),(733,1000304,33),(734,1000304,35),(735,1000305,7),(736,1000306,2),(737,1000306,9),(738,1000306,12),(739,1000306,11),(740,1000306,19),(741,1000306,20),(742,1000306,32),(743,1000306,34),(744,1000307,5),(745,1000307,9),(746,1000307,33),(747,1000307,35),(748,1000308,1),(749,1000308,7),(750,1000308,10),(751,1000308,33),(752,1000308,34),(753,1000308,57),(754,1000309,10),(755,1000310,7),(756,1000310,10),(757,1000311,6),(758,1000312,23),(759,1000312,53),(760,1000312,54),(761,1000312,56),(762,1000313,10),(763,1000314,14),(764,1000314,17),(765,1000314,60),(766,1000315,53),(767,1000316,53),(768,1000317,53),(769,1000318,53),(770,1000319,10),(771,1000320,10),(772,1000320,30),(773,1000320,31),(774,1000321,4),(775,1000321,5),(776,1000321,2),(777,1000321,3),(778,1000321,8),(779,1000321,9),(780,1000321,12),(781,1000321,11),(782,1000321,18),(783,1000321,33),(784,1000321,34),(785,1000321,35),(786,1000321,36),(787,1000322,13),(788,1000323,13),(789,1000324,25),(790,1000325,10),(791,1000326,7),(792,1000326,10),(793,1000327,10),(794,1000327,61),(795,1000327,62),(796,1000328,13),(797,1000328,63),(798,1000329,10),(799,1000329,64),(800,1000330,65),(801,1000331,65),(802,1000327,67),(803,1000327,68),(804,1000327,69),(805,1000330,66),(806,1000331,66),(807,1000332,44),(808,1000332,45),(809,1000333,44),(810,1000333,45),(811,1000334,10),(812,1000335,70),(813,1000336,70),(814,1000337,13),(815,1000337,71),(816,1000337,72),(817,1000338,71),(818,1000338,72),(819,1000338,13),(820,1000339,17),(821,1000339,51),(822,1000339,66),(823,1000339,73),(824,1000340,17),(825,1000340,52),(826,1000341,10),(827,1000342,74),(828,1000342,75),(829,1000343,53),(830,1000347,53),(831,1000348,53),(832,1000349,53),(833,1000350,53),(834,1000351,70),(835,1000352,17),(836,1000358,76),(837,1000359,76),(838,1000360,76),(839,1000361,76),(840,1000362,76),(841,1000363,76),(842,1000366,7),(843,1000356,44),(844,1000356,46),(845,1000367,77),(846,1000368,9),(847,1000368,33),(848,1000368,3),(849,1000369,78),(850,1000370,77),(851,1000370,78),(852,1000371,77),(853,1000371,78),(854,1000369,77),(855,1000372,77),(856,1000372,78),(857,1000373,77),(858,1000373,78),(859,1000374,77),(860,1000374,78),(861,1000375,77),(862,1000375,78),(863,1000376,77),(864,1000376,78),(865,1000377,77),(866,1000377,78),(959,1000378,34);
/*!40000 ALTER TABLE `data_datafile_property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_datafile_property_temp`
--

DROP TABLE IF EXISTS `data_datafile_property_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_datafile_property_temp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datafiletemp_id` int(11) NOT NULL,
  `propertytemp_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `datafile_id` (`datafiletemp_id`,`propertytemp_id`)
) ENGINE=MyISAM AUTO_INCREMENT=287 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_datafile_property_temp`
--

LOCK TABLES `data_datafile_property_temp` WRITE;
/*!40000 ALTER TABLE `data_datafile_property_temp` DISABLE KEYS */;
INSERT INTO `data_datafile_property_temp` VALUES (271,169,34),(279,176,7),(280,177,7),(281,178,7),(282,179,7),(283,180,10),(284,180,11),(285,181,10),(286,181,11);
/*!40000 ALTER TABLE `data_datafile_property_temp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_datafile_temp`
--

DROP TABLE IF EXISTS `data_datafile_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_datafile_temp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` int(11) NOT NULL,
  `filename` varchar(500) NOT NULL,
  `cod_code` int(11) DEFAULT NULL,
  `phase_generic` varchar(255) DEFAULT NULL,
  `phase_name` varchar(255) NOT NULL,
  `chemical_formula` varchar(255) NOT NULL,
  `publication_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=184 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_datafile_temp`
--

LOCK TABLES `data_datafile_temp` WRITE;
/*!40000 ALTER TABLE `data_datafile_temp` DISABLE KEYS */;
INSERT INTO `data_datafile_temp` VALUES (169,1000378,'zaqpdykfzkxkgkfwo.mpod',NULL,NULL,'Wurtzite','ZnO',184),(176,1000379,'qwryety5zmyzlofjlqljhur.mpod',NULL,NULL,'Germanium','Ge',186),(177,1000379,'qwryety5evabyddyhvcmvjp.mpod',NULL,NULL,'Diamond','C',186),(178,1000379,'qwryety5dmgdlcefmonwzhd.mpod',NULL,'fluorite, fluorspar, Irtran-3','Calcium fluoride','CaF2',187),(179,1000379,'qwryety5xauddvrdaufvivh.mpod',NULL,NULL,'Barium Flouride','BaF2',187),(180,1000379,'ywrtaw4=wbtdqwuqqtdvfmk.mpod',NULL,NULL,'BaF2','',188),(181,1000379,'ywrtaw4=diasauyzjkluels.mpod',NULL,NULL,'BaF2','',188);
/*!40000 ALTER TABLE `data_datafile_temp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_experimentalparcond`
--

DROP TABLE IF EXISTS `data_experimentalparcond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_experimentalparcond` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(511) NOT NULL,
  `units` varchar(25) NOT NULL,
  `units_detail` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_experimentalparcond`
--

LOCK TABLES `data_experimentalparcond` WRITE;
/*!40000 ALTER TABLE `data_experimentalparcond` DISABLE KEYS */;
INSERT INTO `data_experimentalparcond` VALUES (1,'_prop_conditions_frequency','conditions frequency','_conditions_frequency','s^-1','hertz'),(2,'_prop_conditions_magnetic_field','conditions magnetic field','_conditions_magnetic_field','T','tesla'),(3,'_prop_conditions_pressure','conditions pressure','_conditions_pressure','Pa','pascal'),(4,'_prop_conditions_reference_temperature_thermoelastic_non_linear_fit','conditions reference temperature thermoelastic non linear fit','_conditions_reference_temperature_thermoelastic_non_linear_fit','K','kelvin'),(5,'_prop_conditions_temperature','conditions temperature','_conditions_temperature','K','kelvin'),(6,'_prop_conditions_temperature_cycle','conditions temperature cycle','_conditions_temperature_cycle','1','pure number'),(7,'_prop_conditions_temperature_range_start','conditions temperature range start','_conditions_temperature_range_start','K','kelvin'),(8,'_prop_conditions_temperature_range_end','conditions temperature range end','_conditions_temperature_range_end','K','kelvin'),(9,'_prop_conditions_wavelength','conditions wavelength','_conditions_wavelength','10^-6.metre','micrometre'),(10,'_prop_frame','frame','_frame','n.a.','n.a.'),(11,'_prop_measurement_method','measurement method','_measurement_method','n.a.','n.a.'),(12,'_prop_measurement_poling','measurement poling','_measurement_poling','n.a.','n.a.'),(13,'_prop_symmetry_point_group_name_H-M','symmetry point group name H-M','_symmetry_point_group_name_H-M','n.a.','n.a.'),(14,'_prop_conditions_atmosphere_gas','conditions atmosphere gas','_conditions_atmosphere_gas','Pa','pascal'),(15,'_prop_conditions_atmosphere_gas_pressure','conditions atmosphere gas pressure','_conditions_atmosphere_gas_pressure','Pa','pascal'),(16,'_prop_conditions_atmosphere_gas_flow','conditions atmosphere gas flow','_conditions_atmosphere_gas_flow','1mn^-1',''),(17,'_prop_thermal_expansion_temperature_reference_T0','thermal expansion temperature reference T0','_thermal_expansion_temperature_reference_T0','K','kelvin'),(18,'_prop_thermal_expansion_temperature_range_begin','thermal expansion temperature range begin','_thermal_expansion_temperature_range_begin','K','kelvin'),(19,'_prop_thermal_expansion_temperature_range_end','thermal expansion temperature range end','_thermal_expansion_temperature_range_end','K','kelvin'),(20,'_prop_superconducting_critical_temperature_mid_50','superconducting critical temperature mid 50','_superconducting_critical_temperature_mid_50','K','kelvin'),(21,'_prop_superconducting_critical_temperature_mid_50_measurement_method','superconducting critical temperature mid 50 measurement method','_superconducting_critical_temperature_mid_50_measurement_method','n.a.','n.a.'),(22,'_prop_superconducting_resistivity_transition_width','superconducting resistivity transition width','_superconducting_resistivity_transition_width','',''),(23,'_prop_superconducting_resistivity_transition_width_measurement_method','superconducting resistivity transition width measurement method','_superconducting_resistivity_transition_width_measurement_method','n.a.','n.a.'),(24,'_prop_chargedensitywave_critical_temperature_TCDW_measurement_method','chargedensitywave critical temperature TCDW measurement method','_chargedensitywave_critical_temperature_TCDW_measurement_method','n.a.','n.a.'),(25,'_prop_heat_capacity_C0P','heat capacity C0P','_heat_capacity_C0P','',''),(26,'_prop_heat_capacity_C1P','heat capacity C1P','_heat_capacity_C1P','',''),(27,'_prop_heat_capacity_C2P','heat capacity C2P','_heat_capacity_C2P','','');
/*!40000 ALTER TABLE `data_experimentalparcond` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_experimentalparcond_temp`
--

DROP TABLE IF EXISTS `data_experimentalparcond_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_experimentalparcond_temp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(511) NOT NULL,
  `units` varchar(25) NOT NULL,
  `units_detail` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_experimentalparcond_temp`
--

LOCK TABLES `data_experimentalparcond_temp` WRITE;
/*!40000 ALTER TABLE `data_experimentalparcond_temp` DISABLE KEYS */;
INSERT INTO `data_experimentalparcond_temp` VALUES (1,'_prop_conditions_frequency','conditions frequency','_conditions_frequency','s^-1','hertz'),(2,'_prop_conditions_magnetic_field','conditions magnetic field','_conditions_magnetic_field','T','tesla'),(3,'_prop_conditions_pressure','conditions pressure','_conditions_pressure','Pa','pascal'),(4,'_prop_conditions_reference_temperature_thermoelastic_non_linear_fit','conditions reference temperature thermoelastic non linear fit','_conditions_reference_temperature_thermoelastic_non_linear_fit','K','kelvin'),(5,'_prop_conditions_temperature','conditions temperature','_conditions_temperature','K','kelvin'),(6,'_prop_conditions_temperature_cycle','conditions temperature cycle','_conditions_temperature_cycle','1','pure number'),(7,'_prop_conditions_temperature_range_start','conditions temperature range start','_conditions_temperature_range_start','K','kelvin'),(8,'_prop_conditions_temperature_range_end','conditions temperature range end','_conditions_temperature_range_end','K','kelvin'),(9,'_prop_conditions_wavelength','conditions wavelength','_conditions_wavelength','10^-6.metre','micrometre'),(10,'_prop_frame','frame','_frame','n.a.','n.a.'),(11,'_prop_measurement_method','measurement method','_measurement_method','n.a.','n.a.'),(12,'_prop_measurement_poling','measurement poling','_measurement_poling','n.a.','n.a.'),(13,'_prop_symmetry_point_group_name_H-M','symmetry point group name H-M','_symmetry_point_group_name_H-M','n.a.','n.a.'),(14,'_prop_conditions_atmosphere_gas','conditions atmosphere gas','_conditions_atmosphere_gas','Pa','pascal'),(15,'_prop_conditions_atmosphere_gas_pressure','conditions atmosphere gas pressure','_conditions_atmosphere_gas_pressure','Pa','pascal'),(16,'_prop_conditions_atmosphere_gas_flow','conditions atmosphere gas flow','_conditions_atmosphere_gas_flow','1mn^-1',''),(17,'_prop_thermal_expansion_temperature_reference_T0','thermal expansion temperature reference T0','_thermal_expansion_temperature_reference_T0','K','kelvin'),(18,'_prop_thermal_expansion_temperature_range_begin','prop thermal expansion temperature range begin','_thermal_expansion_temperature_range_begin','K','kelvin'),(19,'_prop_thermal_expansion_temperature_range_end','prop thermal expansion temperature range end','_thermal_expansion_temperature_range_end','K','kelvin'),(20,'_prop_superconducting_critical_temperature_mid_50','superconducting critical temperature mid 50','_superconducting_critical_temperature_mid_50','K','kelvin'),(21,'_prop_superconducting_critical_temperature_mid_50_measurement_method','superconducting critical temperature mid 50 measurement method','_superconducting_critical_temperature_mid_50_measurement_method','n.a.','n.a.'),(22,'_prop_superconducting_resistivity_transition_width','superconducting resistivity transition width','_superconducting_resistivity_transition_width','',''),(23,'_prop_superconducting_resistivity_transition_width_measurement_method','superconducting resistivity transition width measurement method','_superconducting_resistivity_transition_width_measurement_method','n.a.','n.a.'),(24,'_prop_chargedensitywave_critical_temperature_TCDW_measurement_method','chargedensitywave critical temperature TCDW measurement method','_chargedensitywave_critical_temperature_TCDW_measurement_method','n.a.','n.a.'),(25,'_prop_heat_capacity_C0P','heat capacity C0P','_heat_capacity_C0P','',''),(26,'_prop_heat_capacity_C1P','heat capacity C1P','_heat_capacity_C1P','',''),(27,'_prop_heat_capacity_C2P','heat capacity C2P','_heat_capacity_C2P','',''),(33,'_prop_heat_capacity_parallel','heat capacity parallel','_heat_capacity_parallel','n.a.','n.a.'),(34,'_prop_heat_capacity_perpendicular','heat capaciti perpendicular','_heat_capacity_perpendicular','n.a.','n.a.');
/*!40000 ALTER TABLE `data_experimentalparcond_temp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_phase`
--

DROP TABLE IF EXISTS `data_phase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_phase` (
  `id` int(11) NOT NULL,
  `description` varchar(511) NOT NULL,
  `name` varchar(511) NOT NULL,
  `active` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_phase`
--

LOCK TABLES `data_phase` WRITE;
/*!40000 ALTER TABLE `data_phase` DISABLE KEYS */;
INSERT INTO `data_phase` VALUES (1,'phase name','_phase_name',1),(2,'phase generic','_phase_generic',1),(3,'phase formula','_phase_formula',0),(4,'phase density','_phase_density',0),(5,'phase density temperature','_phase_density_temperature',0),(6,'phase transition temperature melting','_phase_transition_temperature_melting',0),(7,'phase transition temperature rhomb tetra','_phase_transition_temperature_rhomb_tetra',0),(8,'phase transition temperature rhomb ortho','_phase_transition_temperature_rhomb_ortho',0),(9,'phase transition temperature ortho tetra','_phase_transition_temperature_ortho_tetra',0),(10,'phase transition temperature curie','_phase_transition_temperature_curie',0),(11,'phase transition temperature curie ferroelectric','_phase_transition_temperature_curie_ferroelectric',0),(12,'phase cell temperature','_phase_cell_temperature',0),(13,'phase debye temperature','_phase_debye_temperature',0);
/*!40000 ALTER TABLE `data_phase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_property`
--

DROP TABLE IF EXISTS `data_property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_property` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(511) NOT NULL,
  `tensor_dimensions` varchar(10) NOT NULL,
  `units` varchar(25) NOT NULL,
  `units_detail` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=79 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_property`
--

LOCK TABLES `data_property` WRITE;
/*!40000 ALTER TABLE `data_property` DISABLE KEYS */;
INSERT INTO `data_property` VALUES (1,'_prop_dielectric_permittivity_relative_epsrij',' prop dielectric permittivity relative epsrij','_dielectric_permittivity_relative_epsrij','3,3','1','pure number'),(2,'_prop_dielectric_permittivity_relative_epsrijS',' prop dielectric permittivity relative epsrijS','_dielectric_permittivity_relative_epsrijS','3,3','1','pure number'),(3,'_prop_dielectric_permittivity_relative_epsrijT',' prop dielectric permittivity relative epsrijT','_dielectric_permittivity_relative_epsrijT','3,3','1','pure number'),(4,'_prop_dielectric_stiffness_relative_betrijS',' prop dielectric stiffness relative betrijS','_dielectric_stiffness_relative_betrijS','3,3','10^-4','pure number'),(5,'_prop_dielectric_stiffness_relative_betrijT',' prop dielectric stiffness relative betrijT','_dielectric_stiffness_relative_betrijT','3,3','10^-4','pure number'),(6,'_prop_elastic_TOEC_stiffness_cijk',' prop elastic TOEC stiffness cijk','_elastic_TOEC_stiffness_cijk','6,6,6','GPa','giga Pascal'),(7,'_prop_elastic_compliance_sij',' prop elastic compliance sij','_elastic_compliance_sij','6,6','10^-12.Pa^-1','pico Pascal^-1'),(8,'_prop_elastic_compliance_sijD',' prop elastic compliance sijD','_elastic_compliance_sijD','6,6','10^-12.Pa^-1','pico Pascal^-1'),(9,'_prop_elastic_compliance_sijE',' prop elastic compliance sijE','_elastic_compliance_sijE','6,6','10^-12.Pa^-1','pico Pascal^-1'),(10,'_prop_elastic_stiffness_cij',' prop elastic stiffness cij','_elastic_stiffness_cij','6,6','GPa','giga Pascal'),(11,'_prop_elastic_stiffness_cijD',' prop elastic stiffness cijD','_elastic_stiffness_cijD','6,6','GPa','giga Pascal'),(12,'_prop_elastic_stiffness_cijE',' prop elastic stiffness cijE','_elastic_stiffness_cijE','6,6','GPa','giga Pascal'),(13,'_prop_elastic_stiffness_cijS',' prop elastic stiffness cijS','_elastic_stiffness_cijS','6,6','GPa','giga Pascal'),(14,'_prop_electric_charge_carrier_concentration_n',' prop electric charge carrier concentration n','_electric_charge_carrier_concentration_n','0','10^19 cm-3','atoms per cubic centimetre'),(15,'_prop_electric_coercive_field_Eci',' prop electric coercive field Eci','_electric_coercive_field_Eci','3','kV.cm^-1','kilovolts per centimetre'),(16,'_prop_electric_remnant_polarisation_Pri',' prop electric remnant polarisation Pri','_electric_remnant_polarisation_Pri','3','10^-6 Ohm.cm^-2','micro Ohm per square centimetre'),(17,'_prop_electric_resistivity_rhoeij',' prop electric resistivity rhoeij','_electric_resistivity_rhoeij','3,3','10^-6 Ohm.cm','micro Ohm per centimetre'),(18,'_prop_electromechanical_coupling_kij',' prop electromechanical coupling kij','_electromechanical_coupling_kij','3,6','1','pure number'),(19,'_prop_electrooptic_rijkS',' prop electrooptic rijkS','_electrooptic_rijkS','3,3,3','10^-12.m.V','parts per trillion metres volts'),(20,'_prop_electrooptic_rijkT',' prop electrooptic rijkT','_electrooptic_rijkT','3,3,3','10^-12.m.V','parts per trillion metres volts'),(21,'_prop_electrostriction_Dij',' prop electrostriction Dij','_electrostriction_Dij','6,6','10^-20.m^2.V^-2 and m^4.C','10^-20.m^2V^-2 and m^4.C^-2'),(22,'_prop_electrostriction_Dprimeij',' prop electrostriction Dprimeij','_electrostriction_Dprimeij','6,6','10^-20.m^2.V^-2 and m^4.C','10^-20.m^2V^-2 and m^4.C^-2'),(23,'_prop_heat_capacity_C',' prop heat capacity C','_heat_capacity_C','0','Jg^-1K^-1','joules per gram per kelvin'),(24,'_prop_internal_friction_Qij-1',' prop internal friction Qij-1','_internal_friction_Qij-1','6,6','10^-4','pure number'),(25,'_prop_magnetic_antiferromagnetic_ordering_temperature_Neel',' prop magnetic antiferromagnetic ordering temperature Neel','_magnetic_antiferromagnetic_ordering_temperature_Neel','0','K','kelvin'),(26,'_prop_magnetic_paramagnetic_critical_temperature_Neel',' prop magnetic paramagnetic critical temperature Neel','_magnetic_paramagnetic_critical_temperature_Neel','0','K','kelvin'),(27,'_prop_magnetic_paramagnetic_critical_temperature_Neel_transitionwidth',' prop magnetic paramagnetic critical temperature Neel transitionwidth','_magnetic_paramagnetic_critical_temperature_Neel_transitionwidth','0','K','kelvin'),(28,'_prop_optical_index_extraordinary_ne',' prop optical index extraordinary ne','_optical_index_extraordinary_ne','0','1','pure number'),(29,'_prop_optical_index_ordinary_no',' prop optical index ordinary no','_optical_index_ordinary_no','0','1','pure number'),(30,'_prop_optical_index_principal_Ni',' prop optical index principal Ni','_optical_index_principal_Ni','0','1','pure number'),(31,'_prop_photoelastic_pij',' prop photoelastic pij','_photoelastic_pij','6,6','1','pure number'),(32,'_prop_photoelastic_pijE',' prop photoelastic pijE','_photoelastic_pijE','0','1','pure number'),(33,'_prop_piezoelectric_dij',' prop piezoelectric dij','_piezoelectric_dij','3,6','m.V^-1','meter per volt'),(34,'_prop_piezoelectric_eij',' prop piezoelectric eij','_piezoelectric_eij','3,6','C.N^-1','coulomb per newton'),(35,'_prop_piezoelectric_gij',' prop piezoelectric gij','_piezoelectric_gij','3,6','C.m^-2','coulomb oer square metre'),(36,'_prop_piezoelectric_hij',' prop piezoelectric hij','_piezoelectric_hij','3,6','V.m.N^-1','volt metre per newton'),(37,'_prop_piezooptic_piij',' prop piezooptic piij','_piezooptic_piij','6,6','MPa^-1','one over mega Pascal'),(38,'_prop_residual_resistivity_ratio',' prop residual resistivity ratio','_residual_resistivity_ratio','0','1','pure number'),(39,'_prop_residual_resistivity_ratio_high_temperature',' prop residual resistivity ratio high temperature','_residual_resistivity_ratio_high_temperature','0','K','kelvin'),(40,'_prop_residual_resistivity_ratio_low_temperature',' prop residual resistivity ratio low temperature','_residual_resistivity_ratio_low_temperature','0','K','kelvin'),(41,'_prop_superconducting_coherence_length_ksii',' prop superconducting coherence length ksii','_superconducting_coherence_length_ksii','3','nm','nanometre'),(42,'_prop_superconducting_critical_field1_Hc1i',' prop superconducting critical field1 Hc1i','_superconducting_critical_field1_Hc1i','3','T','tesla'),(43,'_prop_superconducting_critical_field2_Hc2i',' prop superconducting critical field2 Hc2i','_superconducting_critical_field2_Hc2i','3','T','tesla'),(44,'_prop_superconducting_critical_temperature_mid_50',' prop superconducting critical temperature mid 50','_superconducting_critical_temperature_mid_50','0','K','kelvin'),(45,'_prop_superconducting_critical_temperature_offset_10',' prop superconducting critical temperature offset 10','_superconducting_critical_temperature_offset_10','0','K','kelvin'),(46,'_prop_superconducting_critical_temperature_onset',' prop superconducting critical temperature onset','_superconducting_critical_temperature_onset','0','K','kelvin'),(47,'_prop_superconducting_critical_temperature_onset_90',' prop superconducting critical temperature onset 90','_superconducting_critical_temperature_onset_90','0','K','kelvin'),(48,'_prop_superconducting_critical_temperature_thermodynamic',' prop superconducting critical temperature thermodynamic','_superconducting_critical_temperature_thermodynamic','0','K','kelvin'),(49,'_prop_superconducting_irreversibility_field_Hirri',' prop superconducting irreversibility field Hirri','_superconducting_irreversibility_field_Hirri','3','T','tesla'),(50,'_prop_superconducting_penetration_depth_lambdai',' prop superconducting penetration depth lambdai','_superconducting_penetration_depth_lambdai','3','nm','nanometre'),(51,'_prop_superconducting_resistivity_transition_width',' prop superconducting resistivity transition width','_superconducting_resistivity_transition_width','0','K','kelvin'),(52,'_prop_superconducting_zero_resistivity_temperature',' prop superconducting zero resistivity temperature','_superconducting_zero_resistivity_temperature','0','K','kelvin'),(53,'_prop_thermal_conductivity_kappaij',' prop thermal conductivity kappaij','_thermal_conductivity_kappaij','3,3','W.K^-1.m^-1','watt per kelvin per metre'),(54,'_prop_thermal_diffusivity_kappadij',' prop thermal diffusivity kappadij','_thermal_diffusivity_kappadij','3,3','m^2.s^-1','metre squared per second'),(55,'_prop_thermal_expansion_Tij',' prop thermal expansion Tij','_thermal_expansion_Tij','6,6','MPa.K^-1','megapascal per kelvin'),(56,'_prop_thermal_expansion_alphaij',' prop thermal expansion alphaij','_thermal_expansion_alphaij','3,3','10^-6.K^-1','parts per million per kelvin'),(57,'_prop_thermoelastic_compliance_1storder_sij1T',' prop thermoelastic compliance 1storder sij1T','_thermoelastic_compliance_1storder_sij1T','6,6','10^-6.K^-1','parts per million per kelvin'),(58,'_prop_thermoelastic_compliance_2ndorder_sij2T',' prop thermoelastic compliance 2ndorder sij2T','_thermoelastic_compliance_2ndorder_sij2T','6,6','10^-9.K^-1','parts per million per kelvin'),(59,'_prop_thermoelastic_compliance_3rdorder_sij3T',' prop thermoelastic compliance 3rdorder sij3T','_thermoelastic_compliance_3rdorder_sij3T','6,6','10^-12.K^-1','parts per million per kelvin'),(60,'_prop_thermoelectric_Seebeck_Seij',' prop thermoelectric Seebeck Seij','_thermoelectric_Seebeck_Seij','3,3','10^-6.V.K^-1','parts per million volts per kelvin'),(61,'_prop_elastic_stiffness_hydrostaticpressure_1storder_cij1P','prop elastic stiffness hydrostaticpressure 1storder cij1P','elastic_stiffness_hydrostaticpressure_1storder_cij1P','6,6','GPa^-1','giga Pascal'),(62,'_prop_elastic_stiffness_hydrostaticpressure_2ndorder_cij2P','prop elastic stiffness hydrostaticpressure 2ndorder cij2P','_elasticstiffness_hydrostaticpressure_2ndorder_cij2P','6,6','GPa^-1','giga Pascal'),(63,'_prop_elastic_compliance_sijS','prop elastic compliance sijS','_elastic_compliance_sijS','6,6','10^-12.Pa^-1','pico Pascal^-1'),(64,'_prop_optical_index_ni',' prop optical index ni','_optical_index_ni','0','1','pure number'),(65,'_prop_superconducting_critical_current_density_Jci','prop superconducting critical current density Jci','_superconducting_critical_current_density_Jci','0','Am^-2','ampere per square metre'),(66,'_prop_superconducting_critical_temperature','prop superconducting critical temperature','_superconducting_critical_temperature','0','K','kelvin'),(67,'_prop_hydrostatic_pressure_range_begin','prop hydrostatic pressure range begin','_hydrostatic_pressure_range_begin','0','GPa','giga Pascal'),(68,'_prop_hydrostatic_pressure_range_end','prop hydrostatic pressure range end','_hydrostatic_pressure_range_end','0','GPa','giga Pascal'),(69,'_prop_reference_hydrostatic_pressure','prop reference hydrostatic pressure','_reference_hydrostatic_pressure','0','GPa','giga Pascal'),(70,'_prop_heat_capacity_Cp','prop heat capacity Cp','_heat_capacity_Cp','0','Jmol^-1K^-1','joule per kelvin mole'),(71,'_prop_thermoelasticstiffness_1storder_cijS1T','prop thermoelasticstiffness 1storder cijS1T','_thermoelasticstiffness_1storder_cijS1T','6,6','10^-6.K^-1','parts per million per kelvin'),(72,'_prop_thermoelasticstiffness_2ndorder_cijS2T','prop thermoelasticstiffness 2ndorder cijS2T','_thermoelasticstiffness_2ndorder_cijS2T','6,6','10^-9.K^-2','parts per million per square kelvin'),(73,'_prop_RRR','prop RRR','_RRR','0','',''),(74,'_prop_thermal_expansion_alphaijT0','prop thermal expansion alphaijT0','_thermal_expansion_alphaijT0','3,3','10^-6.K^-1','parts per million per kelvin'),(75,'_prop_thermal_expansion_alphaijT','prop thermal expansion alphaijT','_thermal_expansion_alphaijT','3,3','10^-6.K^-1','parts per million per kelvin'),(76,'_prop_magnetoelectric_MEalphaij','prop magnetoelectric MEalphaij','_magnetoelectric_MEalphaij','3,3','10^-12 s m^-1',''),(77,'_prop_magnetocrystalline_anisotropy_k1,_k2','prop magnetocrystalline anisotropy k1, k2','_prop_magnetocrystalline_anisotropy_k1,_k2','2','10^4 J.m^-3','joule.meter.^-3'),(78,'_prop_magnetostriction_lambda_100,_lambda_111','prop magnetostriction lambda 100, lambda 111','_prop_magnetostriction_lambda_100,_lambda_111','2','ppm','parts per million');
/*!40000 ALTER TABLE `data_property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_property_temp`
--

DROP TABLE IF EXISTS `data_property_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_property_temp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(511) NOT NULL,
  `tensor_dimensions` varchar(10) NOT NULL,
  `units` varchar(25) NOT NULL,
  `units_detail` varchar(60) NOT NULL,
  `short_tag` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=101 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_property_temp`
--

LOCK TABLES `data_property_temp` WRITE;
/*!40000 ALTER TABLE `data_property_temp` DISABLE KEYS */;
INSERT INTO `data_property_temp` VALUES (1,'_prop_dielectric_permittivity_relative_epsrij',' prop dielectric permittivity relative epsrij','_dielectric_permittivity_relative_epsrij','3,3','1','pure number','epsrij'),(2,'_prop_dielectric_permittivity_relative_epsrijS',' prop dielectric permittivity relative epsrijS','_dielectric_permittivity_relative_epsrijS','3,3','1','pure number','epsrijS'),(3,'_prop_dielectric_permittivity_relative_epsrijT',' prop dielectric permittivity relative epsrijT','_dielectric_permittivity_relative_epsrijT','3,3','1','pure number','epsrijT'),(4,'_prop_dielectric_stiffness_relative_betrijS',' prop dielectric stiffness relative betrijS','_dielectric_stiffness_relative_betrijS','3,3','10^-4','pure number','betrijS'),(5,'_prop_dielectric_stiffness_relative_betrijT',' prop dielectric stiffness relative betrijT','_dielectric_stiffness_relative_betrijT','3,3','10^-4','pure number','betrijT'),(6,'_prop_elastic_TOEC_stiffness_cijk',' prop elastic TOEC stiffness cijk','_elastic_TOEC_stiffness_cijk','6,6,6','GPa','giga Pascal','cijk'),(7,'_prop_elastic_compliance_sij',' prop elastic compliance sij','_elastic_compliance_sij','6,6','10^-12.Pa^-1','pico Pascal^-1','sij'),(8,'_prop_elastic_compliance_sijD',' prop elastic compliance sijD','_elastic_compliance_sijD','6,6','10^-12.Pa^-1','pico Pascal^-1','sijD'),(9,'_prop_elastic_compliance_sijE',' prop elastic compliance sijE','_elastic_compliance_sijE','6,6','10^-12.Pa^-1','pico Pascal^-1','sijE'),(10,'_prop_elastic_stiffness_cij',' prop elastic stiffness cij','_elastic_stiffness_cij','6,6','GPa','giga Pascal','cij'),(11,'_prop_elastic_stiffness_cijD',' prop elastic stiffness cijD','_elastic_stiffness_cijD','6,6','GPa','giga Pascal','cijD'),(12,'_prop_elastic_stiffness_cijE',' prop elastic stiffness cijE','_elastic_stiffness_cijE','6,6','GPa','giga Pascal','cijE'),(13,'_prop_elastic_stiffness_cijS',' prop elastic stiffness cijS','_elastic_stiffness_cijS','6,6','GPa','giga Pascal','cijS'),(14,'_prop_electric_charge_carrier_concentration_n',' prop electric charge carrier concentration n','_electric_charge_carrier_concentration_n','0','10^19 cm-3','atoms per cubic centimetre',NULL),(15,'_prop_electric_coercive_field_Eci',' prop electric coercive field Eci','_electric_coercive_field_Eci','3','kV.cm^-1','kilovolts per centimetre','Eci'),(16,'_prop_electric_remnant_polarisation_Pri',' prop electric remnant polarisation Pri','_electric_remnant_polarisation_Pri','3','10^-6 Ohm.cm^-2','micro Ohm per square centimetre','Pri'),(17,'_prop_electric_resistivity_rhoeij',' prop electric resistivity rhoeij','_electric_resistivity_rhoeij','3,3','10^-6 Ohm.cm','micro Ohm per centimetre','rhoeij'),(18,'_prop_electromechanical_coupling_kij',' prop electromechanical coupling kij','_electromechanical_coupling_kij','3,6','1','pure number','kij'),(19,'_prop_electrooptic_rijkS',' prop electrooptic rijkS','_electrooptic_rijkS','3,3,3','10^-12.m.V','parts per trillion metres volts','rijkS'),(20,'_prop_electrooptic_rijkT',' prop electrooptic rijkT','_electrooptic_rijkT','3,3,3','10^-12.m.V','parts per trillion metres volts','rijkT'),(21,'_prop_electrostriction_Dij',' prop electrostriction Dij','_electrostriction_Dij','6,6','10^-20.m^2.V^-2 and m^4.C','10^-20.m^2V^-2 and m^4.C^-2','Dij'),(22,'_prop_electrostriction_Dprimeij',' prop electrostriction Dprimeij','_electrostriction_Dprimeij','6,6','10^-20.m^2.V^-2 and m^4.C','10^-20.m^2V^-2 and m^4.C^-2','Dprimeij'),(23,'_prop_heat_capacity_C',' prop heat capacity C','_heat_capacity_C','0','Jg^-1K^-1','joules per gram per kelvin',NULL),(24,'_prop_internal_friction_Qij-1',' prop internal friction Qij-1','_internal_friction_Qij-1','6,6','10^-4','pure number','Qij-1'),(25,'_prop_magnetic_antiferromagnetic_ordering_temperature_Neel',' prop magnetic antiferromagnetic ordering temperature Neel','_magnetic_antiferromagnetic_ordering_temperature_Neel','0','K','kelvin',NULL),(26,'_prop_magnetic_paramagnetic_critical_temperature_Neel',' prop magnetic paramagnetic critical temperature Neel','_magnetic_paramagnetic_critical_temperature_Neel','0','K','kelvin',NULL),(27,'_prop_magnetic_paramagnetic_critical_temperature_Neel_transitionwidth',' prop magnetic paramagnetic critical temperature Neel transitionwidth','_magnetic_paramagnetic_critical_temperature_Neel_transitionwidth','0','K','kelvin',NULL),(28,'_prop_optical_index_extraordinary_ne',' prop optical index extraordinary ne','_optical_index_extraordinary_ne','0','1','pure number',NULL),(29,'_prop_optical_index_ordinary_no',' prop optical index ordinary no','_optical_index_ordinary_no','0','1','pure number',NULL),(30,'_prop_optical_index_principal_Ni',' prop optical index principal Ni','_optical_index_principal_Ni','0','1','pure number',NULL),(31,'_prop_photoelastic_pij',' prop photoelastic pij','_photoelastic_pij','6,6','1','pure number','pij'),(32,'_prop_photoelastic_pijE',' prop photoelastic pijE','_photoelastic_pijE','0','1','pure number','pijE'),(33,'_prop_piezoelectric_dij',' prop piezoelectric dij','_piezoelectric_dij','3,6','m.V^-1','meter per volt','dij'),(34,'_prop_piezoelectric_eij',' prop piezoelectric eij','_piezoelectric_eij','3,6','C.N^-1','coulomb per newton','eij'),(35,'_prop_piezoelectric_gij',' prop piezoelectric gij','_piezoelectric_gij','3,6','C.m^-2','coulomb oer square metre','gij'),(36,'_prop_piezoelectric_hij',' prop piezoelectric hij','_piezoelectric_hij','3,6','V.m.N^-1','volt metre per newton','hij'),(37,'_prop_piezooptic_piij',' prop piezooptic piij','_piezooptic_piij','6,6','MPa^-1','one over mega Pascal','piij'),(38,'_prop_residual_resistivity_ratio',' prop residual resistivity ratio','_residual_resistivity_ratio','0','1','pure number',NULL),(39,'_prop_residual_resistivity_ratio_high_temperature',' prop residual resistivity ratio high temperature','_residual_resistivity_ratio_high_temperature','0','K','kelvin',NULL),(40,'_prop_residual_resistivity_ratio_low_temperature',' prop residual resistivity ratio low temperature','_residual_resistivity_ratio_low_temperature','0','K','kelvin',NULL),(41,'_prop_superconducting_coherence_length_ksii',' prop superconducting coherence length ksii','_superconducting_coherence_length_ksii','3','nm','nanometre','ksii'),(42,'_prop_superconducting_critical_field1_Hc1i',' prop superconducting critical field1 Hc1i','_superconducting_critical_field1_Hc1i','3','T','tesla','Hc1i'),(43,'_prop_superconducting_critical_field2_Hc2i',' prop superconducting critical field2 Hc2i','_superconducting_critical_field2_Hc2i','3','T','tesla','Hc2i'),(44,'_prop_superconducting_critical_temperature_mid_50',' prop superconducting critical temperature mid 50','_superconducting_critical_temperature_mid_50','0','K','kelvin',NULL),(45,'_prop_superconducting_critical_temperature_offset_10',' prop superconducting critical temperature offset 10','_superconducting_critical_temperature_offset_10','0','K','kelvin',NULL),(46,'_prop_superconducting_critical_temperature_onset',' prop superconducting critical temperature onset','_superconducting_critical_temperature_onset','0','K','kelvin',NULL),(47,'_prop_superconducting_critical_temperature_onset_90',' prop superconducting critical temperature onset 90','_superconducting_critical_temperature_onset_90','0','K','kelvin',NULL),(48,'_prop_superconducting_critical_temperature_thermodynamic',' prop superconducting critical temperature thermodynamic','_superconducting_critical_temperature_thermodynamic','0','K','kelvin',NULL),(49,'_prop_superconducting_irreversibility_field_Hirri',' prop superconducting irreversibility field Hirri','_superconducting_irreversibility_field_Hirri','3','T','tesla','Hirri'),(50,'_prop_superconducting_penetration_depth_lambdai',' prop superconducting penetration depth lambdai','_superconducting_penetration_depth_lambdai','3','nm','nanometre','lambdai'),(51,'_prop_superconducting_resistivity_transition_width',' prop superconducting resistivity transition width','_superconducting_resistivity_transition_width','0','K','kelvin',NULL),(52,'_prop_superconducting_zero_resistivity_temperature',' prop superconducting zero resistivity temperature','_superconducting_zero_resistivity_temperature','0','K','kelvin',NULL),(53,'_prop_thermal_conductivity_kappaij',' prop thermal conductivity kappaij','_thermal_conductivity_kappaij','3,3','W.K^-1.m^-1','watt per kelvin per metre','kappaij'),(54,'_prop_thermal_diffusivity_kappadij',' prop thermal diffusivity kappadij','_thermal_diffusivity_kappadij','3,3','m^2.s^-1','metre squared per second','kappadij'),(55,'_prop_thermal_expansion_Tij',' prop thermal expansion Tij','_thermal_expansion_Tij','6,6','MPa.K^-1','megapascal per kelvin','Tij'),(56,'_prop_thermal_expansion_alphaij',' prop thermal expansion alphaij','_thermal_expansion_alphaij','3,3','10^-6.K^-1','parts per million per kelvin','alphaij'),(57,'_prop_thermoelastic_compliance_1storder_sij1T',' prop thermoelastic compliance 1storder sij1T','_thermoelastic_compliance_1storder_sij1T','6,6','10^-6.K^-1','parts per million per kelvin','sij1T'),(58,'_prop_thermoelastic_compliance_2ndorder_sij2T',' prop thermoelastic compliance 2ndorder sij2T','_thermoelastic_compliance_2ndorder_sij2T','6,6','10^-9.K^-1','parts per million per kelvin','sij2T'),(59,'_prop_thermoelastic_compliance_3rdorder_sij3T',' prop thermoelastic compliance 3rdorder sij3T','_thermoelastic_compliance_3rdorder_sij3T','6,6','10^-12.K^-1','parts per million per kelvin','sij3T'),(60,'_prop_thermoelectric_Seebeck_Seij',' prop thermoelectric Seebeck Seij','_thermoelectric_Seebeck_Seij','3,3','10^-6.V.K^-1','parts per million volts per kelvin','Seij'),(61,'_prop_elastic_stiffness_hydrostaticpressure_1storder_cij1P','prop elastic stiffness hydrostaticpressure 1storder cij1P','elastic_stiffness_hydrostaticpressure_1storder_cij1P','6,6','GPa^-1','giga Pascal','cij1P'),(62,'_prop_elastic_stiffness_hydrostaticpressure_2ndorder_cij2P','prop elastic stiffness hydrostaticpressure 2ndorder cij2P','_elasticstiffness_hydrostaticpressure_2ndorder_cij2P','6,6','GPa^-1','giga Pascal','cij2P'),(100,'_prop_elastic_compliance_sijS','elastic compliance sijS','_elastic_compliance_sijS','','10^-12.Pa^-1','metre square over tera pascal','sijS'),(64,'_prop_optical_index_ni',' prop optical index ni','_optical_index_ni','0','1','pure number',NULL),(65,'_prop_superconducting_critical_current_density_Jci','prop superconducting critical current density Jci','_superconducting_critical_current_density_Jci','0','Am^-2','ampere per square metre',NULL),(66,'_prop_superconducting_critical_temperature','prop superconducting critical temperature','_superconducting_critical_temperature','0','K','kelvin',NULL),(67,'_prop_hydrostatic_pressure_range_begin','prop hydrostatic pressure range begin','_hydrostatic_pressure_range_begin','0','GPa','giga Pascal',NULL),(68,'_prop_hydrostatic_pressure_range_end','prop hydrostatic pressure range end','_hydrostatic_pressure_range_end','0','GPa','giga Pascal',NULL),(69,'_prop_reference_hydrostatic_pressure','prop reference hydrostatic pressure','_reference_hydrostatic_pressure','0','GPa','giga Pascal',NULL),(70,'_prop_heat_capacity_Cp','prop heat capacity Cp','_heat_capacity_Cp','0','Jmol^-1K^-1','joule per kelvin mole',NULL),(71,'_prop_thermoelasticstiffness_1storder_cijS1T','prop thermoelasticstiffness 1storder cijS1T','_thermoelasticstiffness_1storder_cijS1T','6,6','10^-6.K^-1','parts per million per kelvin','cijS1T'),(72,'_prop_thermoelasticstiffness_2ndorder_cijS2T','prop thermoelasticstiffness 2ndorder cijS2T','_thermoelasticstiffness_2ndorder_cijS2T','6,6','10^-9.K^-2','parts per million per square kelvin','cijS2T'),(73,'_prop_RRR','prop RRR','_RRR','0','','',NULL),(74,'_prop_thermal_expansion_alphaijT0','prop thermal expansion alphaijT0','_thermal_expansion_alphaijT0','3,3','10^-6.K^-1','parts per million per kelvin','alphaijT0'),(75,'_prop_thermal_expansion_alphaijT','prop thermal expansion alphaijT','_thermal_expansion_alphaijT','3,3','10^-6.K^-1','parts per million per kelvin','alphaijT'),(76,'_prop_magnetoelectric_MEalphaij','prop magnetoelectric MEalphaij','_magnetoelectric_MEalphaij','3,3','10^-12 s m^-1','','MEalphaij'),(77,'_prop_magnetocrystalline_anisotropy_k1,_k2','prop magnetocrystalline anisotropy k1, k2','_prop_magnetocrystalline_anisotropy_k1,_k2','2','10^4 J.m^-3','joule.meter.^-3','ki'),(78,'_prop_magnetostriction_lambda_100,_lambda_111','prop magnetostriction lambda 100, lambda 111','_prop_magnetostriction_lambda_100,_lambda_111','2','ppm','parts per million','ki');
/*!40000 ALTER TABLE `data_property_temp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_publarticle`
--

DROP TABLE IF EXISTS `data_publarticle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_publarticle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `authors` varchar(255) NOT NULL,
  `journal` varchar(127) NOT NULL,
  `year` int(11) DEFAULT NULL,
  `volume` varchar(6) DEFAULT NULL,
  `issue` int(11) DEFAULT NULL,
  `first_page` int(11) DEFAULT NULL,
  `last_page` int(11) DEFAULT NULL,
  `reference` varchar(14) DEFAULT NULL,
  `pages_number` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=294 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_publarticle`
--

LOCK TABLES `data_publarticle` WRITE;
/*!40000 ALTER TABLE `data_publarticle` DISABLE KEYS */;
INSERT INTO `data_publarticle` VALUES (1,'Elastic constants and anisotropic internal frictions of decagonal Al72Ni18Co8 single quasicrystal at low temperature','Tarumi R.; Ledbetter H.; Shiomi S.; Ogi H.; Hirao M.; Tsai A.P.','Journal of Applied Physics',2010,'108',1,NULL,NULL,'013514',5),(2,'Third-Order Elastic Constants of Aluminum','Thomas,Jr., J.F.','Physical Review',1968,'175',3,955,962,NULL,NULL),(3,'?','?','?',NULL,'?',NULL,NULL,NULL,NULL,NULL),(4,'Ultrasonic velocities in solid argon','Moeller H.R.; Squire C.F.','Physical Review',1966,'151',2,689,693,NULL,NULL),(5,'Monocrystal elastic constants and derived properties of the cubic and the hexagonal elements','Ledbetter H.; Kim S.','',2000,'2',NULL,NULL,NULL,NULL,NULL),(6,'Shear moduli of polycrystalline cubic elements','Sisodia P.; Verma M.P.','Journal of Physics and Chemistry of Solids',1989,'50',2,223,224,NULL,NULL),(7,'Single-crystal elastic-constants of gamma-cerium','Greiner J.D.; McMasters O.D.; Smith J.F.','Scripta Metallurgica',1980,'14',9,989,991,NULL,NULL),(8,'New nonlinear optical materials','Kurtz S.K.','IEEE Journal of Quantum Electronics',1968,'4',10,578,584,NULL,NULL),(9,'Anomalies in the Elastic Constants and Thermal Expansion of Chromium Single Crystals','Bolef D.I.; de Klerk J.','Physical Review',1963,'129',3,1063,1067,NULL,NULL),(10,'Thermal expansion and temperature dependence of Youngs modulus of single crystal of hexagonal cobalt','Masumoto H.; Saito H.; Kikuchi M.','Science Reports of the Research Institutes Tohoku University Series A-Physics Chemistry and Metallurgy',1967,'19',3,172,NULL,NULL,NULL),(11,'Elastic behaviour of Ni-Co alloys','Leamy H.J.; Warlimon H.','Physica Status Solidi',1970,'37',2,523,NULL,NULL,NULL),(12,'Contactless mode-selective resonance ultrasound spectroscopy: Electromagnetic acoustic resonance','Ogi H.; Ledbetter H.; Kim S.; Hirao M.','Journal of the Acoustical Society of America',1999,'106',2,660,665,NULL,NULL),(13,'Elastic constants of chemical-vapor-deposition diamond thin films: resonance ultrasound spectroscopy with laser-Doppler interferometry','Nakamura N.; Ogi H.; Hirao M.','Acta Materialia',2004,'52',3,765,771,NULL,NULL),(14,'Elastic constants of compression-annealed pyrolitic graphite','Blakslee O.L.','Journal of Applied Physics',1970,'41',8,3373,3382,NULL,NULL),(15,'Invar anomalies of Fe-Pd alloys','Matsui M.; Shimizu T.; Adachi K.','Physica B & C',1983,'119',1,84,89,NULL,NULL),(16,'Growth and electric-elastic properties of KTiAsO4 single crystal','Gao Z.L.; Sun Y.X.; Yin X.; Wang S.P.; Jiang M.H.; Tao X.T.','Journal of Applied Physics',2010,'108',2,NULL,NULL,'024103',4),(17,'Elastic, anelastic, and piezoelectric coefficients of langasite: Resonance ultrasound spectroscopy with laser-doppler interferometry','Ogi H.; Nakamura N.; Sato K.; Hirao M.; Uda S.','IEEE Transactions on Ultrasonics Ferroelectrics and Frequency Control',2003,'50',5,553,560,NULL,NULL),(18,'Acoustic spectroscopy of lithium niobate: Elastic and piezoelectric coefficients','Ogi H.; Kawasaki Y.; Hirao M.; Ledbetter H.','Journal of Applied Physics',2002,'92',5,2451,2456,NULL,NULL),(19,'Complete sets of elastic constants and photoelastic coefficients of pure and MgO-doped lithium niobate crystals at room temperature','Andrushchak A.S.; Mytsyk B.G.; Laba H.P.; Yurkevych O.V.; Solskii I.M.; Kityk A.V.; Sahraoui B.','Journal of Applied Physics',2009,'106',7,NULL,NULL,'073510',6),(20,'Piezo-optic coefficients of MgO-doped LiNbO3 crystals','Mytsyk Bogdan G.; Andrushchak Anatoliy S.; Demyanyshyn Nataliya M.; Kost Yaroslav P.; Kityk Andriy V.; Mandracci Pietro; Schranz Wilfried','Applied Optics',2009,'48',10,1904,1911,NULL,NULL),(21,'Elastic constants, internal friction, and piezoelectric coefficient of alpha-TeO2','Ogi H.; Fukunaga M.; Hirao M.; Ledbetter H.','Physical Review B',2004,'69',2,NULL,NULL,'024104',NULL),(22,'Erratum: A complete set of material properties of single domain 0.26Pb(In1/2Nb1/2)O3-0.46Pb(Mg1/3Nb2/3)O3-0.28PbTiO3 single crystals [Appl. Phys. Lett. 96, 012907 (2010)]','Liu Xiaozhou; Zhang Shujun; Luo Jun; Shrout Thomas R.; Cao Wenwu','Applied Physics Letters',2010,'97',1,NULL,NULL,'019901',2),(23,'Shear-mode piezoelectric properties of ternary Pb(In1/2Nb1/2)O3-Pb(Mg1/3Nb2/3)O3-PbTiO3 single crystals','Wang Wei; Liu Daan; Zhang Qinhui; Ren Bo; Zhang Yaoyao; Jiao Jie; Lin Di; Zhao Xiangyong; Luo Haosu','Journal of Applied Physics',2010,'107',8,NULL,NULL,'084101',4),(24,'Complete sets of elastic, dielectric, and piezoelectric properties of flux-grown [011]-poled Pb(Mg1/3Nb2/3)O3-(28-32)% PbTiO3 single crystals','Shanthi M.; Lim L.C.; Rajan K.K.; Jin J.','Applied Physics Letters',2008,'92',14,NULL,NULL,'142906',3),(25,'Complete set of elastic, dielectric, and piezoelectric constants of orthorhombic 0.71Pb(Mg1/3Nb2/3)O3-0.29PbTiO3 single crystal','Wang Feifei; Luo Laihui; Zhou Dan; Zhao Xiangyong; Luo Haosu','Applied Physics Letters',2007,'90',21,NULL,NULL,'212903',3),(26,'Elastic, piezoelectric, and dielectric properties of multidomain 0.67Pb(Mg1/3Nb2/3)O3-0.33PbTiO3 single crystals','Zhang R.; Jiang B.; Cao W.','Journal of Applied Physics',2001,'90',7,3471,3475,NULL,NULL),(27,'Single-domain properties of 0.67Pb(Mg1/3Nb2/3)O3-0.33PbTiO3 single crystals under electric field bias','Zhang Rui; Jiang Bei; Cao Wenwu','Applied Physics Letters',2003,'82',5,787,789,NULL,NULL),(28,'Complete set of material constants of 0.93Pb(Zn1/3Nb2/3)O3-0.07PbTiO3 domain engineered single crystal','Zhang Rui; Jiang Bei; Cao Wenwu; Amin Ahmed','Journal of Materials Science Letters',2002,'21',NULL,1877,1879,NULL,NULL),(29,'Complete set of elastic, dielectric, and piezoelectric coefficients of 0.93Pb(Zn1/3Nb2/3)O3-0.07PbTiO3 single crystal poled along [011]','Zhang R.; Jiang B.; Jiang W.; Cao W.','Applied Physics Letters',2006,'89',24,NULL,NULL,'242908',3),(30,'Pressure derivatives of elastic-constants of single-crystal MgO and MgAl2O4','Yoneda A.','Journal of Physics of the Earth',1990,'38',1,19,55,NULL,NULL),(31,'Elastic, anelastic, and piezoelectric coefficients of alpha-quartz determined by resonance ultrasound spectroscopy','Ogi H.; Ohmori T.; Nakamura N.; Hirao M.','Journal of Applied Physics',2006,'100',NULL,NULL,NULL,'053511',7),(32,'Elastic Moduli of Silicon vs Hydrostatic Pressure at 25.0 C and - 195.8 C','McSkimin H.J.; Andreatch Jr. P.','Journal of Applied Physics',1964,'35',7,2161,2165,NULL,NULL),(33,'Titanium high-temperature elastic constants through the hcp-bcc phase transformation','Ogi H.; Kai S.; Ledbetter H.; Tarumi M.; Hirao M.; Takashima K.','Acta Materialia',2004,'52',7,2075,2080,NULL,NULL),(34,'Elastic constants of body-centered-cubic titanium monocrystals','Ledbetter H.; Ogi H.; Kai S.; Kim S.; Hirao M.','Journal of Applied Physics',2004,'95',9,4642,4644,NULL,NULL),(35,'Synthesis, growth, and characterization of Nd-doped SrGdGa3O7 crystal','Zhang, Y.Y.; Zhang, H.J.; Yu, H.H.; Wang, J.Y.; Gao, W.L.; Xu, M.; Sun, S.Q.; Jiang, M.H.; Boughton, R.I.','Journal of Applied Physics',2010,'108',6,NULL,NULL,'063534',10),(36,'Three-dimensional superconductivity in nominal composition Fe1.03Se with Tc zero up to 10.9 K induced by internal strain','Ge, Junyi; Cao, Shixun; Yuan, Shujuan; Kang, Baojuan; Zhang, Jincang','Journal of Applied Physics',2010,'108',5,NULL,NULL,'053903',5),(37,'Brillouin Spectroscopy, Calculated Elastic and Bond Properties of GaAsO4','Bhalerao, Gopalkrishna M.; Cambon, Olivier; Haines, Julien; Levelut, Claire; Mermet, Alain; Sirotkin, Sergey; MÃ©naert, Bertrand; Debray, JÃ©rÃ³me; Baraille, Isabelle; Darrigan, Clovis; RÃ©rat, Michel','Inorganic Chemisty',2010,'49',0,9470,9478,NULL,NULL),(38,'KDP:Mn piezoelectric coefficients obtained by x-ray diffraction','Gomes, E.J.L.; Moreira, S.G.C.; de Menezes, A.S.; dos Santos, A.O.; Pereira, D.P.; de Oliveira, P.C.; RemÃ©dios, C.M.R.','Journal of Synchrotron Radiation',2010,'17',6,810,812,NULL,NULL),(39,'A comparative evaluation of elasticity in pentaerythritol tetranitrate using Brillouin scattering and resonant ultrasound spectroscopy','Stevens, Lewis L.; Hooks, Daniel E.; Migliori, Albert','Journal of Applied Physics',2010,'108',5,NULL,NULL,'053512',4),(40,'Electrostriction effect in glass','Sun, Y.; Cao, W.W.; Cross, L.E.','Materials Letters',1986,'4',8,329,336,NULL,NULL),(41,'Complete determination of electrostriction tensor components of KMnF3 single crystals at room temperature','Sun, Y.; Cao, W.W.; Pan, W.Y.; Chang, Z.P.; Cross, L.E.','Journal of Materials Science Letters',1988,'7',NULL,327,330,NULL,NULL),(42,'The variation of the principal elastic moduli of Cu3Au with temperature','Siegel, Sidney','Physical Review',1940,'57',NULL,537,545,NULL,NULL),(43,'Mechanische eigenschaften von messingkristallen','Masima, M.; Sachs, G.','Zeitschrift fu:r Physik',1928,'50',3,161,186,NULL,NULL),(44,'Elasticity of Pintsch crystals of tungsten','Wright, S.J.','Proceedings of the Royal Society of London A',1930,'126',803,613,629,NULL,NULL),(45,'Some properties of single metal crystals','Bridgman, P.W.','Proceedings of the National Academy of Science of the United States of America',1924,'10',NULL,411,415,NULL,NULL),(46,'The variation of the elastic constants of crystalline sodium with temperature between 80 K and 210 K','Quimby, S.L.; Sigiel, Sidney','Physical Review',1938,'54',NULL,293,299,NULL,NULL),(47,'Elastic constants of gold-silver single crystals','RÃ¶lh, H.','Annalen der Physik',1933,'16',NULL,887,NULL,NULL,NULL),(48,'Theory of the plastic properties of solids','Seitz, F.; Read, T.A.','Journal of Applied Physics',1941,'12',2,100,118,NULL,NULL),(49,'Elasticity and creep of Pb single crystals','Swift, Irvin H.; Tyndall, E.P.T.','Physical Review',1942,'61',5,359,364,NULL,NULL),(50,'Elastic constants of single crystals of copper, gold, and lead','Goens, E.; Weerts, J.','Physikalische Zeitschrift',1936,'37',NULL,321,NULL,NULL,NULL),(51,'Elastic moduli of ferromagnetic materials, I: iron crystals','Kimura, R.','Proceedings of the Physical and Mathematical Society of Japan',1939,'21',NULL,686,NULL,NULL,NULL),(52,'Elastic constants of single crystals of iron','Kimura, R.; Ohno, K.','Tohoku University Science Reports',1934,'23',NULL,359,NULL,NULL,NULL),(53,'Elastic constants of single crystals of copper','Kimura, R.','Tokohu University Science Report',1933,'22',NULL,553,NULL,NULL,NULL),(54,'Elastic constants of aluminum single crystals','Goens, E.','Annalen der Physik',1933,'17',NULL,233,NULL,NULL,NULL),(55,'Electromechanical coupling coefficient for surface acoustic waves in single-crystal bulk aluminum nitride','Bu, G.; Ciplys, D.; Shur, M.; Schowalter, L.J.; Schulman, S.; Gaska, R.','Applied Physics Letters',2004,'84',23,4611,4613,NULL,NULL),(56,'Elastic, dielectric, and piezoelectric constants of Pb(In1/2Nb1/2)O3-Pb(Mg1/3Nb2/3)O3-PbTiO3 single crystal poled along [011]c','Sun, Enwei; Zhang, Shujun; Luo, Jun; Shrout, Thomas R.; Cao Wenwu','Applied Physics Letters',2010,'97',3,NULL,NULL,'032902',3),(57,'Single-crystal growth and superconducting properties of LiFeAs','Lee, Bumsung; Khim, Seunghyun; Kim, Jung Soo; Stewart, G.R.; Kim, Kee Hoon','European Physics Journal',2010,'91',NULL,NULL,NULL,'67002',6),(58,'High temperature single crystal properties of mullite','Kriven, W.M.; Palko, J.W.; Sinogeikin, S.; Bass, J.D.; Sayir, A.; Brunauer, G.; Boysen, H.; Frey, F.; Schneider, J.','Journal of the European Ceramic Society',1999,'19',NULL,2529,2541,NULL,NULL),(59,'Structural control of elastic constants of mullite in comparison to sillimanite','Hildmann Bernd; Ledbetter Hassel; Kim Sudook; Schneider Hartmut','Journal of the American Ceramic Society',2001,'84',10,2409,2414,NULL,NULL),(60,'Elastic constants of diamond','Bhagavantam, S.; Bhimasenachar, J.','Nature',1944,'154',3913,546,546,NULL,NULL),(61,'Anisotropic superconducting properties of optimally doped BaFe2(As0.65P0.35)2 under pressure','Goh, Swee K.; Nakai, Y.; Ishida, K.; Klintberg, L.E.; Ihara, Y.; Kasahara, S.; Shibauchi, T.; Matsuda, Y.; Terashima, T.','Physical Review B',2010,'82',9,NULL,NULL,'094502',5),(62,'Rigidity modulus of Beta-Brass single crystals','Good, Walter A.','Physical Review',1941,'60',0,605,609,NULL,NULL),(63,'Behaviour of Young\'s modulus of beta-brass single crystals at low temperature','Rinehart, John S.','Physical Review',1941,'59',0,308,309,NULL,NULL),(64,'Superconductivity in the iron selenide KxFe2Se2 (0<=x<=1.0)','Guo, Jiangang; Jin, Shifeng; Wang, Gang; Wang, Shunchong; Zhu, Kaixing; Zhou, Tingting; He, Meng; Chen, Xiaolong','Physical Review B',2010,'82',18,NULL,NULL,'180520(R)',4),(65,'A new homologous series of iron pnictide oxide superconductors (Fe2As2)(Can+2(Al, Ti)nOy) (n = 2, 3, 4)','Ogino, Hiraku; Machida, Kenji; Yamamoto, Akiyasu; Kishio, Kohji; Shimoyama, Jun-ichi; Tohei, Tetsuya; Ikuhara, Yuichi','Superconductor Science and Technology',2010,'23',11,NULL,NULL,'115005',5),(66,'Anisotropy of the superconducting state parameters and intrinsic pinning in low-level Pr-doped YBa2Cu3O7-d single crystals','Kortyka, A.; Puzniak, R.; Wisniewski, A.; Zehetmayer, M.; Weber, H.W.; Cai, Y.Q.; Yao, X.','Superconductor Science and Technology',2010,'23',10,NULL,NULL,'065001',7),(67,'Isotropic superconductivity in LaRu2P2 with the ThCr2Si2-type structure','Ying, J.J.; Yan, Y.J.; Liu, R.H.; Wang, X.F.; Wang, A.F.; Zhang, M.; Xiang, Z.J.; Chen, X.H.','Superconductor Science and Technology',2010,'23',10,NULL,NULL,'115009',4),(68,'Dielectric constant of Cr2O3','Fang, P.H.; Brower, W.S.','Physical Review',1963,'129',4,1561,1561,NULL,NULL),(69,'Superconductivity at 32K and anisotropy in Tl0.58Rb0.42Fe1.72Se2 crystals','Wang, Hang-Dong; Dong, Chi-Heng; Li, Zu-Juan; Mao, Qian-Hui; Zhu, Sha-Sha; Feng, Chun-Mu; Yuan, H.Q.; Fang, Ming-Hu','European Physics Letters',2011,'93',0,NULL,NULL,'47004',4),(70,'Observation of the magnetoelectric effect in Cr2O3','Shtrikman, S.; Treves, D.','Physical Review',1963,'130',3,986,988,NULL,NULL),(71,'Low temperature transport properties and heat capacity of single-crystal Na8Si46','Stefanoski, S.; Martin, J.; Nolas, G.S.','Journal of Physics: Condensed Matter',2010,'22',0,NULL,NULL,'485404',5),(72,'Preparation and superconductivity of new stage and polytypic phases in potassium-intercalated zirconium nitride chloride (KxZrNCl)','Zheng, Zhangfeng; Yamanaka, Shoji','Chemistry of Materials',2011,'23',0,1558,1563,NULL,NULL),(73,'Precise lattice constants and thermal expansion of K2Pt(CN)4Br0.3.3H2O','Freund, A.; Roth, S.; Ranvaud, R.','Journal of Applied Crystallography',1974,'7',NULL,631,632,NULL,NULL),(74,'Complete set of properties of 0.92Pb(Zn1/3Nb2/3)O3-0.08PbTiO3 single crystal with engineered domains','Zhang, Rui; Jiang, Bei; Jiang, Wenhua; Cao, Wenwu','Materials Letters',2003,'57',NULL,1305,1308,NULL,NULL),(75,'Coexistence of magnetism and superconductivity in the iron-based compound Cs0.8(FeSe0.98)2','Shermadini, Z.; Krzton-Maziopa, A.; Bendele, M.; Khasanov, R.; Luetkens, H.; Conder, K.; Pomjakushina, E.; Weyeneth, S.; Pomjakushin, V.; Bossen, O.; Amato, A.','Physical Review Letters',2011,'106',11,NULL,NULL,'117602',4),(76,'Das flie?en von metallkristallen bei torsion','Karnop, R.; Sachs, G.','Zeitschrift fu:r Physik',1929,'53',9,605,618,NULL,NULL),(77,'Elastic constants of piezo-electric crystals','Bhagavantam, S.; Suryanarayana, D.','Proceedings of the Indian Academy of Science',1944,'20',0,304,309,NULL,NULL),(78,'Lehrburch der Kristallphysik','Voigt, W.','Leipzig: Teubner B.G.',1928,'?',0,NULL,NULL,NULL,NULL),(79,'Ultrasonics','Bergmann, L.','J. Wiley & Sons, London',1938,'?',0,NULL,NULL,NULL,NULL),(80,'The temperature variation of the elastic moduli of NaCl, KCl and MgO','Durand, Milo A.','Physical Review',1936,'50',5,449,455,NULL,NULL),(81,'The elastic constants of crystallized potassium alum','Voigt, W.','Nachrichten Gesellschaft der Wissenschaften Go:ttingen',1918,'?',0,85,NULL,NULL,NULL),(82,'The elastic constants of zinc blende','Voigt, W.','Nachrichten Gesellschaft der Wissenschaften Go:ttingen',1918,'?',0,424,NULL,NULL,NULL),(83,'The elastic moduli of five alkali halides','Bridgman, P.W.','Proceedings of the American Academy of Arts and Sciences',1929,'64',2,19,38,NULL,NULL),(84,'Elastic constants of aluminum nitride','Kazan, M.; Moussaed, E.; Nader, R.; Masri, P.','Physica Status Solidi C',2007,'4',1,204,207,NULL,NULL),(85,'Phonon dynamics in AlN lattice contaminated by oxygen','Kazan, M.; Ruffle, B.; Zgheib, Ch.; Masri, P.','Diamond & Related Materials',2006,'15',0,1525,1534,NULL,NULL),(86,'Vibrational spectroscopy of aluminum nitride','McNeil, L.E.; Grimsditch, M.; French, R.H.','Journal of the American Ceramics Society',1993,'76',0,1132,1136,NULL,NULL),(87,'High-frequency and low-dispersion SAW devices on AlN-Al2O3 and AlN-Si for signal-processing','Tsubouchi, K.; Sugai, K.; Mikoshiba, N.','IEEE Transactions on Sonics and Ultrasonics',1981,'28',5,389,389,NULL,NULL),(88,'Elasticity of single-crystalline graphite: inelastic X-ray scattering study','Bosak, A.; Krisch, M.; Mohr, M.; Maultzsch, J.; Thomsen, C.','Physical Review B',2007,'75',15,NULL,NULL,'153408',NULL),(89,'Elasticity of cubic boron nitride under ambient conditions','Zhang, Jin S.; Bass, Jay D.; Tanigushi, Takashi; Goncharov, Alexander F.; Chang, Yun-Yuan; Jacobsen, Steven D.','Journal of Applied Physics',2011,'109',6,NULL,NULL,'063521',5),(90,'Elastic-constants of boron-nitride','Grimsditch, M.; Zouboulis, E.S.; Polian, A.','Journal of Applied Physics',1994,'76',2,832,834,NULL,NULL),(91,'Cubic boron nitride as a primary calibrant for a high temperature pressure scale','Goncharov, Alexander F.; Sinogeikin, Stanislav; Crowhurst, Jonathan C.; Ahart, Muhtar; Lakshtanov, Dmitry; Prakapenka, Vitali; Bass, Jay; Beck, Pierre; Tkachev, Sergei N.; Zaug, Joseph M.; Fei, Yingwei','High Pressure Research',2007,'27',4,409,417,NULL,NULL),(92,'Elastic constants of crystals: a new method and its application to pyrites and galena','Bhagavantam, S.; Bhimasenachar, J.','Proceedings of the Indian Academy of Sciences',1944,'20',0,298,NULL,NULL,NULL),(93,'Variation with temperature of the principal elastic moduli of NaCl near the melting point','Hunter, L.; Siegel, S.','Physical Review',1942,'61',0,84,NULL,NULL,NULL),(94,'Elastic constants, resistivity and thermal expansion of single magnesium crystals','Goens, E.; Schmid, E.','Physiks Zeitschrift',1936,'37',0,387,NULL,NULL,NULL),(95,'Researches on metal crystals-I. Elastic constants of zinc and cadmium','Gruneisen, E.; Goens, E.','Zeitschrift fu:r Physik',1924,'26',0,235,NULL,NULL,NULL),(96,'Improved apparatus for the measurement of torsional modulus of crystal rods, and application to single crystals of zinc','Goens, E.','Analen der Physik',1933,'16',0,793,NULL,NULL,NULL),(97,'Elastic behaviour and elastic constants of zinc single crystals','Hanson, A.W.','Physical Review',1934,'45',0,324,NULL,NULL,NULL),(98,'Quartz crystal applications','Mason, W.P.','Bell Systems Technology Journal',1943,'22',0,178,NULL,NULL,NULL),(99,'A dynamic measurement of the elastic, electric and piezoelectric constants of Rochelle salt','Mason, W.P.','Physical Review',1939,'55',0,775,789,NULL,NULL),(100,'Determination of the elastic moduli of the piezo-electric crystal Rochelle salt by a statical method','Mandell, W.','Proceedings of the Royal Society A',1927,'116',775,623,636,NULL,NULL),(101,'Change in elastic properties on replacing the potassium atom of Rochelle salt by the ammonium atom','Mandell, W.','Proceedings of the Royal Society A',1928,'121',787,122,130,NULL,NULL),(102,'Elastic deformation in Rochelle salt','Hinz, H.','Zeitschrift fu:r Physik',1939,'111',0,617,NULL,NULL,NULL),(103,'Elastic constants of single crystal UO2 at 25 C','Wachtmann Jr., J.B.; Wheat, M.L.; Anderson, H.J.; Bates, J.L.','Journal of Nuclear Materials',1965,'16',1,39,41,NULL,NULL),(104,'Photo-elastic behaviour of barium nitrate and lead nitrate crystals','Bhagavantam, S.; Krishna Rao, K.V.','Acta Crystallographica',1953,'6',0,799,801,NULL,NULL),(105,'Elastic Properties of Polycrystalline Aluminum Oxynitride Spinel and Their Dependence on Pressure, Temperature, and Composition','Graham, Earl K.; Munly, W.C.; McCauley, James W.; Corbin, Norman D.','Journal of the American Ceramic Society',1988,'71',10,807,812,NULL,NULL),(106,'ALON: a brief history of its emergence and evolution','McCauley, James W.; Patel, Parimal; Chen, Mingwei; Gilde, Gary; Strassburger, Elmar; Paliwal, Bhasker; Ramesh, K.T.; Dandekar, Dattatraya P.','Journal of the European Ceramic Society',2009,'29',2,223,236,NULL,NULL),(107,'Elastic properties of mullite single crystals up to 1400 C','Schreuer, Ju:rgen; Hildmann, Bernd; Schneider, Hartmut','Journal of the American Ceramic Society',2006,'89',5,1624,1631,NULL,NULL),(108,'Complete Elastic tensor for mullite (~2.5Al2O3 SiO2) to high temperatures measured from textured fibers','Palko, J.W.; Sayir, A.; Sinogeikin, S.V.; Kriven, W.M.; Bass, J.D.','Journal of the American Ceramic Society',2002,'85',8,2005,2012,NULL,NULL),(109,'The relationship of elasticity and crystal structure in andalusite and sillimanite','Vaughan, M.T.; Weidner, D.J.','Physics and Chemistry of Minerals',1978,'3',0,133,144,NULL,NULL),(110,'Thermal expansion of mullite','Schneider, H.; Eberhard, E.','Journal of the American Ceramic Society',1990,'73',0,2073,2076,NULL,NULL),(111,'High temperature Thermal expansion of mullite: an in situ neutron diffraction study up to 1600 C','Brunauer, G.; Frey, F.; Boysen, H.; Schneider, H.','Journal of the European Ceramic Society',2001,'21',0,2563,2567,NULL,NULL),(112,'Theral expansion and high-temperature crystal chemistry of the Al2SiO5 polymorphs','Winter, J.K.; Ghose, S.','American Mineralogist',1979,'64',0,573,586,NULL,NULL),(113,'Synthesis and crystal growth of Cs0.8(FeSe0.98)2: a new iron-based superconductor with Tc=27K','Krzton-Maziopa, A.; Shermadini, Z.; Pomjakushina, E.; Pomjakushina, V.; Bendele, M.; Amato, A.; Khasanov, R.; Luetkens, H.; Conder, K.','Journal of Physics: Condensed Matter',2011,'23',0,NULL,NULL,'052203',4),(114,'Phase transition and superconductivity of SrFe2As2 under high pressure','Uhoya, Walter O; Montgomery, Jeffrey M.; Tsoi, Georgiy M.; Vohra, Yogesh K.; McGuire, M.A.; Sefat, Athena S.; Sales, Brian C.; Weir, Samuel T.','Journal of Physics: Condensed Matter',2011,'23',0,NULL,NULL,'122201',6),(115,'Fe-based superconductivity with Tc=31K bordering an antiferromagnetic insulator in (Tl,K)FexSe2','Fang, Ming-Hu; Wang, Hang-Dong; Dong, Chi-Heng; Li, Zu-Juan; Feng, Chun-Mu; Chen, Jian; Yuan, H.Q.','European Physics Letters',2011,'94',0,NULL,NULL,'27009',6),(116,'Single crystal elastic constants and calculated aggregate properties','Simmons, G.; Wang, H.','Cambridge, MA: M.I.T. Press',1971,'?',0,NULL,NULL,'?',NULL),(117,'Elastic constants of some cubic nitrates','Bhimasenachar, J.; Seshagiri Rao, T.','Proceedings of the National Institute of Science of India',1950,'16',4,235,240,NULL,NULL),(118,'Elastic constants of corundum','Bhimasenachar, J.','Proceedings of the National Institute of Science of India',1950,'16',4,241,243,NULL,NULL),(119,'Elastic properties of single crystals and polycrystalline aggregates','Bhagavantam, S.','Proceedings of the Indian Academy of Sciences A',1955,'41',0,72,90,NULL,NULL),(120,'Elastic constants of crystals. A new method and its application to pyrites and galena','Bhagavantam, S.; Bhimasenachar, J.','Proceedings of the Indian Academy of Sciences A',1944,'20',5,298,303,NULL,NULL),(121,'Elastic constants of single crystals of barium nitrate','Bhagavantam, S.; Sundara Rao, R.V.G.','Current Science',1948,'17',0,296,296,NULL,NULL),(122,'Coexistence of superconductivity and antiferromagnetism in single crystals A0.8Fe2-ySe2 (A = K, Rb, Cs, Tl/K and Tl/Rb): evidence from magnetization and resistivity','Liu, R.H.; Luo, X.G.; Zhang, M.; Wang, A.F.; Ying, J.J.; Wang, X.F.; Yan, Y.J.; Xiang, Z.J.; Cheng, P.; Ye, G.J.; Li, Z.Y.; Chen, X.H.','European Physics Letters',2011,'94',0,NULL,NULL,'27008',5),(123,'Elastic constants of magnetite, pyrite and chromite','Doraiswami, M.S.',' Proceedings of the Indian Academy of Sciences, Section A',1947,'25',0,413,416,NULL,NULL),(124,'Thermal expansion of potassium nitrate','Lonappan, M.A.','Proceedings of the Indian Academy of Sciences, Section A',1955,'41',0,239,244,NULL,NULL),(125,'Susceptibility measurements support high-Tc superconductivity in the Ba-La-Cu-O system','Bednorz, J.G.; Takashige, M.; Muller, K.A.','Europhysics Letters',1987,'3',3,379,385,NULL,NULL),(126,'Sructure of the 100K superconductor Ba2YCu3O7 between (5-300) K by neutron powder diffraction','Capponi, J.J.; Chaillout, C.; Hewat, A.W.; Lejay, P.; Marezio, M.; Nguyen, N.; Raveau, B.; Soubeyroux, J.L.; Tholence, J.L.; Tournier, R.','Europhysics Letters',1987,'3',12,1301,1307,NULL,NULL),(127,'Superconductivity and magnetic properties of single crystals of K0.75Fe1.66Se2 and Cs0.81Fe1.61Se2','Ying, J.J.; Wang, X.F.; Luo, X.G.; Wang, A.F.; Zhang, M.; Yan, Y.J.; Xiang, Z.J.; Liu, R.H.; Cheng, P.; Ye, G.J.; Chen, X.H.','Physical Review B',2011,'83',21,NULL,NULL,'212502',4),(128,'The elastic and piezoelectric properties of tungsten bronze ferroelectric crystals .(Sr0.7Ba0.3)2NaNb5O15 and (Sr0.3Ba0.7)2NaNb5O15','Jiang, Wenhua; Cao, Wenwu','Journal of Applied Physics',2005,'97',9,NULL,NULL,'094106',4),(129,'Complete set of material constants of Pb(In1/2Nb1/2)O3Pb(Mg1/3Nb2/3)O3PbTiO3 single crystal with morphotropic phase boundary composition','Liu, Xiaozhou; Zhang, Shujun; Luo, Jun; Shrout, Thomas R.; Cao, Wenwu','Journal of Applied Physics',2009,'106',7,NULL,NULL,'074112',4),(130,'Elastic, piezoelectric, and dielectric properties of 0.58Pb(Mg1/3Nb2/3)O3-0.42PbTiO3 single crystal','Cao, Hu; Schmidt, Hugo; Zhang, Rui; Cao, Wenwu; Luo, Haosu','Journal of Applied Physics',2004,'96',1,549,554,NULL,NULL),(131,'Photoelastic constants of diamond','Ramachandran, G.N.','Proceedings of the Indian Academy of Sciences A',1947,'25',0,208,219,NULL,NULL),(132,'Flux growth and characterization of lead-free piezoelectric single crystal [Bi0.5(Na1-xKx)0.5]TiO3','Yi, Xiujie; Chen, Huanchu; Cao, Wenwu; Zhao, Minglei; Yang, Dongmei; Ma, Guangpen; Yang, Changhong; Han, Jianru','Journal of Crystal Growth',2005,'281',0,364,369,NULL,NULL),(133,'Anisotropy in domain engineered 0.92Pb(Zn1/3Nb2/3)O3-0.08PbTiO3 single crystal and analysis of its property fluctuations','Zhang, Rui; Jiang, Bei; Jiang, Wenhua; Cao, Wenwu','IEEE Transactions on Ultrasonics, Ferroelectrics, and Frequency Control',2002,'49',12,1622,1627,NULL,NULL),(134,'An x-ray powder study of beta-uranium','Thewlis, J.','Acta Crystallographica',1952,'5',0,790,794,NULL,NULL),(135,'Pressure dependence of the elastic constants of single crystalline aluminum oxide','Gieske, J.H.; Barsch, G.R.','Physica Status Solidi',1968,'29',0,121,131,NULL,NULL),(136,'Reconciliation of ab initio theory and experimental elastic properties of Al2O3','Gladden, J.R.; So, Jin H.; Maynard, J.D.; Saxe, P.W.; Le Page, Y.','Applied Physics Letters',2004,'85',3,392,394,NULL,NULL),(137,'Elastic constants of corundum up to 1825 K','Goto, Takayasu; Anderson, Orson L.; Ohno, Ishiro; Yamamoto, Shigeru','Journal of Geophysical Research',1989,'94',86,7588,7602,NULL,NULL),(138,'Elastic constants of synthetic sapphire at 27 C','Bernstein, B.T.','Journal of Applied Physics',1963,'34',1,169,172,NULL,NULL),(139,'Corrected values of elastic constants of sapphire','Mayer, Walter G.; Hiedemann, E.A.','Acta Crystallographica',1961,'14',3,323,323,NULL,NULL),(140,'Elastic constants of synthetic single crystal corundum at room temperature','Wachtman Jr., J.B.; Tefft, W.E.; Lam Jr., D.G.; Stinchfield, R.P.','Journal of Research of the National Bureau of Standards A',1960,'64',3,213,228,NULL,NULL),(141,'Verification of the elastic constants for a-Al2O3 using high-resolution neutron diffraction','Kisi, Erich H.; Howard, Christopher J.; Zhang, Jianfeng','Journal of Applied Crystallography',2011,'44',1,216,218,NULL,NULL),(142,'Elastic constants of synthetic single crystal corundum','Tefft, Wayne E.','Journal of Research of the National Bureau of Standards A',1966,'70',4,277,280,NULL,NULL),(143,'Elastic properties of tetragonal PbTiO3 single crystals by Brillouin scattering','Kalinichev, A.G.; Bass, J.D.; Sun, B.N.; Payne, D.A.','Journal of Materials Research',1997,'12',10,2623,2627,NULL,NULL),(144,'Elastic constants of alumina','Sundara Rao, R.V.G.','Proceedings of the Indian Academy of Sciences A',1949,'26',0,352,360,NULL,NULL),(145,'Investigation of the dielectric, elastic, and piezoelectric properties of Cs2TeMo3O12 crystals','Zhang, Junjie; Gao, Zeliang; Yin, Xin; Zhang, Zhonghan; Sun, Youxuan; Tao, Xutang','Applied Physics Letters',2012,'101',6,NULL,NULL,'062901',4),(146,'Elastic constants of artificial and natural ice samples by Brillouin spectroscopy','Gammon, P.H.; Kiefte, H.; Clouter, M.J.; Denner, W.W.','Journal of Glaciology',1983,'29',103,433,460,NULL,NULL),(147,'Brillouin scattering in diamond','Grimsditch, M.H.; Ramdas, A.K.','Physical Review B',1975,'11',8,3139,3148,NULL,NULL),(148,'Elastic moduli of diamond as a function of pressure and temperature','McSkimin, H.J.; Andreatch Jr., P.','Journal of Applied Physics',1972,'43',7,2944,2948,NULL,NULL),(149,'Intercalation and lattice expansion in titanium disulfide','Whittingham, M. Stanley; Thompson, Arthur H.','The Journal of Chemical Physics',1975,'62',4,1588,1588,NULL,NULL),(150,'Elastic and piezoelectric coefficients of single-crystal barium titanate','Berlincourt, Don; Jaffe,Hans','Physical Review',1958,'111',1,143,148,NULL,NULL),(151,'Dielectric, elastic, piezoelectric, electro-optic, and elasto-optic tensors of BaTiO3 crystals','Zgonik, M.; Bernasconi, P.; Duelli, M.; Schlesser, R.; Gunter, P.; Garrett, M.H.; Rytz, D.; Zhu, Y.; Wu, X.','Physical Review B',1994,'50',9,5941,5949,NULL,NULL),(152,'Piezoelectric, dielectric, and pyroelectric constants of LiH3(SeO3)2','Berlincourt, Don; Cook Jr., W.R.; Rander, Mary Helen','Acta Crystllographica',1963,'16',0,163,165,NULL,NULL),(153,'Crystal growth and piezoelectric, elastic and dielectric properties of novel LiInS2 crystal','Wang, Shanpeng; Gao, Zeliang; Yin, Xin; Liu, Guandong; Ruan, Huapeng; Zhang, Guodong; Shi, Qiong; Dong, Chunming; Tao, Xutang','Journal of Crystal Growth',2013,'362',0,308,311,NULL,NULL),(154,'Elastic relaxations associated with the Pm-3m-R-3c transition in LaAlO3: I. Single crystal elastic moduli at room temperature','Carpenter, M.A.; Sinogeikin, S.V.; Bass, J.D.; Lakshtanov, D.L.; Jacobsen, D.L.','Journal of Physics: Condensed Matter',2010,'22',0,NULL,NULL,'035403',11),(155,'Elastic constants of single crystalline b-Ti70Nb30','Hermann, R.; Hermann, H.; Calin M.; Buchner, B.; Eckert, J.','Scripta Materialia',2012,'66',0,198,201,NULL,NULL),(156,'Experimental determination of third-order elastic constants of diamond','Lang Jr., J.M.; Gupta, Y.M.','Physical Review Letters',2011,'106',12,NULL,NULL,'125502',4),(157,'Growth, morphology and anisotropic thermal properties of Nd-doped Nd-doped Sr3Y2(BO3)4 crystal','Pan, Zhongben; Cong, Hengjiang; Yu, Haohai; Zhang, Huaijin; Wang, Jiyang; Boughton, Robert I.','Journal of Crystal Growth',2013,'363',0,176,184,NULL,NULL),(158,'Acoustic characteristics of FeSe single crystals','Zvyagina, G.A.; Gaydamak, T.N.; Zhekov, K.R.; Bilich, I.V.; Fil, V.D.; Chareev, D.A.; Vasiliev, A.N.','European Physics Letters',2013,'101',0,NULL,NULL,'56005',5),(159,'Bismuth telluride, antimony telluride, and their solid solutions','Scherrer, H.; Scherrer, S','book',1995,NULL,NULL,211,237,NULL,NULL),(160,'Thermal conductivity of II-VI compounds and phonon scattering by Fe2+ impurities','Slack, Glen A.','Physical Review B',1972,'6',10,3791,3800,NULL,NULL),(161,'Inorganic structure types with revised space groups.I.','Cenzual, K.; Gelato, L.M.; Penzo, M.; Parthe, E.','Acta Crystallographica B',1991,'47',NULL,433,439,NULL,NULL),(162,'Elastic and elasto-optical properties of triglycine-zinc chloride crystal','Tylczynski, Z.; Trzaskowska, A.','Journal of Applied Physics',2013,'114',3,NULL,NULL,'033529',4),(163,'Elastic, dielectric and piezoelectric characterization of single domain PIN-PMN-PT: Mn crystals','Huo, Xiaoqing; Zhang, Shujun; Liu, Gang; Zhang, Rui; Luo, Jun; Sahul, Raffi; Cao Wenwu; Shrout, Thomas R.','Journal of Applied Physics',2012,'112',12,NULL,NULL,'124113',5),(164,'Growth of(CH3)2NH2CuCl3 single crystals using evaporation method with different temperatures and solvents','Chen, L.M.; Tao, W.; Zhao, Z.Y.; Li, Q.J.; Ke, W.P.; Wang, X.M.; Liu, X.G.; Fan, C.; Sun, X.F.','Journal of Crystal Growth',2010,'312',21,3243,3246,NULL,NULL),(165,'Brillouin scattering and elastic moduli of silver thiogallate (AgGaS2)','Grimsditch, M.H.; Holah, G.D.','Physical Review B',1975,'12',10,4377,4382,NULL,NULL),(166,'A Method for Determining the Elastic Constants of a Cubic Crystal from Velocity Measurements in a Single Arbitrary Direction; Application to SrTi03','Wachtman Jr., J.B.; Wheat, M.L.; Marzullo, S.','JOURNAL OF RESEARCH of the National Bureau of Standards-A. Physics and Chemistry',1963,'67',2,193,204,NULL,NULL),(167,'Elastic Properties of Fluorapatite','Yoon, Hyo Sub.; Newnham, R.E.','The American Mineralogist',1969,'54',0,1193,1197,NULL,NULL),(168,'Elastic constants and refractive index of boron phosphide','Wettling, W.; Windscheif, J.','Solid State Communications',1984,'50',1,33,34,NULL,NULL),(169,'Evaluation of anisotropy of critical current density in stoichiometric Bi-2212 single crystals','Nakayama, Y.; Kawai, S.; Kiuchi, M.; Otabe, E.S.; Matsushita, T.; Shimoyama, J.; Kishio, K.','Physica C',2009,'469',0,1221,1223,NULL,NULL),(170,'Discovery of a superhard iron tetraboride superconductor','Gou, Huiyang; Dubrovinskaia, Natalia; Bykova, Elena; Tsirlin, Alexander A.; Kasinathan, Deepa; Schelle, Walter; Richter, Asta; Merlini, Marco; Hanfland, Michael; Abakumov, Artem M.; Batuk, Dmitry; van Tendeloo, Gustaaf; Nakajima, Yoichi; Kolmogorov, Aleks','Physical Review Letters',2013,'111',15,NULL,NULL,'157002',5),(171,'Elasticity of single-crystal aragonite by Brillouin spectroscopy','Liu, Lin-gun; Chen, Chien-chih; Lin, Chung-Cherng; Yang, Yi-jong','Physics and Chemistry of Minerals',2005,'32',NULL,97,102,NULL,NULL),(172,'High-Temperature Heat Capacity of Co304 Spinel: Thermally Induced Spin Unpairing Transition','Mocala, K.; Navrotsky, A.; Sherman, D.M.','Physics and Chemistry of Minerals',1992,'19',NULL,88,95,NULL,NULL),(173,'Measurement of Elastic Properties of Single-Crystal CaO up to 1200 K','Oda, Hitoshi; Anderson, Orson L.; Isaak, Donald G.; Suzuki, Isao','Physics and Chemistry of Minerals',1992,'19',NULL,96,105,NULL,NULL),(174,'High-Temperature Thermal Expansion and Elasticity of Calcium-Rich Garnets','Isaak, Donald G.; Anderson, Orson L.; Oda, Hitoshi','Physics and Chemistry of Minerals',1992,'19',NULL,106,120,NULL,NULL),(175,'Multiband Superconductivity of Heavy Electrons in a TlNi2Se2 Single Crystal','Wang, Hangdong; Dong, Chiheng; Mao, Qianhui; Khan, Rajwali; Zhou, Xi; Li, Chenxia; Chen, Bin; Yang, Jinhu; Su, Qiping; Fang, Minghu','Physical Review Letters',2013,'111',NULL,0,0,NULL,6),(176,'Reduced resistivity-anisotropy ratio in Bi2Sr2CaCu208 single crystals showing zero resistance at 97 K','BadÃ¨che, T.; Monnereau, O.; Ghorayeb, A.M.; Grachev, V.; Boulesteix, C.; ','Physica C',1995,'241',NULL,10,16,NULL,NULL),(177,'A Comparison of the Elastic Constants of Chromium as Determined from Diffuse X-Ray and Ultrasonic Techniques','Sumer, A.; Smith, J.F.','Journal of Applied Physics',1963,'34',9,2691,2694,NULL,NULL),(178,'Thermal expansion of boehmite. An anomaly near 560 K due to non-stoichiometric water','Berar, J.-F.; Grebille, D.; Gregoire, P.; Weigel, D.','Journal of Physics and Chemistry of Solids',1984,'45',2,147,150,'',NULL),(179,'Hydrogen thermal motion in calcium hydroxide: Ca (O H)2','Desgranges, L; Grebille, D; Calvarin, g; Chevrier, G; Floquet, N; Niepce, J-C','Acta Crystallographica B (39,1983-)',1993,'49',NULL,812,817,NULL,NULL),(180,'A Comparison of Measurement Techniques for Determining Phosphorus Densities in Semiconductor Silicon','Thurber, Robert. W.','Journal of Electronic Materials',1980,'9',NULL,551,560,NULL,NULL),(181,'The effect of a charge-density wave transition on the transport properties of 2H-NbSe2','Li, Lin-jun; Xu, Zhu-an; Shen, Jing-qin; Qiu, Li-min; Gan, Zhi-hua','Journal of Physics: Condensed Matter',2005,'17',NULL,493,498,NULL,NULL),(182,'Thermal expansion of synthetic aragonite condensed review of elastic properties','Lucas, Anita; Mouallem-Bahout, Mona; Carel, Claude; Gaude, Jean; Matecki, Marc','Journal of Solid State Chemistry',1999,'146',NULL,73,78,NULL,NULL),(183,'Magnetoelectric effect of Cr2O3 in strong static magnetic fields','Wiegelmann H.; Jansen AGM.; Wyder P.; Rivera JP.; Schmid H.','Ferroelectrics',1994,'162',NULL,141,146,NULL,NULL),(184,'The linear magnetoelectric effect in LiCoPO4 Revisited','Rivera JP.','Ferroelectrics',1994,'161',NULL,147,164,NULL,NULL),(185,'Magnetoelectric properties of A2[FeCl5(H2O)] with A = K, Rb, Cs','Ackermann M.; Lorenz T.; Becker P.; Bohaty L.','J. Phys.: Condens. Matter ',2014,'26',NULL,506002,0,NULL,NULL),(186,'Large-Sized Crystal','Zeliang Gao; Xiangxin Tian','Crystal Growth and Desing',2015,'15',0,759,763,'DOI: 10.1021/c',NULL),(187,'Pressure-induced enhancement of Tc above 150 K in Hg-1223','Nunez-Regueiro, M.; Tholence, J.-L; Antipov, E.V.; Capponi, J.-J.; Marezio, M.','Science',1993,'262',NULL,97,99,'207001',6),(188,'Growth and piezoelectric properties of ferroelectric Bi2WO6 mono-domaiin crystals','Hiroaki Takeda; Joong Sang Han; Masaya Nishida; Tadashi Shiosaki; Takuya Hoshina; Takaaki Tsurumi','ELSEVIER',2010,'?',NULL,NULL,NULL,NULL,4),(189,'A review of magnetostrictive iron-gallium alloys','Jayasimha Atulasimha; Alison B Flatau','Smart Materials and Structures',2011,NULL,NULL,NULL,NULL,NULL,NULL),(190,'Magnetic Properties of Highly Textured Fe85Ga15','Martin Kriegisch: Roland Groessinger: Cristina Grijalva: Atif Muhammad: Friedrich Kneidinger: Nasir Mehboob: Frank Kube: Reiko Sato Turtelli','IEEE Transactions on Magnetics',2014,'50',NULL,NULL,NULL,NULL,NULL),(191,'Numerical study of the effective magnetocrystalline anisotropy','Julian Dean: M. T. Bryan: N. A. Morley: G. Hrkac: A. Javed: M. R. J. Gibbs: D. A. Allwood','Journal of Applied Physics',201,'110',NULL,NULL,NULL,'43902',NULL),(293,'Full piezoelectric tensors of wurtzite and zinc blende ZnO and ZnS by first-principles calculations','M. Cattia; *; Y. Noelb; R. Dovesi','Journal of Physics and Chemistry of Solids',2003,'64',0,2183,2190,'?',0);
/*!40000 ALTER TABLE `data_publarticle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_publarticle_temp`
--

DROP TABLE IF EXISTS `data_publarticle_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_publarticle_temp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `authors` varchar(255) NOT NULL,
  `journal` varchar(127) NOT NULL,
  `year` int(11) DEFAULT NULL,
  `volume` varchar(6) DEFAULT NULL,
  `issue` int(11) DEFAULT NULL,
  `first_page` int(11) DEFAULT NULL,
  `last_page` int(11) DEFAULT NULL,
  `reference` varchar(14) DEFAULT NULL,
  `pages_number` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=190 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_publarticle_temp`
--

LOCK TABLES `data_publarticle_temp` WRITE;
/*!40000 ALTER TABLE `data_publarticle_temp` DISABLE KEYS */;
INSERT INTO `data_publarticle_temp` VALUES (184,'Full piezoelectric tensors of wurtzite and zinc blende ZnO and ZnS by first-principles calculations','M. Cattia; *; Y. Noelb; R. Dovesi','Journal of Physics and Chemistry of Solids',2003,'64',0,2183,2190,'?',0),(186,'Constants, Landolt Bornstein, New Series','A.G. Every; A.K. McCurdy','Constants, Landolt Bornstein, New Series',1992,'3',0,29,29,'?',0),(187,'Second and Higher Order Elastic Constants, Landolt Bornstein, New Series','A.G. Every; A.K. McCurdy','Second and Higher Order Elastic Constants, Landolt Bornstein, New Series',1992,'3',0,29,29,'?',0),(188,'aaaaaa','Poterala','european',2,'1',0,3,4,'?',0);
/*!40000 ALTER TABLE `data_publarticle_temp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datafileproperty_condition_detail`
--

DROP TABLE IF EXISTS `datafileproperty_condition_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `datafileproperty_condition_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datafileproperty_id` varchar(255) NOT NULL,
  `condition_id` varchar(255) NOT NULL,
  `value` varchar(511) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datafileproperty_condition_detail`
--

LOCK TABLES `datafileproperty_condition_detail` WRITE;
/*!40000 ALTER TABLE `datafileproperty_condition_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `datafileproperty_condition_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datafileproperty_condition_detail_temp`
--

DROP TABLE IF EXISTS `datafileproperty_condition_detail_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `datafileproperty_condition_detail_temp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datafileproperty_id` varchar(255) NOT NULL,
  `condition_id` varchar(255) NOT NULL,
  `value` varchar(511) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=496 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datafileproperty_condition_detail_temp`
--

LOCK TABLES `datafileproperty_condition_detail_temp` WRITE;
/*!40000 ALTER TABLE `datafileproperty_condition_detail_temp` DISABLE KEYS */;
/*!40000 ALTER TABLE `datafileproperty_condition_detail_temp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dictionary`
--

DROP TABLE IF EXISTS `dictionary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dictionary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(100) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(511) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `definition` longtext,
  `deploy` tinyint(1) unsigned DEFAULT '0',
  `units` varchar(60) DEFAULT NULL,
  `units_detail` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `active` tinyint(1) unsigned DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dictionary`
--

LOCK TABLES `dictionary` WRITE;
/*!40000 ALTER TABLE `dictionary` DISABLE KEYS */;
INSERT INTO `dictionary` VALUES (1,'_phase_name','phase name',NULL,4,NULL,1,'','','char',1),(2,'_phase_generic','phase generic',NULL,4,NULL,1,'','','char',1),(3,'_phase_formula','phase formula',NULL,4,NULL,1,'','','char',1),(4,'_phase_density','density',NULL,11,NULL,1,'','','numb',1),(5,'_phase_density_temperature','density measurement temperature',NULL,11,NULL,1,'K','kelvin','numb',1),(6,'_phase_melting_transition_temperature','melting temperature ',NULL,11,NULL,1,'K','kelvin','numb',1),(7,'_phase_rhomb_tetra_transition_temperature','rhomb tetra transition temperature',NULL,11,NULL,1,'K','kelvin','numb',1),(8,'_phase_rhomb_ortho_transition_temperature','rhomb ortho transition temperature',NULL,11,NULL,1,'K','kelvin','numb',1),(9,'_phase_ortho_tetra_transition_temperature','ortho tetra transition temperature',NULL,11,NULL,1,'K','kelvin','numb',1),(10,'_phase_Curie_temperature','Curie temperature',NULL,11,NULL,1,'K','kelvin','numb',1),(11,'_phase_Curie_ferroelectric_temperature','Curie ferroelectric temperature',NULL,11,NULL,1,'K','kelvin','numb',1),(12,'_phase_cell_temperature','cell temperature',NULL,11,NULL,1,'K','kelvin','numb',1),(13,'_phase_debye_temperature','debye temperature',NULL,11,NULL,1,'K','kelvin','numb',1),(14,'_chemical_formula','chemical formula',NULL,8,NULL,1,'','','char',1),(15,'_chemical_formula_sum','chemical formula sum',NULL,8,NULL,1,'','','char',1),(16,'_book_editor_name','book editor name',NULL,2,NULL,1,NULL,NULL,NULL,1),(17,'_book_title','book title',NULL,2,NULL,1,NULL,NULL,NULL,1),(18,'_book_publisher_city','book publisher city',NULL,2,NULL,1,NULL,NULL,NULL,1),(19,'_book_publisher','book publisher',NULL,2,NULL,1,NULL,NULL,NULL,1),(20,'_book_id_ISBN','book id ISBN',NULL,2,NULL,1,NULL,NULL,NULL,1),(21,'_journal_pages_number','journal pages number',NULL,3,NULL,1,NULL,NULL,NULL,1),(22,'_journal_article_reference','journal article reference',NULL,3,NULL,1,NULL,NULL,NULL,1),(23,'_cod_database_code','cod database code',NULL,5,NULL,1,NULL,NULL,NULL,1),(24,'_symmetry_point_group_name_H-M','symmetry point group name H-M',NULL,6,' Properties are typically related to the point group of the phase It is one of pg = 1, -1, 2, m, 2/m, 222, mm2, mmm, 4, -4, 4/m, 422, 4mm, -42m, 4/mmm, 3, -3, 32, 3m, -3m, 6, -6, 6/m, 622, 6mm, -6m2, 6/mmm, 23, m3, 432, -43m, m3m,  ... Quasicrystal groupoids:	5mm, 8mm, 10mm, 12mm ... ',1,NULL,NULL,'char',1),(25,'_structure_refined','structure refined',NULL,7,NULL,1,NULL,NULL,NULL,1),(28,'_prop_conditions_temperature','temperature','_temperature',9,NULL,1,'K','kelvin','numb',1),(29,'_prop_conditions_temperature_range_start','temperature range start','_temperature_range_begin',9,NULL,1,'K','kelvin','numb',1),(30,'_prop_conditions_temperature_range_end','temperature range end','_temperature_range_end',9,NULL,1,'K','kelvin','numb',1),(31,'_prop_conditions_temperature_cycle','temperature cycle','_temperature_cycle',9,NULL,1,'1','pure number','numb',1),(32,'_prop_conditions_pressure','pressure','_pressure',9,NULL,1,'Pa','pascal','numb',1),(33,'_prop_conditions_frequency','frequency','_frequency',9,NULL,1,'s^-1','hertz','numb',1),(34,'_prop_conditions_magnetic_field','magnetic field','_magnetic_field',9,NULL,1,'T','tesla','numb',1),(35,'_prop_conditions_wavelength','wavelength','_wavelength',9,NULL,1,'10^-6.metre','micrometre','numb',1),(36,'_prop_conditions_reference_temperature_thermoelastic_non_linear_fit','reference temperature thermoelastic non linear fit','_reference_temperature_thermoelastic_non_linear_fit',9,NULL,1,'K','kelvin','numb',1),(37,'_prop_conditions_atmosphere_gas','atmosphere gas','_atmosphere_gas',9,NULL,1,'Pa','pascal',NULL,1),(38,'_prop_conditions_atmosphere_gas_pressure','atmosphere gas pressure','_atmosphere_gas_pressure',9,NULL,1,'Pa','pascal',NULL,1),(39,'_prop_conditions_atmosphere_gas_flow','atmosphere gas flow','_atmosphere_gas_flow',9,NULL,1,'1mn^-1',' ',NULL,1),(40,'_prop_thermal_expansion_temperature_reference_T0','thermal expansion temperature reference T0','_thermal_expansion_temperature_reference_T0',9,NULL,1,'K','kelvin',NULL,1),(41,'_prop_thermal_expansion_temperature_range_begin','thermal expansion temperature range begin','_thermal_expansion_temperature_range_begin',9,NULL,1,'K','kelvin',NULL,1),(42,'_prop_thermal_expansion_temperature_range_end','thermal expansion temperature range end','_thermal_expansion_temperature_range_end',9,NULL,1,'K','kelvin',NULL,1),(43,'_prop_superconducting_critical_temperature_mid_50','superconducting critical temperature mid 50','_superconducting_critical_temperature_mid_50',9,NULL,1,'K','kelvin',NULL,1),(44,'_prop_superconducting_critical_temperature_mid_50_measurement_method','superconducting critical temperature mid 50 measurement method','_superconducting_critical_temperature_mid_50_measurement_method',9,NULL,1,'n.a.','n.a.',NULL,1),(45,'_prop_superconducting_resistivity_transition_width','superconducting resistivity transition width','_superconducting_resistivity_transition_width',9,NULL,1,'n.a.','n.a.',NULL,1),(46,'_prop_superconducting_resistivity_transition_width_measurement_method','superconducting resistivity transition width measurement method','_superconducting_resistivity_transition_width_measurement_method',9,NULL,1,'n.a.','n.a.',NULL,1),(47,'_prop_chargedensitywave_critical_temperature_TCDW_measurement_method','chargedensitywave critical temperature TCDW measurement method','_chargedensitywave_critical_temperature_TCDW_measurement_method',9,NULL,1,'n.a.','n.a.',NULL,1),(48,'_prop_measurement_method','method','_measurement_method',12,NULL,1,'n.a.','n.a.','char',1),(49,'_prop_measurement_poling','poling','_measurement_poling',9,NULL,1,'n.a.','n.a.','char',1),(50,'_prop_frame','frame','_frame',9,NULL,1,'n.a.','n.a.','char',1),(51,'_prop_symmetry_point_group_name_H-M','symmetry point group name H-M','symmetry point group name H-M',10,'The macroscopic property symmetry can differ from that of the crystal point group. For instance, poling in ferroelectric single crystals can modify the global symmetry of dipoles depending on the poling direction.',0,NULL,NULL,NULL,1),(52,'_prop_data_tensorial_index','data tensorial index','  tensorial index',9,NULL,0,NULL,NULL,NULL,1),(53,'_prop_data_uncertainty','data uncertainty ','  uncertainty ',9,NULL,0,NULL,NULL,NULL,1),(54,'_prop_data_value','data value','  value',9,NULL,0,NULL,NULL,NULL,1),(55,'_prop_data_label','data label','  label',9,NULL,0,NULL,NULL,NULL,1),(56,'_prop_heat_capacity_C0P','heat capacity C0P','  heat_capacity_C0P',9,NULL,1,'n.a.','n.a.',NULL,1),(57,'_prop_heat_capacity_C1P','heat capacity C1P','  heat_capacity_C1P',9,NULL,1,'n.a.','n.a.',NULL,1),(58,'_prop_heat_capacity_C2P','heat capacity C2P','  heat_capacity_C2P',9,NULL,1,'n.a.','n.a.',NULL,1),(59,'_prop_elastic_stiffness_cij','elastic stiffness cij','  elastic_stiffness_cij',9,NULL,0,NULL,NULL,NULL,1),(60,'_prop_elastic_compliance_sij','elastic compliance sij','  elastic_compliance_sij',9,NULL,0,NULL,NULL,NULL,1),(61,'_prop_piezoelectric_dij','piezoelectric dij','  piezoelectric_dij',9,NULL,0,NULL,NULL,NULL,1),(62,'_prop_elastic_stiffness_cijD','elastic_stiffness cijD','  elastic_stiffness_cijD',9,NULL,0,'GPa','giga Pascal',NULL,1),(63,'_prop_elastic_stiffness_cijE','elastic stiffness cijE','  elastic_stiffness_cijE',9,NULL,0,'GPa','giga Pascal',NULL,1),(64,'_prop_elastic_stiffness_cijS','elastic stiffness cijS','  elastic_stiffness_cijS',9,NULL,0,'GPa','giga Pascal',NULL,1),(65,'_prop_elastic_compliance_sijD','elastic compliance sijD','  elastic_compliance_sijD',9,NULL,0,'10^-12.Pa^-1','pico Pascal^-1',NULL,1),(66,'_prop_elastic_compliance_sijE','elastic_compliance_sijE','  elastic_compliance_sijE',9,NULL,0,'10^-12.Pa^-1','pico Pascal^-1',NULL,1),(67,'_prop_elastic_stiffness_hydrostaticpressure_1storder_cij1P','elastic stiffness hydrostaticpressure 1storder cij1P','  elastic_stiffness_hydrostaticpressure_1storder_cij1P',9,NULL,0,'GPa^-1','giga Pascal',NULL,1),(68,'_prop_elastic_stiffness_hydrostaticpressure_2ndorder_cij2P','elastic stiffness hydrostaticpressure 2ndorder_cij2P','  elastic_stiffness_hydrostaticpressure_2ndorder_cij2P',9,NULL,0,'GPa^-1','giga Pascal',NULL,1),(69,'_prop_piezoelectric_gij','piezoelectric gij','   piezoelectric gij',9,NULL,0,'C.m^-2','coulomb oer square metre',NULL,1),(70,'_prop_piezoelectric_eij','piezoelectric eij','   piezoelectric_eij',9,NULL,0,'C.N^-1','coulomb per newton',NULL,1),(71,'_prop_piezoelectric_hij','piezoelectric hij','   piezoelectric_hij',9,NULL,0,'V.m.N^-1','volt metre per newton',NULL,1),(72,'_prop_heat_capacity_perpendicular','heat capacity perpendicular','_heat_capacity_perpendicular',9,'n',1,'n.a.','n.a.','numb',1),(73,'_prop_heat_capacity_parallel','heat capacity parallel','_heat_capacity_parallel',9,'n',1,'n.a.','n.a.','numb',1);
/*!40000 ALTER TABLE `dictionary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'site','sites','site'),(8,'paths','data','paths'),(9,'path','data','path'),(10,'publ article','data','publarticle'),(11,'data file','data','datafile'),(12,'mail','mail','configuration'),(13,'Article Information','Article','publarticle'),(14,'Article File Information','Article','datafile'),(15,'CIF File Information','CIF','datafile'),(16,'SMTP Server Configuration','Configuration','configuration'),(17,'Message Server Configuration','Configuration','messagemailsignup'),(18,'Message Server Configuration','Configuration','configurationmessage'),(19,'Category','Configuration','messagecategory'),(20,'Category Detail','Configuration','messagecategorydetail'),(21,'Message','Configuration','messagemail'),(22,'Experimental par condition','Properties','experimentalparcond'),(23,'User','Properties','fileuser'),(24,'Catalog Property','Properties','catalogpropertydataproperty'),(25,'Catalog Property','Properties','catalogproperty'),(26,'type','Properties','type'),(27,'Crystal System','Properties','catalogcrystalsystem'),(28,'catalog point group','Properties','catalogpointgroup'),(29,'file user','data','fileuser'),(30,'dictionary','data','dictionary'),(31,'dictionary','Properties','dictionary'),(32,'Properties','Dictionaries','dictionary'),(33,'Path Configuration','Configuration','path'),(34,'Property Detail','Properties','catalogpropertydetail'),(35,'Axis','Properties','catalogaxis'),(36,'Puntual Group Name','Properties','puntualgroupnames'),(37,'Group Group','Properties','puntualgroupgroups'),(38,'Category','Dictionaries','category'),(39,'Type and Data Property','Properties','typedataproperty'),(40,'type data property catalog property detail admin','data','typedatapropertycatalogpropertydetailadmin'),(41,'Data Property Detail','Properties','typedatapropertycatalogpropertydetailadmin'),(42,'Data Property Detail','Properties','datapropertydetailadmin'),(43,'book','data','book'),(44,'property','data','property'),(45,'Data Property','Properties','property'),(46,'Publish file','Users','fileuser'),(47,'puntual group names','data','puntualgroupnames'),(48,'publish file','Files','fileuser'),(49,'Tag','Properties','tags'),(50,'category tag','Properties','categorytag');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (2,'mpod.cimav.edu.mx','http://mpod.cimav.edu.mx/'),(3,'devmpod.cimav.edu.mx','http://devmpod.cimav.edu.mx/'),(4,'127.0.0.1:8000','http://127.0.0.1:8000/'),(5,'127.0.0.1','http://127.0.0.1/');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experimentalfilecon_datafile`
--

DROP TABLE IF EXISTS `experimentalfilecon_datafile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `experimentalfilecon_datafile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `experimentalfilecon_id` int(11) NOT NULL,
  `datafile_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experimentalfilecon_datafile`
--

LOCK TABLES `experimentalfilecon_datafile` WRITE;
/*!40000 ALTER TABLE `experimentalfilecon_datafile` DISABLE KEYS */;
/*!40000 ALTER TABLE `experimentalfilecon_datafile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experimentalfilecontemp_datafiletemp`
--

DROP TABLE IF EXISTS `experimentalfilecontemp_datafiletemp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `experimentalfilecontemp_datafiletemp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `experimentalfilecontemp_id` int(11) NOT NULL,
  `datafiletemp_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experimentalfilecontemp_datafiletemp`
--

LOCK TABLES `experimentalfilecontemp_datafiletemp` WRITE;
/*!40000 ALTER TABLE `experimentalfilecontemp_datafiletemp` DISABLE KEYS */;
/*!40000 ALTER TABLE `experimentalfilecontemp_datafiletemp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `file_user`
--

DROP TABLE IF EXISTS `file_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `file_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(45) DEFAULT NULL,
  `authuser_id` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `reportvalidation` longtext,
  `datafile_id` int(11) DEFAULT NULL,
  `publish` tinyint(1) DEFAULT NULL,
  `datepublished` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file_user`
--

LOCK TABLES `file_user` WRITE;
/*!40000 ALTER TABLE `file_user` DISABLE KEYS */;
INSERT INTO `file_user` VALUES (4,'zaqpdykfzkxkgkfwo.mpod',1,'2019-03-17 12:06:01','Validation results\n------------------\n\n Block \'zaqpdykfzkxkgkfwo\' is VALID\n',1000378,1,'2019-03-28 00:46:28'),(6,'qwryety5zmyzlofjlqljhur.mpod',16,'2019-04-25 00:12:20','Validation results\n------------------\n\n Block \'qwryety5zmyzlofjlqljhur\' is VALID',NULL,0,NULL),(7,'qwryety5evabyddyhvcmvjp.mpod',16,'2019-04-25 00:13:10','Validation results\n------------------\n\n Block \'qwryety5zmyzlofjlqljhur\' is VALID',NULL,0,NULL),(8,'qwryety5dmgdlcefmonwzhd.mpod',16,'2019-04-25 00:14:21','Validation results\n------------------\n\n Block \'qwryety5zmyzlofjlqljhur\' is VALID',NULL,0,NULL),(9,'qwryety5xauddvrdaufvivh.mpod',16,'2019-04-25 00:15:28','Validation results\n------------------\n\n Block \'qwryety5zmyzlofjlqljhur\' is VALID',NULL,0,NULL),(10,'ywrtaw4=wbtdqwuqqtdvfmk.mpod',1,'2019-04-24 23:23:37','Validation results\n------------------\n\n Block \'ywrtaw4=wbtdqwuqqtdvfmk\' is VALID\n',NULL,0,NULL),(11,'ywrtaw4=diasauyzjkluels.mpod',1,'2019-04-24 23:23:37','Validation results\n------------------\n\n Block \'ywrtaw4=diasauyzjkluels\' is VALID\n',NULL,0,NULL);
/*!40000 ALTER TABLE `file_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `key_notation`
--

DROP TABLE IF EXISTS `key_notation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `key_notation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(1000) DEFAULT NULL,
  `source_components_number` varchar(45) DEFAULT NULL,
  `applyforallproperty` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `key_notation`
--

LOCK TABLES `key_notation` WRITE;
/*!40000 ALTER TABLE `key_notation` DISABLE KEYS */;
INSERT INTO `key_notation` VALUES (1,'zero component','0',0),(2,'non-zero component','1',0),(3,'equal components','1',0),(4,'equal components opposite sing','1',0),(5,'For s, twice the numerical equal of the heavy dot component to which it is joined','1',0),(6,'For c, numerical equal of the heavy dot component to which it is joined','1',0),(7,'For s, 2 (s11 - s12)','2',1),(8,'For c, 1/2  (c11 - c12)','2',1),(9,'Symmetry','0',1),(10,'Twice the numerical equal of the heavy dot component to which it is joined','1',0);
/*!40000 ALTER TABLE `key_notation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keynotation_catalogpropertydetail`
--

DROP TABLE IF EXISTS `keynotation_catalogpropertydetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `keynotation_catalogpropertydetail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keynotation_id` int(11) DEFAULT NULL,
  `catalogpropertydetail_id` int(11) DEFAULT NULL,
  `source` varchar(100) DEFAULT NULL,
  `target` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2300 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keynotation_catalogpropertydetail`
--

LOCK TABLES `keynotation_catalogpropertydetail` WRITE;
/*!40000 ALTER TABLE `keynotation_catalogpropertydetail` DISABLE KEYS */;
INSERT INTO `keynotation_catalogpropertydetail` VALUES (32,2,865,'c11','c11'),(33,2,864,'c12','c12'),(34,2,863,'c13','c13'),(35,2,862,'c14','c14'),(36,2,861,'c15','c15'),(37,2,860,'c16','c16'),(38,2,859,'c22','c22'),(39,2,858,'c23','c23'),(40,2,857,'c24','c24'),(41,2,856,'c25','c25'),(42,2,855,'c26','c26'),(43,2,854,'c33','c33'),(44,2,853,'c34','c34'),(45,2,852,'c35','c35'),(46,2,851,'c36','c36'),(47,2,850,'c44','c44'),(48,2,849,'c45','c45'),(49,2,848,'c46','c46'),(50,2,847,'c55','c55'),(51,2,846,'c56','c56'),(52,2,845,'c66','c66'),(53,2,1594,'c11D','c11D'),(54,2,1593,'c12D','c12D'),(55,2,1592,'c13D','c13D'),(56,2,1591,'c14D','c14D'),(57,2,1590,'c15D','c15D'),(58,2,1589,'c16D','c16D'),(59,2,1588,'c22D','c22D'),(60,2,1587,'c23D','c23D'),(61,2,1586,'c24D','c24D'),(62,2,1585,'c25D','c25D'),(63,2,1584,'c26D','c26D'),(64,2,1583,'c33D','c33D'),(65,2,1582,'c34D','c34D'),(66,2,1581,'c35D','c35D'),(67,2,1580,'c36D','c36D'),(68,2,1579,'c44D','c44D'),(69,2,1578,'c45D','c45D'),(70,2,1577,'c46D','c46D'),(71,2,1576,'c55D','c55D'),(72,2,1575,'c56D','c56D'),(73,2,1574,'c66D','c66D'),(74,2,1686,'c11E','c11E'),(75,2,1685,'c12E','c12E'),(76,2,1684,'c13E','c13E'),(77,2,1683,'c14E','c14E'),(78,2,1682,'c15E','c15E'),(79,2,1681,'c16E','c16E'),(80,2,1680,'c22E','c22E'),(81,2,1679,'c23E','c23E'),(82,2,1678,'c24E','c24E'),(83,2,1677,'c25E','c25E'),(84,2,1676,'c26E','c26E'),(85,2,1675,'c33E','c33E'),(86,2,1674,'c34E','c34E'),(87,2,1673,'c35E','c35E'),(88,2,1672,'c36E','c36E'),(89,2,1671,'c44E','c44E'),(90,2,1670,'c45E','c45E'),(91,2,1669,'c46E','c46E'),(92,2,1668,'c55E','c55E'),(93,2,1667,'c56E','c56E'),(94,2,1666,'c66E','c66E'),(95,2,1777,'c11S','c11S'),(96,2,1776,'c12S','c12S'),(97,2,1775,'c13S','c13S'),(98,2,1774,'c14S','c14S'),(99,2,1773,'c15S','c15S'),(100,2,1772,'c16S','c16S'),(101,2,1771,'c22S','c22S'),(102,2,1770,'c23S','c23S'),(103,2,1769,'c24S','c24S'),(104,2,1768,'c25S','c25S'),(105,2,1767,'c26S','c26S'),(106,2,1766,'c33S','c33S'),(107,2,1765,'c34S','c34S'),(108,2,1764,'c35S','c35S'),(109,2,1763,'c36S','c36S'),(110,2,1762,'c44S','c44S'),(111,2,1761,'c45S','c45S'),(112,2,1760,'c46S','c46S'),(113,2,1759,'c55S','c55S'),(114,2,1758,'c56S','c56S'),(115,2,1757,'c66S','c66S'),(116,2,1869,'c111P','c111P'),(117,2,1868,'c121P','c121P'),(118,2,1867,'c131P','c131P'),(119,2,1866,'c141P','c141P'),(120,2,1865,'c151P','c151P'),(121,2,1864,'c161P','c161P'),(122,2,1863,'c221P','c221P'),(123,2,1862,'c231P','c231P'),(124,2,1861,'c241P','c241P'),(125,2,1860,'c251P','c251P'),(126,2,1859,'c261P','c261P'),(127,2,1858,'c331P','c331P'),(128,2,1857,'c341P','c341P'),(129,2,1856,'c351P','c351P'),(130,2,1855,'c361P','c361P'),(131,2,1854,'c441P','c441P'),(132,2,1853,'c451P','c451P'),(133,2,1852,'c461P','c461P'),(134,2,1851,'c551P','c551P'),(135,2,1850,'c561P','c561P'),(136,2,1849,'c661P','c661P'),(137,2,1961,'c112P','c112P'),(138,2,1960,'c122P','c122P'),(139,2,1959,'c132P','c132P'),(140,2,1958,'c142P','c142P'),(141,2,1957,'c152P','c152P'),(142,2,1956,'c162P','c162P'),(143,2,1955,'c222P','c222P'),(144,2,1954,'c232P','c232P'),(145,2,1953,'c242P','c242P'),(146,2,1952,'c252P','c252P'),(147,2,1951,'c262P','c262P'),(148,2,1950,'c332P','c332P'),(149,2,1949,'c342P','c342P'),(150,2,1948,'c352P','c352P'),(151,2,1947,'c362P','c362P'),(152,2,1946,'c442P','c442P'),(153,2,1945,'c452P','c452P'),(154,2,1944,'c462P','c462P'),(155,2,1943,'c552P','c552P'),(156,2,1942,'c562P','c562P'),(157,2,1941,'c662P','c662P'),(158,2,2054,'c11S1T','c11S1T'),(159,2,2053,'c12S1T','c12S1T'),(160,2,2052,'c13S1T','c13S1T'),(161,2,2051,'c14S1T','c14S1T'),(162,2,2050,'c15S1T','c15S1T'),(163,2,2049,'c16S1T','c16S1T'),(164,2,2048,'c22S1T','c22S1T'),(165,2,2047,'c23S1T','c23S1T'),(166,2,2046,'c24S1T','c24S1T'),(167,2,2045,'c25S1T','c25S1T'),(168,2,2044,'c26S1T','c26S1T'),(169,2,2043,'c33S1T','c33S1T'),(170,2,2042,'c34S1T','c34S1T'),(171,2,2041,'c35S1T','c35S1T'),(172,2,2040,'c36S1T','c36S1T'),(173,2,2039,'c44S1T','c44S1T'),(174,2,2038,'c45S1T','c45S1T'),(175,2,2037,'c46S1T','c46S1T'),(176,2,2036,'c55S1T','c55S1T'),(177,2,2035,'c56S1T','c56S1T'),(178,2,2034,'c66S1T','c66S1T'),(179,2,2146,'c11S2T','c11S2T'),(180,2,2145,'c12S2T','c12S2T'),(181,2,2144,'c13S2T','c13S2T'),(182,2,2143,'c14S2T','c14S2T'),(183,2,2142,'c15S2T','c15S2T'),(184,2,2141,'c16S2T','c16S2T'),(185,2,2140,'c22S2T','c22S2T'),(186,2,2139,'c23S2T','c23S2T'),(187,2,2138,'c24S2T','c24S2T'),(188,2,2137,'c25S2T','c25S2T'),(189,2,2136,'c26S2T','c26S2T'),(190,2,2135,'c33S2T','c33S2T'),(191,2,2134,'c34S2T','c34S2T'),(192,2,2132,'c35S2T','c35S2T'),(193,2,2133,'c36S2T','c36S2T'),(194,2,2131,'c44S2T','c44S2T'),(195,2,2130,'c45S2T','c45S2T'),(196,2,2129,'c46S2T','c46S2T'),(197,2,2128,'c55S2T','c55S2T'),(198,2,2127,'c56S2T','c56S2T'),(199,2,2126,'c66S2T','c66S2T'),(200,2,844,'s11','s11'),(201,2,843,'s12','s12'),(202,2,842,'s13','s13'),(203,2,841,'s14','s14'),(204,2,840,'s15','s15'),(205,2,839,'s16','s16'),(206,2,838,'s22','s22'),(207,2,837,'s23','s23'),(208,2,836,'s24','s24'),(209,2,835,'s25','s25'),(210,2,834,'s26','s26'),(211,2,833,'s33','s33'),(212,2,832,'s34','s34'),(213,2,831,'s35','s35'),(214,2,830,'s36','s36'),(215,2,829,'s44','s44'),(216,2,828,'s45','s45'),(217,2,827,'s46','s46'),(218,2,826,'s55','s55'),(219,2,825,'s56','s56'),(220,2,824,'s66','s66'),(221,2,952,'s11E','s11E'),(222,2,951,'s12E','s12E'),(223,2,950,'s13E','s13E'),(224,2,949,'s14E','s14E'),(225,2,948,'s15E','s15E'),(226,2,947,'s16E','s16E'),(227,2,946,'s22E','s22E'),(228,2,945,'s23E','s23E'),(229,2,944,'s24E','s24E'),(230,2,943,'s25E','s25E'),(231,2,942,'s26E','s26E'),(232,2,941,'s33E','s33E'),(233,2,940,'s34E','s34E'),(234,2,939,'s35E','s35E'),(235,2,938,'s36E','s36E'),(236,2,937,'s44E','s44E'),(237,2,936,'s45E','s45E'),(238,2,935,'s46E','s46E'),(239,2,934,'s55E','s55E'),(240,2,933,'s56E','s56E'),(241,2,932,'s66E','s66E'),(242,2,1044,'s11D','s11D'),(243,2,1043,'s12D','s12D'),(244,2,1042,'s13D','s13D'),(245,2,1041,'s14D','s14D'),(246,2,1040,'s15D','s15D'),(247,2,1039,'s16D','s16D'),(248,2,1038,'s22D','s22D'),(249,2,1037,'s23D','s23D'),(250,2,1036,'s24D','s24D'),(251,2,1035,'s25D','s25D'),(252,2,1034,'s26D','s26D'),(253,2,1033,'s33D','s33D'),(254,2,1032,'s34D','s34D'),(255,2,1031,'s35D','s35D'),(256,2,1030,'s36D','s36D'),(257,2,1029,'s44D','s44D'),(258,2,1028,'s45D','s45D'),(259,2,1027,'s46D','s46D'),(260,2,1026,'s55D','s55D'),(261,2,1025,'s56D','s56D'),(262,2,1024,'s66D','s66D'),(263,2,1136,'s111T','s111T'),(264,2,1135,'s121T','s121T'),(265,2,1134,'s131T','s131T'),(266,2,1133,'s141T','s141T'),(267,2,1132,'s151T','s151T'),(268,2,1131,'s161T','s161T'),(269,2,1130,'s221T','s221T'),(270,2,1129,'s231T','s231T'),(271,2,1128,'s241T','s241T'),(272,2,1127,'s251T','s251T'),(273,2,1126,'s261T','s261T'),(274,2,1125,'s331T','s331T'),(275,2,1124,'s341T','s341T'),(276,2,1123,'s351T','s351T'),(277,2,1122,'s361T','s361T'),(278,2,1121,'s441T','s441T'),(279,2,1120,'s451T','s451T'),(280,2,1119,'s461T','s461T'),(281,2,1118,'s551T','s551T'),(282,2,1117,'s561T','s561T'),(283,2,1116,'s661T','s661T'),(284,2,1227,'s112T','s112T'),(285,2,1226,'s122T','s122T'),(286,2,1225,'s132T','s132T'),(287,2,1224,'s142T','s142T'),(288,2,1223,'s152T','s152T'),(289,2,1222,'s162T','s162T'),(290,2,1221,'s222T','s222T'),(291,2,1220,'s232T','s232T'),(292,2,1219,'s242T','s242T'),(293,2,1218,'s252T','s252T'),(294,2,1217,'s262T','s262T'),(295,2,1216,'s332T','s332T'),(296,2,1215,'s342T','s342T'),(297,2,1214,'s352T','s352T'),(298,2,1213,'s362T','s362T'),(299,2,1212,'s442T','s442T'),(300,2,1211,'s452T','s452T'),(301,2,1210,'s462T','s462T'),(302,2,1209,'s552T','s552T'),(303,2,1208,'s562T','s562T'),(304,2,1207,'s662T','s662T'),(305,2,1319,'s113T','s113T'),(306,2,1318,'s123T','s123T'),(307,2,1317,'s133T','s133T'),(308,2,1316,'s143T','s143T'),(309,2,1315,'s153T','s153T'),(310,2,1314,'s163T','s163T'),(311,2,1313,'s223T','s223T'),(312,2,1312,'s233T','s233T'),(313,2,1311,'s243T','s243T'),(314,2,1310,'s253T','s253T'),(315,2,1309,'s263T','s263T'),(316,2,1308,'s333T','s333T'),(317,2,1307,'s343T','s343T'),(318,2,1306,'s353T','s353T'),(319,2,1305,'s363T','s363T'),(320,2,1304,'s443T','s443T'),(321,2,1303,'s453T','s453T'),(322,2,1302,'s463T','s463T'),(323,2,1301,'s553T','s553T'),(324,2,1300,'s563T','s563T'),(325,2,1299,'s663T','s663T'),(326,2,1411,'s11S','s11S'),(327,2,1410,'s12S','s12S'),(328,2,1409,'s13S','s13S'),(329,2,1408,'s14S','s14S'),(330,2,1407,'s15S','s15S'),(331,2,1406,'s16S','s16S'),(332,2,1405,'s22S','s22S'),(333,2,1404,'s23S','s23S'),(334,2,1403,'s24S','s24S'),(335,2,1402,'s25S','s25S'),(336,2,1401,'s26S','s26S'),(337,2,1400,'s33S','s33S'),(338,2,1399,'s34S','s34S'),(339,2,1398,'s35S','s35S'),(340,2,1397,'s36S','s36S'),(341,2,1396,'s44S','s44S'),(342,2,1395,'s45S','s45S'),(343,2,1394,'s46S','s46S'),(344,2,1393,'s55S','s55S'),(345,2,1392,'s56S','s56S'),(346,2,1391,'s66S','s66S'),(347,2,1424,'s11S','s11S'),(348,2,1423,'s12S','s12S'),(349,2,1422,'s13S','s13S'),(350,2,1421,'s15S','s15S'),(351,2,1420,'s22S','s22S'),(352,2,1419,'s23S','s23S'),(353,2,1418,'s25S','s25S'),(354,2,1417,'s33S','s33S'),(355,2,1416,'s35S','s35S'),(356,2,1415,'s44S','s44S'),(357,2,1414,'s46S','s46S'),(358,2,1413,'s55S','s55S'),(359,2,1412,'s66S','s66S'),(360,2,878,'s11','s11'),(361,2,877,'s12','s12'),(362,2,876,'s13','s13'),(363,2,875,'s15','s15'),(364,2,874,'s22','s22'),(365,2,873,'s23','s23'),(366,2,872,'s25','s25'),(367,2,871,'s33','s33'),(368,2,870,'s35','s35'),(369,2,869,'s44','s44'),(370,2,868,'s46','s46'),(371,2,867,'s55','s55'),(372,2,866,'s66','s66'),(373,2,965,'s11E','s11E'),(374,2,964,'s12E','s12E'),(375,2,963,'s13E','s13E'),(376,2,962,'s15E','s15E'),(377,2,961,'s22E','s22E'),(378,2,960,'s23E','s23E'),(379,2,959,'s25E','s25E'),(380,2,958,'s33E','s33E'),(381,2,957,'s35E','s35E'),(382,2,956,'s44E','s44E'),(383,2,955,'s46E','s46E'),(384,2,954,'s55E','s55E'),(385,2,953,'s66E','s66E'),(386,2,1057,'s11D','s11D'),(387,2,1056,'s12D','s12D'),(388,2,1055,'s13D','s13D'),(389,2,1054,'s15D','s15D'),(390,2,1053,'s22D','s22D'),(391,2,1052,'s23D','s23D'),(392,2,1051,'s25D','s25D'),(393,2,1050,'s33D','s33D'),(394,2,1049,'s35D','s35D'),(395,2,1048,'s44D','s44D'),(396,2,1047,'s46D','s46D'),(397,2,1046,'s55D','s55D'),(398,2,1045,'s66D','s66D'),(399,2,1149,'s111T','s111T'),(400,2,1148,'s121T','s121T'),(401,2,1147,'s131T','s131T'),(402,2,1146,'s151T','s151T'),(403,2,1145,'s221T','s221T'),(404,2,1144,'s231T','s231T'),(405,2,1143,'s251T','s251T'),(406,2,1142,'s331T','s331T'),(407,2,1141,'s351T','s351T'),(408,2,1140,'s441T','s441T'),(409,2,1139,'s461T','s461T'),(410,2,1138,'s551T','s551T'),(411,2,1137,'s661T','s661T'),(412,2,1240,'s112T','s112T'),(413,2,1239,'s122T','s122T'),(414,2,1238,'s132T','s132T'),(415,2,1237,'s152T','s152T'),(416,2,1236,'s222T','s222T'),(417,2,1235,'s232T','s232T'),(418,2,1234,'s252T','s252T'),(419,2,1233,'s332T','s332T'),(420,2,1232,'s352T','s352T'),(421,2,1231,'s442T','s442T'),(422,2,1230,'s462T','s462T'),(423,2,1229,'s552T','s552T'),(424,2,1228,'s662T','s662T'),(425,2,1332,'s113T','s113T'),(426,2,1331,'s123T','s123T'),(427,2,1330,'s133T','s133T'),(428,2,1329,'s153T','s153T'),(429,2,1328,'s223T','s223T'),(430,2,1327,'s233T','s233T'),(431,2,1326,'s253T','s253T'),(432,2,1325,'s333T','s333T'),(433,2,1324,'s353T','s353T'),(434,2,1323,'s443T','s443T'),(435,2,1322,'s463T','s463T'),(436,2,1321,'s553T','s553T'),(437,2,1320,'s663T','s663T'),(438,2,891,'s11','s11'),(439,2,890,'s12','s12'),(440,2,889,'s13','s13'),(441,2,888,'s16','s16'),(442,2,887,'s22','s22'),(443,2,886,'s23','s23'),(444,2,885,'s26','s26'),(445,2,884,'s33','s33'),(446,2,883,'s36','s36'),(447,2,882,'s44','s44'),(448,2,881,'s45','s45'),(449,2,880,'s55','s55'),(450,2,879,'s66','s66'),(451,2,978,'s11E','s11E'),(452,2,977,'s12E','s12E'),(453,2,976,'s13E','s13E'),(454,2,975,'s16E','s16E'),(455,2,974,'s22E','s22E'),(456,2,973,'s23E','s23E'),(457,2,972,'s26E','s26E'),(458,2,971,'s33E','s33E'),(459,2,970,'s36E','s36E'),(460,2,969,'s44E','s44E'),(461,2,968,'s45E','s45E'),(462,2,967,'s55E','s55E'),(463,2,966,'s66E','s66E'),(464,2,1070,'s11D','s11D'),(465,2,1069,'s12D','s12D'),(466,2,1068,'s13D','s13D'),(467,2,1067,'s16D','s16D'),(468,2,1066,'s22D','s22D'),(469,2,1065,'s23D','s23D'),(470,2,1064,'s26D','s26D'),(471,2,1063,'s33D','s33D'),(472,2,1062,'s36D','s36D'),(473,2,1061,'s44D','s44D'),(474,2,1060,'s45D','s45D'),(475,2,1059,'s55D','s55D'),(476,2,1058,'s66D','s66D'),(477,2,1162,'s111T','s111T'),(478,2,1161,'s121T','s121T'),(479,2,1160,'s131T','s131T'),(480,2,1159,'s161T','s161T'),(481,2,1158,'s221T','s221T'),(482,2,1157,'s231T','s231T'),(483,2,1156,'s261T','s261T'),(484,2,1155,'s331T','s331T'),(485,2,1154,'s361T','s361T'),(486,2,1153,'s441T','s441T'),(487,2,1152,'s451T','s451T'),(488,2,1151,'s551T','s551T'),(489,2,1150,'s661T','s661T'),(490,2,1253,'s112T','s112T'),(491,2,1252,'s122T','s122T'),(492,2,1251,'s132T','s132T'),(493,2,1250,'s162T','s162T'),(494,2,1249,'s222T','s222T'),(495,2,1248,'s232T','s232T'),(496,2,1247,'s262T','s262T'),(497,2,1246,'s332T','s332T'),(498,2,1245,'s362T','s362T'),(499,2,1244,'s442T','s442T'),(500,2,1243,'s452T','s452T'),(501,2,1242,'s552T','s552T'),(502,2,1241,'s662T','s662T'),(503,2,1345,'s113T','s113T'),(504,2,1344,'s123T','s123T'),(505,2,1343,'s133T','s133T'),(506,2,1342,'s163T','s163T'),(507,2,1341,'s223T','s223T'),(508,2,1340,'s233T','s233T'),(509,2,1339,'s263T','s263T'),(510,2,1338,'s333T','s333T'),(511,2,1337,'s363T','s363T'),(512,2,1336,'s443T','s443T'),(513,2,1335,'s453T','s453T'),(514,2,1334,'s553T','s553T'),(515,2,1333,'s663T','s663T'),(516,2,1437,'s11S','s11S'),(517,2,1436,'s12S','s12S'),(518,2,1435,'s13S','s13S'),(519,2,1434,'s16S','s16S'),(520,2,1433,'s22S','s22S'),(521,2,1432,'s23S','s23S'),(522,2,1431,'s26S','s26S'),(523,2,1430,'s33S','s33S'),(524,2,1429,'s36S','s36S'),(525,2,1428,'s44S','s44S'),(526,2,1427,'s45S','s45S'),(527,2,1426,'s55S','s55S'),(528,2,1425,'s66S','s66S'),(529,2,1528,'c11','c11'),(530,2,1527,'c12','c12'),(531,2,1526,'c13','c13'),(532,2,1525,'c16','c16'),(533,2,1524,'c22','c22'),(534,2,1523,'c23','c23'),(535,2,1522,'c26','c26'),(536,2,1521,'c33','c33'),(537,2,1520,'c36','c36'),(538,2,1519,'c44','c44'),(539,2,1518,'c45','c45'),(540,2,1517,'c55','c55'),(541,2,1516,'c66','c66'),(542,2,1620,'c11D','c11D'),(543,2,1619,'c12D','c12D'),(544,2,1618,'c13D','c13D'),(545,2,1617,'c16D','c16D'),(546,2,1616,'c22D','c22D'),(547,2,1615,'c23D','c23D'),(548,2,1614,'c26D','c26D'),(549,2,1613,'c33D','c33D'),(550,2,1612,'c36D','c36D'),(551,2,1611,'c44D','c44D'),(552,2,1610,'c45D','c45D'),(553,2,1609,'c55D','c55D'),(554,2,1608,'c66D','c66D'),(555,2,1712,'c11E','c11E'),(556,2,1711,'c12E','c12E'),(557,2,1710,'c13E','c13E'),(558,2,1709,'c16E','c16E'),(559,2,1708,'c22E','c22E'),(560,2,1707,'c23E','c23E'),(561,2,1706,'c26E','c26E'),(562,2,1705,'c33E','c33E'),(563,2,1704,'c36E','c36E'),(564,2,1703,'c44E','c44E'),(565,2,1702,'c45E','c45E'),(566,2,1701,'c55E','c55E'),(567,2,1700,'c66E','c66E'),(568,2,1803,'c11S','c11S'),(569,2,1802,'c12S','c12S'),(570,2,1801,'c13S','c13S'),(571,2,1800,'c16S','c16S'),(572,2,1799,'c22S','c22S'),(573,2,1798,'c23S','c23S'),(574,2,1797,'c26S','c26S'),(575,2,1796,'c33S','c33S'),(576,2,1795,'c36S','c36S'),(577,2,1794,'c44S','c44S'),(578,2,1793,'c45S','c45S'),(579,2,1792,'c55S','c55S'),(580,2,1791,'c66S','c66S'),(581,2,1895,'c111P','c111P'),(582,2,1894,'c121P','c121P'),(583,2,1893,'c131P','c131P'),(584,2,1892,'c161P','c161P'),(585,2,1891,'c221P','c221P'),(586,2,1890,'c231P','c231P'),(587,2,1889,'c261P','c261P'),(588,2,1888,'c331P','c331P'),(589,2,1887,'c361P','c361P'),(590,2,1886,'c441P','c441P'),(591,2,1885,'c451P','c451P'),(592,2,1884,'c551P','c551P'),(593,2,1883,'c661P','c661P'),(594,2,1987,'c112P','c112P'),(595,2,1986,'c122P','c122P'),(596,2,1985,'c132P','c132P'),(597,2,1984,'c162P','c162P'),(598,2,1983,'c222P','c222P'),(599,2,1982,'c232P','c232P'),(600,2,1981,'c262P','c262P'),(601,2,1980,'c332P','c332P'),(602,2,1979,'c362P','c362P'),(603,2,1978,'c442P','c442P'),(604,2,1977,'c452P','c452P'),(605,2,1976,'c552P','c552P'),(606,2,1975,'c662P','c662P'),(607,2,2080,'c11S1T','c11S1T'),(608,2,2079,'c12S1T','c12S1T'),(609,2,2078,'c13S1T','c13S1T'),(610,2,2077,'c16S1T','c16S1T'),(611,2,2076,'c22S1T','c22S1T'),(612,2,2075,'c23S1T','c23S1T'),(613,2,2074,'c26S1T','c26S1T'),(614,2,2073,'c33S1T','c33S1T'),(615,2,2072,'c36S1T','c36S1T'),(616,2,2071,'c44S1T','c44S1T'),(617,2,2070,'c45S1T','c45S1T'),(618,2,2069,'c55S1T','c55S1T'),(619,2,2068,'c66S1T','c66S1T'),(620,2,2172,'c11S2T','c11S2T'),(621,2,2171,'c12S2T','c12S2T'),(622,2,2170,'c13S2T','c13S2T'),(623,2,2169,'c16S2T','c16S2T'),(624,2,2168,'c22S2T','c22S2T'),(625,2,2167,'c23S2T','c23S2T'),(626,2,2166,'c26S2T','c26S2T'),(627,2,2165,'c33S2T','c33S2T'),(628,2,2164,'c36S2T','c36S2T'),(629,2,2163,'c44S2T','c44S2T'),(630,2,2162,'c45S2T','c45S2T'),(631,2,2161,'c55S2T','c55S2T'),(632,2,2160,'c66S2T','c66S2T'),(633,2,1515,'c11','c11'),(634,2,1514,'c12','c12'),(635,2,1513,'c13','c13'),(636,2,1512,'c15','c15'),(637,2,1511,'c22','c22'),(638,2,1510,'c23','c23'),(639,2,1509,'c25','c25'),(640,2,1508,'c33','c33'),(641,2,1507,'c35','c35'),(642,2,1506,'c44','c44'),(643,2,3018,'c46','c46'),(644,2,1505,'c55','c55'),(645,2,1504,'c66','c66'),(646,2,1607,'c11D','c11D'),(647,2,1606,'c12D','c12D'),(648,2,1605,'c13D','c13D'),(649,2,1604,'c15D','c15D'),(650,2,1603,'c22D','c22D'),(651,2,1602,'c23D','c23D'),(652,2,1601,'c25D','c25D'),(653,2,1600,'c33D','c33D'),(654,2,1599,'c35D','c35D'),(655,2,1598,'c44D','c44D'),(656,2,1597,'c46D','c46D'),(657,2,1596,'c55D','c55D'),(658,2,1595,'c66D','c66D'),(659,2,1699,'c11E','c11E'),(660,2,1698,'c12E','c12E'),(661,2,1697,'c13E','c13E'),(662,2,1696,'c15E','c15E'),(663,2,1695,'c22E','c22E'),(664,2,1694,'c23E','c23E'),(665,2,1693,'c25E','c25E'),(666,2,1692,'c33E','c33E'),(667,2,1691,'c35E','c35E'),(668,2,1690,'c44E','c44E'),(669,2,1689,'c46E','c46E'),(670,2,1688,'c55E','c55E'),(671,2,1687,'c66E','c66E'),(672,2,1790,'c11S','c11S'),(673,2,1789,'c12S','c12S'),(674,2,1788,'c13S','c13S'),(675,2,1787,'c15S','c15S'),(676,2,1786,'c22S','c22S'),(677,2,1785,'c23S','c23S'),(678,2,1784,'c25S','c25S'),(679,2,1783,'c33S','c33S'),(680,2,1782,'c35S','c35S'),(681,2,1781,'c44S','c44S'),(682,2,1780,'c46S','c46S'),(683,2,1779,'c55S','c55S'),(684,2,1778,'c66S','c66S'),(685,2,1882,'c111P','c111P'),(686,2,1881,'c121P','c121P'),(687,2,1880,'c131P','c131P'),(688,2,1879,'c151P','c151P'),(689,2,1878,'c221P','c221P'),(690,2,1877,'c231P','c231P'),(691,2,1876,'c251P','c251P'),(692,2,1875,'c331P','c331P'),(693,2,1874,'c351P','c351P'),(694,2,1873,'c441P','c441P'),(695,2,1872,'c461P','c461P'),(696,2,1871,'c551P','c551P'),(697,2,1870,'c661P','c661P'),(698,2,1974,'c112P','c112P'),(699,2,1973,'c122P','c122P'),(700,2,1972,'c132P','c132P'),(701,2,1971,'c152P','c152P'),(702,2,1970,'c222P','c222P'),(703,2,1969,'c232P','c232P'),(704,2,1968,'c252P','c252P'),(705,2,1967,'c332P','c332P'),(706,2,1966,'c352P','c352P'),(707,2,1965,'c442P','c442P'),(708,2,1964,'c462P','c462P'),(709,2,1963,'c552P','c552P'),(710,2,1962,'c662P','c662P'),(711,2,2067,'c11S1T','c11S1T'),(712,2,2066,'c12S1T','c12S1T'),(713,2,2065,'c13S1T','c13S1T'),(714,2,2064,'c15S1T','c15S1T'),(715,2,2063,'c22S1T','c22S1T'),(716,2,2062,'c23S1T','c23S1T'),(717,2,2061,'c25S1T','c25S1T'),(718,2,2060,'c33S1T','c33S1T'),(719,2,2059,'c35S1T','c35S1T'),(720,2,2058,'c44S1T','c44S1T'),(721,2,2057,'c46S1T','c46S1T'),(722,2,2056,'c55S1T','c55S1T'),(723,2,2055,'c66S1T','c66S1T'),(724,2,2159,'c11S2T','c11S2T'),(725,2,2158,'c12S2T','c12S2T'),(726,2,2157,'c13S2T','c13S2T'),(727,2,2156,'c15S2T','c15S2T'),(728,2,2155,'c22S2T','c22S2T'),(729,2,2154,'c23S2T','c23S2T'),(730,2,2153,'c25S2T','c25S2T'),(731,2,2152,'c33S2T','c33S2T'),(732,2,2151,'c35S2T','c35S2T'),(733,2,2150,'c44S2T','c44S2T'),(734,2,2149,'c46S2T','c46S2T'),(735,2,2148,'c55S2T','c55S2T'),(736,2,2147,'c66S2T','c66S2T'),(737,2,1537,'c11','c11'),(738,2,1536,'c12','c12'),(739,2,1535,'c13','c13'),(740,2,1534,'c22','c22'),(741,2,1533,'c23','c23'),(742,2,1532,'c33','c33'),(743,2,1531,'c44','c44'),(744,2,1530,'c55','c55'),(745,2,1529,'c66','c66'),(746,2,1629,'c11D','c11D'),(747,2,1628,'c12D','c12D'),(748,2,1627,'c13D','c13D'),(749,2,1626,'c22D','c22D'),(750,2,1625,'c23D','c23D'),(751,2,1624,'c33D','c33D'),(752,2,1623,'c44D','c44D'),(753,2,1622,'c55D','c55D'),(754,2,1621,'c66D','c66D'),(755,2,1720,'c11E','c11E'),(756,2,1719,'c12E','c12E'),(757,2,1718,'c13E','c13E'),(758,2,1717,'c22E','c22E'),(759,2,1716,'c23E','c23E'),(760,2,1715,'c44E','c44E'),(761,2,1714,'c55E','c55E'),(762,2,1713,'c66E','c66E'),(763,2,1812,'c11S','c11S'),(764,2,1811,'c12S','c12S'),(765,2,1810,'c13S','c13S'),(766,2,1809,'c22S','c22S'),(767,2,1808,'c23S','c23S'),(768,2,1807,'c33S','c33S'),(769,2,1806,'c44S','c44S'),(770,2,1805,'c55S','c55S'),(771,2,1804,'c66S','c66S'),(772,2,1904,'c111P','c111P'),(773,2,1903,'c121P','c121P'),(774,2,1902,'c131P','c131P'),(775,2,1901,'c221P','c221P'),(776,2,1900,'c231P','c231P'),(777,2,1899,'c331P','c331P'),(778,2,1898,'c441P','c441P'),(779,2,1897,'c551P','c551P'),(780,2,1896,'c661P','c661P'),(781,2,1996,'c112P','c112P'),(782,2,1995,'c122P','c122P'),(783,2,1994,'c132P','c132P'),(784,2,1993,'c222P','c222P'),(785,2,1992,'c232P','c232P'),(786,2,1991,'c332P','c332P'),(787,2,1990,'c442P','c442P'),(788,2,1989,'c552P','c552P'),(789,2,1988,'c662P','c662P'),(790,2,2089,'c11S1T','c11S1T'),(791,2,2088,'c12S1T','c12S1T'),(792,2,2087,'c13S1T','c13S1T'),(793,2,2086,'c22S1T','c22S1T'),(794,2,2085,'c23S1T','c23S1T'),(795,2,2084,'c33S1T','c33S1T'),(796,2,2083,'c44S1T','c44S1T'),(797,2,2082,'c55S1T','c55S1T'),(798,2,2081,'c66S1T','c66S1T'),(799,2,2181,'c11S2T','c11S2T'),(800,2,2180,'c12S2T','c12S2T'),(801,2,2179,'c13S2T','c13S2T'),(802,2,2178,'c22S2T','c22S2T'),(803,2,2177,'c23S2T','c23S2T'),(804,2,2176,'c33S2T','c33S2T'),(805,2,2175,'c44S2T','c44S2T'),(806,2,2174,'c55S2T','c55S2T'),(807,2,2173,'c66S2T','c66S2T'),(808,2,900,'s11','s11'),(809,2,899,'s12','s12'),(810,2,898,'s13','s13'),(811,2,897,'s22','s22'),(812,2,896,'s23','s23'),(813,2,895,'s33','s33'),(814,2,894,'s44','s44'),(815,2,893,'s55','s55'),(816,2,892,'s66','s66'),(817,2,987,'s11E','s11E'),(818,2,986,'s12E','s12E'),(819,2,985,'s13E','s13E'),(820,2,984,'s22E','s22E'),(821,2,983,'s23E','s23E'),(822,2,982,'s33E','s33E'),(823,2,981,'s44E','s44E'),(824,2,980,'s55E','s55E'),(825,2,979,'s66E','s66E'),(826,2,1079,'s11D','s11D'),(827,2,1078,'s12D','s12D'),(828,2,1077,'s13D','s13D'),(829,2,1076,'s22D','s22D'),(830,2,1075,'s23D','s23D'),(831,2,1074,'s33D','s33D'),(832,2,1073,'s44D','s44D'),(833,2,1072,'s55D','s55D'),(834,2,1071,'s66D','s66D'),(835,2,1171,'s111T','s111T'),(836,2,1170,'s121T','s121T'),(837,2,1169,'s131T','s131T'),(838,2,1168,'s221T','s221T'),(839,2,1167,'s231T','s231T'),(840,2,1166,'s331T','s331T'),(841,2,1165,'s441T','s441T'),(842,2,1164,'s551T','s551T'),(843,2,1163,'s661T','s661T'),(844,2,1262,'s112T','s112T'),(845,2,1261,'s122T','s122T'),(846,2,1260,'s132T','s132T'),(847,2,1259,'s222T','s222T'),(848,2,1258,'s232T','s232T'),(849,2,1257,'s332T','s332T'),(850,2,1256,'s442T','s442T'),(851,2,1255,'s552T','s552T'),(852,2,1254,'s662T','s662T'),(853,2,1354,'s113T','s113T'),(854,2,1353,'s123T','s123T'),(855,2,1352,'s133T','s133T'),(856,2,1351,'s223T','s223T'),(857,2,1350,'s233T','s233T'),(858,2,1349,'s333T','s333T'),(859,2,1348,'s443T','s443T'),(860,2,1347,'s553T','s553T'),(861,2,1346,'s663T','s663T'),(862,2,1446,'s11S','s11S'),(863,2,1445,'s12S','s12S'),(864,2,1444,'s13S','s13S'),(865,2,1443,'s22S','s22S'),(866,2,1442,'s23S','s23S'),(867,2,1441,'s33S','s33S'),(868,2,1440,'s44S','s44S'),(869,2,1439,'s55S','s55S'),(870,2,1438,'s66S','s66S'),(871,2,903,'s11','s22, s33'),(872,2,902,'s12','s13, s23'),(873,2,901,'s44','s55, s66'),(874,2,990,'s11E','s22E, s33E'),(875,2,989,'s12E','s13E, s23E'),(876,2,988,'s44E','s55E, s66E'),(877,2,1082,'s11D','s22D, s33D'),(878,2,1081,'s12D','s13D, s23D'),(879,2,1080,'s44D','s55D, s66D'),(880,2,1173,'s111T','s221T, s331T'),(881,2,1172,'s121T','s131T, s231T'),(882,2,1265,'s112T','s222T, s332T'),(883,2,1264,'s122T','s132T, s232T'),(884,2,1263,'s442T','s552T, s662T'),(885,2,3217,'s441T','s551T, s661T'),(886,2,1357,'s113T','s223T, s333T'),(887,2,1356,'s123T','s133T, s233T'),(888,2,1355,'s443T','s553T, s663T'),(889,2,1449,'s11S','s22S, s33S'),(890,2,1448,'s12S','s13S, s23S'),(891,2,1447,'s44S','s55S, s66S'),(892,2,1540,'c11','c22, c33'),(893,2,1539,'c12','c13, c23'),(894,2,1538,'c44','c55, c66'),(895,2,1632,'c11D','c22D, c33D'),(896,2,1631,'c12D','c13D, c23D'),(897,2,1630,'c44D','c55D, c66D'),(898,2,1723,'c11E','c22E, c33E'),(899,2,1722,'c12E','c13E, c23E'),(900,2,1721,'c44E','c55E, c66E'),(901,2,1815,'c11S','c22S, c33S'),(902,2,1814,'c12S','c13S, c23S'),(903,2,1813,'c44S','c55S, c66S'),(904,2,1907,'c111P','c221P, c331P'),(905,2,1906,'c121P','c131P, c231P'),(906,2,1905,'c441P','c551P, c661P'),(907,2,1999,'c112P','c222P, c332P'),(908,2,1998,'c122P','c132P, c232P'),(909,2,1997,'c442P','c552P, c662P'),(910,2,2092,'c11S1T','c22S1T, c33S1T'),(911,2,2091,'c12S1T','c13S1T, c23S1T'),(912,2,2090,'c44S1T','c55S1T, c66S1T'),(913,2,2184,'c11S2T','c22S2T, c33S2T'),(914,2,2183,'c12S2T','c13S2T, c23S2T'),(915,2,2182,'c44S2T','c55S2T, c66S2T'),(917,3,931,'s11','s22, s33'),(918,3,930,'s12','s13, s23'),(919,7,930,'s11, s12','s44, s55, s66'),(920,7,931,'s11, s12','s44, s55, s66'),(921,3,1018,'s11E','s22E, s33E'),(922,3,1017,'s12E','s13E, s23E'),(923,7,1018,'s11E, s12E','s44E, s55E, s66E'),(924,7,1017,'s11E, s12E','s44E, s55E, s66E'),(925,3,1110,'s11D','s22D, s33D'),(926,3,1109,'s12D','s13D, s23D'),(927,7,1110,'s11D, s12D','s44D, s55D, s66D'),(928,7,1109,'s11D, s12D','s44D, s55D, s66D'),(929,3,1201,'s111T','s221T, s331T'),(930,3,1200,'s121T','s131T, s231T'),(931,7,1201,'s111T, s121T','s441T, s551T, s661T'),(932,7,1200,'s111T, s121T','s441T, s551T, s661T'),(933,3,1293,'s112T','s222T, s332T'),(934,3,1292,'s122T','s132T, s232T'),(935,7,1293,'s112T, s122T','s442T, s552T, s662T'),(936,7,1292,'s112T, s122T','s442T, s552T, s662T'),(937,3,1385,'s113T','s223T, s333T'),(938,3,1384,'s123T','s133T, s233T'),(939,7,1385,'s113T, s123T','s443T, s553T, s663T'),(940,7,1384,'s113T, s123T','s443T, s553T, s663T'),(941,3,1477,'s11S','s22S, s33S'),(942,3,1476,'s12S','s13S, s23S'),(943,7,1477,'s11S, s12S','s44S, s55S, s66S'),(944,7,1476,'s11S, s12S','s44S, s55S, s66S'),(945,3,1568,'c11','c22, c33'),(946,3,1567,'c12','c13, c23'),(947,8,1568,'c11, c12','c44, c55, c66'),(948,8,1567,'c11, c12','c44, c55, c66'),(949,3,1660,'c11D','c22D, c33D'),(950,3,1659,'c12D','c13D, c23D'),(951,8,1660,'c11D, c12D','c44D, c55D, c66D'),(952,8,1659,'c11D, c12D','c44D, c55D, c66D'),(953,3,1751,'c11E','c22E, c33E'),(954,3,1750,'c12E','c13E, c23E'),(955,8,1751,'c11E, c12E','c44E, c55E, c66E'),(956,8,1750,'c11E, c12E','c44E, c55E, c66E'),(957,3,1843,'c11S','c22S, c33S'),(958,3,1842,'c12S','c13S, c23S'),(959,8,1843,'c11S, c12S','c44S, c55S, c66S'),(960,8,1842,'c11S, c12S','c44S, c55S, c66S'),(961,3,1935,'c111P','c221P, c331P'),(962,3,1934,'c121P','c131P, c231P'),(963,8,1935,'c111P, c121P','c441P, c551P, c661P'),(964,8,1934,'c111P, c121P','c441P, c551P, c661P'),(965,3,2028,'c112P','c222P, c332P'),(966,3,2027,'c122P','c132P, c232P'),(967,8,2028,'c112P, c122P','c442P, c552P, c662P'),(968,8,2027,'c112P, c122P','c442P, c552P, c662P'),(969,3,2120,'c11S1T','c22S1T, c33S1T'),(970,3,2119,'c12S1T','c13S1T, c23S1T'),(971,8,2120,'c11S1T, c12S1T','c44S1T, c55S1T, c66S1T'),(972,8,2119,'c11S1T, c12S1T','c44S1T, c55S1T, c66S1T'),(973,3,2212,'c11S2T','c22S2T, c33S2T'),(974,3,2211,'c12S2T','c13S2T, c23S2T'),(975,8,2212,'c11S2T, c12S2T','c44S2T, c55S2T, c66S2T'),(976,8,2211,'c11S2T, c12S2T','c44S2T, c55S2T, c66S2T'),(981,3,1573,'c11','c22'),(982,2,1572,'c12','c12'),(983,8,1573,'c11, c12','c66'),(984,8,1572,'c11, c12','c66'),(985,3,1571,'c13','c23'),(986,2,1570,'c33','c33'),(987,3,1569,'c44','c55'),(988,3,1665,'c11D','c22D'),(989,2,1664,'c12D','c12D'),(990,8,1665,'c11D, c12D','c66D'),(991,8,1664,'c11D, c12D','c66D'),(992,3,1663,'c13D','c23D'),(993,2,1662,'c33D','c33D'),(994,3,1661,'c44D','c55D'),(995,3,1756,'c11E','c22E'),(996,2,1755,'c12E','c12E'),(997,8,1756,'c11E, c12E','c66E'),(998,8,1755,'c11E, c12E','c66E'),(999,3,1754,'c13E','c23E'),(1000,2,1753,'c33E','c33E'),(1001,3,1752,'c44E','c55E'),(1002,3,1848,'c11S','c22S'),(1003,2,1847,'c12S','c12S'),(1004,8,1848,'c11S, c12S','c66S'),(1005,8,1847,'c11S, c12S','c66S'),(1006,3,1846,'c13S','c23S'),(1007,2,1845,'c33S','c33S'),(1008,3,1844,'c44S','c55S'),(1009,3,1940,'c111P','c221P'),(1010,2,1939,'c121P','c121P'),(1011,8,1940,'c111P, c121P','c661P'),(1012,8,1939,'c111P, c121P','c661P'),(1013,3,1938,'c131P','c231P'),(1014,2,1937,'c331P','c331P'),(1015,3,1936,'c441P','c551P'),(1016,3,2033,'c112P','c222P'),(1017,2,2032,'c122P','c122P'),(1018,8,2033,'c112P, c122P','c662P'),(1019,8,2032,'c112P, c122P','c662P'),(1020,3,2031,'c132P','c232P'),(1021,2,2030,'c332P','c332P'),(1022,3,2029,'c442P','c552P'),(1023,3,2125,'c11S1T','c22S1T'),(1024,2,2124,'c12S1T','c12S1T'),(1025,8,2125,'c11S1T, c12S1T','c66S1T'),(1026,8,2124,'c11S1T, c12S1T','c66S1T'),(1027,3,2123,'c13S1T','c23S1T'),(1028,2,2122,'c33S1T','c33S1T'),(1029,3,2121,'c44S1T','c55S1T'),(1030,3,2217,'c11S2T','c22S2T'),(1031,2,2216,'c12S2T','c12S2T'),(1032,8,2217,'c11S2T, c12S2T','c66S2T'),(1033,8,2216,'c11S2T, c12S2T','c66S2T'),(1034,3,2215,'c13S2T','c23S2T'),(1035,2,2214,'c33S2T','c33S2T'),(1036,3,2213,'c44S2T','c55S2T'),(1037,3,3006,'s11','s22'),(1038,2,3005,'s12','s12'),(1039,7,3006,'s11, s12','s66'),(1040,7,3005,'s11, s12','s66'),(1041,3,3004,'s13','s23'),(1042,2,3003,'s33','s33'),(1043,3,3002,'s44','s55'),(1044,3,1023,'s11E','s22E'),(1045,2,1022,'s12E','s12E'),(1046,7,1023,'s11E, s12E','s66E'),(1047,7,1022,'s11E, s12E','s66E'),(1048,3,1021,'s13E','s23E'),(1049,2,1020,'s33E','s33E'),(1050,3,1019,'s44E','s55E'),(1051,3,1115,'s11D','s22D'),(1052,2,1114,'s12D','s12D'),(1053,7,1115,'s11D, s12D','s66D'),(1054,7,1114,'s11D, s12D','s66D'),(1055,3,1113,'s13D','s23D'),(1056,2,1112,'s33D','s33D'),(1057,3,1111,'s44D','s55D'),(1058,3,1206,'s111T','s221T'),(1059,2,1205,'s121T','s121T'),(1060,7,1206,'s111T, s121T','s661T'),(1061,7,1205,'s111T, s121T','s661T'),(1062,3,1204,'s131T','s231T'),(1063,2,1203,'s331T','s331T'),(1064,3,1202,'s441T','s551T'),(1065,3,1298,'s112T','s222T'),(1066,2,1297,'s122T','s122T'),(1067,7,1298,'s112T, s122T','s662T'),(1068,7,1297,'s112T, s122T','s662T'),(1069,3,1296,'s132T','s232T'),(1070,2,1295,'s332T','s332T'),(1071,3,1294,'s442T','s552T'),(1072,3,1390,'s113T','s223T'),(1073,2,1389,'s123T','s123T'),(1074,7,1390,'s113T, s123T','s663T'),(1075,7,1389,'s113T, s123T','s663T'),(1076,3,1388,'s133T','s233T'),(1077,2,1387,'s333T','s333T'),(1078,3,1386,'s443T','s553T'),(1079,3,1482,'s11S','s22S'),(1080,2,1481,'s12S','s12S'),(1081,7,1482,'s11S, s12S','s66S'),(1082,7,1481,'s11S, s12S','s66S'),(1083,3,1480,'s13S','s23S'),(1084,2,1479,'s33S','s33S'),(1085,3,1478,'s44S','s55S'),(1086,3,1469,'s11S','s22S'),(1087,2,1468,'s12S','s12S'),(1088,7,1469,'s11S, s12S','s66S'),(1089,7,1468,'s11S, s12S','s66S'),(1090,3,1467,'s13S','s23S'),(1091,5,1466,'s14S','s24S, s56S'),(1092,5,1465,'s25S','s15S, s46S'),(1093,2,1464,'s33S','s33S'),(1094,3,1463,'s44S','s55S'),(1095,3,923,'s11','s22'),(1096,2,922,'s12','s12'),(1097,7,923,'s11, s12','s66'),(1098,7,922,'s11, s12','s66'),(1099,3,921,'s13','s23'),(1100,5,920,'s14','s24, s56'),(1101,5,919,'s25','s15, s46'),(1102,2,918,'s33','s33'),(1103,3,917,'s44','s55'),(1104,3,1010,'s11E','s22E'),(1105,2,1009,'s12E','s12E'),(1106,7,1010,'s11E, s12E','s66E'),(1107,7,1009,'s11E, s12E','s66E'),(1108,3,1008,'s13E','s23E'),(1109,5,1007,'s14E','s24E, s56E'),(1110,5,1006,'s25E','s15E, s46E'),(1111,2,1005,'s33E','s33E'),(1112,3,1004,'s44E','s55E'),(1113,3,1102,'s11D','s22D'),(1114,2,1101,'s12D','s12D'),(1115,7,1102,'s11D, s12D','s66D'),(1116,7,1101,'s11D, s12D','s66D'),(1117,3,1100,'s13D','s23D'),(1118,5,1099,'s14D','s24D, s56D'),(1119,5,1098,'s25D','s15D, s46D'),(1120,2,1097,'s33D','s33D'),(1121,3,1096,'s44D','s55D'),(1122,3,1193,'s111T','s221T'),(1123,2,1192,'s121T','s121T'),(1124,7,1193,'s111T, s121T','s661T'),(1125,7,1192,'s111T, s121T','s661T'),(1126,3,1191,'s131T','s231T'),(1127,5,1190,'s141T','s241T, s561T'),(1128,5,1189,'s251T','s151T, s461T'),(1129,2,1188,'s331T','s331T'),(1130,3,1187,'s441T','s551T'),(1131,3,1285,'s112T','s222T'),(1132,2,1284,'s122T','s122T'),(1133,7,1285,'s112T, s122T','s662T'),(1134,7,1284,'s112T, s122T','s662T'),(1135,3,1283,'s132T','s232T'),(1136,5,1282,'s142T','s242T, s562T'),(1137,5,1281,'s252T','s152T, s462T'),(1138,2,1280,'s332T','s332T'),(1139,3,1279,'s442T','s552T'),(1140,3,1377,'s113T','s223T'),(1141,2,1376,'s123T','s123T'),(1142,7,1377,'s113T, s123T','s663T'),(1143,7,1376,'s113T, s123T','s663T'),(1144,3,1375,'s133T','s233T'),(1145,5,1374,'s143T','s243T, s563T'),(1146,5,1373,'s253T','s153T, s463T'),(1147,2,1372,'s333T','s333T'),(1148,3,1371,'s443T','s553T'),(1149,3,1560,'c11','c22'),(1150,2,1559,'c12','c12'),(1151,8,1560,'c11, c12','c66'),(1152,8,1559,'c11, c12','c66'),(1153,3,1558,'c13','c23'),(1154,6,1557,'c14','c24, c56'),(1155,6,1556,'c25','c15, c46'),(1156,2,1555,'c33','c33'),(1157,3,1554,'c44','c55'),(1158,3,1652,'c11D','c22D'),(1159,2,1651,'c12D','c12D'),(1160,8,1652,'c11D, c12D','c66D'),(1161,8,1651,'c11D, c12D','c66D'),(1162,3,1650,'c13D','c23D'),(1163,6,1649,'c14D','c24D, c56D'),(1164,6,1648,'c25D','c15D, c46D'),(1165,2,1647,'c33D','c33D'),(1166,3,1646,'c44D','c55D'),(1167,3,1743,'c11E','c22E'),(1168,2,1742,'c12E','c12E'),(1169,8,1743,'c11E, c12E','c66E'),(1170,8,1742,'c11E, c12E','c66E'),(1171,3,1741,'c13E','c23E'),(1172,6,1740,'c14E','c24E, c56E'),(1173,6,1739,'c25E','c15E, c46E'),(1174,2,1738,'c33E','c33E'),(1175,3,1737,'c44E','c55E'),(1176,3,1835,'c11S','c22S'),(1177,2,1834,'c12S','c12S'),(1178,8,1835,'c11S, c12S','c66S'),(1179,8,1834,'c11S, c12S','c66S'),(1180,3,1833,'c13S','c23S'),(1181,6,1832,'c14S','c24S, c56S'),(1182,6,1831,'c25S','c15S, c46S'),(1183,2,1830,'c33S','c33S'),(1184,3,1829,'c44S','c55S'),(1185,3,1927,'c111P','c221P'),(1186,2,1926,'c121P','c121P'),(1187,8,1927,'c111P, c121P','c661P'),(1188,8,1926,'c111P, c121P','c661P'),(1189,3,1925,'c131P','c231P'),(1190,6,1924,'c141P','c241P, c561P'),(1191,6,1923,'c251P','c151P, c461P'),(1192,2,1922,'c331P','c331P'),(1193,3,1921,'c441P','c551P'),(1194,3,2026,'c112P','c222P'),(1195,2,2025,'c122P','c122P'),(1196,8,2026,'c112P, c122P','c662P'),(1197,8,2025,'c112P, c122P','c662P'),(1198,3,2024,'c132P','c232P'),(1199,6,2023,'c142P','c242P, c562P'),(1200,6,2022,'c252P','c152P, c462P'),(1201,2,2021,'c332P','c332P'),(1202,3,2020,'c442P','c552P'),(1203,3,2112,'c11S1T','c22S1T'),(1204,2,2111,'c12S1T','c12S1T'),(1205,8,2112,'c11S1T, c12S1T','c66S1T'),(1206,8,2111,'c11S1T, c12S1T','c66S1T'),(1207,3,2110,'c13S1T','c23S1T'),(1208,6,2109,'c14S1T','c24S1T, c56S1T'),(1209,6,2108,'c25S1T','c15S1T, c46S1T'),(1210,2,2107,'c33S1T','c33S1T'),(1211,3,2106,'c44S1T','c55S1T'),(1212,3,2204,'c11S2T','c22S2T'),(1213,2,2203,'c12S2T','c12S2T'),(1214,8,2204,'c11S2T, c12S2T','c66S2T'),(1215,8,2203,'c11S2T, c12S2T','c66S2T'),(1216,3,2202,'c13S2T','c23S2T'),(1217,6,2201,'c14S2T','c24S2T, c56S2T'),(1218,6,2200,'c25S2T','c15S2T, c46S2T'),(1219,2,2199,'c33S2T','c33S2T'),(1220,3,2198,'c44S2T','c55S2T'),(1221,3,1566,'c11','c22'),(1222,2,1565,'c12','c12'),(1223,8,1566,'c11, c12','c66'),(1224,8,1565,'c11, c12','c66'),(1225,3,1564,'c13','c23'),(1226,6,1563,'c14','c24, c56'),(1227,2,1562,'c33','c33'),(1228,3,1561,'c44','c55'),(1229,3,1658,'c11D','c22D'),(1230,2,1657,'c12D','c12D'),(1231,8,1658,'c11D, c12D','c66D'),(1232,8,1657,'c11D, c12D','c66D'),(1233,3,1656,'c13D','c23D'),(1234,6,1655,'c14D','c24D, c56D'),(1235,2,1654,'c33D','c33D'),(1236,3,1653,'c44D','c55D'),(1237,3,1749,'c11E','c22E'),(1238,2,1748,'c12E','c12E'),(1239,8,1749,'c11E, c12E','c66E'),(1240,8,1748,'c11E, c12E','c66E'),(1241,3,1747,'c13E','c23E'),(1242,6,1746,'c14E','c24E, c56E'),(1243,2,1745,'c33E','c33E'),(1244,3,1744,'c44E','c55E'),(1245,3,1841,'c11S','c22S'),(1246,2,1840,'c12S','c12S'),(1247,8,1841,'c11S, c12S','c66S'),(1248,8,1840,'c11S, c12S','c66S'),(1249,3,1839,'c13S','c23S'),(1250,6,1838,'c14S','c24S, c56S'),(1251,2,1837,'c33S','c33S'),(1252,3,1836,'c44S','c55S'),(1253,3,1933,'c111P','c221P'),(1254,2,1932,'c121P','c121P'),(1255,8,1933,'c111P, c121P','c661P'),(1256,8,1932,'c111P, c121P','c661P'),(1257,3,1931,'c131P','c231P'),(1258,6,1930,'c141P','c241P, c561P'),(1259,2,1929,'c331P','c331P'),(1260,3,1928,'c441P','c551P'),(1261,3,2019,'c112P','c222P'),(1262,2,2018,'c122P','c122P'),(1263,8,2019,'c112P, c122P','c662P'),(1264,8,2018,'c112P, c122P','c662P'),(1265,3,2017,'c132P','c232P'),(1266,6,2016,'c142P','c242P, c562P'),(1267,2,2014,'c332P','c332P'),(1268,3,2013,'c442P','c552P'),(1269,3,2118,'c11S1T','c22S1T'),(1270,2,2117,'c12S1T','c12S1T'),(1271,8,2118,'c11S1T, c12S1T','c66S1T'),(1272,8,2117,'c11S1T, c12S1T','c66S1T'),(1273,3,2116,'c13S1T','c23S1T'),(1274,6,2115,'c14S1T','c24S1T, c56S1T'),(1275,2,2114,'c33S1T','c33S1T'),(1276,3,2113,'c44S1T','c55S1T'),(1277,3,2210,'c11S2T','c22S2T'),(1278,2,2209,'c12S2T','c12S2T'),(1279,8,2210,'c11S2T, c12S2T','c66S2T'),(1280,8,2209,'c11S2T, c12S2T','c66S2T'),(1281,3,2208,'c13S2T','c23S2T'),(1282,6,2207,'c14S2T','c24S2T, c56S2T'),(1283,2,2206,'c33S2T','c33S2T'),(1284,3,2205,'c44S2T','c55S2T'),(1285,3,2191,'c11S2T','c22S2T'),(1286,2,2190,'c12S2T','c12S2T'),(1287,3,2189,'c13S2T','c23S2T'),(1288,4,2188,'c16S2T','c26S2T'),(1289,2,2187,'c33S2T','c33S2T'),(1290,3,2186,'c44S2T','c55S2T'),(1291,2,2185,'c66S2T','c66S2T'),(1292,3,1547,'c11','c22'),(1293,2,1546,'c12','c12'),(1294,3,1545,'c13','c23'),(1295,4,1544,'c16','c26'),(1296,2,1543,'c33','c33'),(1297,3,1542,'c44','c55'),(1298,2,1541,'c66','c66'),(1299,3,1639,'c11D','c22D'),(1300,2,1638,'c12D','c12D'),(1301,3,1637,'c13D','c23D'),(1302,4,1636,'c16D','c26D'),(1303,2,1635,'c33D','c33D'),(1304,3,1634,'c44D','c55D'),(1305,2,1633,'c66D','c66D'),(1306,3,1730,'c11E','c22E'),(1307,2,1729,'c12E','c12E'),(1308,3,1728,'c13E','c23E'),(1309,4,1727,'c16E','c26E'),(1310,2,1726,'c33E','c33E'),(1311,3,1725,'c44E','c55E'),(1312,2,1724,'c66E','c66E'),(1313,3,1822,'c11S','c22S'),(1314,2,1821,'c12S','c12S'),(1315,3,1820,'c13S','c23S'),(1316,4,1819,'c16S','c26S'),(1317,2,1818,'c33S','c33S'),(1318,3,1817,'c44S','c55S'),(1319,2,1816,'c66S','c66S'),(1320,3,2006,'c112P','c222P'),(1321,2,2005,'c122P','c122P'),(1322,3,2004,'c132P','c232P'),(1323,4,2003,'c162P','c262P'),(1324,2,2002,'c332P','c332P'),(1325,3,2001,'c442P','c552P'),(1326,2,2000,'c662P','c662P'),(1327,3,1914,'c111P','c221P'),(1328,2,1913,'c121P','c121P'),(1329,3,1912,'c131P','c231P'),(1330,4,1911,'c161P','c261P'),(1331,2,1910,'c331P','c331P'),(1332,3,1909,'c441P','c551P'),(1333,2,1908,'c661P','c661P'),(1334,3,2099,'c11S1T','c22S1T'),(1335,2,2098,'c12S1T','c12S1T'),(1336,3,2097,'c13S1T','c23S1T'),(1337,4,2096,'c16S1T','c26S1T'),(1338,2,2095,'c33S1T','c33S1T'),(1339,3,2094,'c44S1T','c55S1T'),(1340,2,2093,'c66S1T','c66S1T'),(1341,3,1553,'c11','c22'),(1342,2,1552,'c12','c12'),(1343,3,1551,'c13','c23'),(1344,2,1550,'c33','c33'),(1345,3,1549,'c44','c55'),(1346,2,1548,'c66','c66'),(1347,3,1645,'c11D','c22D'),(1348,2,1644,'c12D','c12D'),(1349,3,1643,'c13D','c23D'),(1350,2,1642,'c33D','c33D'),(1351,3,1641,'c44D','c55D'),(1352,2,1640,'c66D','c66D'),(1353,3,1736,'c11E','c22E'),(1354,2,1735,'c12E','c12E'),(1355,3,1734,'c13E','c23E'),(1356,2,1733,'c33E','c33E'),(1357,3,1732,'c44E','c55E'),(1358,2,1731,'c66E','c66E'),(1359,3,1828,'c11S','c22S'),(1360,2,1827,'c12S','c12S'),(1361,3,1826,'c13S','c23S'),(1362,2,1825,'c33S','c33S'),(1363,3,1824,'c44S','c55S'),(1364,2,1823,'c66S','c66S'),(1365,3,1920,'c111P','c221P'),(1366,2,1919,'c121P','c121P'),(1367,3,1918,'c131P','c231P'),(1368,2,1917,'c331P','c331P'),(1369,3,1916,'c441P','c551P'),(1370,2,1915,'c661P','c661P'),(1371,3,2012,'c112P','c222P'),(1372,2,2011,'c122P','c122P'),(1373,3,2010,'c132P','c232P'),(1374,2,2009,'c332P','c332P'),(1375,3,2008,'c442P','c552P'),(1376,2,2007,'c662P','c662P'),(1377,3,2105,'c11S1T','c22S1T'),(1378,2,2104,'c12S1T','c12S1T'),(1379,3,2103,'c13S1T','c23S1T'),(1380,2,2102,'c33S1T','c33S1T'),(1381,3,2101,'c44S1T','c55S1T'),(1382,2,2100,'c66S1T','c66S1T'),(1383,3,2197,'c11S2T','c22S2T'),(1384,2,2196,'c12S2T','c12S2T'),(1385,3,2195,'c13S2T','c23S2T'),(1386,2,2194,'c33S2T','c33S2T'),(1387,3,2193,'c44S2T','c55S2T'),(1388,2,2192,'c66S2T','c66S2T'),(1389,3,916,'s11','s22'),(1390,2,915,'s12','s12'),(1391,3,914,'s13','s23'),(1392,2,913,'s33','s33'),(1393,3,912,'s44','s55'),(1394,2,911,'s66','s66'),(1395,3,1003,'s11E','s22E'),(1396,2,1002,'s12E','s12E'),(1397,3,1001,'s13E','s23E'),(1398,2,1000,'s33E','s33E'),(1399,3,999,'s44E','s55E'),(1400,2,998,'s66E','s66E'),(1401,3,1095,'s11D','s22D'),(1402,2,1094,'s12D','s12D'),(1403,3,1093,'s13D','s23D'),(1404,2,1092,'s33D','s33D'),(1405,3,1091,'s44D','s55D'),(1406,2,1090,'s66D','s66D'),(1407,3,1186,'s111T','s221T'),(1408,2,1185,'s121T','s121T'),(1409,3,1184,'s131T','s231T'),(1410,2,1183,'s331T','s331T'),(1411,3,1182,'s441T','s551T'),(1412,2,1181,'s661T','s661T'),(1413,3,1278,'s112T','s222T'),(1414,2,1277,'s122T','s122T'),(1415,3,1276,'s132T','s232T'),(1416,2,1275,'s332T','s332T'),(1417,3,1274,'s442T','s552T'),(1418,2,1273,'s662T','s662T'),(1419,3,1370,'s113T','s223T'),(1420,2,1369,'s123T','s123T'),(1421,3,1368,'s133T','s233T'),(1422,2,1367,'s333T','s333T'),(1423,3,1366,'s443T','s553T'),(1424,2,1365,'s663T','s663T'),(1425,3,1462,'s11S','s22S'),(1426,2,1461,'s12S','s12S'),(1427,3,1460,'s13S','s23S'),(1428,2,1459,'s33S','s33S'),(1429,3,1458,'s44S','s55S'),(1430,2,1457,'s66S','s66S'),(1431,3,1456,'s11S','s22S'),(1432,2,1455,'s12S','s12S'),(1433,3,1454,'s13S','s23S'),(1434,4,1453,'s16S','s26S'),(1435,2,1452,'s33S','s33S'),(1436,3,1451,'s44S','s55S'),(1437,2,1450,'s66S','s66S'),(1438,3,1089,'s11D','s22D'),(1439,2,1088,'s12D','s12D'),(1440,3,1087,'s13D','s23D'),(1441,4,1086,'s16D','s26D'),(1442,2,1085,'s33D','s33D'),(1443,3,1084,'s44D','s55D'),(1444,2,1083,'s66D','s66D'),(1445,3,929,'s11','s22'),(1446,2,928,'s12','s12'),(1447,7,929,'s11, s12','s66'),(1448,7,928,'s11, s12','s66'),(1449,3,927,'s13','s23'),(1450,5,926,'s14','s24, s56'),(1451,2,925,'s33','s33'),(1452,3,924,'s44','s55'),(1453,3,1016,'s11E','s22E'),(1454,2,1015,'s12E','s12E'),(1455,7,1016,'s11E, s12E','s66E'),(1456,7,1015,'s11E, s12E','s66E'),(1457,3,1014,'s13E','s23E'),(1458,5,1013,'s14E','s24E, s56E'),(1459,2,1012,'s33E','s33E'),(1460,3,1011,'s44E','s55E'),(1461,3,1108,'s11D','s22D'),(1462,2,1107,'s12D','s12D'),(1463,7,1108,'s11D, s12D','s66D'),(1464,7,1107,'s11D, s12D','s66D'),(1465,3,1106,'s13D','s23D'),(1466,5,1105,'s14D','s24D, s56D'),(1467,2,1104,'s33D','s33D'),(1468,3,1103,'s44D','s55D'),(1469,3,1199,'s111T','s221T'),(1470,2,1198,'s121T','s121T'),(1471,7,1199,'s111T, s121T','s661T'),(1472,7,1198,'s111T, s121T','s661T'),(1473,3,1197,'s131T','s231T'),(1474,5,1196,'s141T','s241T, s561T'),(1475,2,1195,'s331T','s331T'),(1476,3,1194,'s441T','s551T'),(1477,3,1291,'s112T','s222T'),(1478,2,1290,'s122T','s122T'),(1479,7,1291,'s112T, s122T','s662T'),(1480,7,1290,'s112T, s122T','s662T'),(1481,3,1289,'s132T','s232T'),(1482,5,1288,'s142T','s242T, s562T'),(1483,2,1287,'s332T','s332T'),(1484,3,1286,'s442T','s552T'),(1485,3,1383,'s113T','s223T'),(1486,2,1382,'s123T','s123T'),(1487,7,1383,'s113T, s123T','s663T'),(1488,7,1382,'s113T, s123T','s663T'),(1489,3,1381,'s133T','s233T'),(1490,5,1380,'s143T','s243T, s563T'),(1491,2,1379,'s333T','s333T'),(1492,3,1378,'s443T','s553T'),(1493,3,1475,'s11S','s22S'),(1494,2,1474,'s12S','s12S'),(1495,7,1475,'s11S, s12S','s66S'),(1496,7,1474,'s11S, s12S','s66S'),(1497,3,1473,'s13S','s23S'),(1498,5,1472,'s14S','s24S, s56S'),(1499,2,1471,'s33S','s33S'),(1500,3,1470,'s44S','s55S'),(1501,3,997,'s11E','s22E'),(1502,2,996,'s12E','s12E'),(1503,3,995,'s13E','s23E'),(1504,4,994,'s16E','s26E'),(1505,2,993,'s33E','s33E'),(1506,3,992,'s44E','s55E'),(1507,2,991,'s66E','s66E'),(1508,3,910,'s11','s22'),(1509,2,909,'s12','s12'),(1510,3,908,'s13','s23'),(1511,4,907,'s16','s26'),(1512,2,906,'s33','s33'),(1513,3,905,'s44','s55'),(1514,2,904,'s66','s66'),(1515,2,2354,'e11','e11'),(1516,2,2355,'e12','e12'),(1517,2,2356,'e13','e13'),(1518,2,2357,'e14','e14'),(1519,2,2358,'e15','e15'),(1520,2,2359,'e16','e16'),(1521,2,2360,'e21','e21'),(1522,2,2362,'e22','e22'),(1523,2,2361,'e23','e23'),(1524,2,2363,'e24','e24'),(1525,2,2364,'e25','e25'),(1526,2,2365,'e26','e26'),(1527,2,2366,'e31','e31'),(1528,2,2367,'e32','e32'),(1529,2,2368,'e33','e33'),(1530,2,2369,'e34','e34'),(1531,2,2371,'e35','e35'),(1532,2,2370,'e36','e36'),(1533,2,2235,'d11','d11'),(1534,2,2234,'d12','d12'),(1535,2,2233,'d13','d13'),(1536,2,2232,'d14','d14'),(1537,2,2231,'d15','d15'),(1538,2,2230,'d16','d16'),(1539,2,2229,'d21','d21'),(1540,2,2228,'d22','d22'),(1541,2,2227,'d23','d23'),(1542,2,2226,'d24','d24'),(1543,2,2225,'d25','d25'),(1544,2,2224,'d26','d26'),(1545,2,2223,'d31','d31'),(1546,2,2222,'d32','d32'),(1547,2,2221,'d33','d33'),(1548,2,2220,'d34','d34'),(1549,2,2218,'d35','d35'),(1550,2,2219,'d36','d36'),(1551,2,2431,'g11','g11'),(1552,2,2432,'g12','g12'),(1553,2,2433,'g13','g13'),(1554,2,2434,'g14','g14'),(1555,2,2435,'g15','g15'),(1556,2,2436,'g16','g16'),(1557,2,2437,'g21','g21'),(1558,2,2439,'g22','g22'),(1559,2,2438,'g23','g23'),(1560,2,2440,'g24','g24'),(1561,2,2441,'g25','g25'),(1562,2,2442,'g26','g26'),(1563,2,2443,'g31','g31'),(1564,2,2444,'g32','g32'),(1565,2,2445,'g33','g33'),(1566,2,2446,'g34','g34'),(1567,2,2448,'g35','g35'),(1568,2,2447,'g36','g36'),(1569,2,2508,'h11','h11'),(1570,2,2509,'h12','h12'),(1571,2,2510,'h13','h13'),(1572,2,2511,'h14','h14'),(1573,2,2512,'h15','h15'),(1574,2,2513,'h16','h16'),(1575,2,2514,'h21','h21'),(1576,2,2516,'h22','h22'),(1577,2,2515,'h23','h23'),(1578,2,2517,'h24','h24'),(1579,2,2518,'h25','h25'),(1580,2,2519,'h26','h26'),(1581,2,2520,'h31','h31'),(1582,2,2521,'h32','h32'),(1583,2,2522,'h33','h33'),(1584,2,2523,'h34','h34'),(1585,2,2525,'h35','h35'),(1586,2,2524,'h36','h36'),(1587,2,2585,'k11','k11'),(1588,2,2586,'k12','k12'),(1589,2,2587,'k13','k13'),(1590,2,2588,'k14','k14'),(1591,2,2589,'k15','k15'),(1592,2,2590,'k16','k16'),(1593,2,2591,'k21','k21'),(1594,2,2593,'k22','k22'),(1595,2,2592,'k23','k23'),(1596,2,2594,'k24','k24'),(1597,2,2595,'k25','k25'),(1598,2,2596,'k26','k26'),(1599,2,2597,'k31','k31'),(1600,2,2598,'k32','k32'),(1601,2,2599,'k33','k33'),(1602,2,2600,'k34','k34'),(1603,2,2602,'k35','k35'),(1604,2,2601,'k36','k36'),(1605,2,2569,'k14','k14'),(1606,2,2570,'k16','k16'),(1607,2,2571,'k21','k21'),(1608,2,2572,'k22','k22'),(1609,2,2573,'k23','k23'),(1610,2,2574,'k25','k25'),(1611,2,2575,'k34','k34'),(1612,2,2576,'k36','k36'),(1613,2,2577,'k14','k14'),(1614,2,2578,'k15','k15'),(1615,2,2579,'k24','k24'),(1616,2,2580,'k25','k25'),(1617,2,2581,'k31','k31'),(1618,2,2582,'k32','k32'),(1619,2,2583,'k33','k33'),(1620,2,2584,'k36','k36'),(1621,2,2549,'k11','k11'),(1622,2,2550,'k12','k12'),(1623,2,2551,'k13','k13'),(1624,2,2552,'k16','k16'),(1625,2,2553,'k21','k21'),(1626,2,2554,'k22','k22'),(1627,2,2555,'k23','k23'),(1628,2,2556,'k26','k26'),(1629,2,2557,'k34','k34'),(1630,2,2558,'k35','k35'),(1631,2,2559,'k11','k11'),(1632,2,2560,'k12','k12'),(1633,2,2561,'k13','k13'),(1634,2,2562,'k15','k15'),(1635,2,2563,'k24','k24'),(1636,2,2564,'k26','k26'),(1637,2,2565,'k31','k31'),(1638,2,2566,'k32','k32'),(1639,2,2567,'k33','k33'),(1640,2,2568,'k35','k35'),(1641,2,2540,'k14','k14'),(1642,2,2542,'k25','k25'),(1643,2,2543,'k36','k36'),(1644,2,3069,'k15','k15'),(1645,2,3070,'k24','k24'),(1646,2,3071,'k31','k31'),(1647,2,3080,'k32','k32'),(1648,2,3081,'k33','k33'),(1649,2,2251,'d14','d14'),(1650,2,2250,'d16','d16'),(1651,2,2249,'d21','d21'),(1652,2,2248,'d22','d22'),(1653,2,2247,'d23','d23'),(1654,2,2246,'d25','d25'),(1655,2,2245,'d34','d34'),(1656,2,2244,'d36','d36'),(1657,2,2415,'g14','g14'),(1658,2,2416,'g16','g16'),(1659,2,2417,'g21','g21'),(1660,2,2418,'g22','g22'),(1661,2,2419,'g23','g23'),(1662,2,2420,'g25','g25'),(1663,2,2421,'g34','g34'),(1664,2,2422,'g36','g36'),(1665,2,3233,'e14','e14'),(1666,2,3232,'e16','e16'),(1667,2,3231,'e21','e21'),(1668,2,3230,'e22','e22'),(1669,2,3229,'e23','e23'),(1670,2,3228,'e25','e25'),(1671,2,3227,'e34','e34'),(1672,2,3226,'e36','e36'),(1673,2,3241,'e14','e14'),(1674,2,3240,'e16','e16'),(1675,2,3239,'e21','e21'),(1676,2,3238,'e22','e22'),(1677,2,3237,'e23','e23'),(1678,2,3236,'e25','e25'),(1679,2,3235,'e34','e34'),(1680,2,3234,'e36','e36'),(1681,2,3249,'h14','h14'),(1682,2,3248,'h16','h16'),(1683,2,3247,'h21','h21'),(1684,2,3246,'h22','h22'),(1685,2,3245,'h23','h23'),(1686,2,3244,'h25','h25'),(1687,2,3243,'h34','h34'),(1688,2,3242,'h36','h36'),(1689,2,3257,'h14','h14'),(1690,2,3256,'h16','h16'),(1691,2,3255,'h21','h21'),(1692,2,3254,'h22','h22'),(1693,2,3253,'h23','h23'),(1694,2,3252,'h25','h25'),(1695,2,3251,'h34','h34'),(1696,2,3250,'h36','h36'),(1697,2,2243,'d14','d14'),(1698,2,2242,'d15','d15'),(1699,2,2241,'d24','d24'),(1700,2,2240,'d25','d25'),(1701,2,2239,'d31','d31'),(1702,2,2238,'d32','d32'),(1703,2,2237,'d33','d33'),(1704,2,2236,'d36','d36'),(1705,2,2423,'g14','g14'),(1706,2,2424,'g15','g15'),(1707,2,2425,'g24','g24'),(1708,2,2426,'g25','g25'),(1709,2,2427,'g31','g31'),(1710,2,2428,'g32','g32'),(1711,2,2429,'g33','g33'),(1712,2,2430,'g36','g36'),(1713,2,2405,'g11','g11'),(1714,2,2406,'g12','g12'),(1715,2,2407,'g13','g13'),(1716,2,2408,'g15','g15'),(1717,2,2409,'g24','g24'),(1718,2,2410,'g26','g26'),(1719,2,2411,'g31','g31'),(1720,2,2412,'g32','g32'),(1721,2,2413,'g33','g33'),(1722,2,2414,'g35','g35'),(1723,2,2395,'g11','g11'),(1724,2,2396,'g12','g12'),(1725,2,2397,'g13','g13'),(1726,2,2398,'g16','g16'),(1727,2,2399,'g21','g21'),(1728,2,2400,'g22','g22'),(1729,2,2401,'g23','g23'),(1730,2,2402,'g26','g26'),(1731,2,2403,'g34','g34'),(1732,2,2404,'g35','g35'),(1733,2,2261,'d11','d11'),(1734,2,2260,'d12','d12'),(1735,2,2329,'d12','d12'),(1736,2,2259,'d13','d13'),(1737,2,2258,'d15','d15'),(1738,2,2257,'d24','d24'),(1739,2,2256,'d26','d26'),(1740,2,2255,'d31','d31'),(1741,2,2254,'d32','d32'),(1742,2,2253,'d33','d33'),(1743,2,2252,'d35','d35'),(1744,2,2271,'d11','d11'),(1745,2,2270,'d12','d12'),(1746,2,2269,'d13','d13'),(1747,2,2268,'d16','d16'),(1748,2,2267,'d21','d21'),(1749,2,2266,'d22','d22'),(1750,2,2265,'d23','d23'),(1751,2,2264,'d26','d26'),(1752,2,2263,'d34','d34'),(1753,2,2262,'d35','d35'),(1754,2,2318,'e11','e11'),(1755,2,2319,'e12','e12'),(1756,2,2320,'e13','e13'),(1757,2,2321,'e16','e16'),(1758,2,2322,'e21','e21'),(1759,2,2323,'e22','e22'),(1760,2,2324,'e23','e23'),(1761,2,2325,'e26','e26'),(1762,2,2326,'e34','e34'),(1763,2,2327,'e35','e35'),(1764,2,2346,'e14','e14'),(1765,2,2347,'e15','e15'),(1766,2,2348,'e24','e24'),(1767,2,2349,'e25','e25'),(1768,2,2350,'e31','e31'),(1769,2,2351,'e32','e32'),(1770,2,2352,'e33','e33'),(1771,2,2353,'e36','e36'),(1772,2,2338,'e14','e14'),(1773,2,2339,'e16','e16'),(1774,2,2340,'e21','e21'),(1775,2,2341,'e22','e22'),(1776,2,2342,'e23','e23'),(1777,2,2343,'e25','e25'),(1778,2,2344,'e34','e34'),(1779,2,2345,'e36','e36'),(1780,2,2492,'h14','h14'),(1781,2,2493,'h16','h16'),(1782,2,2494,'h21','h21'),(1783,2,2495,'h22','h22'),(1784,2,2496,'h23','h23'),(1785,2,2497,'h25','h25'),(1786,2,2498,'h34','h34'),(1787,2,2499,'h36','h36'),(1788,2,2482,'h11','h11'),(1789,2,2483,'h12','h12'),(1790,2,2484,'h13','h13'),(1791,2,2485,'h15','h15'),(1792,2,2486,'h24','h24'),(1793,2,2487,'h26','h26'),(1794,2,2488,'h31','h31'),(1795,2,2489,'h32','h32'),(1796,2,2490,'h33','h33'),(1797,2,2491,'h35','h35'),(1798,2,2328,'e11','e11'),(1799,2,3258,'e12','e12'),(1800,2,2330,'e13','e13'),(1801,2,2331,'e15','e15'),(1802,2,2332,'e24','e24'),(1803,2,2333,'e26','e26'),(1804,2,2334,'e31','e31'),(1805,2,2335,'e32','e32'),(1806,2,2336,'e33','e33'),(1807,2,2337,'e35','e35'),(1808,2,2500,'h14','h14'),(1809,2,2501,'h15','h15'),(1810,2,2502,'h24','h24'),(1811,2,2503,'h25','h25'),(1812,2,2504,'h31','h31'),(1813,2,2505,'h32','h32'),(1814,2,2506,'h33','h33'),(1815,2,2507,'h36','h36'),(1816,2,2472,'h11','h11'),(1817,2,2473,'h12','h12'),(1818,2,2474,'h13','h13'),(1819,2,2475,'h16','h16'),(1820,2,2476,'h21','h21'),(1821,2,2477,'h22','h22'),(1822,2,2478,'h23','h23'),(1823,2,2479,'h26','h26'),(1824,2,2480,'h34','h34'),(1825,2,2481,'h35','h35'),(1826,3,2280,'d14','d25, d36'),(1827,3,2310,'e14','e25, e36'),(1828,3,2387,'g14','g25, g36'),(1829,3,2464,'h14','h25, h36'),(1830,3,2541,'k14','k25, k36'),(1831,2,2309,'e14','e14'),(1832,2,2311,'e25','e25'),(1833,2,2312,'e36','e36'),(1834,2,2386,'g14','g14'),(1835,2,2388,'g25','g25'),(1836,2,2389,'g36','g36'),(1837,4,2294,'d14','d25'),(1838,3,2293,'d15','d24'),(1839,3,2292,'d31','d32'),(1840,2,2291,'d33','d33'),(1841,3,2299,'e14','e25'),(1842,4,2301,'e15','e24'),(1843,3,2300,'e31','e32'),(1844,2,2302,'e36','e36'),(1845,4,2286,'d14','d25'),(1846,3,2285,'d15','d24'),(1847,3,2284,'d31','d32'),(1848,2,2283,'d33','d33'),(1849,3,2306,'e14','e25'),(1850,2,2308,'e36','e36'),(1851,4,2295,'e14','e25'),(1852,3,2296,'e15','e24'),(1853,3,2297,'e31','e32'),(1854,2,2298,'e33','e33'),(1855,4,2372,'g14','g25'),(1856,3,2373,'g15','g24'),(1857,3,2374,'g31','g32'),(1858,2,2375,'g33','g33'),(1859,4,2449,'h14','h25'),(1860,3,2450,'h15','h24'),(1861,3,2451,'h31','h32'),(1862,2,2452,'h33','h33'),(1863,4,2526,'k14','k25'),(1864,3,2527,'k15','k24'),(1865,3,2528,'k31','k32'),(1866,2,2529,'k33','k33'),(1867,3,2530,'k14','k25'),(1868,4,2532,'k15','k24'),(1869,3,2531,'k31','k32'),(1870,2,2533,'k36','k36'),(1871,3,2290,'d14','d25'),(1872,4,2289,'d15','d24'),(1873,3,2288,'d31','d32'),(1874,2,2287,'d36','d36'),(1875,3,2376,'g14','g25'),(1876,4,2378,'g15','g24'),(1877,3,2377,'g31','g32'),(1878,2,2379,'g36','g36'),(1879,3,2453,'h14','h25'),(1880,4,2455,'h15','h24'),(1881,3,2454,'h31','h32'),(1882,2,2456,'h36','h36'),(1883,4,2535,'k14','k25'),(1884,4,2304,'e14','e25'),(1885,4,2381,'g14','g25'),(1886,4,2458,'h14','h25'),(1887,3,2534,'k15','k24'),(1888,3,2536,'k31','k32'),(1889,2,2538,'k33','k33'),(1890,3,2303,'e15','e24'),(1891,3,2305,'e31','e32'),(1892,2,2307,'e33','e33'),(1893,3,2380,'g15','g24'),(1894,3,2382,'g31','g32'),(1895,2,2384,'g33','g33'),(1896,3,2457,'h15','h24'),(1897,3,2459,'h31','h32'),(1898,2,2461,'h33','h33'),(1899,3,2537,'k14','k25'),(1900,2,2539,'k36','k36'),(1901,3,2282,'d14','d25'),(1902,2,2281,'d36','d36'),(1903,3,2383,'g14','g25'),(1904,2,2385,'g36','g36'),(1905,3,2460,'h14','h25'),(1906,2,2462,'h36','h36'),(1907,10,2609,'d11','d12, d26'),(1908,4,2607,'d14','d25'),(1909,3,2606,'d15','d24'),(1910,10,2605,'d22','d21, d16'),(1911,3,2604,'d31','d32'),(1912,2,2603,'d33','d33'),(1913,10,3087,'d11','d12, d26'),(1914,4,3086,'d14','d25'),(1915,4,2621,'d14','d25'),(1916,2,2620,'d15','d24'),(1917,10,2619,'d22','d21, d16'),(1918,3,2618,'d31','d32'),(1919,2,2617,'d33','d33'),(1920,4,2639,'e14','e25'),(1921,2,2638,'e15','e24'),(1922,10,2637,'e22','e21, e16'),(1923,3,2636,'e31','e32'),(1924,2,2635,'e33','e33'),(1925,10,2634,'e11','e12, e26'),(1926,4,2633,'e14','e25'),(1927,3,2632,'e15','e24'),(1928,3,2631,'e31','e32'),(1929,2,2627,'e33','e33'),(1930,4,2657,'g14','g25'),(1931,2,2656,'g15','g24'),(1932,10,2655,'g22','g21, g16'),(1933,3,2654,'g31','g32'),(1934,2,2653,'g33','g33'),(1935,4,2675,'h14','h25'),(1936,2,2674,'h15','h24'),(1937,10,2673,'h22','h21, h16'),(1938,3,2672,'h31','h32'),(1939,2,2671,'h33','h33'),(1940,4,2693,'k14','k25'),(1941,2,2692,'k15','k24'),(1942,10,2691,'k22','k21, k16'),(1943,3,2690,'k31','k32'),(1944,2,2689,'k33','k33'),(1945,10,2688,'k11','k12, k26'),(1946,4,2687,'k14','k25'),(1947,3,2686,'k15','k24'),(1948,3,2685,'k31','k32'),(1949,2,2681,'k33','k33'),(1950,10,2670,'h11','h12, h26'),(1951,4,2669,'h14','h25'),(1952,3,2668,'h15','h24'),(1953,3,2667,'h31','h32'),(1954,2,2663,'h33','h33'),(1955,10,2652,'g11','g12, g26'),(1956,4,2651,'g14','g25'),(1957,3,2650,'g15','g24'),(1958,3,2649,'g31','g32'),(1959,2,2645,'g33','g33'),(1960,10,2616,'d11','d12, d26'),(1961,4,2615,'d14','d25'),(1962,3,2614,'d15','d24'),(1963,3,2613,'d31','d32'),(1964,2,2612,'d33','d33'),(1965,4,2705,'d14','d25'),(1966,3,2704,'d15','d24'),(1967,3,2703,'d31','d32'),(1968,2,2702,'d33','d33'),(1969,3,2701,'d15','d24'),(1970,3,2700,'d31','d32'),(1971,2,2699,'d33','d33'),(1972,4,2698,'d14','d25'),(1973,10,2695,'d22','d12, d16'),(1974,10,2694,'d11','d12, d26'),(1975,10,2709,'e22','e21, e16'),(1976,10,2723,'g22','g12, g16'),(1977,10,2737,'h22','h12, h16'),(1978,10,2751,'k22','k12, k16'),(1979,10,2750,'k11','k12, k26'),(1980,10,2708,'e11','e12, e26'),(1981,10,2722,'g11','g12, g26'),(1982,10,2736,'h11','h12, h26'),(1983,4,2761,'k14','k25'),(1984,3,2760,'k15','k24'),(1985,3,2759,'k31','k32'),(1986,2,2758,'k33','k33'),(1987,4,2733,'g14','g25'),(1988,3,2732,'g15','g24'),(1989,3,2731,'g31','g32'),(1990,2,2730,'g33','g33'),(1991,3,2757,'k15','k24'),(1992,3,2756,'k31','k32'),(1993,2,2755,'k33','k33'),(1994,3,2743,'h15','h24'),(1995,3,2742,'h31','h32'),(1996,2,2741,'h33','h33'),(1997,3,2729,'g15','g24'),(1998,3,2728,'g31','g32'),(1999,2,2727,'g33','g33'),(2000,3,2715,'e15','e24'),(2001,3,2714,'e31','e32'),(2002,2,2713,'e33','e33'),(2003,4,2712,'e14','e25'),(2004,4,2726,'g14','g25'),(2005,4,2740,'h14','h25'),(2006,4,2754,'k14','k25'),(2007,10,2753,'k11','k12, k26'),(2008,10,2752,'k22','k21, k16'),(2009,10,2739,'h11','h12, h26'),(2010,10,2738,'h22','h21, h16'),(2011,10,2725,'g11','g12, g26'),(2012,10,2724,'g22','g21, g16'),(2013,10,2711,'e11','e12, e26'),(2014,10,2710,'e22','e21, e16'),(2015,10,2697,'d11','d12, d26'),(2016,10,2696,'d22','d21, d16'),(2017,2,2279,'d14','d14'),(2018,2,2278,'d25','d25'),(2019,2,2277,'d36','d36'),(2020,2,3059,'d15','d15'),(2021,2,3058,'d24','d24'),(2022,2,3057,'d31','d31'),(2023,2,3072,'d32','d32'),(2024,2,3073,'d33','d33'),(2025,10,2628,'e11','e12, e26'),(2026,4,2626,'e14','e25'),(2027,3,2625,'e15','e24'),(2028,10,2624,'e22','e21, e16'),(2029,3,2623,'e31','e32'),(2030,2,2622,'e33','e33'),(2031,10,2630,'e11','e12, e26'),(2032,4,3092,'e14','e25'),(2070,3,3167,'MEalpha12','MEalpha21'),(2071,3,3165,'MEalpha23','MEalpha32'),(2072,2,3163,'MEalpha11','MEalpha11'),(2073,3,3162,'MEalpha13','MEalpha31'),(2074,2,3161,'MEalpha22','MEalpha22'),(2075,2,3159,'MEalpha33','MEalpha33'),(2076,2,2815,'epsr11','epsr11'),(2077,3,2817,'epsr13','epsr31'),(2078,2,2816,'epsr22','epsr22'),(2079,2,2818,'epsr33','epsr33'),(2080,2,2819,'epsr11','epsr11'),(2081,3,2820,'epsr12','epsr21'),(2082,3,2821,'epsr13','epsr31'),(2083,2,2822,'epsr22','epsr22'),(2084,3,2823,'epsr23','epsr32'),(2085,2,2824,'epsr33','epsr33'),(2086,2,3158,'MEalpha11','MEalpha11'),(2087,3,3157,'MEalpha12','MEalpha21'),(2088,3,3156,'MEalpha13','MEalpha31'),(2089,2,3154,'MEalpha22','MEalpha22'),(2090,3,3153,'MEalpha23','MEalpha32'),(2091,2,3150,'MEalpha33','MEalpha33'),(2092,3,3172,'MEalpha23','MEalpha32'),(2093,2,3170,'MEalpha11','MEalpha11'),(2094,2,3169,'MEalpha22','MEalpha22'),(2095,2,3168,'MEalpha33','MEalpha33'),(2096,2,2825,'epsr11','epsr11'),(2097,2,2826,'epsr22','epsr22'),(2098,2,2827,'epsr33','epsr33'),(2099,3,2830,'epsr11','epsr22, epsr33'),(2100,3,3184,'MEalpha11','MEalpha22, MEalpha33'),(2101,4,3179,'MEalpha12','MEalpha21'),(2102,3,3178,'MEalpha11','MEalpha22'),(2103,2,3177,'MEalpha33','MEalpha33'),(2104,3,3176,'MEalpha11','MEalpha22'),(2105,4,3175,'MEalpha12','MEalpha21'),(2106,2,3173,'MEalpha33','MEalpha33'),(2107,3,2829,'epsr11','epsr22'),(2108,2,2828,'epsr33','epsr33'),(2109,4,3183,'MEalpha11','MEalpha22'),(2110,4,3182,'MEalpha11','MEalpha22'),(2111,3,3181,'MEalpha12','MEalpha21'),(2112,3,2831,'epsr11','epsr22, epsr33'),(2113,2,2853,'epsr11T','epsr11T'),(2114,3,2854,'epsr12T','epsr21T'),(2115,3,2855,'epsr13T','epsr31T'),(2116,2,2856,'epsr22T','epsr22T'),(2117,3,2857,'epsr23T','epsr32T'),(2118,2,2858,'epsr33T','epsr33T'),(2119,2,2836,'epsr11S','epsr11S'),(2120,3,2837,'epsr12S','epsr21S'),(2121,3,2838,'epsr13S','epsr31S'),(2122,2,2839,'epsr22S','epsr22S'),(2123,3,2840,'epsr23S','epsr32S'),(2124,2,2841,'epsr33S','epsr33S'),(2125,2,2870,'betr11S','betr11S'),(2126,3,2871,'betr12S','betr21S'),(2127,3,2872,'betr13S','betr31S'),(2128,2,2873,'betr22S','betr22S'),(2129,3,2874,'betr23S','betr32S'),(2130,2,2875,'betr33S','betr33S'),(2131,2,2887,'betr11T','betr11T'),(2132,3,2888,'betr12T','betr21T'),(2133,3,2889,'betr13T','betr31T'),(2134,2,2890,'betr22T','betr22T'),(2135,3,2891,'betr23T','betr32T'),(2136,2,2892,'betr33T','betr33T'),(2137,2,2904,'rhoe11','rhoe11'),(2138,3,2905,'rhoe12','rhoe21'),(2139,3,2906,'rhoe13','rhoe31'),(2140,2,2907,'rhoe22','rhoe22'),(2141,3,2908,'rhoe23','rhoe32'),(2142,2,2909,'rhoe33','rhoe33'),(2143,2,2921,'kappa11','kappa11'),(2144,3,2922,'kappa12','kappa21'),(2145,3,2923,'kappa13','kappa31'),(2146,2,2924,'kappa22','kappa22'),(2147,3,2925,'kappa23','kappa32'),(2148,2,2926,'kappa33','kappa33'),(2149,2,2938,'kappad11','kappad11'),(2150,3,2939,'kappad12','kappad21'),(2151,3,2940,'kappad13','kappad31'),(2152,2,2941,'kappad22','kappad22'),(2153,3,2942,'kappad23','kappad32'),(2154,2,2943,'kappad33','kappad33'),(2155,2,2955,'alpha11','alpha11'),(2156,3,2956,'alpha12','alpha21'),(2157,3,2957,'alpha13','alpha31'),(2158,2,2958,'alpha22','alpha22'),(2159,3,2959,'alpha23','alpha32'),(2160,2,2960,'alpha33','alpha33'),(2161,2,2972,'Se11','Se11'),(2162,3,2973,'Se12','Se21'),(2163,3,2974,'Se13','Se31'),(2164,2,2975,'Se22','Se22'),(2165,3,2976,'Se23','Se32'),(2166,2,2977,'Se33','Se33'),(2167,2,3190,'alpha11T0','alpha11T0'),(2168,3,3189,'alpha12T0','alpha21T0'),(2169,3,3188,'alpha13T0','alpha31T0'),(2170,2,3187,'alpha22T0','alpha22T0'),(2171,3,3186,'alpha23T0','alpha32T0'),(2172,2,3185,'alpha33T0','alpha33T0'),(2173,2,3196,'alpha11T','alpha11T'),(2174,3,3195,'alpha12T','alpha21T'),(2175,3,3194,'alpha13T','alpha31T'),(2176,2,3193,'alpha22T','alpha22T'),(2177,3,3192,'alpha23T','alpha32T'),(2178,2,3191,'alpha33T','alpha33T'),(2179,2,2832,'epsr11S','epsr11S'),(2180,3,2834,'epsr13S','epsr31S'),(2181,2,2833,'epsr22S','epsr22S'),(2182,2,2835,'epsr33S','epsr33S'),(2183,2,2849,'epsr11T','epsr11T'),(2184,3,2851,'epsr13T','epsr31T'),(2185,2,2850,'epsr22T','epsr22T'),(2186,2,2852,'epsr33T','epsr33T'),(2187,2,2866,'betr11S','betr11S'),(2188,3,2868,'betr13S','betr31S'),(2189,2,2867,'betr22S','betr22S'),(2190,2,2869,'betr33S','betr33S'),(2191,2,2883,'betr11T','betr11T'),(2192,3,2885,'betr13T','betr31T'),(2193,2,2884,'betr22T','betr22T'),(2194,2,2886,'betr33T','betr33T'),(2195,2,2900,'rhoe11','rhoe11'),(2196,3,2902,'rhoe13','rhoe31'),(2197,2,2901,'rhoe22','rhoe22'),(2198,2,2903,'rhoe33','rhoe33'),(2199,2,2917,'kappa11','kappa11'),(2200,3,2919,'kappa13','kappa31'),(2201,2,2918,'kappa22','kappa22'),(2202,2,2920,'kappa33','kappa33'),(2203,2,2934,'kappad11','kappad11'),(2204,3,2936,'kappad13','kappad31'),(2205,2,2935,'kappad22','kappad22'),(2206,2,2937,'kappad33','kappad33'),(2207,2,2951,'alpha11','alpha11'),(2208,3,2953,'alpha13','alpha31'),(2209,2,2952,'alpha22','alpha22'),(2210,2,2954,'alpha33','alpha33'),(2211,2,2968,'Se11','Se11'),(2212,3,2970,'Se13','Se31'),(2213,2,2969,'Se22','Se22'),(2214,2,2971,'Se33','Se33'),(2215,2,3200,'alpha11T0','alpha11T0'),(2216,3,3199,'alpha13T0','alpha31T0'),(2217,2,3198,'alpha22T0','alpha22T0'),(2218,2,3197,'alpha33T0','alpha33T0'),(2219,2,3204,'alpha11T','alpha11T'),(2220,3,3203,'alpha13T','alpha31T'),(2221,2,3202,'alpha22T','alpha22T'),(2222,2,3201,'alpha33T','alpha33T'),(2223,2,2842,'epsr11S','epsr11S'),(2224,2,2843,'epsr22S','epsr22S'),(2225,2,2844,'epsr33S','epsr33S'),(2226,2,2859,'epsr11T','epsr11T'),(2227,2,2860,'epsr22T','epsr22T'),(2228,2,2861,'epsr33T','epsr33T'),(2229,2,2876,'betr11S','betr11S'),(2230,2,2877,'betr22S','betr22S'),(2231,2,2878,'betr33S','betr33S'),(2232,2,2893,'betr11T','betr11T'),(2233,2,2894,'betr22T','betr22T'),(2234,2,2895,'betr33T','betr33T'),(2235,2,2910,'rhoe11','rhoe11'),(2236,2,2911,'rhoe22','rhoe22'),(2237,2,2912,'rhoe33','rhoe33'),(2238,2,2927,'kappa11','kappa11'),(2239,2,2928,'kappa22','kappa22'),(2240,2,2929,'kappa33','kappa33'),(2241,2,2944,'kappad11','kappad11'),(2242,2,2945,'kappad22','kappad22'),(2243,2,2946,'kappad33','kappad33'),(2244,2,2961,'alpha11','alpha11'),(2245,2,2962,'alpha22','alpha22'),(2246,2,2963,'alpha33','alpha33'),(2247,2,2978,'Se11','Se11'),(2248,2,2979,'Se22','Se22'),(2249,2,2980,'Se33','Se33'),(2250,2,3207,'alpha11T0','alpha11T0'),(2251,2,3206,'alpha22T0','alpha22T0'),(2252,2,3205,'alpha33T0','alpha33T0'),(2253,2,3210,'alpha11T','alpha11T'),(2254,2,3209,'alpha22T','alpha22T'),(2255,2,3208,'alpha33T','alpha33T'),(2256,3,2848,'epsr11S','epsr22S, epsr33S'),(2257,3,2865,'epsr11T','epsr22T, epsr33T'),(2258,3,2882,'betr11S','betr22S, betr33S'),(2259,3,2899,'betr11T','betr22T, betr33T'),(2260,3,2916,'rhoe11','rhoe22, rhoe33'),(2261,3,2933,'kappa11','kappa22, kappa33'),(2262,3,2950,'kappad11','kappad22, kappad33'),(2263,3,2967,'alpha11','alpha22, alpha33'),(2264,3,2984,'Se11','Se22, Se33'),(2265,3,3211,'alpha11T0','alpha22T0, alpha33T0'),(2266,3,3212,'alpha11T','alpha22T, alpha33T'),(2267,3,2846,'epsr11S','epsr22S'),(2268,2,2845,'epsr33S','epsr33S'),(2269,3,2863,'epsr11T','epsr22T'),(2270,2,2862,'epsr33T','epsr33T'),(2271,3,2880,'betr11S','betr22S'),(2272,2,2879,'betr33S','betr33S'),(2273,3,2897,'betr11T','betr22T'),(2274,2,2896,'betr33T','betr33T'),(2275,3,2914,'rhoe11','rhoe22'),(2276,2,2913,'rhoe33','rhoe33'),(2277,3,2931,'kappa11','kappa22'),(2278,2,2930,'kappa33','kappa33'),(2279,3,2948,'kappad11','kappad22'),(2280,2,2947,'kappad33','kappad33'),(2281,3,2965,'alpha11','alpha22'),(2282,2,2964,'alpha33','alpha33'),(2283,3,2982,'Se11','Se22'),(2284,2,2981,'Se33','Se33'),(2285,3,3216,'alpha11T0','alpha22T0'),(2286,2,3215,'alpha33T0','alpha33T0'),(2287,3,3214,'alpha11T','alpha22T'),(2288,2,3213,'alpha33T','alpha33T'),(2289,3,2864,'epsr11T','epsr22T, epsr33T'),(2290,3,2898,'betr11T','betr22T, betr33T'),(2291,3,2966,'alpha11','alpha22, alpha33'),(2292,3,2983,'Se11','Se22, Se33'),(2293,3,3259,'alpha11T0','alpha22T0, alpha33T0'),(2294,3,3260,'alpha11T','alpha22T, alpha33T'),(2295,3,2847,'epsr11S','epsr22S, epsr33S'),(2296,3,2881,'betr11S','betr22S, betr33S'),(2297,3,2915,'rhoe11','rhoe22, rhoe33'),(2298,3,2932,'kappa11','kappa22, kappa33'),(2299,3,2949,'kappad11','kappad22, kappad33');
/*!40000 ALTER TABLE `keynotation_catalogpropertydetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mail_configuration`
--

DROP TABLE IF EXISTS `mail_configuration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mail_configuration` (
  `id` int(11) NOT NULL,
  `EMAIL_HOST` varchar(1024) NOT NULL,
  `EMAIL_USE_TLS` tinyint(1) NOT NULL,
  `EMAIL_HOST_USER` varchar(255) NOT NULL,
  `EMAIL_HOST_PASSWORD` varchar(255) NOT NULL,
  `EMAIL_PORT` int(11) NOT NULL,
  `EMAIL_DOMAIN` varchar(1024) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mail_configuration`
--

LOCK TABLES `mail_configuration` WRITE;
/*!40000 ALTER TABLE `mail_configuration` DISABLE KEYS */;
INSERT INTO `mail_configuration` VALUES (1,'smtp.gmail.com',1,'mpod@cimav.edu.mx','c1m4v2017',587,'cimav.edu.mx');
/*!40000 ALTER TABLE `mail_configuration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message_category`
--

DROP TABLE IF EXISTS `message_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `message_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message_category`
--

LOCK TABLES `message_category` WRITE;
/*!40000 ALTER TABLE `message_category` DISABLE KEYS */;
INSERT INTO `message_category` VALUES (1,'activation','Message for account activation'),(2,'notification','User notification'),(3,'notificationtostaff','Notification to staff');
/*!40000 ALTER TABLE `message_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message_category_detail`
--

DROP TABLE IF EXISTS `message_category_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `message_category_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_id` int(11) DEFAULT NULL,
  `messagecategory_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message_category_detail`
--

LOCK TABLES `message_category_detail` WRITE;
/*!40000 ALTER TABLE `message_category_detail` DISABLE KEYS */;
INSERT INTO `message_category_detail` VALUES (1,1,1,2,0),(2,6,2,2,0),(3,5,3,1,0),(4,7,2,2,0);
/*!40000 ALTER TABLE `message_category_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message_mail`
--

DROP TABLE IF EXISTS `message_mail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `message_mail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email_message` varchar(3072) NOT NULL,
  `email_subject` varchar(255) DEFAULT NULL,
  `email_regards` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message_mail`
--

LOCK TABLES `message_mail` WRITE;
/*!40000 ALTER TABLE `message_mail` DISABLE KEYS */;
INSERT INTO `message_mail` VALUES (1,'Please click on the link below to confirm your registration:','Activate Your MPOD  Account','Hi'),(5,'Has uploaded a new case, please click on the link below to show file online or open the attached file:','MPOD - Team: New CIF submitted','The user'),(6,'Your file will be under review to show file online click the link:','Your CIF file has been received','Hi'),(7,'Your file was published to show online click the link:','Your CIF file has been published','Hi');
/*!40000 ALTER TABLE `message_mail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mpodfile`
--

DROP TABLE IF EXISTS `mpodfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mpodfile` (
  `id` int(11) NOT NULL,
  `revision` varchar(3) DEFAULT NULL,
  `description1` text,
  `site` varchar(100) DEFAULT NULL,
  `description2` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mpodfile`
--

LOCK TABLES `mpodfile` WRITE;
/*!40000 ALTER TABLE `mpodfile` DISABLE KEYS */;
INSERT INTO `mpodfile` VALUES (1,'001','This file is available in the Material Properties Open Database (MPOD),','http://mpod.cimav.edu.mx/','The file may be used within the scientific community so long as<br/>proper attribution is given to the journal article from which the<br/>data were obtained.');
/*!40000 ALTER TABLE `mpodfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `other_tags`
--

DROP TABLE IF EXISTS `other_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `other_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(45) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `other_tags`
--

LOCK TABLES `other_tags` WRITE;
/*!40000 ALTER TABLE `other_tags` DISABLE KEYS */;
INSERT INTO `other_tags` VALUES (1,'phase',1),(2,'symmetry',1),(3,'structure',1);
/*!40000 ALTER TABLE `other_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `path`
--

DROP TABLE IF EXISTS `path`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `path` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cifs_dir` varchar(511) DEFAULT NULL,
  `cifs_dir_valids` varchar(511) DEFAULT NULL,
  `cifs_dir_invalids` varchar(511) DEFAULT NULL,
  `core_dic_filepath` varchar(511) DEFAULT NULL,
  `mpod_dic_filepath` varchar(511) DEFAULT NULL,
  `cifs_dir_output` varchar(511) DEFAULT NULL,
  `stl_dir` varchar(511) DEFAULT NULL,
  `datafiles_path` varchar(511) DEFAULT NULL,
  `so_dir` varchar(45) DEFAULT NULL,
  `devmode` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `path`
--

LOCK TABLES `path` WRITE;
/*!40000 ALTER TABLE `path` DISABLE KEYS */;
INSERT INTO `path` VALUES (1,'.\\\\media\\\\datafiles\\\\','.\\\\media\\\\datafiles\\\\valid\\\\','.\\\\media\\\\datafiles\\\\invalid\\\\','.\\\\media\\\\dictionary\\\\cif_core.dic','.\\\\media\\\\dictionary\\\\cif_material_properties_0_0_6.dic','.\\\\media\\\\datafiles\\\\output\\\\','.\\\\media\\\\stlfiles\\\\','.\\\\media\\\\datafiles\\\\','.\\\\media\\\\sofiles\\\\',1),(2,'/var/www/MPOD/media/datafiles/','/var/www/MPOD/media/datafiles/valid/','/var/www/MPOD/media/datafiles/invalid/','/var/www/MPOD/media/dictionary/cif_core.dic','/var/www/MPOD/media/dictionary/cif_material_properties_0_0_6.dic','/var/www/MPOD/media/datafiles/output/','/var/www/MPOD/media/stlfiles/','/var/www/MPOD/media/datafiles/','/var/www/MPOD/media/sofiles/',0),(3,'/EclipseWork/mpod/media/datafiles/','/EclipseWork/mpod/media/datafiles/valid/','/EclipseWork/mpod/media/datafiles/invalid/','/EclipseWork/mpod/media/dictionary/cif_core.dic','/EclipseWork/mpod/media/dictionary/cif_material_properties_0_0_6.dic','/EclipseWork/mpod/media/datafiles/output/','/EclipseWork/mpod/media/stlfiles/','/EclipseWork/mpod/media/datafiles/','/EclipseWork/mpod/media/sofiles/',1),(4,'/var/www/mpod/media/datafiles/','/var/www/mpod/media/datafiles/valid/','/var/www/mpod/media/datafiles/invalid/','/var/www/mpod/media/dictionary/cif_core.dic','/var/www/mpod/media/dictionary/cif_material_properties_0_0_6.dic','/var/www/mpod/media/datafiles/output/','/var/www/mpod/media/stlfiles/','/var/www/mpod/media/datafiles/','/var/www/mpod/media/sofiles/',0),(5,'/var/www/mpod/mpod/media/datafiles/valid/','/var/www/mpod/mpod/media/datafiles/valid/','/var/www/mpod/mpod/media/datafiles/invalid/','/var/www/mpod/mpod/media/dictionary/cif_core.dic','/var/www/mpod/mpod/media/dictionary/cif_material_properties_0_0_6.dic','/var/www/mpod/mpod/media/datafiles/output/','/var/www/mpod/mpod/media/stlfiles/','/var/www/mpod/mpod/media/datafiles/','/var/www/mpod/mpod/media/sofiles/',NULL);
/*!40000 ALTER TABLE `path` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paths`
--

DROP TABLE IF EXISTS `paths`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paths` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cifs_dir` varchar(511) DEFAULT NULL,
  `cifs_dir_valids` varchar(511) DEFAULT NULL,
  `cifs_dir_invalids` varchar(511) DEFAULT NULL,
  `core_dic_filepath` varchar(511) DEFAULT NULL,
  `mpod_dic_filepath` varchar(511) DEFAULT NULL,
  `cifs_dir_output` varchar(511) DEFAULT NULL,
  `stl_dir` varchar(511) DEFAULT NULL,
  `datafiles_path` varchar(511) DEFAULT NULL,
  `devmode` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paths`
--

LOCK TABLES `paths` WRITE;
/*!40000 ALTER TABLE `paths` DISABLE KEYS */;
INSERT INTO `paths` VALUES (1,'.\\\\media\\\\datafiles\\\\test\\\\','/EclipseWork/mpod/media/datafiles/test/valid/','/EclipseWork/mpod/media/datafiles/test/invalid/','/EclipseWork/mpod/media/dictionary/cif_core.dic','/EclipseWork/mpod/media/dictionary/cif_material_properties_0_0_6.dic','/EclipseWork/mpod/media/datafiles/test/','.\\\\media\\\\stlfiles\\\\','.\\\\media\\\\datafiles\\\\',1),(2,'/var/www/MPOD/media/datafiles/test/',NULL,NULL,NULL,NULL,NULL,'/var/www/MPOD/media/stlfiles/','/var/www/MPOD/media/datafiles/',0),(3,'/EclipseWork/mpod/media/datafiles/test/',NULL,NULL,NULL,NULL,NULL,'/EclipseWork/mpod/media/stlfiles/','/EclipseWork/mpod/media/datafiles/',1),(4,'/var/www/mpod/media/datafiles/test/',NULL,NULL,NULL,NULL,NULL,'/var/www/mpod/media/stlfiles/','/var/www/mpod/media/datafiles/',0);
/*!40000 ALTER TABLE `paths` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `point_group_groups`
--

DROP TABLE IF EXISTS `point_group_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `point_group_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `catalogpointgroup_id` int(11) NOT NULL,
  `pointgroupnames_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=164 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `point_group_groups`
--

LOCK TABLES `point_group_groups` WRITE;
/*!40000 ALTER TABLE `point_group_groups` DISABLE KEYS */;
INSERT INTO `point_group_groups` VALUES (1,1,2),(2,2,2),(3,3,2),(4,4,1),(5,5,1),(6,6,1),(7,7,1),(98,35,39),(8,8,4),(9,10,3),(10,9,4),(11,12,3),(12,11,3),(70,8,38),(71,9,38),(74,11,38),(73,12,38),(72,10,38),(16,3,7),(17,7,7),(18,19,8),(19,22,8),(20,20,9),(21,21,9),(22,23,9),(24,12,10),(23,9,10),(25,26,11),(26,30,11),(77,3,38),(76,2,38),(75,1,38),(55,24,17),(54,20,16),(53,19,16),(52,23,16),(51,22,16),(49,21,16),(48,37,15),(47,38,15),(40,1,13),(41,2,13),(42,3,13),(43,4,13),(44,5,13),(45,6,13),(46,7,13),(56,26,17),(57,27,17),(58,28,17),(59,29,17),(60,30,17),(62,16,18),(63,17,18),(64,18,18),(65,13,19),(66,14,19),(67,15,19),(68,35,20),(69,36,20),(78,5,38),(79,6,38),(80,4,38),(81,7,38),(82,24,38),(84,26,38),(85,27,38),(86,28,38),(87,29,38),(88,30,38),(89,37,38),(90,38,38),(91,25,38),(92,40,38),(93,41,38),(94,42,38),(95,43,38),(96,44,38),(99,46,39),(100,13,43),(101,47,43),(102,49,43),(103,14,44),(104,50,44),(105,51,44),(106,16,45),(107,52,45),(108,53,45),(109,17,46),(110,54,46),(111,55,46),(112,56,46),(113,1,47),(114,8,47),(115,24,47),(116,40,47),(117,57,47),(118,58,47),(119,59,47),(120,60,47),(121,61,47),(122,62,47),(123,2,48),(124,48,48),(125,63,48),(126,4,49),(127,10,49),(128,28,49),(129,43,49),(130,62,49),(131,64,49),(132,65,49),(133,66,49),(134,67,49),(135,68,49),(136,69,49),(137,86,49),(138,87,49),(139,88,49),(140,6,50),(141,70,50),(142,71,50),(143,72,50),(144,73,50),(145,5,51),(146,11,51),(147,27,51),(148,74,51),(149,76,51),(150,77,51),(151,78,51),(152,79,51),(153,80,51),(154,81,51),(155,82,51),(156,89,51),(157,90,51),(158,19,52),(159,21,52),(160,83,52),(161,84,52),(162,85,52),(163,25,17);
/*!40000 ALTER TABLE `point_group_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `point_group_names`
--

DROP TABLE IF EXISTS `point_group_names`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `point_group_names` (
  `id` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `description` varchar(511) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=53 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `point_group_names`
--

LOCK TABLES `point_group_names` WRITE;
/*!40000 ALTER TABLE `point_group_names` DISABLE KEYS */;
INSERT INTO `point_group_names` VALUES (1,'(4mm, -42m, 422, 4/mmm)',NULL),(2,' (4, -4, 4/m)',NULL),(21,'None',''),(3,'(32, -3m, 3m)',NULL),(4,'(3, -3)',NULL),(7,'(4/m, 4/mmm)',NULL),(8,'(23, -43m)',NULL),(9,' (m3, 432, m3m)',NULL),(10,'(-3, -3m)',NULL),(11,'(6/m, 6/mmm)',NULL),(13,'(4, -4, 4/m, 422, 4mm, -42m, 4/mmm)',NULL),(15,'(infinf, infinfm)',NULL),(16,'(23, -43m, m3, 432, m3m)',NULL),(17,'(6, -6, 6/m, 6mm, 622, -6m2, 6/mmm)','(6, -6, 6/m, 6mm, 622, -6m2, 6/mmm)'),(18,'(222, 2mm, mmm)',NULL),(19,'(2, m, 2/m)',NULL),(20,'(1, -1)','(1, -1)'),(38,'(3, -3, 32, -3m, 3m, 4, -4, 4/m, 4mm, -42m, 422, 4/mmm, 6, -6, 3/m, 6/m, 6mm, 622, -6m2, 6/mmm, 6/mmm, infinf, infinfm, inf/m,  inf2,  inf/mm)',''),(39,'(1, -1*)','(1, -1*)'),(43,'(2, m*, 2/m*)','(2, m*, 2/m*)'),(44,'(m, 2*, 2*/m)','(m, 2*, 2*/m)'),(45,'(222, m*m*2, m*m*m*)','(222, m*m*2, m*m*m*)'),(46,'(2mm, 22*2*, m*m2*, m*mm)','(2mm, 22*2*, m*m2*, m*mm)'),(47,'(4, 3, 6, inf, -3*, -4*, 4/m*, -6*, 6/m*, infm*)','(4, 3, 6, inf, -3*, -4*, 4/m*, -6*, 6/m*, infm*)'),(48,'(-4, 4*/m*, 4*)','(-4, 4*/m*, 4*)'),(49,'(422, 32, 622, inf2, infm*, 3m*, -3*m*, 4m*m*, 4/m*m*m*, 6m*m*, -6*m*2, -4*2m*, 6/m*m*m*, inf/m*m*)','(422, 32, 622, inf2, infm*, 3m*, -3*m*, 4m*m*, 4/m*m*m*, 6m*m*, -6*m*2, -4*2m*, 6/m*m*m*, inf/m*m*)'),(50,'(-42m, 4*22, 4*mm*, -42*m*, 4*/m*mm*)','(-42m, 4*22, 4*mm*, -42*m*, 4*/m*mm*)'),(51,'(4mm, 3m, 6mm, 32*, 42*2*, 4/m*mm, 62*2*, -6*m2*, 6/m*mm, inf2*, inf/m*m, -3*m, -4*2*m)','(4mm, 3m, 6mm, 32*, 42*2*, 4/m*mm, 62*2*, -6*m2*, 6/m*mm, inf2*, inf/m*m, -3*m, -4*2*m)'),(52,'(23, 432, m*3, -4*3m*, m*3m*)','(23, 432, m*3, -4*3m*, m*3m*)');
/*!40000 ALTER TABLE `point_group_names` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prop_looped_tags`
--

DROP TABLE IF EXISTS `prop_looped_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prop_looped_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(45) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prop_looped_tags`
--

LOCK TABLES `prop_looped_tags` WRITE;
/*!40000 ALTER TABLE `prop_looped_tags` DISABLE KEYS */;
INSERT INTO `prop_looped_tags` VALUES (1,'_prop_data_label',1),(2,'_prop_data_tensorial_index',1),(3,'_prop_data_value',1);
/*!40000 ALTER TABLE `prop_looped_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prop_tags`
--

DROP TABLE IF EXISTS `prop_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prop_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(45) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prop_tags`
--

LOCK TABLES `prop_tags` WRITE;
/*!40000 ALTER TABLE `prop_tags` DISABLE KEYS */;
INSERT INTO `prop_tags` VALUES (1,'conditions',1),(2,'measurement',1),(3,'frame',1),(4,'symmetry',1),(5,'data',1),(6,'thermal',1),(7,'superconducting',0),(8,'temperatura',0),(9,'heat',0);
/*!40000 ALTER TABLE `prop_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_values`
--

DROP TABLE IF EXISTS `property_values`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `property_values` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datafileproperty_id` int(11) DEFAULT NULL,
  `label` varchar(255) NOT NULL,
  `tensorial_index` int(11) NOT NULL,
  `value` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=406 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_values`
--

LOCK TABLES `property_values` WRITE;
/*!40000 ALTER TABLE `property_values` DISABLE KEYS */;
INSERT INTO `property_values` VALUES (405,959,'eij',33,'0.96'),(404,959,'eij',32,'-0.62'),(403,959,'eij',31,'-0.62'),(401,959,'eij',15,'-0.3'),(402,959,'eij',24,'-0.3');
/*!40000 ALTER TABLE `property_values` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_values_temp`
--

DROP TABLE IF EXISTS `property_values_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `property_values_temp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datafilepropertytemp_id` int(11) NOT NULL,
  `label` varchar(255) NOT NULL,
  `tensorial_index` int(11) NOT NULL,
  `value` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2241 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_values_temp`
--

LOCK TABLES `property_values_temp` WRITE;
/*!40000 ALTER TABLE `property_values_temp` DISABLE KEYS */;
INSERT INTO `property_values_temp` VALUES (2119,271,'eij',15,'-0.3'),(2120,271,'eij',24,'-0.3'),(2121,271,'eij',31,'-0.62'),(2122,271,'eij',32,'-0.62'),(2123,271,'eij',33,'0.96'),(2124,274,'sij',11,'9.73'),(2125,274,'sij',12,'-2.64'),(2126,274,'sij',13,'-2.64'),(2127,274,'sij',22,'9.73'),(2128,274,'sij',23,'-5.28'),(2129,274,'sij',33,'9.73'),(2130,274,'sij',44,'14.90'),(2131,274,'sij',55,'14.90'),(2132,274,'sij',66,'14.90'),(2133,275,'sij',11,'9.73'),(2134,275,'sij',12,'-2.64'),(2135,275,'sij',13,'-2.64'),(2136,275,'sij',22,'9.73'),(2137,275,'sij',23,'-5.28'),(2138,275,'sij',33,'9.73'),(2139,275,'sij',44,'14.90'),(2140,275,'sij',55,'14.90'),(2141,275,'sij',66,'14.90'),(2142,276,'sij',11,'9.73'),(2143,276,'sij',12,'-2.64'),(2144,276,'sij',13,'-2.64'),(2145,276,'sij',22,'9.73'),(2146,276,'sij',23,'-5.28'),(2147,276,'sij',33,'9.73'),(2148,276,'sij',44,'14.90'),(2149,276,'sij',55,'14.90'),(2150,276,'sij',66,'14.90'),(2151,277,'sij',11,'0.951'),(2152,277,'sij',12,'-0.0987'),(2153,277,'sij',13,'-0.0987'),(2154,277,'sij',22,'0.951'),(2155,277,'sij',23,'-0.1974'),(2156,277,'sij',33,'0.951'),(2157,277,'sij',44,'1.732'),(2158,277,'sij',55,'1.732'),(2159,277,'sij',66,'1.732'),(2160,278,'sij',11,'0.951'),(2161,278,'sij',12,'-0.0987'),(2162,278,'sij',13,'-0.0987'),(2163,278,'sij',22,'0.951'),(2164,278,'sij',23,'-0.1974'),(2165,278,'sij',33,'0.951'),(2166,278,'sij',44,'1.732'),(2167,278,'sij',55,'1.732'),(2168,278,'sij',66,'1.732'),(2169,279,'sij',11,'9.73'),(2170,279,'sij',12,'-2.64'),(2171,279,'sij',13,'-2.64'),(2172,279,'sij',22,'9.73'),(2173,279,'sij',23,'-5.28'),(2174,279,'sij',33,'9.73'),(2175,279,'sij',44,'14.90'),(2176,279,'sij',55,'14.90'),(2177,279,'sij',66,'14.90'),(2178,280,'sij',11,'0.951'),(2179,280,'sij',12,'-0.0987'),(2180,280,'sij',13,'-0.0987'),(2181,280,'sij',22,'0.951'),(2182,280,'sij',23,'-0.1974'),(2183,280,'sij',33,'0.951'),(2184,280,'sij',44,'1.732'),(2185,280,'sij',55,'1.732'),(2186,280,'sij',66,'1.732'),(2187,281,'sij',11,'6.93'),(2188,281,'sij',12,'-1.52'),(2189,281,'sij',13,'-1.52'),(2190,281,'sij',22,'6.93'),(2191,281,'sij',23,'-3.04'),(2192,281,'sij',33,'6.93'),(2193,281,'sij',44,'29.5'),(2194,281,'sij',55,'29.5'),(2195,281,'sij',66,'29.5'),(2196,282,'sij',11,'15.2'),(2197,282,'sij',12,'-4.7'),(2198,282,'sij',13,'-4.7'),(2199,282,'sij',22,'15.2'),(2200,282,'sij',23,'-9.4'),(2201,282,'sij',33,'15.2'),(2202,282,'sij',44,'39.6'),(2203,282,'sij',55,'39.6'),(2204,282,'sij',66,'39.6'),(2205,283,'cij',11,'1'),(2206,283,'cij',12,'2'),(2207,283,'cij',13,'2'),(2208,283,'cij',22,'1'),(2209,283,'cij',23,'2'),(2210,283,'cij',33,'1'),(2211,283,'cij',44,'3'),(2212,283,'cij',55,'3'),(2213,283,'cij',66,'3'),(2214,284,'cijD',11,'4'),(2215,284,'cijD',12,'5'),(2216,284,'cijD',13,'5'),(2217,284,'cijD',22,'4'),(2218,284,'cijD',23,'5'),(2219,284,'cijD',33,'4'),(2220,284,'cijD',44,'6'),(2221,284,'cijD',55,'6'),(2222,284,'cijD',66,'6'),(2223,285,'cij',11,'1'),(2224,285,'cij',12,'2'),(2225,285,'cij',13,'2'),(2226,285,'cij',22,'1'),(2227,285,'cij',23,'2'),(2228,285,'cij',33,'1'),(2229,285,'cij',44,'3'),(2230,285,'cij',55,'3'),(2231,285,'cij',66,'3'),(2232,286,'cijD',11,'4'),(2233,286,'cijD',12,'5'),(2234,286,'cijD',13,'5'),(2235,286,'cijD',22,'4'),(2236,286,'cijD',23,'5'),(2237,286,'cijD',33,'4'),(2238,286,'cijD',44,'6'),(2239,286,'cijD',55,'6'),(2240,286,'cijD',66,'6');
/*!40000 ALTER TABLE `property_values_temp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(100) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `categorytag_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
INSERT INTO `tags` VALUES (1,'conditions',1,2),(2,'measurement',1,2),(3,'frame',1,2),(4,'symmetry',1,2),(5,'data',1,2),(6,'thermal',1,2),(7,'superconducting',0,6),(8,'temperature',0,6),(9,'heat',1,1),(10,'phase',1,4),(11,'symmetry',1,4),(12,'structure',1,4),(13,'conditions',1,1),(14,'measurement',1,1),(15,'frame',1,1),(16,'symmetry',1,1),(18,'_cod_database_code',1,5),(19,'_phase_generic',1,5),(20,'_phase_name',1,5),(21,'_chemical_formula',1,5),(22,'_journal_name_full',1,3),(23,'_journal_year',1,3),(24,'_journal_volume',1,3),(25,'_journal_issue',1,3),(26,'_journal_page_first',1,3),(27,'_journal_page_last',1,3),(28,'_journal_article_reference',1,3),(29,'_journal_pages_number',1,3),(30,'thermal',1,1);
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `type`
--

DROP TABLE IF EXISTS `type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(511) NOT NULL,
  `catalogproperty_id` int(11) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `tensor` varchar(100) DEFAULT NULL,
  `clusterurl` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `type`
--

LOCK TABLES `type` WRITE;
/*!40000 ALTER TABLE `type` DISABLE KEYS */;
INSERT INTO `type` VALUES (2,'s','compliance',1,1,'compliance','selasfib'),(1,'c','stiffness',1,1,'stiffness','celasfib'),(3,'dg','piezoelectricdg',2,1,'thirdranktensordg','dpiezofib'),(4,'k','magnetoelectricity no',3,1,'secondranktensor','dielecfib'),(11,'y','magnetoelectricity yes',3,1,'secondranktensor','dielecfib'),(10,'t','Test1Testtype',8,1,NULL,NULL),(5,'4n','simetric no',4,0,'fourthranktensor','fourthranktensor'),(6,'4y','simetric yes',4,0,'fourthranktensor','fourthranktensor'),(7,'eh','piezoelectriceh',2,1,'thirdranktensoreh','epiezofib');
/*!40000 ALTER TABLE `type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `type_data_property`
--

DROP TABLE IF EXISTS `type_data_property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `type_data_property` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) DEFAULT NULL,
  `dataproperty_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `type_data_property`
--

LOCK TABLES `type_data_property` WRITE;
/*!40000 ALTER TABLE `type_data_property` DISABLE KEYS */;
INSERT INTO `type_data_property` VALUES (1,1,10),(3,3,33),(4,1,11),(5,1,12),(6,1,13),(7,1,61),(8,1,62),(9,1,71),(10,1,72),(11,2,7),(12,2,9),(13,2,8),(14,2,57),(15,2,58),(16,2,59),(17,2,63),(18,4,1),(19,4,2),(20,4,3),(21,4,4),(22,4,5),(23,4,17),(24,4,53),(25,4,54),(26,4,56),(27,4,60),(29,7,34),(30,3,35),(31,7,36),(32,3,18),(87,11,76),(88,5,31),(90,5,37),(91,6,55),(92,6,21),(93,6,22),(94,6,24),(95,4,74),(96,4,75);
/*!40000 ALTER TABLE `type_data_property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile`
--

DROP TABLE IF EXISTS `user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `bio` text,
  `phone` varchar(20) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `organization` varchar(100) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile`
--

LOCK TABLES `user_profile` WRITE;
/*!40000 ALTER TABLE `user_profile` DISABLE KEYS */;
INSERT INTO `user_profile` VALUES (1,5,'asda','999','chih','mex','bm',NULL),(7,11,'','','','','',NULL),(8,12,'','','','','',NULL),(10,14,'','','','','',NULL),(11,15,'','.','Chihuahua','Chihuahua','CIMAV',NULL),(12,16,'','6141036063','Chihuahua ','Mexico','CIMAV',NULL),(14,18,'','','','','',NULL),(15,19,'','','','','',NULL),(16,20,'','','','','',NULL),(17,21,'','','','','',NULL),(18,22,'','','','','',NULL),(19,23,'','','','','',NULL),(20,24,'','','','','',NULL),(21,25,'','','','','',NULL),(22,26,'','','','','',NULL),(23,27,'','','','','',NULL),(24,28,'','','','','',NULL),(25,29,'','','','','',NULL),(26,30,'','','','','',NULL),(27,31,'','','','','',NULL),(28,32,'','','','','',NULL),(29,33,'','','','','',NULL),(30,34,'','','','','',NULL),(31,35,'','','','','',NULL),(32,36,'','','','','',NULL),(33,37,'','','','','',NULL),(34,38,'','','','','',NULL),(35,39,'','','','','',NULL),(36,40,'','','','','',NULL),(37,41,'','','','','',NULL),(38,42,'','6144391102','Chihuahua','Mexico','CIMAV, S.C.',NULL);
/*!40000 ALTER TABLE `user_profile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-05-22 18:21:51
