DROP TABLE IF EXISTS `all_loan_items`;
CREATE TABLE `all_loan_items` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `unique_id` varchar(255) NOT NULL, #项目的唯一识别ID
  `loan_title` varchar(255) NOT NULL, #借款项目描述
  `loan_amount` int(11) NOT NULL, #借款总额
  `loan_term` int(11) NOT NULL, #借款期限
  `interest_rate` int(11) NOT NULL, #年化收益率
  `min_investment` int(11) DEFAULT 0, # 最小的投资额度
  `dest_url` varchar(1024) NOT NULL, #项目的详细地址
  `loan_type` varchar(50) DEFAULT NULL, #借款类型
  `credit_rating` varchar(10) DEFAULT NULL, #信用等级
  `site_id` varchar(10) NOT NULL DEFAULT '', #站点名称
  `item_endtime` bigint(18), #融资的结束时间
  `progress_rate` int(11) DEFAULT NULL, #借款进度
  `item_status` tinyint(2) NOT NULL, # 0 筹款, 1 满标, 2 开始还款, 3 还款结束
  `overdue` tinyint(1) DEFAULT  0, # 0 无逾期, 1 有部分逾期, 2 逾期
  `baddebt` tinyint(1) DEFAULT 0, # 0 正常 1 坏账
  `update_time` bigint(18) NOT NULL, #记录更新时间
#  PRIMARY KEY (`id`),
  KEY `index_site_status` (`site_id`,`item_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `index_engine_jobs`;
CREATE TABLE `index_engine_jobs` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `job_name` varchar(50) NOT NULL, #任务名称
  `update_time` bigint(18) NOT NULL, #任务结束时间
  key `index_jobname` (`job_name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
-- drop table if exists `online_loan_items`;
-- CREATE TABLE `online_loan_items` (
--   `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
--   `unique_id` varchar(255) NOT NULL, #项目的唯一识别ID
--   `loan_title` varchar(255) NOT NULL, #借款项目描述
--   `loan_amount` int(11) NOT NULL, #借款总额
--   `loan_term` int(11) NOT NULL, #借款期限
--   `interest_rate` int(11) NOT NULL, #年化收益率
--   `min_investment` int(11) DEFAULT 0, # 最小的投资额度
--   `dest_url` varchar(1024) NOT NULL, #项目的详细地址
--   `loan_type` varchar(50) DEFAULT NULL, #借款类型
--   `credit_rating` varchar(10) DEFAULT NULL, #信用等级
--   `site_id` varchar(10) NOT NULL DEFAULT '', #站点名称
--   `item_endtime` bigint(18), #融资的结束时间
--   `update_time` bigint(18) NOT NULL, #记录更新时间
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;