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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=157 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=341 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `curriculumYear` int NOT NULL,
  `name_th_sh` varchar(50) NOT NULL,
  `name_en_sh` varchar(50) NOT NULL,
  `level` varchar(30) NOT NULL,
  `studyTime` int NOT NULL,
  `division_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baseapp_curriculum_division_id_fda5c50e_fk_baseapp_division_id` (`division_id`),
  CONSTRAINT `baseapp_curriculum_division_id_fda5c50e_fk_baseapp_division_id` FOREIGN KEY (`division_id`) REFERENCES `baseapp_division` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baseapp_decoration`
--

DROP TABLE IF EXISTS `baseapp_decoration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baseapp_decoration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `name_sh` varchar(30) NOT NULL,
  `level` varchar(15) NOT NULL,
  `type` varchar(30) NOT NULL,
  `getDate` date NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `editDate` datetime(6) NOT NULL,
  `editor_id` bigint NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baseapp_decoration_editor_id_5f701b6c_fk_baseapp_personnel_id` (`editor_id`),
  KEY `baseapp_decoration_personnel_id_e83d9838_fk_baseapp_personnel_id` (`personnel_id`),
  KEY `baseapp_decoration_recorder_id_b6d675bc_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `baseapp_decoration_editor_id_5f701b6c_fk_baseapp_personnel_id` FOREIGN KEY (`editor_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `baseapp_decoration_personnel_id_e83d9838_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `baseapp_decoration_recorder_id_b6d675bc_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `editDate` datetime(6) NOT NULL,
  `editor_id` bigint NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baseapp_education_editor_id_cf8f8d1f_fk_baseapp_personnel_id` (`editor_id`),
  KEY `baseapp_education_personnel_id_2adcd2d8_fk_baseapp_personnel_id` (`personnel_id`),
  KEY `baseapp_education_recorder_id_38379db0_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `baseapp_education_editor_id_cf8f8d1f_fk_baseapp_personnel_id` FOREIGN KEY (`editor_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `baseapp_education_personnel_id_2adcd2d8_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `baseapp_education_recorder_id_38379db0_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `editDate` datetime(6) NOT NULL,
  `editor_id` bigint NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baseapp_expertise_editor_id_e7545d7b_fk_baseapp_personnel_id` (`editor_id`),
  KEY `baseapp_expertise_personnel_id_8b0457dc_fk_baseapp_personnel_id` (`personnel_id`),
  KEY `baseapp_expertise_recorder_id_5711daad_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `baseapp_expertise_editor_id_e7545d7b_fk_baseapp_personnel_id` FOREIGN KEY (`editor_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `baseapp_expertise_personnel_id_8b0457dc_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `baseapp_expertise_recorder_id_5711daad_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
-- Table structure for table `baseapp_header`
--

DROP TABLE IF EXISTS `baseapp_header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baseapp_header` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `recordDate` datetime(6) NOT NULL,
  `division_id` bigint NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baseapp_header_division_id_32a80b85_fk_baseapp_division_id` (`division_id`),
  KEY `baseapp_header_personnel_id_badbbd49_fk_baseapp_personnel_id` (`personnel_id`),
  KEY `baseapp_header_recorder_id_c51159ad_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `baseapp_header_division_id_32a80b85_fk_baseapp_division_id` FOREIGN KEY (`division_id`) REFERENCES `baseapp_division` (`id`),
  CONSTRAINT `baseapp_header_personnel_id_badbbd49_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `baseapp_header_recorder_id_c51159ad_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baseapp_manager`
--

DROP TABLE IF EXISTS `baseapp_manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baseapp_manager` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(50) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baseapp_manager_personnel_id_42186f11_fk_baseapp_personnel_id` (`personnel_id`),
  KEY `baseapp_manager_recorder_id_3d553082_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `baseapp_manager_personnel_id_42186f11_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `baseapp_manager_recorder_id_3d553082_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `type` varchar(50) NOT NULL,
  `gender` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `birthDate` date NOT NULL,
  `hiringDate` date NOT NULL,
  `picture` varchar(100) NOT NULL,
  `recorderId` int NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `editorId` int NOT NULL,
  `editDate` datetime(6) NOT NULL,
  `division_id` bigint NOT NULL,
  `title` varchar(20) NOT NULL,
  `editable` tinyint(1) NOT NULL,
  `currently` varchar(50) NOT NULL,
  `telephone` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `baseapp_personnel_division_id_fb67c60a_fk_baseapp_division_id` (`division_id`),
  CONSTRAINT `baseapp_personnel_division_id_fb67c60a_fk_baseapp_division_id` FOREIGN KEY (`division_id`) REFERENCES `baseapp_division` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baseapp_responsible`
--

DROP TABLE IF EXISTS `baseapp_responsible`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baseapp_responsible` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `recordDate` datetime(6) NOT NULL,
  `division_id` bigint NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baseapp_responsible_division_id_53fe803a_fk_baseapp_division_id` (`division_id`),
  KEY `baseapp_responsible_personnel_id_db93c01d_fk_baseapp_p` (`personnel_id`),
  KEY `baseapp_responsible_recorder_id_6ab2d1fe_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `baseapp_responsible_division_id_53fe803a_fk_baseapp_division_id` FOREIGN KEY (`division_id`) REFERENCES `baseapp_division` (`id`),
  CONSTRAINT `baseapp_responsible_personnel_id_db93c01d_fk_baseapp_p` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `baseapp_responsible_recorder_id_6ab2d1fe_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `eduSemeter` int NOT NULL,
  `mission` varchar(50) NOT NULL,
  `topic` longtext NOT NULL,
  `detail` longtext NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `editDate` datetime(6) NOT NULL,
  `editor_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_command_editor_id_58928b43_fk_baseapp_personnel_id` (`editor_id`),
  KEY `workapp_command_recorder_id_06b235ed_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `workapp_command_editor_id_58928b43_fk_baseapp_personnel_id` FOREIGN KEY (`editor_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_command_recorder_id_06b235ed_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_commandfile`
--

DROP TABLE IF EXISTS `workapp_commandfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_commandfile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) DEFAULT NULL,
  `filetype` varchar(50) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `command_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_commandfile_command_id_1a7cb75c_fk_workapp_command_id` (`command_id`),
  KEY `workapp_commandfile_recorder_id_89a5fcfb_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `workapp_commandfile_command_id_1a7cb75c_fk_workapp_command_id` FOREIGN KEY (`command_id`) REFERENCES `workapp_command` (`id`),
  CONSTRAINT `workapp_commandfile_recorder_id_89a5fcfb_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_commandperson`
--

DROP TABLE IF EXISTS `workapp_commandperson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_commandperson` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(30) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `command_id` bigint NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_commandperson_command_id_7384d690_fk_workapp_command_id` (`command_id`),
  KEY `workapp_commandperso_personnel_id_0d89fb15_fk_baseapp_p` (`personnel_id`),
  KEY `workapp_commandperso_recorder_id_2dd4761c_fk_baseapp_p` (`recorder_id`),
  CONSTRAINT `workapp_commandperso_personnel_id_0d89fb15_fk_baseapp_p` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_commandperso_recorder_id_2dd4761c_fk_baseapp_p` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_commandperson_command_id_7384d690_fk_workapp_command_id` FOREIGN KEY (`command_id`) REFERENCES `workapp_command` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_commandurl`
--

DROP TABLE IF EXISTS `workapp_commandurl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_commandurl` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `command_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_commandurl_command_id_bd1116c7_fk_workapp_command_id` (`command_id`),
  KEY `workapp_commandurl_recorder_id_79425020_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `workapp_commandurl_command_id_bd1116c7_fk_workapp_command_id` FOREIGN KEY (`command_id`) REFERENCES `workapp_command` (`id`),
  CONSTRAINT `workapp_commandurl_recorder_id_79425020_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `leaveType` varchar(50) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `editDate` datetime(6) NOT NULL,
  `editor_id` bigint NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  `editable` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_leave_editor_id_aceadd27_fk_baseapp_personnel_id` (`editor_id`),
  KEY `workapp_leave_personnel_id_84cc093a_fk_baseapp_personnel_id` (`personnel_id`),
  KEY `workapp_leave_recorder_id_36b265d1_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `workapp_leave_editor_id_aceadd27_fk_baseapp_personnel_id` FOREIGN KEY (`editor_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_leave_personnel_id_84cc093a_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_leave_recorder_id_36b265d1_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_leavefile`
--

DROP TABLE IF EXISTS `workapp_leavefile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_leavefile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) DEFAULT NULL,
  `filetype` varchar(50) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `leave_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_leavefile_leave_id_f23196fe_fk_workapp_leave_id` (`leave_id`),
  KEY `workapp_leavefile_recorder_id_5590ba36_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `workapp_leavefile_leave_id_f23196fe_fk_workapp_leave_id` FOREIGN KEY (`leave_id`) REFERENCES `workapp_leave` (`id`),
  CONSTRAINT `workapp_leavefile_recorder_id_5590ba36_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_leaveurl`
--

DROP TABLE IF EXISTS `workapp_leaveurl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_leaveurl` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `leave_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_leaveurl_leave_id_bbd51fac_fk_workapp_leave_id` (`leave_id`),
  KEY `workapp_leaveurl_recorder_id_8d98f988_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `workapp_leaveurl_leave_id_bbd51fac_fk_workapp_leave_id` FOREIGN KEY (`leave_id`) REFERENCES `workapp_leave` (`id`),
  CONSTRAINT `workapp_leaveurl_recorder_id_8d98f988_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `editor_id` bigint NOT NULL,
  `editDate` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_performance_personnel_id_d4658b3e_fk_baseapp_p` (`personnel_id`),
  KEY `workapp_performance_recorder_id_a3649e47_fk_baseapp_personnel_id` (`recorder_id`),
  KEY `workapp_performance_editor_id_49e2b018_fk_baseapp_personnel_id` (`editor_id`),
  CONSTRAINT `workapp_performance_editor_id_49e2b018_fk_baseapp_personnel_id` FOREIGN KEY (`editor_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_performance_personnel_id_d4658b3e_fk_baseapp_p` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_performance_recorder_id_a3649e47_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_performancefile`
--

DROP TABLE IF EXISTS `workapp_performancefile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_performancefile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) DEFAULT NULL,
  `filetype` varchar(50) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `performance_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_performancef_performance_id_515074f1_fk_workapp_p` (`performance_id`),
  KEY `workapp_performancef_recorder_id_d6cad01f_fk_baseapp_p` (`recorder_id`),
  CONSTRAINT `workapp_performancef_performance_id_515074f1_fk_workapp_p` FOREIGN KEY (`performance_id`) REFERENCES `workapp_performance` (`id`),
  CONSTRAINT `workapp_performancef_recorder_id_d6cad01f_fk_baseapp_p` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_performanceurl`
--

DROP TABLE IF EXISTS `workapp_performanceurl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_performanceurl` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `performance_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_performanceu_performance_id_8a13a622_fk_workapp_p` (`performance_id`),
  KEY `workapp_performanceu_recorder_id_98c8ff12_fk_baseapp_p` (`recorder_id`),
  CONSTRAINT `workapp_performanceu_performance_id_8a13a622_fk_workapp_p` FOREIGN KEY (`performance_id`) REFERENCES `workapp_performance` (`id`),
  CONSTRAINT `workapp_performanceu_recorder_id_98c8ff12_fk_baseapp_p` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `budget` double NOT NULL,
  `budgetType` varchar(30) NOT NULL,
  `source` varchar(255) NOT NULL,
  `reference` longtext NOT NULL,
  `percentSuccess` int NOT NULL,
  `publishMethod` longtext NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `editDate` datetime(6) NOT NULL,
  `editor_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  `publishDate` date NOT NULL,
  `publishDb` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_research_editor_id_9df2fc79_fk_baseapp_personnel_id` (`editor_id`),
  KEY `workapp_research_recorder_id_0674ef61_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `workapp_research_editor_id_9df2fc79_fk_baseapp_personnel_id` FOREIGN KEY (`editor_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_research_recorder_id_0674ef61_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_researchfile`
--

DROP TABLE IF EXISTS `workapp_researchfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_researchfile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) DEFAULT NULL,
  `filetype` varchar(50) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `recorder_id` bigint NOT NULL,
  `research_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_researchfile_recorder_id_dbf1aa6f_fk_baseapp_p` (`recorder_id`),
  KEY `workapp_researchfile_research_id_81261dde_fk_workapp_research_id` (`research_id`),
  CONSTRAINT `workapp_researchfile_recorder_id_dbf1aa6f_fk_baseapp_p` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_researchfile_research_id_81261dde_fk_workapp_research_id` FOREIGN KEY (`research_id`) REFERENCES `workapp_research` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_researchperson`
--

DROP TABLE IF EXISTS `workapp_researchperson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_researchperson` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(30) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  `research_id` bigint NOT NULL,
  `percent` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_researchpers_personnel_id_1c80c86f_fk_baseapp_p` (`personnel_id`),
  KEY `workapp_researchpers_recorder_id_057e4380_fk_baseapp_p` (`recorder_id`),
  KEY `workapp_researchpers_research_id_e9e9efe0_fk_workapp_r` (`research_id`),
  CONSTRAINT `workapp_researchpers_personnel_id_1c80c86f_fk_baseapp_p` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_researchpers_recorder_id_057e4380_fk_baseapp_p` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_researchpers_research_id_e9e9efe0_fk_workapp_r` FOREIGN KEY (`research_id`) REFERENCES `workapp_research` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_researchurl`
--

DROP TABLE IF EXISTS `workapp_researchurl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_researchurl` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `recorder_id` bigint NOT NULL,
  `research_id` bigint NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_researchurl_recorder_id_5e22fa43_fk_baseapp_personnel_id` (`recorder_id`),
  KEY `workapp_researchurl_research_id_531654b6_fk_workapp_research_id` (`research_id`),
  CONSTRAINT `workapp_researchurl_recorder_id_5e22fa43_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_researchurl_research_id_531654b6_fk_workapp_research_id` FOREIGN KEY (`research_id`) REFERENCES `workapp_research` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `topic` longtext NOT NULL,
  `objective` longtext NOT NULL,
  `place` varchar(255) NOT NULL,
  `budget` double NOT NULL,
  `budgetType` varchar(30) NOT NULL,
  `source` varchar(255) NOT NULL,
  `receiver` varchar(255) NOT NULL,
  `num_receiver` int NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `editDate` datetime(6) NOT NULL,
  `editor_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_socialservice_editor_id_0fa8c5ca_fk_baseapp_personnel_id` (`editor_id`),
  KEY `workapp_socialservic_recorder_id_7ece6878_fk_baseapp_p` (`recorder_id`),
  CONSTRAINT `workapp_socialservic_recorder_id_7ece6878_fk_baseapp_p` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_socialservice_editor_id_0fa8c5ca_fk_baseapp_personnel_id` FOREIGN KEY (`editor_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_socialservicefile`
--

DROP TABLE IF EXISTS `workapp_socialservicefile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_socialservicefile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) DEFAULT NULL,
  `filetype` varchar(50) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `recorder_id` bigint NOT NULL,
  `socialservice_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_socialservic_recorder_id_f018f3c1_fk_baseapp_p` (`recorder_id`),
  KEY `workapp_socialservic_socialservice_id_45015cea_fk_workapp_s` (`socialservice_id`),
  CONSTRAINT `workapp_socialservic_recorder_id_f018f3c1_fk_baseapp_p` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_socialservic_socialservice_id_45015cea_fk_workapp_s` FOREIGN KEY (`socialservice_id`) REFERENCES `workapp_socialservice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_socialserviceperson`
--

DROP TABLE IF EXISTS `workapp_socialserviceperson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_socialserviceperson` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(30) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  `socialservice_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_socialservic_personnel_id_1f9e94b6_fk_baseapp_p` (`personnel_id`),
  KEY `workapp_socialservic_recorder_id_71d0359b_fk_baseapp_p` (`recorder_id`),
  KEY `workapp_socialservic_socialservice_id_1bc3602e_fk_workapp_s` (`socialservice_id`),
  CONSTRAINT `workapp_socialservic_personnel_id_1f9e94b6_fk_baseapp_p` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_socialservic_recorder_id_71d0359b_fk_baseapp_p` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_socialservic_socialservice_id_1bc3602e_fk_workapp_s` FOREIGN KEY (`socialservice_id`) REFERENCES `workapp_socialservice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_socialserviceurl`
--

DROP TABLE IF EXISTS `workapp_socialserviceurl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_socialserviceurl` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `recorder_id` bigint NOT NULL,
  `socialservice_id` bigint NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_socialservic_recorder_id_84542984_fk_baseapp_p` (`recorder_id`),
  KEY `workapp_socialservic_socialservice_id_2ea18b77_fk_workapp_s` (`socialservice_id`),
  CONSTRAINT `workapp_socialservic_recorder_id_84542984_fk_baseapp_p` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_socialservic_socialservice_id_2ea18b77_fk_workapp_s` FOREIGN KEY (`socialservice_id`) REFERENCES `workapp_socialservice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `editDate` datetime(6) NOT NULL,
  `editor_id` bigint NOT NULL,
  `personnel_id` bigint NOT NULL,
  `recorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_training_editor_id_a6850f06_fk_baseapp_personnel_id` (`editor_id`),
  KEY `workapp_training_personnel_id_6c2478b3_fk_baseapp_personnel_id` (`personnel_id`),
  KEY `workapp_training_recorder_id_21f847a5_fk_baseapp_personnel_id` (`recorder_id`),
  CONSTRAINT `workapp_training_editor_id_a6850f06_fk_baseapp_personnel_id` FOREIGN KEY (`editor_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_training_personnel_id_6c2478b3_fk_baseapp_personnel_id` FOREIGN KEY (`personnel_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_training_recorder_id_21f847a5_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_trainingfile`
--

DROP TABLE IF EXISTS `workapp_trainingfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_trainingfile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) DEFAULT NULL,
  `filetype` varchar(50) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `recorder_id` bigint NOT NULL,
  `training_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_trainingfile_recorder_id_7c2e839e_fk_baseapp_p` (`recorder_id`),
  KEY `workapp_trainingfile_training_id_dbbf4885_fk_workapp_training_id` (`training_id`),
  CONSTRAINT `workapp_trainingfile_recorder_id_7c2e839e_fk_baseapp_p` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_trainingfile_training_id_dbbf4885_fk_workapp_training_id` FOREIGN KEY (`training_id`) REFERENCES `workapp_training` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workapp_trainingurl`
--

DROP TABLE IF EXISTS `workapp_trainingurl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workapp_trainingurl` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `recordDate` datetime(6) NOT NULL,
  `recorder_id` bigint NOT NULL,
  `training_id` bigint NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workapp_trainingurl_recorder_id_ee891c86_fk_baseapp_personnel_id` (`recorder_id`),
  KEY `workapp_trainingurl_training_id_d3046282_fk_workapp_training_id` (`training_id`),
  CONSTRAINT `workapp_trainingurl_recorder_id_ee891c86_fk_baseapp_personnel_id` FOREIGN KEY (`recorder_id`) REFERENCES `baseapp_personnel` (`id`),
  CONSTRAINT `workapp_trainingurl_training_id_d3046282_fk_workapp_training_id` FOREIGN KEY (`training_id`) REFERENCES `workapp_training` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-13 21:30:44
