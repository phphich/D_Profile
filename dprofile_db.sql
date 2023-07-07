-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: db_dprofile
-- ------------------------------------------------------
-- Server version	8.0.22

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
INSERT INTO `auth_group` VALUES (1,'Administrator'),(8,'Header'),(4,'Manager'),(7,'Personnel'),(5,'Staff');
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
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add division',7,'add_division'),(26,'Can change division',7,'change_division'),(27,'Can delete division',7,'delete_division'),(28,'Can view division',7,'view_division'),(29,'Can add faculty',8,'add_faculty'),(30,'Can change faculty',8,'change_faculty'),(31,'Can delete faculty',8,'delete_faculty'),(32,'Can view faculty',8,'view_faculty'),(33,'Can add personnel',9,'add_personnel'),(34,'Can change personnel',9,'change_personnel'),(35,'Can delete personnel',9,'delete_personnel'),(36,'Can view personnel',9,'view_personnel'),(37,'Can add expertise',10,'add_expertise'),(38,'Can change expertise',10,'change_expertise'),(39,'Can delete expertise',10,'delete_expertise'),(40,'Can view expertise',10,'view_expertise'),(41,'Can add education',11,'add_education'),(42,'Can change education',11,'change_education'),(43,'Can delete education',11,'delete_education'),(44,'Can view education',11,'view_education'),(45,'Can add curriculum',12,'add_curriculum'),(46,'Can change curriculum',12,'change_curriculum'),(47,'Can delete curriculum',12,'delete_curriculum'),(48,'Can view curriculum',12,'view_curriculum'),(49,'Can add curr affiliation',13,'add_curraffiliation'),(50,'Can change curr affiliation',13,'change_curraffiliation'),(51,'Can delete curr affiliation',13,'delete_curraffiliation'),(52,'Can view curr affiliation',13,'view_curraffiliation'),(53,'Can add responsible',14,'add_responsible'),(54,'Can change responsible',14,'change_responsible'),(55,'Can delete responsible',14,'delete_responsible'),(56,'Can view responsible',14,'view_responsible'),(57,'Can add command',15,'add_command'),(58,'Can change command',15,'change_command'),(59,'Can delete command',15,'delete_command'),(60,'Can view command',15,'view_command'),(61,'Can add leave',16,'add_leave'),(62,'Can change leave',16,'change_leave'),(63,'Can delete leave',16,'delete_leave'),(64,'Can view leave',16,'view_leave'),(65,'Can add performance',17,'add_performance'),(66,'Can change performance',17,'change_performance'),(67,'Can delete performance',17,'delete_performance'),(68,'Can view performance',17,'view_performance'),(69,'Can add research',18,'add_research'),(70,'Can change research',18,'change_research'),(71,'Can delete research',18,'delete_research'),(72,'Can view research',18,'view_research'),(73,'Can add social service',19,'add_socialservice'),(74,'Can change social service',19,'change_socialservice'),(75,'Can delete social service',19,'delete_socialservice'),(76,'Can view social service',19,'view_socialservice'),(77,'Can add training',20,'add_training'),(78,'Can change training',20,'change_training'),(79,'Can delete training',20,'delete_training'),(80,'Can view training',20,'view_training'),(81,'Can add training url',21,'add_trainingurl'),(82,'Can change training url',21,'change_trainingurl'),(83,'Can delete training url',21,'delete_trainingurl'),(84,'Can view training url',21,'view_trainingurl'),(85,'Can add training file',22,'add_trainingfile'),(86,'Can change training file',22,'change_trainingfile'),(87,'Can delete training file',22,'delete_trainingfile'),(88,'Can view training file',22,'view_trainingfile'),(89,'Can add social service url',23,'add_socialserviceurl'),(90,'Can change social service url',23,'change_socialserviceurl'),(91,'Can delete social service url',23,'delete_socialserviceurl'),(92,'Can view social service url',23,'view_socialserviceurl'),(93,'Can add social service person',24,'add_socialserviceperson'),(94,'Can change social service person',24,'change_socialserviceperson'),(95,'Can delete social service person',24,'delete_socialserviceperson'),(96,'Can view social service person',24,'view_socialserviceperson'),(97,'Can add social service file',25,'add_socialservicefile'),(98,'Can change social service file',25,'change_socialservicefile'),(99,'Can delete social service file',25,'delete_socialservicefile'),(100,'Can view social service file',25,'view_socialservicefile'),(101,'Can add research url',26,'add_researchurl'),(102,'Can change research url',26,'change_researchurl'),(103,'Can delete research url',26,'delete_researchurl'),(104,'Can view research url',26,'view_researchurl'),(105,'Can add research person',27,'add_researchperson'),(106,'Can change research person',27,'change_researchperson'),(107,'Can delete research person',27,'delete_researchperson'),(108,'Can view research person',27,'view_researchperson'),(109,'Can add research file',28,'add_researchfile'),(110,'Can change research file',28,'change_researchfile'),(111,'Can delete research file',28,'delete_researchfile'),(112,'Can view research file',28,'view_researchfile'),(113,'Can add performance url',29,'add_performanceurl'),(114,'Can change performance url',29,'change_performanceurl'),(115,'Can delete performance url',29,'delete_performanceurl'),(116,'Can view performance url',29,'view_performanceurl'),(117,'Can add performance file',30,'add_performancefile'),(118,'Can change performance file',30,'change_performancefile'),(119,'Can delete performance file',30,'delete_performancefile'),(120,'Can view performance file',30,'view_performancefile'),(121,'Can add leave url',31,'add_leaveurl'),(122,'Can change leave url',31,'change_leaveurl'),(123,'Can delete leave url',31,'delete_leaveurl'),(124,'Can view leave url',31,'view_leaveurl'),(125,'Can add leave file',32,'add_leavefile'),(126,'Can change leave file',32,'change_leavefile'),(127,'Can delete leave file',32,'delete_leavefile'),(128,'Can view leave file',32,'view_leavefile'),(129,'Can add command url',33,'add_commandurl'),(130,'Can change command url',33,'change_commandurl'),(131,'Can delete command url',33,'delete_commandurl'),(132,'Can view command url',33,'view_commandurl'),(133,'Can add command person',34,'add_commandperson'),(134,'Can change command person',34,'change_commandperson'),(135,'Can delete command person',34,'delete_commandperson'),(136,'Can view command person',34,'view_commandperson'),(137,'Can add command file',35,'add_commandfile'),(138,'Can change command file',35,'change_commandfile'),(139,'Can delete command file',35,'delete_commandfile'),(140,'Can view command file',35,'view_commandfile'),(141,'Can add manager',36,'add_manager'),(142,'Can change manager',36,'change_manager'),(143,'Can delete manager',36,'delete_manager'),(144,'Can view manager',36,'view_manager'),(145,'Can add header',37,'add_header'),(146,'Can change header',37,'change_header'),(147,'Can delete header',37,'delete_header'),(148,'Can view header',37,'view_header'),(149,'Can add decoration',38,'add_decoration'),(150,'Can change decoration',38,'change_decoration'),(151,'Can delete decoration',38,'delete_decoration'),(152,'Can view decoration',38,'view_decoration');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$PDShv8LdtLS9uJpMoU3yfy$PfaVKIge0kR/NM9bbkI9Ao6fwlyA37Nske0voXDzJLM=','2023-05-20 09:07:21.141887',1,'admin','','','admin@hotmail.com',1,1,'2023-05-19 13:05:55.462351'),(4,'pbkdf2_sha256$600000$XfvlVjyrBn6YWyuhb5zQVD$X24CbiWpE/rxLj4OwbLVH7TT+38+I85Iq6UDsVST9kM=','2023-07-04 15:04:52.834064',1,'phichayapak.ph@rmuti.ac.th','Phitchayaphak','Phiphitphatphaisit','phichayapak.ph@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(5,'pbkdf2_sha256$600000$TDIApT18Kd7aDxjoEHuwX3$9/nlOsXSsSS83rwxQY5O3YkE3XETY/xbFGFVQ0GFXxM=','2023-07-04 14:59:22.141593',0,'path@hotmail.com','Pathamakorn','Nethayavijit','path@hotmail.com',1,1,'2023-05-20 10:10:15.620464'),(6,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'tassanee.lu@rmuti.ac.th','Tassanee','Loonrasri','tassanee.lu@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(7,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'arisa.kh@rmuti.ac.th','Arisa','Khethongma','arisa.kh@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(8,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'nathaporn.ji@rmuti.ac.th','์Nathaporn','Jirajesada','nathaporn.ji@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(9,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'nathaya.kh@rmuti.ac.th','์Nuthaya','Khamparanon','nathaya.kh@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(10,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'tayawut.ph@rmuti.ac.th','Thayawat','Phothongsangarun','tayawut.ph@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(11,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'arirat.ch@rmuti.ac.th','Arirat','Chuaboonkerd Noth','arirat.ch@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(12,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'supawadee.kh@rmuti.ac.th','Supawadee','Khocharat','supawadee.kh@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(13,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'khemporn.su@rmuti.ac.th','Khemporn','Summart','khemporn.su@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(14,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'Jirathikarn.ji@rmuti.ac.th','Jirathikarn','Wuthipan','Jirathikarn.ji@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(15,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'kanoknapah.so@rmuti.ac.th','Kanoknapat','Sokeiw','kanoknapah.so@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(16,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'mujarin.kh@rmuti.ac.th','Mujarin','Keawyong','mujarin.kh@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(17,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'priyakorn.na@rmuti.ac.th','Priyakorn','Nugrong','priyakorn.na@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(18,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'thanai.sr@rmuti.ac.th','Thainai','Sriesan','thanai.sr@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(19,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'thanadom.ra@rmuti.ac.th','Thanadom','Rasrirathana','thanadom.ra@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(20,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'jarapha.ch@rmuti.ac.th','Jirapha','Charathirawat','jarapha.ch@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(21,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'sudarat.ph@rmuti.ac.th','Sudarat','Phongsathitphat','sudarat.ph@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(22,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'jutharat.kh@rmuti.ac.th','Jutharat','Khunthum','jutharat.kh@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(23,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'rathanawadee.sa@rmuti.ac.th','Rathanawadee','Sangmari','rathanawadee.sa@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(24,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'ukrit.ph@rmuti.ac.th','Ukrit','Phanna','ukrit.ph@rmuti.ac.th',1,1,'2023-05-20 10:10:15.620464'),(25,'pbkdf2_sha256$600000$1qkhTT0RkDmFDeC6GoJHEi$cnrO6cjPRZcewpjLfPSRscgdMYUDIy2bBlE/aYaMfG0=','2023-05-22 13:13:57.554587',0,'wanitha.bo@rmuti.ac.th','Wanitha','Boonchome','wanitha.bo@rmuti.ac.th',0,1,'2023-05-20 10:10:15.620464'),(26,'pbkdf2_sha256$600000$QajwiaBGdWaSPeG8hAtTGc$NcWUdWqmTz28sIdFhEIIpBJmbO4d3hRqYOo3hwdPpz0=','2023-06-01 14:36:20.420685',0,'pornthapin.su@rmuti.ac.th','Pornthaphin','Suksangprasit','pornthapin.su@rmuti.ac.th',0,1,'2023-05-20 10:10:15.620464'),(27,'pbkdf2_sha256$600000$hlr5dH9Vg8XQItb58GLufF$FINIQSyVo6uyzdKhTRgxdBKxC0ZHU4XwTTe6PzHx7OE=','2023-06-01 15:23:51.753612',0,'somphong@hotmail.com','sompong','nongsomchai','somphong@hotmail.com',1,1,'2023-06-01 10:24:53.868231'),(28,'pbkdf2_sha256$600000$2O36mMlim71nFtoZcGsjAZ$E8uvvLVJrN3jHEfufcKCr17fQlj14HueQpWbRe6gRpQ=','2023-07-04 15:21:04.119828',0,'sarawut.su@rmuti.ac.th','Sarawut','Suewuthikul','sarawut.su@rmuti.ac.th',1,1,'2023-06-08 08:27:18.453459'),(29,'pbkdf2_sha256$600000$PvTWo9o5rkLZCWOuhbmpfP$4h8dHkszDZLtjQFZqnwEYA1sXnSyys9vQ8crrJMPyIw=',NULL,0,'supaporn.an@rmuti.ac.th','Supaporn','Anuphapphaiboon','supaporn.an@rmuti.ac.th',1,1,'2023-06-16 12:35:11.877994');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (74,4,1),(71,5,7),(70,6,4),(82,7,8),(55,8,4),(54,9,7),(53,10,4),(58,11,4),(56,12,7),(69,13,7),(61,14,7),(60,15,7),(67,16,7),(66,17,7),(65,18,7),(64,19,4),(62,20,4),(68,21,7),(63,22,7),(50,23,7),(52,24,7),(51,25,4),(49,26,7),(78,27,5),(84,28,8),(85,29,7);
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
-- Dumping data for table `baseapp_curraffiliation`
--

LOCK TABLES `baseapp_curraffiliation` WRITE;
/*!40000 ALTER TABLE `baseapp_curraffiliation` DISABLE KEYS */;
INSERT INTO `baseapp_curraffiliation` VALUES (1,'ผู้รับผิดชอบหลักสูตร','2023-07-04 14:33:02.536161',4,17,26);
/*!40000 ALTER TABLE `baseapp_curraffiliation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_curriculum`
--

LOCK TABLES `baseapp_curriculum` WRITE;
/*!40000 ALTER TABLE `baseapp_curriculum` DISABLE KEYS */;
INSERT INTO `baseapp_curriculum` VALUES (1,'บริหารธุรกิจบัณฑิต (สาขาเทคโนโลยีธุรกิจดิจิทัล)','Bachelor\'s of Business Administration (Digital Business Technology)',2563,'บธ.บ. (เทคโนโลยีธุรกิจดิจิทัล)','B.BA. (Digital Business Techn)','ปริญญาตรี',4,2),(2,'บัญชีบัณฑิต','Accounting',2563,'บช.','B.AC.','ปริญญาตรี',4,3),(3,'บริหารธุรกิจบัณฑิต (สาขาการตลาด)','ฺBachelor\'s of Business Administration (Marketing)',2563,'บธ.บ. (การตลาด)','B.BA. (Marketing)','ปริญญาตรี',4,5),(4,'บริหารธุรกิจบัณฑิต (สาขาการจัดการ)','Bachelor\'s of Business Administration (Management)',2563,'บธ.บ. (การจัดการ)','B.BA. (Management)','ปริญญาตรี',4,4);
/*!40000 ALTER TABLE `baseapp_curriculum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_decoration`
--

LOCK TABLES `baseapp_decoration` WRITE;
/*!40000 ALTER TABLE `baseapp_decoration` DISABLE KEYS */;
INSERT INTO `baseapp_decoration` VALUES (1,'2023-07-06 00:00:00.000000','ชั้นที่ 5','เหรียญเงินมงกุฏไทย','ร.ง.ม.','ต่ำกว่าสายสะพาย','2023-07-06 08:20:00.156637','2023-07-06 08:20:00.156637',26,23,26);
/*!40000 ALTER TABLE `baseapp_decoration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_division`
--

LOCK TABLES `baseapp_division` WRITE;
/*!40000 ALTER TABLE `baseapp_division` DISABLE KEYS */;
INSERT INTO `baseapp_division` VALUES (2,'ระบบสารสนเทศ','Information System','BIS'),(3,'การบัญชี','Accounting','BAC'),(4,'การจัดการ','Management','BMG'),(5,'การตลาด','Marketing','BMK');
/*!40000 ALTER TABLE `baseapp_division` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_education`
--

LOCK TABLES `baseapp_education` WRITE;
/*!40000 ALTER TABLE `baseapp_education` DISABLE KEYS */;
INSERT INTO `baseapp_education` VALUES (1,'ปริญญาตรี','วิทยาศาสตร์บัณฑิต (สาขาวิทยาการคอมพิวเตอร์)','Bachelor\'s of Science (Computer Science)','วท.บ. (วิทยาการคอมพิวเตอร์)','BSc. (Computer Science)',2550,'มหาวิทยาลัยขอนแก่น','2023-06-09 08:05:41.888648','2023-06-09 08:05:41.888648',28,28,28),(2,'ปริญญาโท','วิทยาศาสตร์มหาบัณฑิต (สาขาวิทยาการคอมพิวเตอร์)','Master of Science (Computer Science)','วท.ม. (วิทยาการคอมพิวเตอร์)','MSc. (Computer Science)',2551,'มหาวิทยาลัยขอนแก่น','2023-06-09 08:06:47.552034','2023-06-09 08:06:47.552034',28,28,28);
/*!40000 ALTER TABLE `baseapp_education` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_expertise`
--

LOCK TABLES `baseapp_expertise` WRITE;
/*!40000 ALTER TABLE `baseapp_expertise` DISABLE KEYS */;
/*!40000 ALTER TABLE `baseapp_expertise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_faculty`
--

LOCK TABLES `baseapp_faculty` WRITE;
/*!40000 ALTER TABLE `baseapp_faculty` DISABLE KEYS */;
INSERT INTO `baseapp_faculty` VALUES (1,'คณะบริหารธุรกิจและเทคโนโลยีสารสนเทศ','Faculty of Business Administration and Information Technology','มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน','150 ถ.ศรีจันทร์ อ.เมือง จ.ขอนแก่น','043-336371-2','https://www.fbi.rmuti.ac.th/','go together','LERD');
/*!40000 ALTER TABLE `baseapp_faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_header`
--

LOCK TABLES `baseapp_header` WRITE;
/*!40000 ALTER TABLE `baseapp_header` DISABLE KEYS */;
INSERT INTO `baseapp_header` VALUES (2,'2023-06-06 08:45:51.010243',5,4,26),(3,'2023-06-08 08:27:51.061677',2,28,26);
/*!40000 ALTER TABLE `baseapp_header` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_manager`
--

LOCK TABLES `baseapp_manager` WRITE;
/*!40000 ALTER TABLE `baseapp_manager` DISABLE KEYS */;
INSERT INTO `baseapp_manager` VALUES (1,'คณบดี','2023-06-06 08:31:12.199393',8,26),(2,'รองคณบดีฝ่ายวิชาการและวิจัย','2023-06-06 08:31:30.857778',7,26);
/*!40000 ALTER TABLE `baseapp_manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_personnel`
--

LOCK TABLES `baseapp_personnel` WRITE;
/*!40000 ALTER TABLE `baseapp_personnel` DISABLE KEYS */;
INSERT INTO `baseapp_personnel` VALUES (2,'path@hotmail.com','573','ปัทมากร','เนตยวิจิตร','Pathamakorn','Nethayavijit','ผู้ช่วยศาสตราจารย์','สายวิชาการ','หญิง','718/27 ถ.หน้าเมือง ต.ในเมือง อ.เมือง จ.ขอนแก่น 40000','2023-05-18','2023-05-18','images/personnels/2.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-06-29 11:41:59.554142',2,'นางสาว',0,'ปฏิบัติหน้าที่ปกติ',''),(3,'tassanee.lu@rmuti.ac.th','444','ทรรศนีย์','ลุนราศรี','Tassanee','Loonrasri','อาจารย์','สายวิชาการ','หญิง','ฟหกดหฟ','2023-05-18','2023-05-18','images/personnels/3.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',2,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(4,'arisa.kh@rmuti.ac.th','111','อลิษา','เกษทองมา','Arisa','Khethongma','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/4.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',5,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(5,'nathaporn.ji@rmuti.ac.th','111','นัฏพร','จิรเจษฏา','์Nathaporn','Jirajesada','ผู้ช่วยศาสตราจารย์','สายสนับสนุน','หญิง','111','2023-05-20','2023-05-20','images/personnels/5.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',5,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(6,'nathaya.kh@rmuti.ac.th','111','นทยา','กัมพลานนท์','์Nuthaya','Khamparanon','ผู้ช่วยศาสตราจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/6.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',5,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(7,'tayawut.ph@rmuti.ac.th','111','ทายาวุฒิ','โพธิ์ทองแสงอรุณ','Thayawat','Phothongsangarun','ผู้ช่วยศาสตราจารย์','สายวิชาการ','ชาย','111','2023-05-20','2023-05-20','images/personnels/7.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',5,'นาย',1,'ปฏิบัติหน้าที่ปกติ',''),(8,'arirat.ch@rmuti.ac.th','111','อารีรัตน์','เชื้อบุญเกิด โนท','Arirat','Chuaboonkerd Noth','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/8.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',5,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(9,'supawadee.kh@rmuti.ac.th','111','สุภาวดี','คชรัตน์','Supawadee','Khocharat','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/9.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',5,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(10,'khemporn.su@rmuti.ac.th','111','เข็มพร','สุ่มมาตร','Khemporn','Summart','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/10.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',3,'นาง',1,'ปฏิบัติหน้าที่ปกติ',''),(11,'Jirathikarn.ji@rmuti.ac.th','111','จิรัตติกาล','วุฒิพันธุ์','Jirathikarn','Wuthipan','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/11.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',3,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(12,'kanoknapah.so@rmuti.ac.th','111','กนกนภัทร์','โสเขียว','Kanoknapat','Sokeiw','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/12.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',3,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(13,'mujarin.kh@rmuti.ac.th','111','มุจรินทร์','แก้วหย่อง','Mujarin','Keawyong','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/13.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',3,'นาง',1,'ปฏิบัติหน้าที่ปกติ',''),(14,'priyakorn.na@rmuti.ac.th','111','ปริยากร','นักร้อง','Priyakorn','Nugrong','อาจารย์','สายวิชาการ','หญิง','11','2023-05-20','2023-05-20','images/personnels/14.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',3,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(15,'thanai.sr@rmuti.ac.th','111','ธนัย','ศรีอิสาน','Thainai','Sriesan','อาจารย์','สายวิชาการ','ชาย','111','2023-05-20','2023-05-20','images/personnels/15.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',3,'นาย',1,'ปฏิบัติหน้าที่ปกติ',''),(16,'thanadom.ra@rmuti.ac.th','111','ฐณดม','ราศรีรัตนะ','Thanadom','Rasrirathana','ผู้ช่วยศาสตราจารย์','สายวิชาการ','ชาย','222','2023-05-20','2023-05-20','images/personnels/16.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',3,'นาย',1,'ปฏิบัติหน้าที่ปกติ',''),(17,'jarapha.ch@rmuti.ac.th','111','จิราภา','ชลาธาราวัฒน์','Jirapha','Charathirawat','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/17.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',3,'นาง',1,'ปฏิบัติหน้าที่ปกติ',''),(18,'sudarat.ph@rmuti.ac.th','111','สุดารัตน์','พงษ์สถิตพัฒน์','Sudarat','Phongsathitphat','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/18.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',3,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(19,'jutharat.kh@rmuti.ac.th','111','จุฑารัตน์','คุณทุม','Jutharat','Khunthum','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/19.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',3,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(20,'rathanawadee.sa@rmuti.ac.th','111','รัตนาวดี','แสงมาลี','Rathanawadee','Sangmari','อาจารย์','สายวิชาการ','หญิง','ddd','2023-05-20','2023-05-20','images/personnels/20.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',4,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(21,'ukrit.ph@rmuti.ac.th','111','อุกฤษณ์','พรรณะ','Ukrit','Phanna','อาจารย์','สายวิชาการ','ชาย','111','2023-05-20','2023-05-20','images/personnels/21.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',4,'นาย',1,'ปฏิบัติหน้าที่ปกติ',''),(22,'wanitha.bo@rmuti.ac.th','111','วนิตา','บุญโฉม','Wanitha','Boonchome','ผู้ช่วยศาสตราจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/22.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',4,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(23,'pornthapin.su@rmuti.ac.th','111','พรเทพินทร์','สุขแสงประสิทธิ์','Pornthaphin','Suksangprasit','อาจารย์','สายวิชาการ','หญิง','111','2023-05-20','2023-05-20','images/personnels/23.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-06-01 10:36:20.901190',4,'นางสาว',1,'ปฏิบัติหน้าที่ปกติ',''),(26,'phichayapak.ph@rmuti.ac.th','4123','พิชญะภาคย์','พิพิธพัฒน์ไพสิฐ','Phitchayaphak','Phiphitphatphaisit','อาจารย์','สายวิชาการ','ชาย','255/7','2515-12-07','2541-06-22','images/personnels/26.jpg',26,'2023-05-29 08:05:36.959981',26,'2023-05-29 08:05:36.959981',2,'นาย',1,'ปฏิบัติหน้าที่ปกติ',''),(27,'somphong@hotmail.com','11111','สมปอง','น้องสมชาย','sompong','nongsomchai','ไม่มี','สายสนับสนุน','ชาย','khonkean','2023-06-01','2023-06-03','images/personnels/27.png',26,'2023-06-01 10:24:53.718840',26,'2023-06-01 15:23:36.905052',2,'นาย',1,'ปฏิบัติหน้าที่ปกติ',''),(28,'sarawut.su@rmuti.ac.th','1234','ศราวุธ','ซื่อวุฒิกุล','Sarawut','Suewuthikul','อาจารย์','สายวิชาการ','ชาย','555 ขอนแก่น','2023-06-08','2023-06-08','images/personnels/28.jpg',26,'2023-06-08 08:27:18.324309',26,'2023-06-08 08:27:18.324309',2,'นาย',1,'ปฏิบัติหน้าที่ปกติ',''),(29,'supaporn.an@rmuti.ac.th','697','สุภาภรณ์','อนุภาพไพรบูรณ์','Supaporn','Anuphapphaiboon','อาจารย์','สายวิชาการ','หญิง','150 มทร. อีสาน วิทยาเขตขอนแก่น 40000','2514-06-16','2540-01-17','images/personnels/29.jpg',26,'2023-06-16 12:35:11.749416',26,'2023-06-16 12:38:34.560299',2,'นาง',1,'ปฏิบัติหน้าที่ปกติ','');
/*!40000 ALTER TABLE `baseapp_personnel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_responsible`
--

LOCK TABLES `baseapp_responsible` WRITE;
/*!40000 ALTER TABLE `baseapp_responsible` DISABLE KEYS */;
/*!40000 ALTER TABLE `baseapp_responsible` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(13,'baseapp','curraffiliation'),(12,'baseapp','curriculum'),(38,'baseapp','decoration'),(7,'baseapp','division'),(11,'baseapp','education'),(10,'baseapp','expertise'),(8,'baseapp','faculty'),(37,'baseapp','header'),(36,'baseapp','manager'),(9,'baseapp','personnel'),(14,'baseapp','responsible'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(15,'workapp','command'),(35,'workapp','commandfile'),(34,'workapp','commandperson'),(33,'workapp','commandurl'),(16,'workapp','leave'),(32,'workapp','leavefile'),(31,'workapp','leaveurl'),(17,'workapp','performance'),(30,'workapp','performancefile'),(29,'workapp','performanceurl'),(18,'workapp','research'),(28,'workapp','researchfile'),(27,'workapp','researchperson'),(26,'workapp','researchurl'),(19,'workapp','socialservice'),(25,'workapp','socialservicefile'),(24,'workapp','socialserviceperson'),(23,'workapp','socialserviceurl'),(20,'workapp','training'),(22,'workapp','trainingfile'),(21,'workapp','trainingurl');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-06-01 10:00:02.707883'),(2,'auth','0001_initial','2023-06-01 10:00:29.207043'),(3,'admin','0001_initial','2023-06-01 10:00:36.282723'),(4,'admin','0002_logentry_remove_auto_add','2023-06-01 10:00:36.639077'),(5,'admin','0003_logentry_add_action_flag_choices','2023-06-01 10:00:36.879155'),(6,'contenttypes','0002_remove_content_type_name','2023-06-01 10:00:41.374958'),(7,'auth','0002_alter_permission_name_max_length','2023-06-01 10:00:42.708291'),(8,'auth','0003_alter_user_email_max_length','2023-06-01 10:00:44.858466'),(9,'auth','0004_alter_user_username_opts','2023-06-01 10:00:45.025939'),(10,'auth','0005_alter_user_last_login_null','2023-06-01 10:00:46.384255'),(11,'auth','0006_require_contenttypes_0002','2023-06-01 10:00:46.546014'),(12,'auth','0007_alter_validators_add_error_messages','2023-06-01 10:00:46.625039'),(13,'auth','0008_alter_user_username_max_length','2023-06-01 10:00:48.352482'),(14,'auth','0009_alter_user_last_name_max_length','2023-06-01 10:00:53.171448'),(15,'auth','0010_alter_group_name_max_length','2023-06-01 10:00:56.754109'),(16,'auth','0011_update_proxy_permissions','2023-06-01 10:00:56.900331'),(17,'auth','0012_alter_user_first_name_max_length','2023-06-01 10:00:59.046317'),(18,'baseapp','0001_initial','2023-06-01 10:01:47.229329'),(19,'baseapp','0002_remove_curraffiliation_editdate_and_more','2023-06-01 10:01:51.860832'),(20,'baseapp','0003_personnel_title','2023-06-01 10:01:53.029230'),(21,'baseapp','0004_responsible_delete_permission','2023-06-01 10:02:03.148523'),(22,'sessions','0001_initial','2023-06-01 10:02:05.050186'),(23,'workapp','0001_initial','2023-06-01 10:04:30.297688'),(24,'workapp','0002_performance_editor_performance_editordate_and_more','2023-06-01 10:04:35.311237'),(25,'workapp','0003_rename_editordate_performance_editdate_and_more','2023-06-01 10:04:36.636501'),(26,'baseapp','0005_manager_header','2023-06-06 08:30:24.904825'),(27,'workapp','0004_remove_research_percent_resp','2023-06-08 08:20:02.301108'),(28,'workapp','0005_alter_researchperson_status_and_more','2023-06-08 12:41:02.288699'),(29,'workapp','0006_rename_editdate_leavefile_recorddate_and_more','2023-06-12 08:11:09.733623'),(30,'workapp','0007_commandurl_description_leaveurl_description_and_more','2023-06-12 08:11:19.539160'),(31,'workapp','0008_alter_commandurl_description_and_more','2023-06-12 08:11:19.884673'),(32,'workapp','0009_remove_research_keyword_research_reference','2023-06-23 09:23:48.985891'),(33,'workapp','0002_leave_editable','2023-06-29 15:38:10.130997'),(34,'baseapp','0002_personnel_currently_personnel_telephone_and_more','2023-07-06 08:19:17.046546'),(35,'workapp','0003_rename_percent_success_research_percentsuccess_and_more','2023-07-06 08:19:27.877652');
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
INSERT INTO `workapp_command` VALUES (1,'123/2566','2566-06-06',2566,2566,1,'การจัดการเรียนการสอน','แต่งตั้งกรรมการคุมสอบกลางภาค 3/2565','สอบกลางภาค','2023-06-06 08:53:30.628318','2023-06-06 08:53:51.419426',2,2),(2,'123/2565','2566-06-12',2566,2565,1,'การจัดการเรียนการสอน','คุมสอบ','หกดห','2023-06-12 08:10:32.256059','2023-06-12 08:10:32.256059',28,28),(3,'12345/2565','2566-06-12',2566,2565,1,'การจัดการเรียนการสอน','คุมสอบ','กหดหฟดหฟ\r\nฟหกดห\r\nดฟห\r\nดฟหกด','2023-06-12 08:12:08.728627','2023-06-12 08:12:08.728627',28,28),(4,'123/2565','2566-06-12',2566,2565,1,'การบริการทางวิชาการแก่สังคม','กหดหดหฟดฟหด','หฟดหฟดหกดห','2023-06-12 08:12:37.666016','2023-06-12 08:25:39.891411',26,26),(5,'123456/2566','2566-06-12',2566,2566,1,'การวิจัย','หกดหฟ','ดฟหด','2023-06-12 08:20:12.713036','2023-07-04 14:58:05.207565',26,26),(6,'111/2566','2566-06-12',2566,2566,1,'การบริการทางวิชาการแก่สังคม','sdf','sdfsaf','2023-06-12 08:21:06.909883','2023-06-12 08:25:22.749046',26,26);
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
INSERT INTO `workapp_commandperson` VALUES (1,'กรรมการสอบ','2023-06-06 08:53:30.748043',1,2,2),(2,'กรรมการ','2023-06-06 08:53:50.694147',1,12,2),(3,'กรรมการ','2023-06-06 08:53:50.769792',1,19,2),(4,'กรรมการ','2023-06-06 08:53:50.958655',1,16,2),(5,'กรรมการ','2023-06-06 08:53:51.007379',1,3,2),(6,'กรรมการ','2023-06-06 08:53:51.218114',1,7,2),(7,'กรรมการ','2023-06-06 08:53:51.318128',1,15,2),(8,'กรรมการ','2023-07-04 14:58:04.885838',5,12,26),(9,'กรรมการ','2023-07-04 14:58:04.946884',5,11,26),(10,'กรรมการ','2023-07-04 14:58:05.044828',5,17,26),(11,'กรรมการ','2023-07-04 14:58:05.128526',5,19,26),(12,'กรรมการ','2023-07-04 14:58:05.170980',5,16,26);
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
INSERT INTO `workapp_leave` VALUES (1,'2566-06-06','2566-06-06',1,2566,'ลาป่วย','ลาพักผ่อน','2023-06-06 08:52:21.215372','2023-06-06 08:52:21.215372',2,2,2,1),(2,'2566-06-13','2566-06-13',1,2565,'ลาป่วย','sadfsaf','2023-06-13 16:20:04.913454','2023-06-13 16:20:45.922854',26,2,26,1),(3,'2566-06-13','2566-06-13',1,2565,'ลาป่วย','sdfsa','2023-06-13 16:20:14.445888','2023-06-13 16:20:14.445888',26,2,26,1),(4,'2566-06-13','2566-06-13',1,2565,'ลาป่วย','sdfasfsa','2023-06-13 16:20:28.272297','2023-06-13 16:20:28.272297',26,2,26,1),(5,'2566-06-13','2566-06-13',1,2566,'ลาป่วย','sdfasfsafas','2023-06-13 16:21:02.399808','2023-06-29 15:39:51.359416',26,2,26,0),(6,'2566-06-01','2566-06-10',10,2566,'ลาพักผ่อนประจำปี','พักผ่อน','2023-06-16 09:47:19.049179','2023-06-16 09:47:19.049179',26,23,26,1);
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
INSERT INTO `workapp_performance` VALUES (1,'2566-06-22',2566,2566,1,'นักวิจัยดีเด่น','นักวิจัยดีเด่น ด้านการมีส่วนร่วมกับชุมชน',0,'ไม่ใช้งบประมาณ','กระทรวงวิทยาศาสตร์','2023-06-22 11:40:25.196675',23,26,26,'2023-06-22 11:40:25.196675');
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
INSERT INTO `workapp_research` VALUES (1,2566,'การจำแนกประเภทสินค้าด้วยเทคโนโลยีประมวลผลภาพ','Data classification with image processing','ศึกษาการจำแนกประเภทสินค้ด้วยภาพ',100000,'งบประมาณภายนอก','มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน',100,'การประชุมวิชาการ','2023-06-08 08:34:13.590189','2023-06-23 09:28:18.537923',26,26,'กนกนภัส  โสเขียว และคณะ. (2566). การจำแนกประเภทสินค้าด้วยเทคโนโลยีประมวลผลภาพ. สมาคมการวิจัยแห่งชาติ. 12(10). หน้า 65-85.','0000-00-00',''),(2,2566,'การศึกษาการพัฒนาองค์กรดิจิทัล','fdasfasf','asfasfasf',10000,'งบประมาณรายได้','มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน',100,'การประชุมวิชาการ','2023-06-08 08:36:14.813103','2023-06-08 08:42:13.211950',28,28,'-','0000-00-00',''),(3,2567,'การศึกษาการท่องเที่ยวเชิงนวตกรรม','Study of Travel on Innovation','ศึกษา\r\nวิจัย\r\nสรุปผล',500000,'งบประมาณภายนอก','กระทรวง อว.',100,'การประชุมวิชาการ','2023-06-13 15:43:45.125771','2023-07-04 14:51:42.759404',26,26,'อารีรัตน์ เชื้อบุญเกิด โนท และคณะ. (2565). การศึกษาการท่องเที่ยวเชิงนวตกรรม. สมาคมการวิจัยแห่งชาติ. 12(10). หน้า 55-65.','0000-00-00','');
/*!40000 ALTER TABLE `workapp_research` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_researchfile`
--

LOCK TABLES `workapp_researchfile` WRITE;
/*!40000 ALTER TABLE `workapp_researchfile` DISABLE KEYS */;
INSERT INTO `workapp_researchfile` VALUES (1,'[3_1]-ผล_simulate_AP_แบบเดม.pdf','pdf','2023-07-04 14:51:42.649761',26,3);
/*!40000 ALTER TABLE `workapp_researchfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_researchperson`
--

LOCK TABLES `workapp_researchperson` WRITE;
/*!40000 ALTER TABLE `workapp_researchperson` DISABLE KEYS */;
INSERT INTO `workapp_researchperson` VALUES (1,'หัวหน้าโครงการวิจัย','2023-06-08 08:37:06.877480',28,28,2,50),(2,'นักวิจัยร่วม','2023-06-08 08:37:21.323531',3,28,2,20),(4,'นักวิจัยร่วม','2023-06-08 08:42:13.168654',2,28,2,30),(6,'หัวหน้าโครงการวิจัย','2023-06-13 15:33:07.972374',12,26,1,50),(10,'นักวิจัยร่วม','2023-06-13 15:41:13.681472',11,26,1,10),(11,'นักวิจัยร่วม','2023-06-13 15:41:13.793701',17,26,1,10),(12,'นักวิจัยร่วม','2023-06-13 15:41:13.851901',19,26,1,10),(13,'นักวิจัยร่วม','2023-06-13 15:41:13.989829',16,26,1,10),(14,'หัวหน้าโครงการวิจัย','2023-06-13 15:56:40.253041',6,26,3,50),(16,'ผู้ร่วมวิจัย','2023-06-13 15:57:06.959691',9,26,3,10),(17,'ผู้ร่วมวิจัย','2023-06-13 15:57:07.162901',4,26,3,10),(18,'ผู้ร่วมวิจัย','2023-06-13 15:57:07.287015',8,26,3,10),(19,'ผู้ร่วมวิจัย','2023-06-13 15:57:35.368422',5,26,3,20),(20,'นักวิจัยร่วม','2023-06-23 09:28:18.453549',22,26,1,10);
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
INSERT INTO `workapp_socialservice` VALUES (1,'2566-06-08','2566-06-08',1,2566,2566,1,'โครงการอบรมวิชาชีพ การขายสินค้าบนเว็บ','','บ้านสงเปือย อ.ภูเวียง จ.ขอนแก่น',100000,'งบประมาณรายได้','มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน','กลุ่มวิสาหกิจชุมชน',50,'2023-06-08 12:44:12.875083','2023-06-09 08:13:16.196362',28,28);
/*!40000 ALTER TABLE `workapp_socialservice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_socialservicefile`
--

LOCK TABLES `workapp_socialservicefile` WRITE;
/*!40000 ALTER TABLE `workapp_socialservicefile` DISABLE KEYS */;
INSERT INTO `workapp_socialservicefile` VALUES (1,'[1_1]-ACM-AIS-is2020.pdf','pdf','2023-06-09 08:12:49.598552',28,1);
/*!40000 ALTER TABLE `workapp_socialservicefile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_socialserviceperson`
--

LOCK TABLES `workapp_socialserviceperson` WRITE;
/*!40000 ALTER TABLE `workapp_socialserviceperson` DISABLE KEYS */;
INSERT INTO `workapp_socialserviceperson` VALUES (1,'ผู้ร่วมโครงการ','2023-06-09 08:12:30.430565',3,28,1),(2,'ผู้ร่วมโครงการ','2023-06-09 08:12:30.503403',2,28,1),(3,'ผู้ร่วมโครงการ','2023-06-09 08:12:30.602613',26,28,1);
/*!40000 ALTER TABLE `workapp_socialserviceperson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_socialserviceurl`
--

LOCK TABLES `workapp_socialserviceurl` WRITE;
/*!40000 ALTER TABLE `workapp_socialserviceurl` DISABLE KEYS */;
INSERT INTO `workapp_socialserviceurl` VALUES (1,'http://www.tamplet.com','2023-06-09 08:13:04.101603',28,1,''),(2,'http://github.com','2023-06-09 08:13:16.058049',28,1,'');
/*!40000 ALTER TABLE `workapp_socialserviceurl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_training`
--

LOCK TABLES `workapp_training` WRITE;
/*!40000 ALTER TABLE `workapp_training` DISABLE KEYS */;
INSERT INTO `workapp_training` VALUES (1,'2566-06-06','2566-06-06',1,2566,2566,1,'การวิจัยเชิงนวตกรรม','วิทยาเขตขอนแก่น',0,'ไม่ใช้งบประมาณ','2023-06-06 08:50:11.644455','2023-06-06 08:50:47.211190',2,2,2),(2,'2566-06-13','2566-06-13',1,2566,2566,1,'sdfsa','sadfasf',25000,'งบประมาณภายนอก','2023-06-13 16:21:45.952468','2023-06-15 15:50:51.233101',26,23,26),(3,'2566-06-01','2566-06-01',1,2567,2567,1,'dsafasfsa','fdsafasfas',5000,'งบประมาณส่วนตัว','2023-06-13 16:22:05.328760','2023-06-15 15:50:42.733852',26,23,26);
/*!40000 ALTER TABLE `workapp_training` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_trainingfile`
--

LOCK TABLES `workapp_trainingfile` WRITE;
/*!40000 ALTER TABLE `workapp_trainingfile` DISABLE KEYS */;
INSERT INTO `workapp_trainingfile` VALUES (1,'[3_1]-weScore.xls','xls','2023-07-04 14:35:14.325480',26,3);
/*!40000 ALTER TABLE `workapp_trainingfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_trainingurl`
--

LOCK TABLES `workapp_trainingurl` WRITE;
/*!40000 ALTER TABLE `workapp_trainingurl` DISABLE KEYS */;
INSERT INTO `workapp_trainingurl` VALUES (1,'http://google.com','2023-07-04 14:36:45.345384',26,3,'ไฟล์แนบ');
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

-- Dump completed on 2023-07-06 13:07:45
