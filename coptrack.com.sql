/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50130
Source Host           : localhost:3306
Source Database       : coptrack.com

Target Server Type    : MYSQL
Target Server Version : 50130
File Encoding         : 65001

Date: 2019-06-20 13:28:47
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `auth_group`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for `auth_group_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissions_group_id_58c48ba9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for `auth_permission`
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_51277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES ('1', 'Can add log entry', '1', 'add_logentry');
INSERT INTO `auth_permission` VALUES ('2', 'Can change log entry', '1', 'change_logentry');
INSERT INTO `auth_permission` VALUES ('3', 'Can delete log entry', '1', 'delete_logentry');
INSERT INTO `auth_permission` VALUES ('4', 'Can add permission', '2', 'add_permission');
INSERT INTO `auth_permission` VALUES ('5', 'Can change permission', '2', 'change_permission');
INSERT INTO `auth_permission` VALUES ('6', 'Can delete permission', '2', 'delete_permission');
INSERT INTO `auth_permission` VALUES ('7', 'Can add group', '3', 'add_group');
INSERT INTO `auth_permission` VALUES ('8', 'Can change group', '3', 'change_group');
INSERT INTO `auth_permission` VALUES ('9', 'Can delete group', '3', 'delete_group');
INSERT INTO `auth_permission` VALUES ('10', 'Can add user', '4', 'add_user');
INSERT INTO `auth_permission` VALUES ('11', 'Can change user', '4', 'change_user');
INSERT INTO `auth_permission` VALUES ('12', 'Can delete user', '4', 'delete_user');
INSERT INTO `auth_permission` VALUES ('13', 'Can add content type', '5', 'add_contenttype');
INSERT INTO `auth_permission` VALUES ('14', 'Can change content type', '5', 'change_contenttype');
INSERT INTO `auth_permission` VALUES ('15', 'Can delete content type', '5', 'delete_contenttype');
INSERT INTO `auth_permission` VALUES ('16', 'Can add session', '6', 'add_session');
INSERT INTO `auth_permission` VALUES ('17', 'Can change session', '6', 'change_session');
INSERT INTO `auth_permission` VALUES ('18', 'Can delete session', '6', 'delete_session');

-- ----------------------------
-- Table structure for `auth_user`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of auth_user
-- ----------------------------

-- ----------------------------
-- Table structure for `auth_user_groups`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_30a071c9_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_30a071c9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_24702650_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for `auth_user_user_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_permissions_user_id_7cd7acb6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for `django_admin_log`
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_5151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_1c5f563_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_1c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin__content_type_id_5151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for `django_content_type`
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_3ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES ('1', 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES ('3', 'auth', 'group');
INSERT INTO `django_content_type` VALUES ('2', 'auth', 'permission');
INSERT INTO `django_content_type` VALUES ('4', 'auth', 'user');
INSERT INTO `django_content_type` VALUES ('5', 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES ('6', 'sessions', 'session');

-- ----------------------------
-- Table structure for `django_migrations`
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES ('1', 'contenttypes', '0001_initial', '2019-03-01 05:11:26');
INSERT INTO `django_migrations` VALUES ('2', 'auth', '0001_initial', '2019-03-01 05:11:28');
INSERT INTO `django_migrations` VALUES ('3', 'admin', '0001_initial', '2019-03-01 05:11:29');
INSERT INTO `django_migrations` VALUES ('4', 'contenttypes', '0002_remove_content_type_name', '2019-03-01 05:11:29');
INSERT INTO `django_migrations` VALUES ('5', 'auth', '0002_alter_permission_name_max_length', '2019-03-01 05:11:30');
INSERT INTO `django_migrations` VALUES ('6', 'auth', '0003_alter_user_email_max_length', '2019-03-01 05:11:30');
INSERT INTO `django_migrations` VALUES ('7', 'auth', '0004_alter_user_username_opts', '2019-03-01 05:11:30');
INSERT INTO `django_migrations` VALUES ('8', 'auth', '0005_alter_user_last_login_null', '2019-03-01 05:11:31');
INSERT INTO `django_migrations` VALUES ('9', 'auth', '0006_require_contenttypes_0002', '2019-03-01 05:11:31');
INSERT INTO `django_migrations` VALUES ('10', 'sessions', '0001_initial', '2019-03-01 05:11:31');

-- ----------------------------
-- Table structure for `django_session`
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('9flpp3fn637fzpxjto6wupyxfh2euh8n', 'YzExNWZkNjE0YmIzN2YyZDY4OTM1YzE0YTBkM2M1ZDYwZjk5ZTM0NDp7InVzZXJuYW1lIjoib21AZ21haWwuY29tIiwidV9pZCI6MTIsInVzZXJfdHlwZSI6ImVtcGxveWVyIn0=', '2019-05-17 05:42:14');
INSERT INTO `django_session` VALUES ('hs0pgs3bdg1ricr3kaxn2hkhv4z87c3y', 'NTZmYTk0OWJjM2ExZmQwYmFlOWZiYWJhM2M3MWRlMjQxY2Q4M2Y5Yjp7InVzZXJuYW1lIjoiYmJAZ21haWwuY29tIiwidV9pZCI6MywidXNlcl90eXBlIjoicG9saWNlIn0=', '2019-04-24 07:35:56');
INSERT INTO `django_session` VALUES ('jt3b0hbnz1vplrecre9gdzpm5rqy3lr6', 'OTJkNTdjYjVlZmEyN2U1MDU4ZmE4YTIxMjNjZTZiYjg0NTBiZDk2Yjp7InVzZXJuYW1lIjoib3BAZ21haWwuY29tIiwidV9pZCI6MTEsInVzZXJfdHlwZSI6ImVtcGxveWVyIn0=', '2019-03-26 06:49:09');
INSERT INTO `django_session` VALUES ('nquorgon8643zrylgjgv3z8kyb7lw8la', 'YjY0NDQ0NmY4MGU3YmMwOGRlYWE5ZDE0OTU0YWUwZjk5MWM0NzZlZjp7InVzZXJuYW1lIjoiQkJAR01BSUwuQ09NIiwidV9pZCI6MywidXNlcl90eXBlIjoicG9saWNlIn0=', '2019-05-30 06:12:10');
INSERT INTO `django_session` VALUES ('p9a9m23fcjuo9cu4ji3j6atm5plj3aos', 'YjA2NjgwNTg4OGRiMjI1Zjg3MjE2MGI3NWJkYTlkMjk4M2Y3YzZmZjp7InVzZXJuYW1lIjoidGhvZHVAZ21haWwuY29tIiwidV9pZCI6MSwidXNlcl90eXBlIjoicG9saWNlIn0=', '2019-07-04 05:16:26');
INSERT INTO `django_session` VALUES ('sdgssognhnm4o81u44z1zlg5n6paacwq', 'OTJkNTdjYjVlZmEyN2U1MDU4ZmE4YTIxMjNjZTZiYjg0NTBiZDk2Yjp7InVzZXJuYW1lIjoib3BAZ21haWwuY29tIiwidV9pZCI6MTEsInVzZXJfdHlwZSI6ImVtcGxveWVyIn0=', '2019-03-26 07:43:56');
INSERT INTO `django_session` VALUES ('t7osinir219ji2m4np10udx9xhwjcx3l', 'OTJkNTdjYjVlZmEyN2U1MDU4ZmE4YTIxMjNjZTZiYjg0NTBiZDk2Yjp7InVzZXJuYW1lIjoib3BAZ21haWwuY29tIiwidV9pZCI6MTEsInVzZXJfdHlwZSI6ImVtcGxveWVyIn0=', '2019-03-26 10:36:27');
INSERT INTO `django_session` VALUES ('w3a8421xni0w7nfs8nafwy5zumzzl1qq', 'ZDRkYTQ2NTUwNjNjNzI4MmZjZDUwY2E3NmMxYWQwYTg5ZDFhYjQ0Yzp7InVzZXJuYW1lIjoiYWRtaW5AZ21haWwuY29tIiwidV9pZCI6MCwidXNlcl90eXBlIjoiYWRtaW4ifQ==', '2019-04-24 05:45:54');
INSERT INTO `django_session` VALUES ('xkjxyojj4kzqmz4hfdgwsd1de2bb2nq6', 'NmYwZTMyMGM0NzNkYjlhODMyYTM1NzNkYzljZTliYzFiNjUwNjViODp7InVzZXJuYW1lIjoia2Fra2FAZ21haWwuY29tIiwidV9pZCI6MiwidXNlcl90eXBlIjoicG9saWNlIn0=', '2019-07-04 07:57:33');

-- ----------------------------
-- Table structure for `tbl_admin`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_admin`;
CREATE TABLE `tbl_admin` (
  `admin_id` int(5) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `mobile` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `pasw` varchar(50) NOT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_admin
-- ----------------------------
INSERT INTO `tbl_admin` VALUES ('1', 'Admin', 'India', 'Kerala', '0486287678', '9496181704', 'admin@gmail.com', 'admin');
INSERT INTO `tbl_admin` VALUES ('2', 'Admin', 'India', 'Kerala', '0486287678', '9496181704', 'admin@gmail.com', 'admin');

-- ----------------------------
-- Table structure for `tbl_complaint`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_complaint`;
CREATE TABLE `tbl_complaint` (
  `cmp_id` int(10) NOT NULL AUTO_INCREMENT,
  `emp_id` int(10) NOT NULL,
  `complaint` varchar(500) NOT NULL,
  `cmp_date` varchar(50) NOT NULL,
  PRIMARY KEY (`cmp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_complaint
-- ----------------------------

-- ----------------------------
-- Table structure for `tbl_emp`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_emp`;
CREATE TABLE `tbl_emp` (
  `emp_id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `firm_name` varchar(50) NOT NULL,
  `aadhar_no` varchar(20) NOT NULL,
  `dob` varchar(50) NOT NULL,
  `emp_address` varchar(100) NOT NULL,
  `place` varchar(50) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `pswd` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`emp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_emp
-- ----------------------------
INSERT INTO `tbl_emp` VALUES ('1', 'Manoharan', '', 'TTVConstructions', '123DFRTG', '1983-06-19', 'Sreegulam  road,\r\nNear Padhama Theator', 'Kochi', '4567834555', '7890654355', 'manoharan@gmail.com', 'mano', 'Active');
INSERT INTO `tbl_emp` VALUES ('3', 'Urmila', 'female', 'UrmilasPickles', '78JHYD8', '1982-03-19', 'Kakkadi Road,\r\nNear private bus stand', 'Kakkadi', '398768908', '987389098', 'urmila@gmail.com', 'urmila', 'Active');
INSERT INTO `tbl_emp` VALUES ('5', 'Haris', 'male', 'HarisPhotos', '4567FGHYT', '1986-10-20', 'Neart absoft  pvt  lmtd,\r\nIndia', 'Kunnam', '435678567', '9876897432', 'haris@gmail.com', 'haris', 'pending');
INSERT INTO `tbl_emp` VALUES ('7', 'Jayakrishnan', 'male', 'APVTCements', '5674GHJB', '1986-11-20', 'Kadavanthra p.o,\r\nNear Malabar goldshowroom', 'Kadavanthra', '434456785', '9768543860', 'jaya@gmail.com', 'jaya', 'Rejected');

-- ----------------------------
-- Table structure for `tbl_feedback`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_feedback`;
CREATE TABLE `tbl_feedback` (
  `feedback_id` int(10) NOT NULL AUTO_INCREMENT,
  `date` varchar(50) NOT NULL,
  `emp_id` varchar(10) NOT NULL,
  `worker_id` varchar(10) NOT NULL,
  `feedback_title` varchar(50) NOT NULL,
  `feedback_description` varchar(500) NOT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_feedback
-- ----------------------------
INSERT INTO `tbl_feedback` VALUES ('1', '2019-06-20', '1', '4', 'Responsible', 'A responsible person');

-- ----------------------------
-- Table structure for `tbl_jobdetails`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_jobdetails`;
CREATE TABLE `tbl_jobdetails` (
  `job_id` int(10) NOT NULL AUTO_INCREMENT,
  `emp_id` int(10) NOT NULL,
  `job_details` varchar(100) NOT NULL,
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_jobdetails
-- ----------------------------

-- ----------------------------
-- Table structure for `tbl_login`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_login`;
CREATE TABLE `tbl_login` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `user_type` varchar(50) NOT NULL,
  `u_id` int(10) NOT NULL,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_login
-- ----------------------------
INSERT INTO `tbl_login` VALUES ('admin@gmail.com', 'admin', 'admin', '0', 'true');
INSERT INTO `tbl_login` VALUES ('anu@gmal.com', 'anu123', 'worker', '4', 'true');
INSERT INTO `tbl_login` VALUES ('ayya@gmail.com', 'ayya', 'worker', '3', 'true');
INSERT INTO `tbl_login` VALUES ('haris@gmail.com', 'haris', 'employer', '5', 'false');
INSERT INTO `tbl_login` VALUES ('janakan@gmail.com', 'j', 'worker', '2', 'true');
INSERT INTO `tbl_login` VALUES ('jaya@gmail.com', 'jaya', 'employer', '7', 'reject');
INSERT INTO `tbl_login` VALUES ('kakka@gmail.com', 'kakka', 'police', '2', 'true');
INSERT INTO `tbl_login` VALUES ('manoharan@gmail.com', 'mano', 'employer', '1', 'true');
INSERT INTO `tbl_login` VALUES ('sathyan@gmail.com', 'sathyan', 'worker', '5', 'reject');
INSERT INTO `tbl_login` VALUES ('sumesh@gmail.com', 'sumesh', 'worker', '6', 'false');
INSERT INTO `tbl_login` VALUES ('thodu@gmail.com', 'thodu', 'police', '1', 'true');
INSERT INTO `tbl_login` VALUES ('udayan@gmail.com', 'udayan', 'worker', '8', 'false');
INSERT INTO `tbl_login` VALUES ('urmila@gmail.com', 'urmila', 'employer', '3', 'true');

-- ----------------------------
-- Table structure for `tbl_myworker`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_myworker`;
CREATE TABLE `tbl_myworker` (
  `myworker_id` int(10) NOT NULL AUTO_INCREMENT,
  `emp_id` varchar(10) NOT NULL,
  `worker_id` varchar(10) NOT NULL,
  `vacancy_id` varchar(10) NOT NULL,
  `date` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`myworker_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_myworker
-- ----------------------------
INSERT INTO `tbl_myworker` VALUES ('1', '1', '4', '', '2019-06-20', 'fixed');
INSERT INTO `tbl_myworker` VALUES ('2', '1', '3', '0', '2019-06-20', 'fixed');

-- ----------------------------
-- Table structure for `tbl_noc`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_noc`;
CREATE TABLE `tbl_noc` (
  `noc_id` int(10) NOT NULL AUTO_INCREMENT,
  `worker_id` varchar(10) NOT NULL,
  `station_id` varchar(10) NOT NULL,
  `date` varchar(50) NOT NULL,
  `crime` varchar(50) NOT NULL,
  `crime_details` varchar(1000) NOT NULL,
  PRIMARY KEY (`noc_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_noc
-- ----------------------------
INSERT INTO `tbl_noc` VALUES ('1', '4', '1', '2019-06-20', 'No crime', 'He is a gentle person and able to do work');
INSERT INTO `tbl_noc` VALUES ('2', '1', '1', '2019-06-19', 'Rape', 'He raped a girl on 7/Dec/2017. ');
INSERT INTO `tbl_noc` VALUES ('3', '2', '1', '2019-06-19', 'No crime', 'Back ground history is very god');
INSERT INTO `tbl_noc` VALUES ('4', '5', '1', '2019-06-20', 'Robbery', 'He rubbered a bank in 12/Oct/2012');
INSERT INTO `tbl_noc` VALUES ('5', '3', '1', '2019-06-20', 'No crime', 'He is a good person');
INSERT INTO `tbl_noc` VALUES ('6', '3', '1', '2019-06-20', 'Thief', 'He stolen a ring in jewellery on 20/June/2019');
INSERT INTO `tbl_noc` VALUES ('7', '6', '1', '2019-06-20', 'No crime', 'Good');
INSERT INTO `tbl_noc` VALUES ('8', '8', '2', '2019-06-20', 'Robbery', 'He participated a bank robbery in 6/Dec/2017 ');

-- ----------------------------
-- Table structure for `tbl_noccomplaint`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_noccomplaint`;
CREATE TABLE `tbl_noccomplaint` (
  `complaint_id` int(10) NOT NULL AUTO_INCREMENT,
  `worker_id` varchar(10) NOT NULL,
  `noc_id` varchar(10) NOT NULL,
  `complaint` varchar(50) NOT NULL,
  `complaint_date` varchar(50) NOT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_noccomplaint
-- ----------------------------
INSERT INTO `tbl_noccomplaint` VALUES ('1', '4', '2', 'I am a good persion. I thin you have any mistake', '2019-06-20');
INSERT INTO `tbl_noccomplaint` VALUES ('2', '3', '6', 'I am not stolen', '2019-07-20');
INSERT INTO `tbl_noccomplaint` VALUES ('3', '8', '8', 'uio', '2019-11-11');

-- ----------------------------
-- Table structure for `tbl_policestation`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_policestation`;
CREATE TABLE `tbl_policestation` (
  `station_id` int(10) NOT NULL AUTO_INCREMENT,
  `branch` varchar(50) NOT NULL,
  `address` varchar(100) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `mobile` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `district` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`station_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_policestation
-- ----------------------------
INSERT INTO `tbl_policestation` VALUES ('1', 'Thodupuzha', 'Near private bus stand\r\nThodupuzha', '456723456', '9876567890', 'thodu@gmail.com', 'Idukki', 'Thodupuzha', 'Kerala', 'thodu');
INSERT INTO `tbl_policestation` VALUES ('2', 'Kakkanad', 'Near KSRTC,\r\nKakkanad', '234564567', '987567898', 'kakka@gmail.com', 'Ekm', 'Ekm', 'Kerala', 'kakka');

-- ----------------------------
-- Table structure for `tbl_vacancy`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_vacancy`;
CREATE TABLE `tbl_vacancy` (
  `vacancy_id` int(10) NOT NULL AUTO_INCREMENT,
  `date` varchar(50) NOT NULL,
  `emp_id` varchar(150) NOT NULL,
  `vacancy` varchar(50) NOT NULL,
  `vacancy_no` varchar(50) NOT NULL,
  `description` varchar(100) NOT NULL,
  PRIMARY KEY (`vacancy_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_vacancy
-- ----------------------------
INSERT INTO `tbl_vacancy` VALUES ('1', '2019-06-19', '1', 'Meser', '4', 'Urgently require 4 mesans with highly experienced.');
INSERT INTO `tbl_vacancy` VALUES ('2', '2019-06-19', '1', 'Crainoperator', '5', 'Crain operator with high vehicle lisence');

-- ----------------------------
-- Table structure for `tbl_worker`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_worker`;
CREATE TABLE `tbl_worker` (
  `worker_id` int(10) NOT NULL AUTO_INCREMENT,
  `image` varchar(500) NOT NULL,
  `worker_name` varchar(50) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `dob` varchar(50) NOT NULL,
  `aadhar_number` varchar(50) NOT NULL,
  `regis_date` varchar(50) NOT NULL,
  `place` varchar(50) NOT NULL,
  `address` varchar(100) NOT NULL,
  `languages_known` varchar(100) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `mobile` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `paswd` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`worker_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_worker
-- ----------------------------
INSERT INTO `tbl_worker` VALUES ('2', 'pictures/22.jpg', 'Janakan', 'male', '1986-09-19', '789YHJNU', '2019-06-19', 'ThamilNadu', 'Palakkad Boarder,Thamil nadu\r\n', 'Malayalam', '0878943234', '9807546786', 'janakan@gmail.com', 'janakan', 'Active');
INSERT INTO `tbl_worker` VALUES ('3', 'pictures/25.jpg', 'Ayyachami', 'male', '1976-10-19', '8765YTRED', '2019-06-19', 'ThamilNadu', 'Kokkamangalam,\r\nThripura', 'Thamil', '0987656789', '9870234543', 'ayya@gmail.com', 'ayya', 'Active');
INSERT INTO `tbl_worker` VALUES ('4', 'pictures/K_Venkatesh_Raja.jpg', 'Anu', 'male', '1989-07-19', '2345HJUK', '2019-06-19', 'WestBengal', 'Kailasappet,\r\nWest Bengal', 'BengaliMalayalam', '0990763445', '9989776545', 'anu@gmal.com', 'anu', 'fixed');
INSERT INTO `tbl_worker` VALUES ('5', 'pictures/Paulraj_Rajamani.jpg', 'Sathyan', 'male', '1988-06-19', '1234FGTH', '2019-06-19', 'HimachalPredesh', 'Himalaya hills,\r\nEdakkal', 'Hindi', '0435678945', '9867895456', 'sathyan@gmail.com', 'sathyan', 'Rejected');
INSERT INTO `tbl_worker` VALUES ('6', 'pictures/1479525429.jpg', 'Sumesh', 'male', '1989-06-20', '4567DFGH', '2019-06-20', 'Udharakhand', 'Orivila, Utharakhand', 'Hindi', '0456734523', '987894357', 'sumesh@gmail.com', 'sumesh', 'Pending');
INSERT INTO `tbl_worker` VALUES ('8', 'pictures/thTDPAHBNU_1yWJIke.jpg', 'Udayan', 'male', '1984-06-20', '8907SDFG', '2019-06-20', 'Maharashtra', 'Maharashtra street', 'Maratti', '067847856', '9890654356', 'udayan@gmail.com', 'udayan', 'Pending');

-- ----------------------------
-- Table structure for `tbl_workerdetails`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_workerdetails`;
CREATE TABLE `tbl_workerdetails` (
  `worker_id` varchar(10) NOT NULL,
  `vacancy_id` varchar(10) NOT NULL,
  `qualification` varchar(50) NOT NULL,
  `experience` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_workerdetails
-- ----------------------------
INSERT INTO `tbl_workerdetails` VALUES ('4', '1', 'SSLC', '10');
INSERT INTO `tbl_workerdetails` VALUES ('2', '2', 'Below SSLC', '1');

-- ----------------------------
-- Table structure for `tbl_workershedule`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_workershedule`;
CREATE TABLE `tbl_workershedule` (
  `shedule_id` int(10) NOT NULL AUTO_INCREMENT,
  `emp_id` int(10) NOT NULL,
  `worker_id` int(10) NOT NULL,
  `job_details` varchar(100) NOT NULL,
  `salary` int(100) NOT NULL,
  `time_from` varchar(50) NOT NULL,
  `working_houres` varchar(50) NOT NULL,
  PRIMARY KEY (`shedule_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_workershedule
-- ----------------------------
INSERT INTO `tbl_workershedule` VALUES ('1', '1', '4', 'Loading', '600', '2019-06-20', '6hr');
