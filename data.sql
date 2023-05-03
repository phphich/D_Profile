-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: db_dprofile
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add division',7,'add_division'),(26,'Can change division',7,'change_division'),(27,'Can delete division',7,'delete_division'),(28,'Can view division',7,'view_division'),(29,'Can add faculty',8,'add_faculty'),(30,'Can change faculty',8,'change_faculty'),(31,'Can delete faculty',8,'delete_faculty'),(32,'Can view faculty',8,'view_faculty'),(33,'Can add personnel',9,'add_personnel'),(34,'Can change personnel',9,'change_personnel'),(35,'Can delete personnel',9,'delete_personnel'),(36,'Can view personnel',9,'view_personnel'),(37,'Can add expertise',10,'add_expertise'),(38,'Can change expertise',10,'change_expertise'),(39,'Can delete expertise',10,'delete_expertise'),(40,'Can view expertise',10,'view_expertise'),(41,'Can add education',11,'add_education'),(42,'Can change education',11,'change_education'),(43,'Can delete education',11,'delete_education'),(44,'Can view education',11,'view_education'),(45,'Can add documents',12,'add_documents'),(46,'Can change documents',12,'change_documents'),(47,'Can delete documents',12,'delete_documents'),(48,'Can view documents',12,'view_documents'),(49,'Can add curriculum',13,'add_curriculum'),(50,'Can change curriculum',13,'change_curriculum'),(51,'Can delete curriculum',13,'delete_curriculum'),(52,'Can view curriculum',13,'view_curriculum'),(53,'Can add curr affiliation',14,'add_curraffiliation'),(54,'Can change curr affiliation',14,'change_curraffiliation'),(55,'Can delete curr affiliation',14,'delete_curraffiliation'),(56,'Can view curr affiliation',14,'view_curraffiliation'),(57,'Can add training',15,'add_training'),(58,'Can change training',15,'change_training'),(59,'Can delete training',15,'delete_training'),(60,'Can view training',15,'view_training'),(61,'Can add social service',16,'add_socialservice'),(62,'Can change social service',16,'change_socialservice'),(63,'Can delete social service',16,'delete_socialservice'),(64,'Can view social service',16,'view_socialservice'),(65,'Can add research',17,'add_research'),(66,'Can change research',17,'change_research'),(67,'Can delete research',17,'delete_research'),(68,'Can view research',17,'view_research'),(69,'Can add performance',18,'add_performance'),(70,'Can change performance',18,'change_performance'),(71,'Can delete performance',18,'delete_performance'),(72,'Can view performance',18,'view_performance'),(73,'Can add leave',19,'add_leave'),(74,'Can change leave',19,'change_leave'),(75,'Can delete leave',19,'delete_leave'),(76,'Can view leave',19,'view_leave'),(77,'Can add command',20,'add_command'),(78,'Can change command',20,'change_command'),(79,'Can delete command',20,'delete_command'),(80,'Can view command',20,'view_command');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$hpHdCcRlr2D8mTNjHTko8J$gztH7jU/ojBGQIJmt6OF5cHiykJv5BRxArvIa5C19rI=','2023-05-03 15:11:02.112758',1,'admin','','','admin@rmuti.ac.th',1,1,'2023-05-03 15:02:27.419352');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `baseapp_curraffiliation`
--

DROP TABLE IF EXISTS `baseapp_curraffiliation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baseapp_curraffiliation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(30) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `curriculum_id` bigint NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baseapp_curraffiliat_curriculum_id_74dc74ff_fk_baseapp_c` (`curriculum_id`),
  KEY `baseapp_curraffiliat_personnel_id_4f64cdf7_fk_baseapp_p` (`personnel_id`),
  KEY `baseapp_curraffiliat_recorder_id_5103e558_fk_baseapp_p` (`recorder_id`),
  CONSTRAINT `baseapp_curraffiliat_curriculum_id_74dc74ff_fk_baseapp_c` FOREIGN KEY (`curriculum_id`) REFERENCES `baseapp_curriculum` (`id`),
  CONSTRAINT `baseapp_curraffiliat_personnel_id_4f64cdf7_fk_baseapp_p` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `baseapp_curraffiliat_recorder_id_5103e558_fk_baseapp_p` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `baseapp_curraffiliation`
--

LOCK TABLES `baseapp_curraffiliation` WRITE;
/*!40000 ALTER TABLE `baseapp_curraffiliation` DISABLE KEYS */;
/*!40000 ALTER TABLE `baseapp_curraffiliation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `baseapp_curriculum`
--

DROP TABLE IF EXISTS `baseapp_curriculum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baseapp_curriculum` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name_th` varchar(100) NOT NULL,
  `name_en` varchar(100) NOT NULL,
  `name_th_sh` varchar(50) NOT NULL,
  `name_en_sh` varchar(50) NOT NULL,
  `level` varchar(30) NOT NULL,
  `studyTime` int NOT NULL,
  `division_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baseapp_curriculum_division_id_fda5c50e_fk_baseapp_division_id` (`division_id`),
  CONSTRAINT `baseapp_curriculum_division_id_fda5c50e_fk_baseapp_division_id` FOREIGN KEY (`division_id`) REFERENCES `baseapp_division` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `baseapp_curriculum`
--

LOCK TABLES `baseapp_curriculum` WRITE;
/*!40000 ALTER TABLE `baseapp_curriculum` DISABLE KEYS */;
INSERT INTO `baseapp_curriculum` VALUES (1,'บริหารธุรกิจบัณฑิต (สาขาเทคโนโลยีธุรกิจดิจิทัล)','Bachelor\'s of Business Administration (Digital Business Technology)','บธ.บ. (เทคโนโลยีธุรกิจดิจิทัล)','B.BA. (Digital Business Technology)','ปริญญาตรี',4,1);
/*!40000 ALTER TABLE `baseapp_curriculum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `baseapp_division`
--

DROP TABLE IF EXISTS `baseapp_division`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baseapp_division` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name_th` varchar(50) NOT NULL,
  `name_en` varchar(50) NOT NULL,
  `name_sh` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `baseapp_division`
--

LOCK TABLES `baseapp_division` WRITE;
/*!40000 ALTER TABLE `baseapp_division` DISABLE KEYS */;
INSERT INTO `baseapp_division` VALUES (1,'ระบบสารสนเทศ','Information System','ฺBIS');
/*!40000 ALTER TABLE `baseapp_division` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `baseapp_documents`
--

DROP TABLE IF EXISTS `baseapp_documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baseapp_documents` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `doctype` varchar(15) NOT NULL,
  `refId` int NOT NULL,
  `filename` varchar(100) NOT NULL,
  `filetype` varchar(30) NOT NULL,
  `uploadDate` datetime(6) NOT NULL,
  `file` varchar(100) NOT NULL,
  `personnel_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baseapp_documents_personnel_id_d8623a6c_fk_baseapp_personnel_id` (`personnel_id`),
  CONSTRAINT `baseapp_documents_personnel_id_d8623a6c_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `baseapp_documents`
--

LOCK TABLES `baseapp_documents` WRITE;
/*!40000 ALTER TABLE `baseapp_documents` DISABLE KEYS */;
/*!40000 ALTER TABLE `baseapp_documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `baseapp_education`
--

DROP TABLE IF EXISTS `baseapp_education`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baseapp_education` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `level` varchar(30) NOT NULL,
  `degree_th` varchar(100) NOT NULL,
  `degree_en` varchar(100) NOT NULL,
  `degree_th_sh` varchar(50) NOT NULL,
  `degree_en_sh` varchar(50) NOT NULL,
  `yearGraduate` int NOT NULL,
  `institute` varchar(100) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baseapp_education_personnel_id_2adcd2d8_fk_baseapp_personnel_id` (`personnel_id`),
  KEY `baseapp_education_recorder_id_38379db0_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `baseapp_education_personnel_id_2adcd2d8_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `baseapp_education_recorder_id_38379db0_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `baseapp_education`
--

LOCK TABLES `baseapp_education` WRITE;
/*!40000 ALTER TABLE `baseapp_education` DISABLE KEYS */;
/*!40000 ALTER TABLE `baseapp_education` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `baseapp_expertise`
--

DROP TABLE IF EXISTS `baseapp_expertise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baseapp_expertise` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `topic` varchar(100) NOT NULL,
  `detail` longtext NOT NULL,
  `experience` longtext NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baseapp_expertise_personnel_id_8b0457dc_fk_baseapp_personnel_id` (`personnel_id`),
  KEY `baseapp_expertise_recorder_id_5711daad_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `baseapp_expertise_personnel_id_8b0457dc_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `baseapp_expertise_recorder_id_5711daad_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `baseapp_expertise`
--

LOCK TABLES `baseapp_expertise` WRITE;
/*!40000 ALTER TABLE `baseapp_expertise` DISABLE KEYS */;
/*!40000 ALTER TABLE `baseapp_expertise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `baseapp_faculty`
--

DROP TABLE IF EXISTS `baseapp_faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baseapp_faculty` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name_th` varchar(100) NOT NULL,
  `name_en` varchar(100) NOT NULL,
  `university` varchar(100) NOT NULL,
  `address` longtext NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `website` varchar(50) NOT NULL,
  `vision` longtext NOT NULL,
  `philosophy` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `baseapp_faculty`
--

LOCK TABLES `baseapp_faculty` WRITE;
/*!40000 ALTER TABLE `baseapp_faculty` DISABLE KEYS */;
INSERT INTO `baseapp_faculty` VALUES (1,'คณะบริหารธุรกิจและเทคโนโลยีสารสนเทศ','Faculty of Business Administration and Information Technology','มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน วิทยาเขตขอนแก่น','150 ถ.ศรีจันทร์ ต.ในเมือง อ.เมือง จ.ขอนแก่น','043-336371-2','้้http://fib.rmuti.ac.th','LERD','BEST and GOOD');
/*!40000 ALTER TABLE `baseapp_faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `baseapp_personnel`
--

DROP TABLE IF EXISTS `baseapp_personnel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baseapp_personnel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(30) NOT NULL,
  `sId` varchar(15) NOT NULL,
  `firstname_th` varchar(50) NOT NULL,
  `lastname_th` varchar(50) NOT NULL,
  `firstname_en` varchar(50) NOT NULL,
  `lastname_en` varchar(50) NOT NULL,
  `status` varchar(30) NOT NULL,
  `type` varchar(10) NOT NULL,
  `gender` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `birthDate` date NOT NULL,
  `hiringDate` date NOT NULL,
  `picture` varchar(100) NOT NULL,
  `division_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `baseapp_personnel_division_id_fb67c60a_fk_baseapp_division_id` (`division_id`),
  CONSTRAINT `baseapp_personnel_division_id_fb67c60a_fk_baseapp_division_id` FOREIGN KEY (`division_id`) REFERENCES `baseapp_division` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `baseapp_personnel`
--

LOCK TABLES `baseapp_personnel` WRITE;
/*!40000 ALTER TABLE `baseapp_personnel` DISABLE KEYS */;
INSERT INTO `baseapp_personnel` VALUES (1,'phichayapak.ph@rmuti.ac.th','1','ก','ก','a','a','อาจารย์','สายวิชาการ','ชาย','aaa','2515-12-07','2541-06-22','static/images/personnels/6-1-2565_14-37-08_FyN2Goo.jpg',1);
/*!40000 ALTER TABLE `baseapp_personnel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2023-05-03 15:12:02.639192','1','คณะบริหารธุรกิจและเทคโนโลยีสารสนเทศ มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน วิทยาเขตขอนแก่น',1,'[{\"added\": {}}]',8,1),(2,'2023-05-03 15:12:20.364925','1','ระบบสารสนเทศ (ฺBIS)',1,'[{\"added\": {}}]',7,1),(3,'2023-05-03 15:12:41.871198','1','บริหารธุรกิจบัณฑิต (สาขาเทคโนโลยีธุรกิจดิจิทัล)',1,'[{\"added\": {}}]',13,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(14,'baseapp','curraffiliation'),(13,'baseapp','curriculum'),(7,'baseapp','division'),(12,'baseapp','documents'),(11,'baseapp','education'),(10,'baseapp','expertise'),(8,'baseapp','faculty'),(9,'baseapp','personnel'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(20,'workapp','command'),(19,'workapp','leave'),(18,'workapp','performance'),(17,'workapp','research'),(16,'workapp','socialservice'),(15,'workapp','training');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-05-03 13:58:57.540472'),(2,'auth','0001_initial','2023-05-03 13:59:18.209716'),(3,'admin','0001_initial','2023-05-03 13:59:27.225095'),(4,'admin','0002_logentry_remove_auto_add','2023-05-03 13:59:27.530399'),(5,'admin','0003_logentry_add_action_flag_choices','2023-05-03 13:59:27.808406'),(6,'contenttypes','0002_remove_content_type_name','2023-05-03 13:59:31.576049'),(7,'auth','0002_alter_permission_name_max_length','2023-05-03 13:59:33.395474'),(8,'auth','0003_alter_user_email_max_length','2023-05-03 13:59:35.811221'),(9,'auth','0004_alter_user_username_opts','2023-05-03 13:59:35.857635'),(10,'auth','0005_alter_user_last_login_null','2023-05-03 13:59:37.488002'),(11,'auth','0006_require_contenttypes_0002','2023-05-03 13:59:37.640176'),(12,'auth','0007_alter_validators_add_error_messages','2023-05-03 13:59:37.730582'),(13,'auth','0008_alter_user_username_max_length','2023-05-03 13:59:41.867161'),(14,'auth','0009_alter_user_last_name_max_length','2023-05-03 13:59:45.971696'),(15,'auth','0010_alter_group_name_max_length','2023-05-03 13:59:47.805650'),(16,'auth','0011_update_proxy_permissions','2023-05-03 13:59:47.851624'),(17,'auth','0012_alter_user_first_name_max_length','2023-05-03 13:59:49.826931'),(18,'baseapp','0001_initial','2023-05-03 14:00:27.897693'),(19,'sessions','0001_initial','2023-05-03 14:00:30.010491'),(20,'workapp','0001_initial','2023-05-03 14:01:18.466032');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workapp_command`
--

DROP TABLE IF EXISTS `workapp_command`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_command` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comId` varchar(30) NOT NULL,
  `comDate` date NOT NULL,
  `fiscalYear` int NOT NULL,
  `eduYear` int NOT NULL,
  `eduSemeter` varchar(10) NOT NULL,
  `mission` varchar(50) NOT NULL,
  `topic` longtext NOT NULL,
  `detail` longtext NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_command_personnel_id_a0bced0c_fk_baseapp_personnel_id` (`personnel_id`),
  KEY `workapp_command_recorder_id_06b235ed_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `workapp_command_personnel_id_a0bced0c_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_command_recorder_id_06b235ed_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workapp_command`
--

LOCK TABLES `workapp_command` WRITE;
/*!40000 ALTER TABLE `workapp_command` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_command` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workapp_leave`
--

DROP TABLE IF EXISTS `workapp_leave`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_leave` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `days` int NOT NULL,
  `fiscalYear` int NOT NULL,
  `eduYear` int NOT NULL,
  `leaveType` varchar(50) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_leave_personnel_id_84cc093a_fk_baseapp_personnel_id` (`personnel_id`),
  KEY `workapp_leave_recorder_id_36b265d1_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `workapp_leave_personnel_id_84cc093a_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_leave_recorder_id_36b265d1_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workapp_leave`
--

LOCK TABLES `workapp_leave` WRITE;
/*!40000 ALTER TABLE `workapp_leave` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_leave` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workapp_performance`
--

DROP TABLE IF EXISTS `workapp_performance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_performance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `getDate` date NOT NULL,
  `fiscalYear` int NOT NULL,
  `eduYear` int NOT NULL,
  `eduSemeter` int NOT NULL,
  `topic` varchar(255) NOT NULL,
  `detail` longtext NOT NULL,
  `budget` double NOT NULL,
  `budgetType` varchar(30) NOT NULL,
  `source` varchar(255) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_performance_personnel_id_d4658b3e_fk_baseapp_p` (`personnel_id`),
  KEY `workapp_performance_recorder_id_a3649e47_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `workapp_performance_personnel_id_d4658b3e_fk_baseapp_p` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_performance_recorder_id_a3649e47_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workapp_performance`
--

LOCK TABLES `workapp_performance` WRITE;
/*!40000 ALTER TABLE `workapp_performance` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_performance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workapp_research`
--

DROP TABLE IF EXISTS `workapp_research`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_research` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fiscalYear` int NOT NULL,
  `title_th` longtext NOT NULL,
  `title_en` longtext NOT NULL,
  `objective` longtext NOT NULL,
  `percent_resp` int NOT NULL,
  `budget` double NOT NULL,
  `budgetType` varchar(30) NOT NULL,
  `source` varchar(255) NOT NULL,
  `keyword` longtext NOT NULL,
  `percent_success` int NOT NULL,
  `publish_method` longtext NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_research_personnel_id_dfb5d04c_fk_baseapp_personnel_id` (`personnel_id`),
  KEY `workapp_research_recorder_id_0674ef61_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `workapp_research_personnel_id_dfb5d04c_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_research_recorder_id_0674ef61_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workapp_research`
--

LOCK TABLES `workapp_research` WRITE;
/*!40000 ALTER TABLE `workapp_research` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_research` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workapp_socialservice`
--

DROP TABLE IF EXISTS `workapp_socialservice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_socialservice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `days` int NOT NULL,
  `fiscalYear` int NOT NULL,
  `eduYear` int NOT NULL,
  `eduSemeter` int NOT NULL,
  `topic` double NOT NULL,
  `objective` longtext NOT NULL,
  `place` varchar(255) NOT NULL,
  `budget` double NOT NULL,
  `budgetType` varchar(30) NOT NULL,
  `source` varchar(255) NOT NULL,
  `receiver` varchar(255) NOT NULL,
  `num_receiver` int NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_socialservic_personnel_id_6077a67c_fk_baseapp_p` (`personnel_id`),
  KEY `workapp_socialservic_recorder_id_7ece6878_fk_baseapp_p` (`recorder_id`),
  CONSTRAINT `workapp_socialservic_personnel_id_6077a67c_fk_baseapp_p` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_socialservic_recorder_id_7ece6878_fk_baseapp_p` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workapp_socialservice`
--

LOCK TABLES `workapp_socialservice` WRITE;
/*!40000 ALTER TABLE `workapp_socialservice` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_socialservice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workapp_training`
--

DROP TABLE IF EXISTS `workapp_training`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_training` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `days` int NOT NULL,
  `fiscalYear` int NOT NULL,
  `eduYear` int NOT NULL,
  `eduSemeter` int NOT NULL,
  `topic` varchar(255) NOT NULL,
  `place` varchar(255) NOT NULL,
  `budget` double NOT NULL,
  `budgetType` varchar(30) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_training_personnel_id_6c2478b3_fk_baseapp_personnel_id` (`personnel_id`),
  KEY `workapp_training_recorder_id_21f847a5_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `workapp_training_personnel_id_6c2478b3_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_training_recorder_id_21f847a5_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workapp_training`
--

LOCK TABLES `workapp_training` WRITE;
/*!40000 ALTER TABLE `workapp_training` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_training` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-03 22:43:26
