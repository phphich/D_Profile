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
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add division',7,'add_division'),(26,'Can change division',7,'change_division'),(27,'Can delete division',7,'delete_division'),(28,'Can view division',7,'view_division'),(29,'Can add faculty',8,'add_faculty'),(30,'Can change faculty',8,'change_faculty'),(31,'Can delete faculty',8,'delete_faculty'),(32,'Can view faculty',8,'view_faculty'),(33,'Can add personnel',9,'add_personnel'),(34,'Can change personnel',9,'change_personnel'),(35,'Can delete personnel',9,'delete_personnel'),(36,'Can view personnel',9,'view_personnel'),(37,'Can add expertise',10,'add_expertise'),(38,'Can change expertise',10,'change_expertise'),(39,'Can delete expertise',10,'delete_expertise'),(40,'Can view expertise',10,'view_expertise'),(41,'Can add education',11,'add_education'),(42,'Can change education',11,'change_education'),(43,'Can delete education',11,'delete_education'),(44,'Can view education',11,'view_education'),(45,'Can add documents',12,'add_documents'),(46,'Can change documents',12,'change_documents'),(47,'Can delete documents',12,'delete_documents'),(48,'Can view documents',12,'view_documents'),(49,'Can add curriculum',13,'add_curriculum'),(50,'Can change curriculum',13,'change_curriculum'),(51,'Can delete curriculum',13,'delete_curriculum'),(52,'Can view curriculum',13,'view_curriculum'),(53,'Can add curr affiliation',14,'add_curraffiliation'),(54,'Can change curr affiliation',14,'change_curraffiliation'),(55,'Can delete curr affiliation',14,'delete_curraffiliation'),(56,'Can view curr affiliation',14,'view_curraffiliation'),(57,'Can add training',15,'add_training'),(58,'Can change training',15,'change_training'),(59,'Can delete training',15,'delete_training'),(60,'Can view training',15,'view_training'),(61,'Can add social service',16,'add_socialservice'),(62,'Can change social service',16,'change_socialservice'),(63,'Can delete social service',16,'delete_socialservice'),(64,'Can view social service',16,'view_socialservice'),(65,'Can add research',17,'add_research'),(66,'Can change research',17,'change_research'),(67,'Can delete research',17,'delete_research'),(68,'Can view research',17,'view_research'),(69,'Can add performance',18,'add_performance'),(70,'Can change performance',18,'change_performance'),(71,'Can delete performance',18,'delete_performance'),(72,'Can view performance',18,'view_performance'),(73,'Can add leave',19,'add_leave'),(74,'Can change leave',19,'change_leave'),(75,'Can delete leave',19,'delete_leave'),(76,'Can view leave',19,'view_leave'),(77,'Can add command',20,'add_command'),(78,'Can change command',20,'change_command'),(79,'Can delete command',20,'delete_command'),(80,'Can view command',20,'view_command');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$hpHdCcRlr2D8mTNjHTko8J$gztH7jU/ojBGQIJmt6OF5cHiykJv5BRxArvIa5C19rI=','2023-05-05 00:36:39.915211',1,'admin','','','admin@rmuti.ac.th',1,1,'2023-05-03 15:02:27.419352');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
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
INSERT INTO `baseapp_curraffiliation` VALUES (1,'อาจารย์ประจำหลักสูตร','2023-05-05 11:42:45.736177',1,1,1),(3,'อาจารย์ประจำหลักสูตร','2023-05-05 14:04:46.619821',1,4,1),(6,'ผู้รับผิดชอบหลักสูตร','2023-05-05 14:10:03.000880',4,10,1),(7,'อาจารย์ประจำหลักสูตร','2023-05-05 14:10:14.484199',4,4,1),(9,'อาจารย์ประจำหลักสูตร','2023-05-05 14:18:05.563198',1,9,1),(18,'อาจารย์ประจำหลักสูตร','2023-05-05 14:38:07.447182',3,11,1);
/*!40000 ALTER TABLE `baseapp_curraffiliation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_curriculum`
--

LOCK TABLES `baseapp_curriculum` WRITE;
/*!40000 ALTER TABLE `baseapp_curriculum` DISABLE KEYS */;
INSERT INTO `baseapp_curriculum` VALUES (1,'บริหารธุรกิจบัณฑิต (สาขาเทคโนโลยีธุรกิจดิจิทัล)','Bachelor\'s of Business Administration (Digital Business Technology)','บธ.บ. (เทคโนโลยีธุรกิจดิจิทัล)','B.BA. (Digital Business Technology)','ปริญญาตรี',4,1),(3,'บริหารธุรกิจบัณฑิต (สาขาการจัดการ)','Bachelor\'s of Business Administration (Management)','บธ.บ. (การจัดการ)','B.BA. (Management)','ปริญญาตรี',4,4),(4,'บริหารธุรกิจบัณฑิต (การตลาด)','ฺBachelor\'s of Business Administration (Marketing)','บธ.บ. (การตลาด)','B.BA. (Margeting)','ปริญญาโท',3,3);
/*!40000 ALTER TABLE `baseapp_curriculum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_division`
--

LOCK TABLES `baseapp_division` WRITE;
/*!40000 ALTER TABLE `baseapp_division` DISABLE KEYS */;
INSERT INTO `baseapp_division` VALUES (1,'ระบบสารสนเทศ','Information System','ฺBIS'),(2,'การบัญชี','Accounting','BAC'),(3,'การตลาด','Marketing','BMK'),(4,'การจัดการ','Management','BMG');
/*!40000 ALTER TABLE `baseapp_division` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_documents`
--

LOCK TABLES `baseapp_documents` WRITE;
/*!40000 ALTER TABLE `baseapp_documents` DISABLE KEYS */;
/*!40000 ALTER TABLE `baseapp_documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_education`
--

LOCK TABLES `baseapp_education` WRITE;
/*!40000 ALTER TABLE `baseapp_education` DISABLE KEYS */;
INSERT INTO `baseapp_education` VALUES (1,'ปริญญาตรี','บริหารธุรกิจบัณฑิต (ระบบสารสนเทศ)','Bachelor\'s of Business Administration (Information System)','บธ.บ. (ระบบสารสนเทศ)','B.BA. (Information System)',2541,'สถาบันเทคโนโลยีราชมงคล','2023-05-05 03:44:49.186653',1,1),(2,'ปริญญาโท','บริหารธุรกิจบัณฑิต (ระบบสารสนเทศ)dddd','Bachelor\'s of Business Administration (Information System)dddd','บธ.บ. (ระบบสารสนเทศ)ddd','B.BA. (Information System)',2545,'สจพ.','2023-05-05 03:47:58.185136',1,1),(5,'ปริญญาเอก','ปรัชญาดุษฏีบัณฑิต (สารสนเทศศึกษา)','Doctoral Philosophy (Information Studies)','ป.รด. (สารสนเทศศึกษา)','Ph.D. (Information Studies)',2561,'มหาวิทยาลัยขอนแก่น','2023-05-05 05:10:56.356046',1,1),(7,'ปริญญาตรี','บริหารธุรกิจบัณฑิต (ระบบสารสนเทศ)','Bachelor\'s of Business Administration (Information System)','บธ.บ. (ระบบสารสนเทศ)','ฺB.BA. (Information System)',2540,'สถาบันเทคโนโลยีราชมงคล','2023-05-05 08:01:48.547444',9,9);
/*!40000 ALTER TABLE `baseapp_education` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_expertise`
--

LOCK TABLES `baseapp_expertise` WRITE;
/*!40000 ALTER TABLE `baseapp_expertise` DISABLE KEYS */;
INSERT INTO `baseapp_expertise` VALUES (1,'การจัดการฐานข้อมูลกกกก','หกดหฟดกกหฟดฟหดกดห\r\nหกฟดฟห\r\nหกดฟหด','กฟหดฟหกด\r\nหกฟด\r\nฟหกดฟหหฟดฟหดฟหด','2023-05-05 06:18:13.740563',1,1),(2,'การเขียนโปรแกรม','หกดหฟดฟห','ดฟหดฟหดฟหด','2023-05-05 06:18:23.302141',1,1),(3,'การวิเคราะห์และออกแบบระบบ','กฟหดฟหด','กหดฟหดฟหดกฟหดกหฟด','2023-05-05 06:18:35.188762',1,1);
/*!40000 ALTER TABLE `baseapp_expertise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_faculty`
--

LOCK TABLES `baseapp_faculty` WRITE;
/*!40000 ALTER TABLE `baseapp_faculty` DISABLE KEYS */;
INSERT INTO `baseapp_faculty` VALUES (1,'คณะบริหารธุรกิจและเทคโนโลยีสารสนเทศ','Faculty of Business Administration and Information Technology','มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน วิทยาเขตขอนแก่น','150 ถ.ศรีจันทร์ ต.ในเมือง อ.เมือง จ.ขอนแก่น','043-336371-2','้้http://fib.rmuti.ac.th','LERD','BEST and GOOD');
/*!40000 ALTER TABLE `baseapp_faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `baseapp_personnel`
--

LOCK TABLES `baseapp_personnel` WRITE;
/*!40000 ALTER TABLE `baseapp_personnel` DISABLE KEYS */;
INSERT INTO `baseapp_personnel` VALUES (1,'phichayapak.ph@rmuti.ac.th','412','พิชญะภาคย์','พิพิธพัฒน์ไพสิฐ','Phitchayaphak','Phiphitphatphaisit','อาจารย์','สายวิชาการ','ชาย','255/7000','2515-12-07','2541-06-22','images/personnels/1.jpg',1),(4,'khemporn.su@rmuti.ac.th','333','เข็มพร','สุ่มมาตร','Khemporn','Summart','อาจารย์','สายวิชาการ','หญิง','3333','1111-01-01','2222-02-02','images/personnels/4.png',2),(9,'supaporn.an@hotmail.com','555','สุภาภรณ์','อนุภาพไพรบูรณ์','Supaporn','Anuphapphaiboon','อาจารย์','สายวิชาการ','หญิง','KKC','1111-01-01','2222-02-02','images/personnels/9.png',1),(10,'nathaporn.ji@rmuti.ac.th','111','นัฏพร','จิรเจษฏา','Nathaporn','Jirajesada','ผู้ช่วยศาสตราจารย์','สายวิชาการ','หญิง','HP Home Khonkean','2514-12-13','2537-01-01','images/personnels/10.png',3),(11,'Jirathikarn.ji@hotmail.com','4444','จิรัตติกาล','จิระพัน','Jirathikarn','Jiraphan','อาจารย์','สายวิชาการ','หญิง','MK','1010-01-01','2020-02-01','images/personnels/11.png',2);
/*!40000 ALTER TABLE `baseapp_personnel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2023-05-03 15:12:02.639192','1','คณะบริหารธุรกิจและเทคโนโลยีสารสนเทศ มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน วิทยาเขตขอนแก่น',1,'[{\"added\": {}}]',8,1),(2,'2023-05-03 15:12:20.364925','1','ระบบสารสนเทศ (ฺBIS)',1,'[{\"added\": {}}]',7,1),(3,'2023-05-03 15:12:41.871198','1','บริหารธุรกิจบัณฑิต (สาขาเทคโนโลยีธุรกิจดิจิทัล)',1,'[{\"added\": {}}]',13,1),(4,'2023-05-05 00:37:03.711992','2','การบัญชี (Acc.)',1,'[{\"added\": {}}]',7,1),(5,'2023-05-05 00:37:17.437423','3','การตลาด (BMK)',1,'[{\"added\": {}}]',7,1),(6,'2023-05-05 00:37:26.830761','2','การบัญชี (BAC)',2,'[{\"changed\": {\"fields\": [\"Name sh\"]}}]',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(14,'baseapp','curraffiliation'),(13,'baseapp','curriculum'),(7,'baseapp','division'),(12,'baseapp','documents'),(11,'baseapp','education'),(10,'baseapp','expertise'),(8,'baseapp','faculty'),(9,'baseapp','personnel'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(20,'workapp','command'),(19,'workapp','leave'),(18,'workapp','performance'),(17,'workapp','research'),(16,'workapp','socialservice'),(15,'workapp','training');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-05-03 13:58:57.540472'),(2,'auth','0001_initial','2023-05-03 13:59:18.209716'),(3,'admin','0001_initial','2023-05-03 13:59:27.225095'),(4,'admin','0002_logentry_remove_auto_add','2023-05-03 13:59:27.530399'),(5,'admin','0003_logentry_add_action_flag_choices','2023-05-03 13:59:27.808406'),(6,'contenttypes','0002_remove_content_type_name','2023-05-03 13:59:31.576049'),(7,'auth','0002_alter_permission_name_max_length','2023-05-03 13:59:33.395474'),(8,'auth','0003_alter_user_email_max_length','2023-05-03 13:59:35.811221'),(9,'auth','0004_alter_user_username_opts','2023-05-03 13:59:35.857635'),(10,'auth','0005_alter_user_last_login_null','2023-05-03 13:59:37.488002'),(11,'auth','0006_require_contenttypes_0002','2023-05-03 13:59:37.640176'),(12,'auth','0007_alter_validators_add_error_messages','2023-05-03 13:59:37.730582'),(13,'auth','0008_alter_user_username_max_length','2023-05-03 13:59:41.867161'),(14,'auth','0009_alter_user_last_name_max_length','2023-05-03 13:59:45.971696'),(15,'auth','0010_alter_group_name_max_length','2023-05-03 13:59:47.805650'),(16,'auth','0011_update_proxy_permissions','2023-05-03 13:59:47.851624'),(17,'auth','0012_alter_user_first_name_max_length','2023-05-03 13:59:49.826931'),(18,'baseapp','0001_initial','2023-05-03 14:00:27.897693'),(19,'sessions','0001_initial','2023-05-03 14:00:30.010491'),(20,'workapp','0001_initial','2023-05-03 14:01:18.466032');
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
-- Dumping data for table `workapp_leave`
--

LOCK TABLES `workapp_leave` WRITE;
/*!40000 ALTER TABLE `workapp_leave` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_leave` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_performance`
--

LOCK TABLES `workapp_performance` WRITE;
/*!40000 ALTER TABLE `workapp_performance` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_performance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_research`
--

LOCK TABLES `workapp_research` WRITE;
/*!40000 ALTER TABLE `workapp_research` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_research` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `workapp_socialservice`
--

LOCK TABLES `workapp_socialservice` WRITE;
/*!40000 ALTER TABLE `workapp_socialservice` DISABLE KEYS */;
/*!40000 ALTER TABLE `workapp_socialservice` ENABLE KEYS */;
UNLOCK TABLES;

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

-- Dump completed on 2023-05-05 22:58:28
