/*
 Navicat MySQL Data Transfer

 Source Server         : 我的服务器
 Source Server Type    : MySQL
 Source Server Version : 50717
 Source Host           : localhost:3306
 Source Schema         : aj

 Target Server Type    : MySQL
 Target Server Version : 50717
 File Encoding         : 65001

 Date: 20/06/2018 21:04:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ihome_area
-- ----------------------------
DROP TABLE IF EXISTS `ihome_area`;
CREATE TABLE `ihome_area`  (
  `create_time` datetime(0) NULL DEFAULT NULL,
  `update_time` datetime(0) NULL DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ihome_area
-- ----------------------------
INSERT INTO `ihome_area` VALUES (NULL, NULL, 1, '锦江区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 2, '金牛区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 3, '青羊区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 4, '高新区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 5, '武侯区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 6, '天府新区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 7, '双流县');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 8, '成华区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 9, '青白江区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 10, '新都区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 11, '温江区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 12, '温江区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 13, '郫县');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 14, '蒲江县');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 15, '大邑县');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 16, '新津县');

-- ----------------------------
-- Table structure for ihome_facility
-- ----------------------------
DROP TABLE IF EXISTS `ihome_facility`;
CREATE TABLE `ihome_facility`  (
  `create_time` datetime(0) NULL DEFAULT NULL,
  `update_time` datetime(0) NULL DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `css` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ihome_facility
-- ----------------------------
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 1, '无线网络', 'wirelessnetwork-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 2, '热水淋浴', 'shower-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 3, '空调', 'aircondition-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 4, '暖气', 'heater-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 5, '允许吸烟', 'smoke-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 6, '饮水设备', 'drinking-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 7, '牙具', 'brush-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 8, '香皂', 'soap-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 9, '拖鞋', 'slippers-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 10, '手纸', 'toiletpaper-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 11, '毛巾', 'towel-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 12, '沐浴露、洗发露', 'toiletries-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 13, '冰箱', 'icebox-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 14, '洗衣机', 'washer-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 15, '电梯', 'elevator-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 16, '允许做饭', 'iscook-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 17, '允许带宠物', 'pet-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 18, '允许聚会', 'meet-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 19, '门禁系统', 'accesssys-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 20, '停车位', 'parkingspace-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 21, '有线网络', 'wirednetwork-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 22, '电视', 'tv-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 23, '浴缸', 'jinzhi-ico');

-- ----------------------------
-- Table structure for ihome_house
-- ----------------------------
DROP TABLE IF EXISTS `ihome_house`;
CREATE TABLE `ihome_house`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(0) NULL DEFAULT NULL,
  `update_time` datetime(0) NULL DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `title` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `price` int(11) NULL DEFAULT 0,
  `address` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '',
  `room_count` int(11) NULL DEFAULT 1,
  `acreage` int(11) NULL DEFAULT 0,
  `unit` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '',
  `capacity` int(11) NULL DEFAULT 1,
  `beds` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '',
  `deposit` int(11) NULL DEFAULT 0,
  `min_days` int(11) NULL DEFAULT 1,
  `max_days` int(11) NULL DEFAULT 0,
  `order_count` int(11) NULL DEFAULT 0,
  `index_image_url` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_house_u`(`user_id`) USING BTREE,
  INDEX `fk_area`(`area_id`) USING BTREE,
  CONSTRAINT `fk_area` FOREIGN KEY (`area_id`) REFERENCES `ihome_area` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_house_u` FOREIGN KEY (`user_id`) REFERENCES `ihome_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ihome_house_facility
-- ----------------------------
DROP TABLE IF EXISTS `ihome_house_facility`;
CREATE TABLE `ihome_house_facility`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(0) NULL DEFAULT NULL,
  `update_time` datetime(0) NULL DEFAULT NULL,
  `house_id` int(11) NOT NULL,
  `facility_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_f_id`(`house_id`) USING BTREE,
  INDEX `fk_fy_id`(`facility_id`) USING BTREE,
  CONSTRAINT `fk_f_id` FOREIGN KEY (`house_id`) REFERENCES `ihome_house` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_fy_id` FOREIGN KEY (`facility_id`) REFERENCES `ihome_facility` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ihome_house_image
-- ----------------------------
DROP TABLE IF EXISTS `ihome_house_image`;
CREATE TABLE `ihome_house_image`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(0) NULL DEFAULT NULL,
  `update_time` datetime(0) NULL DEFAULT NULL,
  `house_id` int(11) NOT NULL,
  `url` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_ho_id`(`house_id`) USING BTREE,
  CONSTRAINT `fk_ho_id` FOREIGN KEY (`house_id`) REFERENCES `ihome_house` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ihome_order
-- ----------------------------
DROP TABLE IF EXISTS `ihome_order`;
CREATE TABLE `ihome_order`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `create_time` datetime(0) NULL DEFAULT NULL,
  `update_time` datetime(0) NULL DEFAULT NULL,
  `begin_date` datetime(0) NULL,
  `end_date` datetime(0) NULL,
  `days` int(11) NOT NULL,
  `house_price` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `status` enum('WAIT_ACCEPT','WAIT_PAYMENT','PAID','WAIT_COMMENT','COMPLETE','CANCELED','REJECTED') CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT 'WAIT_ACCEPT',
  `comment` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_user_i`(`user_id`) USING BTREE,
  INDEX `fk_ho_i`(`house_id`) USING BTREE,
  CONSTRAINT `fk_ho_i` FOREIGN KEY (`house_id`) REFERENCES `ihome_house` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_user_i` FOREIGN KEY (`user_id`) REFERENCES `ihome_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ihome_user
-- ----------------------------
DROP TABLE IF EXISTS `ihome_user`;
CREATE TABLE `ihome_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `pwd_hash` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `avatar` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `id_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `id_card` varchar(18) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `create_time` datetime(0) NULL DEFAULT NULL,
  `update_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `phone`(`phone`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  UNIQUE INDEX `id_card`(`id_card`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ihome_user
-- ----------------------------
INSERT INTO `ihome_user` VALUES (1, '15512341234', 'pbkdf2:sha256:50000$1q4bOp4U$0177650eb41e2326f9c332d4cb324f80ef5637d56c88d84a41dd1599cf06fde1', '小黄', 'mm.jpg', '小黄黄', '123456789012345678', '2018-06-20 17:34:51', '2018-06-20 20:05:56');

SET FOREIGN_KEY_CHECKS = 1;
