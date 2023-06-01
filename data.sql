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
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Administrator'),(4,'Manager'),(7,'Personnel'),(5,'Staff');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add division',7,'add_division'),(26,'Can change division',7,'change_division'),(27,'Can delete division',7,'delete_division'),(28,'Can view division',7,'view_division'),(29,'Can add faculty',8,'add_faculty'),(30,'Can change faculty',8,'change_faculty'),(31,'Can delete faculty',8,'delete_faculty'),(32,'Can view faculty',8,'view_faculty'),(33,'Can add personnel',9,'add_personnel'),(34,'Can change personnel',9,'change_personnel'),(35,'Can delete personnel',9,'delete_personnel'),(36,'Can view personnel',9,'view_personnel'),(37,'Can add expertise',10,'add_expertise'),(38,'Can change expertise',10,'change_expertise'),(39,'Can delete expertise',10,'delete_expertise'),(40,'Can view expertise',10,'view_expertise'),(41,'Can add education',11,'add_education'),(42,'Can change education',11,'change_education'),(43,'Can delete education',11,'delete_education'),(44,'Can view education',11,'view_education'),(45,'Can add documents',12,'add_documents'),(46,'Can change documents',12,'change_documents'),(47,'Can delete documents',12,'delete_documents'),(48,'Can view documents',12,'view_documents'),(49,'Can add curriculum',13,'add_curriculum'),(50,'Can change curriculum',13,'change_curriculum'),(51,'Can delete curriculum',13,'delete_curriculum'),(52,'Can view curriculum',13,'view_curriculum'),(53,'Can add curr affiliation',14,'add_curraffiliation'),(54,'Can change curr affiliation',14,'change_curraffiliation'),(55,'Can delete curr affiliation',14,'delete_curraffiliation'),(56,'Can view curr affiliation',14,'view_curraffiliation'),(57,'Can add command',15,'add_command'),(58,'Can change command',15,'change_command'),(59,'Can delete command',15,'delete_command'),(60,'Can view command',15,'view_command'),(61,'Can add leave',16,'add_leave'),(62,'Can change leave',16,'change_leave'),(63,'Can delete leave',16,'delete_leave'),(64,'Can view leave',16,'view_leave'),(65,'Can add performance',17,'add_performance'),(66,'Can change performance',17,'change_performance'),(67,'Can delete performance',17,'delete_performance'),(68,'Can view performance',17,'view_performance'),(69,'Can add research',18,'add_research'),(70,'Can change research',18,'change_research'),(71,'Can delete research',18,'delete_research'),(72,'Can view research',18,'view_research'),(73,'Can add social service',19,'add_socialservice'),(74,'Can change social service',19,'change_socialservice'),(75,'Can delete social service',19,'delete_socialservice'),(76,'Can view social service',19,'view_socialservice'),(77,'Can add training',20,'add_training'),(78,'Can change training',20,'change_training'),(79,'Can delete training',20,'delete_training'),(80,'Can view training',20,'view_training'),(81,'Can add training url',21,'add_trainingurl'),(82,'Can change training url',21,'change_trainingurl'),(83,'Can delete training url',21,'delete_trainingurl'),(84,'Can view training url',21,'view_trainingurl'),(85,'Can add training file',22,'add_trainingfile'),(86,'Can change training file',22,'change_trainingfile'),(87,'Can delete training file',22,'delete_trainingfile'),(88,'Can view training file',22,'view_trainingfile'),(89,'Can add social service url',23,'add_socialserviceurl'),(90,'Can change social service url',23,'change_socialserviceurl'),(91,'Can delete social service url',23,'delete_socialserviceurl'),(92,'Can view social service url',23,'view_socialserviceurl'),(93,'Can add social service person',24,'add_socialserviceperson'),(94,'Can change social service person',24,'change_socialserviceperson'),(95,'Can delete social service person',24,'delete_socialserviceperson'),(96,'Can view social service person',24,'view_socialserviceperson'),(97,'Can add social service file',25,'add_socialservicefile'),(98,'Can change social service file',25,'change_socialservicefile'),(99,'Can delete social service file',25,'delete_socialservicefile'),(100,'Can view social service file',25,'view_socialservicefile'),(101,'Can add research url',26,'add_researchurl'),(102,'Can change research url',26,'change_researchurl'),(103,'Can delete research url',26,'delete_researchurl'),(104,'Can view research url',26,'view_researchurl'),(105,'Can add research person',27,'add_researchperson'),(106,'Can change research person',27,'change_researchperson'),(107,'Can delete research person',27,'delete_researchperson'),(108,'Can view research person',27,'view_researchperson'),(109,'Can add research file',28,'add_researchfile'),(110,'Can change research file',28,'change_researchfile'),(111,'Can delete research file',28,'delete_researchfile'),(112,'Can view research file',28,'view_researchfile'),(113,'Can add performance url',29,'add_performanceurl'),(114,'Can change performance url',29,'change_performanceurl'),(115,'Can delete performance url',29,'delete_performanceurl'),(116,'Can view performance url',29,'view_performanceurl'),(117,'Can add performance file',30,'add_performancefile'),(118,'Can change performance file',30,'change_performancefile'),(119,'Can delete performance file',30,'delete_performancefile'),(120,'Can view performance file',30,'view_performancefile'),(121,'Can add leave url',31,'add_leaveurl'),(122,'Can change leave url',31,'change_leaveurl'),(123,'Can delete leave url',31,'delete_leaveurl'),(124,'Can view leave url',31,'view_leaveurl'),(125,'Can add leave file',32,'add_leavefile'),(126,'Can change leave file',32,'change_leavefile'),(127,'Can delete leave file',32,'delete_leavefile'),(128,'Can view leave file',32,'view_leavefile'),(129,'Can add command url',33,'add_commandurl'),(130,'Can change command url',33,'change_commandurl'),(131,'Can delete command url',33,'delete_commandurl'),(132,'Can view command url',33,'view_commandurl'),(133,'Can add command person',34,'add_commandperson'),(134,'Can change command person',34,'change_commandperson'),(135,'Can delete command person',34,'delete_commandperson'),(136,'Can view command person',34,'view_commandperson'),(137,'Can add command file',35,'add_commandfile'),(138,'Can change command file',35,'change_commandfile'),(139,'Can delete command file',35,'delete_commandfile'),(140,'Can view command file',35,'view_commandfile'),(141,'Can add permission',36,'add_permission'),(142,'Can change permission',36,'change_permission'),(143,'Can delete permission',36,'delete_permission'),(144,'Can view permission',36,'view_permission');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$PDShv8LdtLS9uJpMoU3yfy$PfaVKIge0kR/NM9bbkI9Ao6fwlyA37Nske0voXDzJLM=','2023-05-20 09:07:21.141887',1,'admin','','','admin@hotmail.com',1,1,'2023-05-19 13:05:55.462351'),(4,'pbkdf2_sha256$600000$HsZS9R3cbjaMgcL8casjba$sJoQoeH39FTJzyQzSW2ePfehNFO7Ys7Gf+W1tZdA1U0=','2023-05-27 00:23:07.266569',1,'phichayapak.ph@rmuti.ac.th','Phitchayaphak','Phiphitphatphaisit','phichayapak.ph@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(5,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-27 06:52:43.646447',0,'path@hotmail.com','Pathamakorn','Nethayavijit','path@hotmail.com',1,1,'2023-05-20 10:10:15.620464'),(6,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'tassanee.lu@rmuti.ac.th','Tassanee','Loonrasri','tassanee.lu@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(7,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'arisa.kh@rmuti.ac.th','Arisa','Khethongma','arisa.kh@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(8,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'nathaporn.ji@rmuti.ac.th','์Nathaporn','Jirajesada','nathaporn.ji@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(9,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'nathaya.kh@rmuti.ac.th','์Nuthaya','Khamparanon','nathaya.kh@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(10,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'tayawut.ph@rmuti.ac.th','Thayawat','Phothongsangarun','tayawut.ph@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(11,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'arirat.ch@rmuti.ac.th','Arirat','Chuaboonkerd Noth','arirat.ch@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(12,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'supawadee.kh@rmuti.ac.th','Supawadee','Khocharat','supawadee.kh@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(13,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'khemporn.su@rmuti.ac.th','Khemporn','Summart','khemporn.su@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(14,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'Jirathikarn.ji@rmuti.ac.th','Jirathikarn','Wuthipan','Jirathikarn.ji@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(15,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'kanoknapah.so@rmuti.ac.th','Kanoknapat','Sokeiw','kanoknapah.so@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(16,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'mujarin.kh@rmuti.ac.th','Mujarin','Keawyong','mujarin.kh@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(17,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'priyakorn.na@rmuti.ac.th','Priyakorn','Nugrong','priyakorn.na@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(18,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'thanai.sr@rmuti.ac.th','Thainai','Sriesan','thanai.sr@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(19,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'thanadom.ra@rmuti.ac.th','Thanadom','Rasrirathana','thanadom.ra@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(20,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'jarapha.ch@rmuti.ac.th','Jirapha','Charathirawat','jarapha.ch@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(21,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'sudarat.ph@rmuti.ac.th','Sudarat','Phongsathitphat','sudarat.ph@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(22,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'jatharat.kh@rmuti.ac.th','Jutharat','Khunthum','jatharat.kh@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(23,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'rathanawadee.sa@rmuti.ac.th','Rathanawadee','Sangmari','rathanawadee.sa@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(24,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'ukrit.ph@rmuti.ac.th','Ukrit','Phanna','ukrit.ph@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(25,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'wanitha.bo@rmuti.ac.th','Wanitha','Boonchome','wanitha.bo@rmuti.ac.th',0,1,'2023-05-20 10:10:15.620464'),(26,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'pornthapin.su@rmuti.ac.th','Pornthaphin','Suksangprasit','pornthapin.su@rmuti.ac.th',0,1,'2023-05-20 10:10:15.620464');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (35,4,1),(41,5,7),(32,6,4),(20,7,7),(18,8,4),(17,9,7),(16,10,4),(21,11,4),(19,12,7),(31,13,7),(23,14,7),(22,15,7),(29,16,7),(28,17,7),(27,18,7),(26,19,4),(24,20,4),(30,21,7),(25,22,7),(13,23,7),(15,24,7),(14,25,4),(12,26,7);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `baseapp_permission`
--

LOCK TABLES `baseapp_permission` WRITE;
/*!40000 ALTER TABLE `baseapp_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `baseapp_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_faculty`
--

LOCK TABLES `baseapp_faculty` WRITE;
/*!40000 ALTER TABLE `baseapp_faculty` DISABLE KEYS */;
INSERT INTO `baseapp_faculty` VALUES (1,'คณะบริหารธุรกิจและเทคโนโลยีสารสนเทศ','Faculty of Business Administration and Information Technology','มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน','150 ถ.ศรีจันทร์ อ.เมือง จ.ขอนแก่น','043-336371-2','้้http://fib.rmuti.ac.th','go together','LERD');
/*!40000 ALTER TABLE `baseapp_faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_division`
--

LOCK TABLES `baseapp_division` WRITE;
/*!40000 ALTER TABLE `baseapp_division` DISABLE KEYS */;
INSERT INTO `baseapp_division` VALUES (2,'ระบบสารสนเทศ','Information System','ฺBIS'),(3,'การบัญชี','Accounting','ฺBAC'),(4,'การจัดการ','Management','BMG'),(5,'การตลาด','Marketing','BMK');
/*!40000 ALTER TABLE `baseapp_division` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_curriculum`
--

LOCK TABLES `baseapp_curriculum` WRITE;
/*!40000 ALTER TABLE `baseapp_curriculum` DISABLE KEYS */;
INSERT INTO `baseapp_curriculum` VALUES (1,'บริหารธุรกิจบัณฑิต (สาขาเทคโนโลยีธุรกิจดิจิทัล)','Bachelor\'s of Business Administration (Digital Business Technology)',2563,'บธ.บ. (เทคโนโลยีธุรกิจดิจิทัล)','B.BA. (Digital Business Techn)','ปริญญาตรี',4,2),
(2,'บัญชีบัณฑิต','Accounting',2563,'บช.','B.AC.','ปริญญาตรี',4,3),
(3,'บริหารธุรกิจบัณฑิต (สาขาการตลาด)','ฺBachelor\'s of Business Administration (Marketing)',2563,'บธ.บ. (การตลาด)','B.BA. (Marketing)','ปริญญาตรี',4,5),
(4,'บริหารธุรกิจบัณฑิต (สาขาการจัดการ)','Bachelor\'s of Business Administration (Management)',2563,'บธ.บ. (การจัดการ)','B.BA. (Management)','ปริญญาตรี',4,4);
/*!40000 ALTER TABLE `baseapp_curriculum` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `baseapp_personnel`
--

LOCK TABLES `baseapp_personnel` WRITE;
/*!40000 ALTER TABLE `baseapp_personnel` DISABLE KEYS */;
INSERT INTO `baseapp_personnel` VALUES 
(2,'path@hotmail.com','555','ปัทมากร','เนตยวิจิตร','Pathamakorn','Nethayavijit','ผู้ช่วยศาสตราจารย์','สายวิชาการ','หญิง','dsadfs','2023-05-18','2023-05-18','images/personnels/2.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',2, 'นางสาว'),
(3,'tassanee.lu@rmuti.ac.th','444','ทรรศนีย์','ลุนราศรี','Tassanee','Loonrasri','อาจารย์','สายวิชาการ','หญิง','ฟหกดหฟ','2023-05-18','2023-05-18','images/personnels/3.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',2, 'นางสาว'),
(4,'arisa.kh@rmuti.ac.th','111','อลิษา','เกษทองมา','Arisa','Khethongma','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/4.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',5, 'นางสาว'),
(5,'nathaporn.ji@rmuti.ac.th','111','นัฏพร','จิรเจษฏา','์Nathaporn','Jirajesada','ผู้ช่วยศาสตราจารย์','สายสนับสนุน','หญิง','111','2023-05-20','2023-05-20','images/personnels/5.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',5, 'นางสาว'),
(6,'nathaya.kh@rmuti.ac.th','111','นทยา','กัมพลานนท์','์Nuthaya','Khamparanon','ผู้ช่วยศาสตราจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/6.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',5, 'นางสาว'),
(7,'tayawut.ph@rmuti.ac.th','111','ทายาวุฒิ','โพธิ์ทองแสงอรุณ','Thayawat','Phothongsangarun','ผู้ช่วยศาสตราจารย์','สายวิชาการ','ชาย','111','2023-05-20','2023-05-20','images/personnels/7.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',5, 'นาย'),
(8,'arirat.ch@rmuti.ac.th','111','อารีรัตน์','เชื้อบุญเกิด โนท','Arirat','Chuaboonkerd Noth','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/8.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',5, 'นางสาว'),
(9,'supawadee.kh@rmuti.ac.th','111','สุภาวดี','คชรัตน์','Supawadee','Khocharat','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/9.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',5, 'นางสาว'),
(10,'khemporn.su@rmuti.ac.th','111','เข็มพร','สุ่มมาตร','Khemporn','Summart','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/10.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',3, 'นาง'),
(11,'Jirathikarn.ji@rmuti.ac.th','111','จิรัตติกาล','วุฒิพันธุ์','Jirathikarn','Wuthipan','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/11.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',3, 'นางสาว'),
(12,'kanoknapah.so@rmuti.ac.th','111','กนกนภัทร์','โสเขียว','Kanoknapat','Sokeiw','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/12.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',3, 'นางสาว'),
(13,'mujarin.kh@rmuti.ac.th','111','มุจรินทร์','แก้วหย่อง','Mujarin','Keawyong','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/13.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',3, 'นาง'),
(14,'priyakorn.na@rmuti.ac.th','111','ปริยากร','นักร้อง','Priyakorn','Nugrong','อาจารย์','สายวิชาการ','หญิง','11','2023-05-20','2023-05-20','images/personnels/14.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',3, 'นางสาว'),
(15,'thanai.sr@rmuti.ac.th','111','ธนัย','ศรีอิสาน','Thainai','Sriesan','อาจารย์','สายวิชาการ','ชาย','111','2023-05-20','2023-05-20','images/personnels/15.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',3, 'นาบ'),
(16,'thanadom.ra@rmuti.ac.th','111','ฐณดม','ราศรีรัตนะ','Thanadom','Rasrirathana','ผู้ช่วยศาสตราจารย์','สายวิชาการ','ชาย','222','2023-05-20','2023-05-20','images/personnels/16.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',3, 'นาย'),
(17,'jarapha.ch@rmuti.ac.th','111','จิราภา','ชลาธาราวัฒน์','Jirapha','Charathirawat','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/17.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',3, 'นาง'),
(18,'sudarat.ph@rmuti.ac.th','111','สุดารัตน์','พงษ์สถิตพัฒน์','Sudarat','Phongsathitphat','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/18.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',3, 'นางสาว'),
(19,'jatharat.kh@rmuti.ac.th','111','จุฑารัตน์','คุณทุม','Jutharat','Khunthum','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/19.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',3, 'นางสาว'),
(20,'rathanawadee.sa@rmuti.ac.th','111','รัตนาวดี','แสงมาลี','Rathanawadee','Sangmari','อาจารย์','สายวิชาการ','หญิง','ddd','2023-05-20','2023-05-20','images/personnels/20.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',4, 'นางสาว'),
(21,'ukrit.ph@rmuti.ac.th','111','อุกฤษณ์','พรรณะ','Ukrit','Phanna','อาจารย์','สายวิชาการ','ชาย','111','2023-05-20','2023-05-20','images/personnels/21.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',4, 'นาย'),
(22,'wanitha.bo@rmuti.ac.th','111','วนิตา','บุญโฉม','Wanitha','Boonchome','ผู้ช่วยศาสตราจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/22.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',4, 'นางสาว'),
(23,'pornthapin.su@rmuti.ac.th','111','พรเทพินทร์','สุขแสงประสิทธิ์','Pornthaphin','Suksangprasit','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/23.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',4, 'นางสาว'),
(26,'phichayapak.ph@rmuti.ac.th','4123','พิชญะภาคย์','พิพิธพัฒน์ไพสิฐ','Phitchayaphak','Phiphitphatphaisit','อาจารย์','สายวิชาการ','ชาย','255/7','2515-12-07','2541-06-22','images/personnels/26.jpg',26,'2023-05-29 08:05:36.959981', 26,'2023-05-29 08:05:36.959981',2, 'นาย');
/*!40000 ALTER TABLE `baseapp_personnel` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `baseapp_education`
--

LOCK TABLES `baseapp_education` WRITE;
/*!40000 ALTER TABLE `baseapp_education` DISABLE KEYS */;
INSERT INTO `baseapp_education` VALUES (1,'ปริญญาตรี','บริหารธุรกิจบัณฑิต (ระบบสารสนเทศ)','Bachelor\'s of Business Administration (Information System)','บธ.บ. (ระบบสารสนเทศ)','ฺB.BA. (Information System)',2541,'สถาบันเทคโนโลยีราชมงคล','2023-05-19 13:10:16.468331',2,2),(2,'ปริญญาตรี','บริหารธุรกิจบัณฑิต (ระบบสารสนเทศ)','Bachelor\'s of Business Administration (Information System)','บธ.บ. (ระบบสารสนเทศ)','ฺB.BA. (Information System)',2545,'สถาบันเทคโนโลยีราชมงคล','2023-05-21 06:21:21.896502',3,3),(3,'ปริญญาโท','dsafas','dsfsaf','safsaf','asfasf',250,'asfasf','2023-05-23 06:17:23.805899',2,2);
/*!40000 ALTER TABLE `baseapp_education` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_expertise`
--

LOCK TABLES `baseapp_expertise` WRITE;
/*!40000 ALTER TABLE `baseapp_expertise` DISABLE KEYS */;
INSERT INTO `baseapp_expertise` VALUES (1,'การจัดการฐานข้อมูล','การจัดการฐานข้อมูล MySQL, MS SQL Server, Oracle','วิทยากร','2023-05-19 13:10:57.971300',2,2),(2,'dsfas','fasfasfas','fasfasfasfas','2023-05-23 06:20:31.195339',2,2),(3,'dsfasf','asdfasfas','fasfasfasfasfasf','2023-05-23 06:20:36.819216',2,2);
/*!40000 ALTER TABLE `baseapp_expertise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_curraffiliation`
--

LOCK TABLES `baseapp_curraffiliation` WRITE;
/*!40000 ALTER TABLE `baseapp_curraffiliation` DISABLE KEYS */;
INSERT INTO `baseapp_curraffiliation` VALUES (9,'กรรมการประจำหลักสูตร','2023-05-20 09:33:30.756100',2,13,2),(10,'ผู้รับผิดชอบหลักสูตร','2023-05-20 09:33:40.042944',2,16,2),(12,'กรรมการประจำหลักสูตร','2023-05-20 10:08:32.554354',3,7,2),(13,'ผู้รับผิดชอบหลักสูตร','2023-05-20 10:08:43.924915',3,5,2),(14,'กรรมการประจำหลักสูตร','2023-05-20 10:08:52.644978',3,8,2),(15,'กรรมการประจำหลักสูตร','2023-05-20 10:09:01.309474',3,9,2),(16,'กรรมการประจำหลักสูตร','2023-05-20 10:09:12.885318',3,6,2),(17,'กรรมการประจำหลักสูตร','2023-05-20 10:09:23.738831',1,2,2),(18,'กรรมการประจำหลักสูตร','2023-05-20 10:09:31.028372',1,3,2),(19,'ผู้รับผิดชอบหลักสูตร','2023-05-20 10:10:29.474239',1,26,2),(20,'กรรมการประจำหลักสูตร','2023-05-20 14:43:17.265761',2,15,2),(21,'กรรมการประจำหลักสูตร','2023-05-20 14:43:32.147647',2,10,2),(22,'ผู้รับผิดชอบหลักสูตร','2023-05-23 07:14:05.453581',4,20,2),(23,'กรรมการประจำหลักสูตร','2023-05-23 07:14:27.471367',4,21,2),(24,'กรรมการประจำหลักสูตร','2023-05-23 07:14:43.465059',4,23,2),(25,'กรรมการประจำหลักสูตร','2023-05-23 07:14:53.346677',4,22,2);
/*!40000 ALTER TABLE `baseapp_curraffiliation` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2023-05-19 13:07:33.131146','1','คณะบริหารธุรกิจและเทคโนโลยีสารสนเทศ มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน',1,'[{\"added\": {}}]',8,1),(2,'2023-05-19 13:07:52.695118','4','การจัดการ (BMG)',1,'[{\"added\": {}}]',7,1),(3,'2023-05-19 13:08:03.495293','5','การตลาด (BMK)',1,'[{\"added\": {}}]',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(14,'baseapp','curraffiliation'),(13,'baseapp','curriculum'),(7,'baseapp','division'),(12,'baseapp','documents'),(11,'baseapp','education'),(10,'baseapp','expertise'),(8,'baseapp','faculty'),(36,'baseapp','permission'),(9,'baseapp','personnel'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(15,'workapp','command'),(35,'workapp','commandfile'),(34,'workapp','commandperson'),(33,'workapp','commandurl'),(16,'workapp','leave'),(32,'workapp','leavefile'),(31,'workapp','leaveurl'),(17,'workapp','performance'),(30,'workapp','performancefile'),(29,'workapp','performanceurl'),(18,'workapp','research'),(28,'workapp','researchfile'),(27,'workapp','researchperson'),(26,'workapp','researchurl'),(19,'workapp','socialservice'),(25,'workapp','socialservicefile'),(24,'workapp','socialserviceperson'),(23,'workapp','socialserviceurl'),(20,'workapp','training'),(22,'workapp','trainingfile'),(21,'workapp','trainingurl');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-05-18 13:36:10.602359'),(2,'auth','0001_initial','2023-05-18 13:36:40.827593'),(3,'admin','0001_initial','2023-05-18 13:36:52.503666'),(4,'admin','0002_logentry_remove_auto_add','2023-05-18 13:36:52.738020'),(5,'admin','0003_logentry_add_action_flag_choices','2023-05-18 13:36:53.019283'),(6,'contenttypes','0002_remove_content_type_name','2023-05-18 13:36:57.575318'),(7,'auth','0002_alter_permission_name_max_length','2023-05-18 13:37:02.129008'),(8,'auth','0003_alter_user_email_max_length','2023-05-18 13:37:08.230891'),(9,'auth','0004_alter_user_username_opts','2023-05-18 13:37:08.402792'),(10,'auth','0005_alter_user_last_login_null','2023-05-18 13:37:11.535356'),(11,'auth','0006_require_contenttypes_0002','2023-05-18 13:37:11.613538'),(12,'auth','0007_alter_validators_add_error_messages','2023-05-18 13:37:11.863516'),(13,'auth','0008_alter_user_username_max_length','2023-05-18 13:37:15.222641'),(14,'auth','0009_alter_user_last_name_max_length','2023-05-18 13:37:18.119333'),(15,'auth','0010_alter_group_name_max_length','2023-05-18 13:37:21.567347'),(16,'auth','0011_update_proxy_permissions','2023-05-18 13:37:21.661056'),(17,'auth','0012_alter_user_first_name_max_length','2023-05-18 13:37:26.932157'),(18,'baseapp','0001_initial','2023-05-18 13:38:13.664160'),(19,'sessions','0001_initial','2023-05-18 13:38:15.445260'),(20,'workapp','0001_initial','2023-05-18 13:40:16.042191'),(21,'baseapp','0002_permission','2023-05-22 13:36:42.859746'),(22,'workapp','0002_alter_trainingfile_file','2023-05-22 13:36:43.203446'),(23,'workapp','0003_alter_command_edusemeter','2023-05-25 01:18:47.196659'),(24,'workapp','0004_commandperson_recorder_alter_commandperson_personnel_and_more','2023-05-25 13:21:24.458095'),(25,'baseapp','0003_alter_personnel_options','2023-05-27 08:30:16.248849'),(26,'workapp','0005_commandfile_recorder_commandurl_recorder','2023-05-27 08:48:50.336258');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_command`
--

LOCK TABLES `workapp_command` WRITE;
/*!40000 ALTER TABLE `workapp_command` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_command` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_commandfile`
--

LOCK TABLES `workapp_commandfile` WRITE;
/*!40000 ALTER TABLE `workapp_commandfile` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_commandfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_commandperson`
--

LOCK TABLES `workapp_commandperson` WRITE;
/*!40000 ALTER TABLE `workapp_commandperson` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_commandperson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_commandurl`
--

LOCK TABLES `workapp_commandurl` WRITE;
/*!40000 ALTER TABLE `workapp_commandurl` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_commandurl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_leave`
--

LOCK TABLES `workapp_leave` WRITE;
/*!40000 ALTER TABLE `workapp_leave` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_leave` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_leavefile`
--

LOCK TABLES `workapp_leavefile` WRITE;
/*!40000 ALTER TABLE `workapp_leavefile` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_leavefile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_leaveurl`
--

LOCK TABLES `workapp_leaveurl` WRITE;
/*!40000 ALTER TABLE `workapp_leaveurl` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_leaveurl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_performance`
--

LOCK TABLES `workapp_performance` WRITE;
/*!40000 ALTER TABLE `workapp_performance` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_performance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_performancefile`
--

LOCK TABLES `workapp_performancefile` WRITE;
/*!40000 ALTER TABLE `workapp_performancefile` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_performancefile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_performanceurl`
--

LOCK TABLES `workapp_performanceurl` WRITE;
/*!40000 ALTER TABLE `workapp_performanceurl` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_performanceurl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_research`
--

LOCK TABLES `workapp_research` WRITE;
/*!40000 ALTER TABLE `workapp_research` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_research` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_researchfile`
--

LOCK TABLES `workapp_researchfile` WRITE;
/*!40000 ALTER TABLE `workapp_researchfile` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_researchfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_researchperson`
--

LOCK TABLES `workapp_researchperson` WRITE;
/*!40000 ALTER TABLE `workapp_researchperson` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_researchperson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_researchurl`
--

LOCK TABLES `workapp_researchurl` WRITE;
/*!40000 ALTER TABLE `workapp_researchurl` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_researchurl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_socialservice`
--

LOCK TABLES `workapp_socialservice` WRITE;
/*!40000 ALTER TABLE `workapp_socialservice` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_socialservice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_socialservicefile`
--

LOCK TABLES `workapp_socialservicefile` WRITE;
/*!40000 ALTER TABLE `workapp_socialservicefile` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_socialservicefile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_socialserviceperson`
--

LOCK TABLES `workapp_socialserviceperson` WRITE;
/*!40000 ALTER TABLE `workapp_socialserviceperson` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_socialserviceperson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_socialserviceurl`
--

LOCK TABLES `workapp_socialserviceurl` WRITE;
/*!40000 ALTER TABLE `workapp_socialserviceurl` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_socialserviceurl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_training`
--

LOCK TABLES `workapp_training` WRITE;
/*!40000 ALTER TABLE `workapp_training` DISABLE KEYS */;
INSERT INTO `workapp_training` VALUES (7,'2023-05-20','2023-05-25',6,2023,2023,1,'การจัดการฐานข้อมูล','มหาวิทยาลัยขอนแก่น',10000,'งบประมาณรายได้','2023-05-29 08:05:36.959981',2,26),(9,'2566-05-20','2566-05-20',1,2564,2565,1,'การตรวจสอบความถูกต้องการประเมินผลการเรียนการสอน','มทร. อีสาน วิทยาเขตขอนแก่น',0,'งบประมาณรายได้','2023-05-20 07:51:04.574709',2,26),(10,'2566-05-20','2566-05-20',1,2564,2565,1,'การเก็บข้อมูลชุมชน','บ้านนาน้องงาม',0,'งบประมาณรายได้','2023-05-20 07:51:12.998855',2,2),(11,'2566-05-22','2566-05-22',1,2566,2565,1,'tests','tests',0,'ไม่ใช้งบประมาณ','2023-05-22 12:47:03.530944',15,15),(12,'2566-05-23','2566-05-23',1,2566,2565,1,'dsafsa','fasfasf',0,'งบประมาณรายได้','2023-05-23 06:49:01.260672',2,26);
/*!40000 ALTER TABLE `workapp_training` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_trainingfile`
--

LOCK TABLES `workapp_trainingfile` WRITE;
/*!40000 ALTER TABLE `workapp_trainingfile` DISABLE KEYS */;
INSERT INTO `workapp_trainingfile` VALUES (10,'[7_10]-จดหมายจากลกศษย.pdf','pdf',7),(13,'[7_13]-SAR-65-บธ.บ.เทคโนโลยธรกจดจทล-All.doc','doc',7);
/*!40000 ALTER TABLE `workapp_trainingfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_trainingurl`
--

LOCK TABLES `workapp_trainingurl` WRITE;
/*!40000 ALTER TABLE `workapp_trainingurl` DISABLE KEYS */;
INSERT INTO `workapp_trainingurl` VALUES (7,'https://lms.kkc.rmuti.ac.th/',7);
/*!40000 ALTER TABLE `workapp_trainingurl` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-27 16:02:38
