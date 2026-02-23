/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50130
Source Host           : localhost:3306
Source Database       : coptrack.com

Target Server Type    : MYSQL
Target Server Version : 50130
File Encoding         : 65001

Date: 2019-05-15 12:33:56
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
INSERT INTO `django_session` VALUES ('nquorgon8643zrylgjgv3z8kyb7lw8la', 'YzExNWZkNjE0YmIzN2YyZDY4OTM1YzE0YTBkM2M1ZDYwZjk5ZTM0NDp7InVzZXJuYW1lIjoib21AZ21haWwuY29tIiwidV9pZCI6MTIsInVzZXJfdHlwZSI6ImVtcGxveWVyIn0=', '2019-05-27 04:59:53');
INSERT INTO `django_session` VALUES ('sdgssognhnm4o81u44z1zlg5n6paacwq', 'OTJkNTdjYjVlZmEyN2U1MDU4ZmE4YTIxMjNjZTZiYjg0NTBiZDk2Yjp7InVzZXJuYW1lIjoib3BAZ21haWwuY29tIiwidV9pZCI6MTEsInVzZXJfdHlwZSI6ImVtcGxveWVyIn0=', '2019-03-26 07:43:56');
INSERT INTO `django_session` VALUES ('t7osinir219ji2m4np10udx9xhwjcx3l', 'OTJkNTdjYjVlZmEyN2U1MDU4ZmE4YTIxMjNjZTZiYjg0NTBiZDk2Yjp7InVzZXJuYW1lIjoib3BAZ21haWwuY29tIiwidV9pZCI6MTEsInVzZXJfdHlwZSI6ImVtcGxveWVyIn0=', '2019-03-26 10:36:27');
INSERT INTO `django_session` VALUES ('w3a8421xni0w7nfs8nafwy5zumzzl1qq', 'ZDRkYTQ2NTUwNjNjNzI4MmZjZDUwY2E3NmMxYWQwYTg5ZDFhYjQ0Yzp7InVzZXJuYW1lIjoiYWRtaW5AZ21haWwuY29tIiwidV9pZCI6MCwidXNlcl90eXBlIjoiYWRtaW4ifQ==', '2019-04-24 05:45:54');

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
INSERT INTO `tbl_admin` VALUES ('2', 'Juna Thomas', 'India', 'Kerala', '0486213453', '9496181604', 'admin@gmail.com', 'admin');

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
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_emp
-- ----------------------------
INSERT INTO `tbl_emp` VALUES ('1', 'tj', 'male', 'jkyk', '8978', '2003', 'ku', 'tj', '8905678967', '8976545678', 'g@gmail.com', 'y', 'pending');
INSERT INTO `tbl_emp` VALUES ('2', 'f', 'male', 'f', '7788', '2019-03-21', 'd', 'd', '3456789087', '8976545678', 'x@gmail.com', 'x', 'pending');
INSERT INTO `tbl_emp` VALUES ('3', 'f', 'male', 'f', '7788', '2019-03-21', 'd', 'd', '3456789087', '8976545678', 'x@gmail.com', 'x', 'pending');
INSERT INTO `tbl_emp` VALUES ('4', 'f', 'male', 'f', '7788', '2019-03-21', 'd', 'd', '3456789087', '8976545678', 'x@gmail.com', 'x', 'pending');
INSERT INTO `tbl_emp` VALUES ('5', 'f', 'male', 'f', '7788', '2019-03-21', 'd', 'd', '3456789087', '8976545678', 'x@gmail.com', 'x', 'pending');
INSERT INTO `tbl_emp` VALUES ('6', 'f', 'male', 'f', '7788', '2019-03-21', 'd', 'd', '3456789087', '8976545678', 'x@gmail.com', 'x', 'pending');
INSERT INTO `tbl_emp` VALUES ('7', 's', 'male', 's', '333', '2019-03-12', 'dd', 'd', '7890876545', '4567892345', 'c@gmail.com', 'c', 'pending');
INSERT INTO `tbl_emp` VALUES ('8', 's', 'male', 's', '333', '2019-03-12', 'dd', 'd', '7890876545', '4567892345', 'c@gmail.com', 'c', 'pending');
INSERT INTO `tbl_emp` VALUES ('9', 's', 'male', 's', '333', '2019-03-12', 'dd', 'd', '7890876545', '4567892345', 'c@gmail.com', 'c', 'pending');
INSERT INTO `tbl_emp` VALUES ('10', 'gg', 'female', 'hh', '34', '2019-05-29', 'hh', 'hh', '8790765671', '4567432351', 'hh@gmail.com', 'w', 'pending');
INSERT INTO `tbl_emp` VALUES ('11', 'm', 'male', 'm', '89', '2019-03-21', 'yy', 'y', '8790765678', '8907654347', 'op@gmail.com', 'oo', 'Active');
INSERT INTO `tbl_emp` VALUES ('12', 'manoharan', 'female', 'o', '0', '2019-03-08', 'oo', 'o', '9890876789', '9878909878', 'om@gmail.com', 'o', 'Active');
INSERT INTO `tbl_emp` VALUES ('13', 'q', 'female', 'q', '123456789', '2019-04-06', 'qqqq', 'q', '1234567890', '11234567890', 'q@gmail.com', '123', 'Active');
INSERT INTO `tbl_emp` VALUES ('14', 't', 'female', 't', '78', '2019-03-08', 'tt', 't', '1123456789', '1123456789', 't@gmail.com', 'tt', 'Rejected');
INSERT INTO `tbl_emp` VALUES ('15', 'mm', 'female', 'mm', '45', '2019-02-06', 'mm', 'mm', '12345678899', '1234567899', 'mm@gmail.com', 'g', 'Active');
INSERT INTO `tbl_emp` VALUES ('16', 'd', 'female', 'd', '66', '2019-03-11', 'd', 'd', '5345678909', '5345678909', 'd@gmail.com', 'd', 'Active');
INSERT INTO `tbl_emp` VALUES ('17', 'yyty', 'female', 'ddf', '656', '2019-03-15', 'tdtt', 'tyy', '6677678867', '6677678867', 'd@gmail.com', 'd', 'pending');
INSERT INTO `tbl_emp` VALUES ('18', 'ghg', 'male', 'jhk', '4589', '2014-03-14', 'yjy', 'yiyui', '987654321', '987654321', 'l@gmail.com', 'l', 'pending');
INSERT INTO `tbl_emp` VALUES ('19', 'ghg', 'male', 'jhk', '4589', '2014-03-14', 'yjy', 'yiyui', '987654321', '987654321', 'l@gmail.com', 'l', 'Active');
INSERT INTO `tbl_emp` VALUES ('20', 'HGF', 'male', 'FHH', 'FH534', '2019-03-16', 'GFH', 'tyy', '987654321', '987654321', 'l@gmail.com', 'l', 'pending');
INSERT INTO `tbl_emp` VALUES ('21', 'HGF', 'male', 'FHH', 'FH534', '2019-03-16', 'GFH', 'tyy', '987654321', '987654321', 'l@gmail.com', 'l', 'pending');
INSERT INTO `tbl_emp` VALUES ('22', 'ff', 'male', 'ff', 'ff', '2019-05-14', 'ff', 'ffc', '987654321', '987654321', 'ff@gmail.com', 'ff', 'Rejected');
INSERT INTO `tbl_emp` VALUES ('23', 'll', 'male', 'll', 'll', '2019-05-14', 'pp', 'll', '987654321', '987654321', 'llk@gmail.com', 'llk', 'Active');
INSERT INTO `tbl_emp` VALUES ('24', 'teena', 'female', 'sss', 'sss', '2019-03-23', 'sss', 'sss', '987654321', '987654321', 'teena@gmail.com', 'teena', 'pending');
INSERT INTO `tbl_emp` VALUES ('25', 'kichu', 'female', 'dddd', '5666', '2019-03-23', 'dddd', 'ddd', '987654321', '987654321', 'kichu@gail.com', 'kichu', 'pending');
INSERT INTO `tbl_emp` VALUES ('26', 'kichu', 'female', 'kk', 'kk', '2019-05-15', 'cc', 'cc', '987654321', '987654321', 'kichu@gmail.com', 'kichu', 'pending');
INSERT INTO `tbl_emp` VALUES ('27', 'Manilal', 'male', 'gg', 'gg', '2019-05-01', 'gg', 'gg', '987654321', '987654321', 'manilal@gmail.com', 'manilal', 'pending');

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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_feedback
-- ----------------------------
INSERT INTO `tbl_feedback` VALUES ('1', '2019-03-12 14:46:37.689000', '11', '5', 'zzz', 'zzzz');
INSERT INTO `tbl_feedback` VALUES ('2', '2019-03-12 14:46:55.884000', '11', '5', 'vvv', 'vvv');
INSERT INTO `tbl_feedback` VALUES ('3', '2019-03-12 14:58:52.550000', '11', '5', 'zzza', 'za');
INSERT INTO `tbl_feedback` VALUES ('5', '2019-03-17 13:26:45.417000', '12', '3', 'very bad work', 'ffgf');
INSERT INTO `tbl_feedback` VALUES ('6', '2019-03-17 13:27:01.726000', '12', '3', 'lazy', 'dddf');
INSERT INTO `tbl_feedback` VALUES ('7', '2019-05-04', '12', '3', 'Care', 'good');
INSERT INTO `tbl_feedback` VALUES ('8', '2019-03-18', '12', '2', 'dd', 'dd');
INSERT INTO `tbl_feedback` VALUES ('9', '2019-05-03', '12', '2', 'good', 'nice work');
INSERT INTO `tbl_feedback` VALUES ('10', '2019-05-09', '12', '3', 'Lazy worker', 'Very lazy. no works are done');

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
INSERT INTO `tbl_login` VALUES ('a@gmail.com', 'a', 'admin', '0', 'true');
INSERT INTO `tbl_login` VALUES ('admin@gmail.com', 'admin', 'admin', '0', 'true');
INSERT INTO `tbl_login` VALUES ('alex@gmail.com', 'alex', 'worker', '6', 'true');
INSERT INTO `tbl_login` VALUES ('aq@gmail.com', '123', 'worker', '6', 'true');
INSERT INTO `tbl_login` VALUES ('arya@gmail.com', 'rya', 'worker', '15', 'false');
INSERT INTO `tbl_login` VALUES ('asd@gmai.com', 'asd', 'worker', '6', 'true');
INSERT INTO `tbl_login` VALUES ('aysha@gmail.com', 'qq', 'worker', '1', 'true');
INSERT INTO `tbl_login` VALUES ('bb@gmail.com', 'bb', 'police', '3', 'true');
INSERT INTO `tbl_login` VALUES ('c@gmail.com', 'c', 'employer', '10', 'true');
INSERT INTO `tbl_login` VALUES ('ccfg@gmail.com', 'ccfg', 'worker', '6', 'true');
INSERT INTO `tbl_login` VALUES ('d@gmail.com', 'd', 'employer', '16', 'true');
INSERT INTO `tbl_login` VALUES ('ee@gmail.com', 'ee', 'worker', '5', 'true');
INSERT INTO `tbl_login` VALUES ('ff@gmail.com', 'ff', 'employer', '22', 'true');
INSERT INTO `tbl_login` VALUES ('g@gmail.com', 'g', 'admin', '0', 'false');
INSERT INTO `tbl_login` VALUES ('h@gmail.com', 'g', 'employer', '15', 'true');
INSERT INTO `tbl_login` VALUES ('hhg@gmail.com', 'hg', 'worker', '6', 'true');
INSERT INTO `tbl_login` VALUES ('juna@gmail.com', 'juna', 'worker', '8', 'true');
INSERT INTO `tbl_login` VALUES ('k@gmail.com', 'k', 'admin', '0', 'true');
INSERT INTO `tbl_login` VALUES ('kavya@gmail.com', 'cc', 'worker', '2', 'true');
INSERT INTO `tbl_login` VALUES ('kichu@gail.com', 'kichu', 'employer', '25', 'false');
INSERT INTO `tbl_login` VALUES ('kichu@gmail.com', 'kichu', 'employer', '26', 'false');
INSERT INTO `tbl_login` VALUES ('kkv@gmail.com', 'vv', 'worker', '4', 'true');
INSERT INTO `tbl_login` VALUES ('ktym@gmail.com', 'rr', 'police', '5', 'true');
INSERT INTO `tbl_login` VALUES ('kunju@gmail.com', 'kunju', 'worker', '7', 'true');
INSERT INTO `tbl_login` VALUES ('l@gmail.com', 'l', 'employer', '19', 'true');
INSERT INTO `tbl_login` VALUES ('llk@gmail.com', 'llk', 'employer', '23', 'true');
INSERT INTO `tbl_login` VALUES ('llm@gail.com', 'll', 'worker', '6', 'true');
INSERT INTO `tbl_login` VALUES ('manilal@gmail.com', 'manilal', 'employer', '27', 'false');
INSERT INTO `tbl_login` VALUES ('nayan@gmail.com', 'nayan', 'worker', '6', 'false');
INSERT INTO `tbl_login` VALUES ('nj@gmail.com', 'nn', 'police', '4', 'true');
INSERT INTO `tbl_login` VALUES ('nnk@gmail.com', 'nnk', 'worker', '5', 'true');
INSERT INTO `tbl_login` VALUES ('om@gmail.com', 'oo', 'employer', '12', 'true');
INSERT INTO `tbl_login` VALUES ('op@gmail.com', 'ss', 'employer', '11', 'true');
INSERT INTO `tbl_login` VALUES ('q@gmail.com', '123', 'employer', '13', 'true');
INSERT INTO `tbl_login` VALUES ('qqa@gmil.com', 'qqa', 'worker', '6', 'true');
INSERT INTO `tbl_login` VALUES ('sumi@gmail.com', 'dd', 'worker', '3', 'true');
INSERT INTO `tbl_login` VALUES ('sweety@gmail.com', 'sweety', 'worker', '7', 'true');
INSERT INTO `tbl_login` VALUES ('t@gmail.com', 'tt', 'employer', '14', 'true');
INSERT INTO `tbl_login` VALUES ('teena@gmail.com', 'teena', 'employer', '24', 'false');
INSERT INTO `tbl_login` VALUES ('vcx@gmail.com', 'vcx', 'worker', '6', 'true');
INSERT INTO `tbl_login` VALUES ('w@gmail.com', 'w', 'employer', '0', 'false');
INSERT INTO `tbl_login` VALUES ('zzc@gmail.com', 'zz', 'worker', '6', 'true');
INSERT INTO `tbl_login` VALUES ('zzx@gmail.com', 'zzx', 'worker', '6', 'true');

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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_myworker
-- ----------------------------
INSERT INTO `tbl_myworker` VALUES ('1', '11', '5', '1', '2019-03-12 15:41:45.630000', 'fixed');
INSERT INTO `tbl_myworker` VALUES ('2', '11', '5', '1', '2019-03-13 10:43:02.410000', 'fixed');
INSERT INTO `tbl_myworker` VALUES ('3', '11', '5', '1', '2019-03-13 11:06:06.952000', 'fixed');
INSERT INTO `tbl_myworker` VALUES ('4', '11', '5', '1', '2019-03-13 11:06:06.952000', 'fixed');
INSERT INTO `tbl_myworker` VALUES ('5', '11', '5', '1', '2019-03-13 11:06:06.952000', 'fixed');
INSERT INTO `tbl_myworker` VALUES ('6', '11', '5', '1', '2019-03-13 11:07:33.574000', 'fixed');
INSERT INTO `tbl_myworker` VALUES ('7', '12', '2', '3', '2019-03-15 15:54:56.851000', 'fixed');
INSERT INTO `tbl_myworker` VALUES ('8', '12', '3', '3', '2019-03-16 12:20:31.193000', 'fixed');
INSERT INTO `tbl_myworker` VALUES ('9', '12', '1', '3', '2019-03-16 13:13:25.716000', 'fixed');
INSERT INTO `tbl_myworker` VALUES ('10', '12', '7', '', '2019-05-03', 'fixed');

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
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_noc
-- ----------------------------
INSERT INTO `tbl_noc` VALUES ('3', '3', '3', '2019-03-21', 'robbery', 'crime found\r\n');
INSERT INTO `tbl_noc` VALUES ('5', '', '3', '2019-03-15 14:56:35.535000', 'ccc', 'ccca');
INSERT INTO `tbl_noc` VALUES ('6', '', '3', '2019-03-15 15:11:51.331000', 'vvv', 'vv');
INSERT INTO `tbl_noc` VALUES ('7', 'worker_id', '3', '2019-03-15 15:14:31.551000', 'xxxaa', 'aaaxx');
INSERT INTO `tbl_noc` VALUES ('8', '1', '3', '2019-03-15 15:15:43.256000', 'zzz', 'zzz');
INSERT INTO `tbl_noc` VALUES ('9', '4', '3', '2019-03-16 12:18:24.607000', 'rape a girl', 'dfd');
INSERT INTO `tbl_noc` VALUES ('11', '1', '3', '2019-03-18', 'zzz', 'zzzz');
INSERT INTO `tbl_noc` VALUES ('12', '7', '3', '2019-05-09', 'good', 'good');
INSERT INTO `tbl_noc` VALUES ('13', '1', '3', '2019-05-03', 'no crime', 'very good');
INSERT INTO `tbl_noc` VALUES ('14', '8', '3', '2019-05-03', 'no crime', 'v good');
INSERT INTO `tbl_noc` VALUES ('15', '8', '3', '2019-05-09', 'No crime', 'His crime history is clean');
INSERT INTO `tbl_noc` VALUES ('16', '5', '3', '2019-05-09', 'Robbered', 'He was robbered a bank in 20/12/2016');
INSERT INTO `tbl_noc` VALUES ('17', '6', '3', '2019-05-13', 'robbery', 'gghg');
INSERT INTO `tbl_noc` VALUES ('18', '5', '3', '2019-05-13', 'robbery', 'ghjhgbjn');

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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_noccomplaint
-- ----------------------------
INSERT INTO `tbl_noccomplaint` VALUES ('1', '3', '3', 'dfdg', '2019-03-18');
INSERT INTO `tbl_noccomplaint` VALUES ('2', '3', '3', 'fgh', '2019-03-18');
INSERT INTO `tbl_noccomplaint` VALUES ('3', '3', '3', 'i am not robbered', '2019-03-26');
INSERT INTO `tbl_noccomplaint` VALUES ('4', '3', '3', 'its not fare', '2019-05-03');
INSERT INTO `tbl_noccomplaint` VALUES ('5', '3', '3', 'I am not do this crime', '2019-05-04');
INSERT INTO `tbl_noccomplaint` VALUES ('6', '3', '3', 'Its fake noc. Iam not robbered', '2019-05-09');

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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_policestation
-- ----------------------------
INSERT INTO `tbl_policestation` VALUES ('1', 't', 't', '5678906567', '7890765456', 'h@gmail.com', 'gg', 'g', 'g', 'g');
INSERT INTO `tbl_policestation` VALUES ('2', 'nn', 'nn', '1234567890', '1234567890', 'nn@gmail.com', 'nn', 'nn', 'nn', 'nn');
INSERT INTO `tbl_policestation` VALUES ('3', 'bb', 'uu', '1234567890', '1234567898', 'bb@gmail.com', 'uuu', 'bb', 'bb', 'bb');
INSERT INTO `tbl_policestation` VALUES ('4', 'cc', 'cc', '987654321', '987410000', 'nj@gmail.com', 'nn', 'nn', 'nn', 'nn');
INSERT INTO `tbl_policestation` VALUES ('5', 'kottayam', 'rrr', '987654321', '987654321', 'ktym@gmail.com', 'rrr', 'rrr', 'rr', 'rr');

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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_vacancy
-- ----------------------------
INSERT INTO `tbl_vacancy` VALUES ('2', '2019-03-15 15:41:40.583000', '10', 'tailor', '3', 'ff');
INSERT INTO `tbl_vacancy` VALUES ('3', '2019-05-04', '12', 'plumber', '67', 'not any hard working');
INSERT INTO `tbl_vacancy` VALUES ('4', '2019-05-09', '12', 'Tailor', '4', 'Its tasome a tailorig shop. I some hardworking tailors with 3 yr experience');

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
INSERT INTO `tbl_worker` VALUES ('1', 'pictures/Mega_HD_Wallpapers_1_sXjvBQo.png', 'aysha', 'female', '2019-03-17', 'xx', '2019-04-11', 'xx', 'pp', 'xx', '0987654321', '0987654321', 'aysha@gmail.com', 'qq', 'fixed');
INSERT INTO `tbl_worker` VALUES ('2', 'pictures/Mega_HD_Wallpapers_10_jaL8Ro8.jpg', 'kavya', 'female', '2019-03-15', 'xx', '2019-03-15 12:09:34.637000', 'cc', 'cc', 'cc', '0987654321', '098764321', 'kavya@gmail.com', 'cc', 'fixed');
INSERT INTO `tbl_worker` VALUES ('3', 'pictures/Mega_HD_Wallpapers_19.jpg', 'sumi', 'male', '2019-03-18', 'ss', '2019-03-15 12:09:34.637000', 'sss', 'ss', 'sss', '0987654321', '0987654321', 'sumi@gmail.com', 'dd', 'fixed');
INSERT INTO `tbl_worker` VALUES ('4', 'pictures/Mega_HD_Wallpapers_12_PVyNKC6.jpg', 'vvv', 'male', '2019-03-19', 'xcv', '2019-03-16 12:03:41.323000', 'vvv', 'vvv', 'vvv', '0987654321', '0987654321', 'kkv@gmail.com', 'vv', 'Rejected');
INSERT INTO `tbl_worker` VALUES ('5', 'pictures/Mega_HD_Wallpapers_19_BYMaZF9.jpg', 'bbbv', 'male', '2019-06-16', 'vvv', '2019-03-16 12:03:41.323000', 'vvvv', 'vvv', 'vvv', '0987654321', '0987621098', 'nnk@gmail.com', 'nnk', 'Rejected');
INSERT INTO `tbl_worker` VALUES ('6', 'pictures/Mega_HD_Wallpapers_10_EcoOuOw.jpg', 'kavitha', 'female', 'female', '2019-03-18', '2019-03-25 09:48:14.083000', '2019-03-16 13:13:25.716000', 'kk', 'sss', 'sss', '0987654321', '09876321', 'nayan', 'Pending');
INSERT INTO `tbl_worker` VALUES ('7', 'pictures/Mega_HD_Wallpapers_13_tnk8K2a.jpg', 'sweety', 'male', '2019-06-16', 'xxx', '2019-03-16 13:27:58.384000', 'vvv', 'sss', 'ttt', '0987654321', '0987654321', 'sweety@gmail.com', 'sweety', 'Rejected');
INSERT INTO `tbl_worker` VALUES ('8', 'pictures/Mega_HD_Wallpapers_115.jpg', 'juna thomas', 'female', '2019-04-12', 'hhh', '2019-04-11', 'jj', 'jj', 'jj', '0987654321', '0987654321', 'juna@gmail.com', 'juna', 'Active');

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
INSERT INTO `tbl_workerdetails` VALUES ('12', '12', 'hf', '5');
INSERT INTO `tbl_workerdetails` VALUES ('11', '6', 'VCB', '5');
INSERT INTO `tbl_workerdetails` VALUES ('11', '6', 'VCB', '5');
INSERT INTO `tbl_workerdetails` VALUES ('11', '6', 'MCA', '1');
INSERT INTO `tbl_workerdetails` VALUES ('5', '6', 'ghgh', '4');
INSERT INTO `tbl_workerdetails` VALUES ('5', '1', 'mca', '2');
INSERT INTO `tbl_workerdetails` VALUES ('0', '1', 'rr', '8');
INSERT INTO `tbl_workerdetails` VALUES ('0', '2', '10', '2');
INSERT INTO `tbl_workerdetails` VALUES ('3', '2', 'cdc', '1');
INSERT INTO `tbl_workerdetails` VALUES ('2', '3', 'cxc', '3');
INSERT INTO `tbl_workerdetails` VALUES ('3', '3', 'fff', '1');
INSERT INTO `tbl_workerdetails` VALUES ('1', '3', 'ddd', '34');
INSERT INTO `tbl_workerdetails` VALUES ('5', '3', 'nnn', '9');
INSERT INTO `tbl_workerdetails` VALUES ('7', '3', 'www', '2');
INSERT INTO `tbl_workerdetails` VALUES ('8', '3', 'mca', '2');

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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tbl_workershedule
-- ----------------------------
INSERT INTO `tbl_workershedule` VALUES ('10', '12', '3', 'tailor', '200', '2019-03-18', '2hr');
INSERT INTO `tbl_workershedule` VALUES ('11', '12', '3', 'road', '400', '2019-04-09', '7hr');
INSERT INTO `tbl_workershedule` VALUES ('13', '12', '2', 'shop', '300', '2019-04-09', '8hr');
INSERT INTO `tbl_workershedule` VALUES ('14', '12', '2', 'TAILOR', '500', '2019-05-04', '5');
INSERT INTO `tbl_workershedule` VALUES ('15', '12', '3', 'Plumber', '300', '2019-05-04', '2hr');
INSERT INTO `tbl_workershedule` VALUES ('16', '12', '3', 'painting', '500', '2019-05-06', '2hr');
INSERT INTO `tbl_workershedule` VALUES ('17', '12', '2', 'hotel', '400', '2019-05-06', '10hr');
INSERT INTO `tbl_workershedule` VALUES ('18', '12', '3', 'Tailor', '400', '2019-05-09', '5hr');
INSERT INTO `tbl_workershedule` VALUES ('19', '12', '7', 'Plumber', '3000', '2019-05-09', '15hr');
INSERT INTO `tbl_workershedule` VALUES ('20', '12', '3', 'Carpender', '500', '2019-05-12', '8hr');
