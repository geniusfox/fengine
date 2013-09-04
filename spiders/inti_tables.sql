DROP TABLE IF EXISTS `loan_items`;
CREATE TABLE `loan_items` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `loan_title` varchar(255) NOT NULL, #借款标题
  `loan_amount` int(11) NOT NULL, #借款总额
  `loan_term` int(11) NOT NULL, #借款期限
  `interest_rate` int(11) NOT NULL, #年化收益率
  `min_investment` int(11) DEFAULT 0, # 最小的投资额度
  `dest_url` varchar(1024) NOT NULL, #项目的详细地址
  `loan_type` varchar(50) DEFAULT NULL, #借款类型
  `credit_rating` varchar(10) DEFAULT NULL, #信用等级
  `progress_rate` int(11) DEFAULT NULL, 
  `site_id` varchar(10) NOT NULL DEFAULT '', #站点名称
  `unique_id` varchar(255) NOT NULL, #项目的唯一识别ID
  `item_endtime` bigint(18), #融资的结束时间
  `update_time` bigint(18) NOT NULL,
  `item_status` tinyint(2) NOT NULL,
  #PRIMARY KEY (`id`),
  KEY `index_site_status` (`site_id`,`item_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;