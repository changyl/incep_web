create database incep_web;



CREATE TABLE `tb_databases_config` (
	`auto_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`id` INT(11) NOT NULL,
	`host` VARCHAR(45) NOT NULL,
	`user` VARCHAR(45) NOT NULL,
	`passwd` VARCHAR(45) NOT NULL,
	`port` INT(11) UNSIGNED NOT NULL DEFAULT '3306',
	`db_name` VARCHAR(45) NOT NULL DEFAULT '',
	`create_time` TIMESTAMP NOT NULL,
	`creator` INT(11) UNSIGNED NULL DEFAULT '0',
	`update_time` TIMESTAMP NOT NULL,
	`updator` INT(11) UNSIGNED NOT NULL DEFAULT '0',
	`flag` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0',
	`db_tag` VARCHAR(45) NOT NULL,
	PRIMARY KEY (`auto_id`),
	UNIQUE INDEX `id_UNIQUE` (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;


CREATE TABLE `tb_review` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`database_id` INT(10) UNSIGNED NOT NULL,
	`content` LONGTEXT NOT NULL,
	`creator` INT(11) UNSIGNED NOT NULL,
	`create_time` DATETIME NOT NULL,
	`flag` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0',
	`review_id` INT(10) UNSIGNED NOT NULL DEFAULT '0',
	`review_time` DATETIME NULL DEFAULT NULL,
	`remarks` VARCHAR(512) NOT NULL DEFAULT '',
	PRIMARY KEY (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

CREATE TABLE `tb_review_detail` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`tid` INT(11) NOT NULL DEFAULT '0',
	`stage` VARCHAR(120) NOT NULL DEFAULT '',
	`errlevel` INT(11) UNSIGNED NOT NULL DEFAULT '0',
	`stagestatus` VARCHAR(512) NOT NULL DEFAULT '',
	`errormessage` VARCHAR(1000) NOT NULL DEFAULT '',
	`SQL` VARCHAR(510) NOT NULL DEFAULT '',
	`Affected_rows` INT(10) UNSIGNED NOT NULL DEFAULT '0',
	`sequence` VARCHAR(50) NOT NULL DEFAULT '',
	`backup_dbname` VARCHAR(50) NOT NULL DEFAULT '',
	`execute_time` INT(11) NOT NULL DEFAULT '0' COMMENT '执行时间',
	`sqlsha1` VARCHAR(50) NOT NULL DEFAULT '',
	`sql_id` INT(11) NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`),
	UNIQUE INDEX `uniq_sqlid_tid` (`sql_id`, `tid`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;


CREATE TABLE `tb_review_history` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`database_id` INT(10) UNSIGNED NOT NULL,
	`content` TEXT NOT NULL,
	`creator` INT(11) UNSIGNED NOT NULL,
	`create_time` DATETIME NOT NULL,
	`flag` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0',
	`review_id` INT(10) UNSIGNED NOT NULL DEFAULT '0',
	`review_time` DATETIME NOT NULL,
	`remarks` VARCHAR(512) NOT NULL DEFAULT '',
	PRIMARY KEY (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tb_review_stat` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`amount` INT(11) NOT NULL DEFAULT '0',
	`data_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `data_date_UNIQUE` (`data_date`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;


CREATE DEFINER=`root`@`%` EVENT `e_daily_stat`
	ON SCHEDULE
		EVERY 1 DAY STARTS '2017-08-17 18:30:31'
	ON COMPLETION PRESERVE
	ENABLE
	COMMENT ''
	DO call stat_crud
	
	
	
CREATE DEFINER=`root`@`%` PROCEDURE `stat_crud`()
LANGUAGE SQL
NOT DETERMINISTIC
CONTAINS SQL
SQL SECURITY DEFINER
COMMENT ''
BEGIN
	insert into tb_review_stat(amount,data_date) SELECT count(*) cnt,date_format(create_time,'%Y-%m-%d 00:00:00') FROM auto_database.tb_review where create_time>concat(DATE_SUB(curdate(),INTERVAL 1 DAY),' 00:00:00') and create_time<concat(DATE_SUB(curdate(),INTERVAL 0 DAY),' 00:00:00') group by date_format(create_time,'%Y-%m-%d');
END
