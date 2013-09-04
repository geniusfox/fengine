##Spider系统功能
###抓取的通用功能
* Http连接的默认设置、是否Debug模式
* 抓取页面HTML内容的标记，提出掉无用的CSS、Script标签，在数据端前后增加<#data>...</#data>的标记
* 抓取的运行日志记录、状态分析
* 数据校验&入库

###每个Spider特殊部分
* 目标数据的URL
* 网页数据的解析，XML解析或者String直接正则获取
* 解析后的数据字段映射

###存储规则
* 根据抓取网站的id_[list/detail/..]_timestamp.html 文件存储

###基本字段

col_name | col_type | col_desc
------------ | ------------- | ------------
item_name	| varchar(255)	| 借款说明
loan_amount	| int(11)	| 借款总金额
loan_term	| int(8) | 按月计算的借款期限
interest_rate	| decimal(4,2) 	| 年利率，百分比数据 14.2% 
credit_rating	| varchar(255)	| 信用等级
repayment_method |tinyint(2)	| 还款方式
repayment_term	| tinyint(2)	| 还款周期
dest_url	| varch(1024)	| 目标地址
progress_rate	| int(3) | 项目进度
unique_id	| varchar(50) | 目标网站项目唯一标示，可以是ID，也可以是项目名字...



###抓取网站的列表
####人人贷 renrendai.com
	ListURL:http://www.renrendai.com/lend/lendPage.action
	数据字段:借款人、金额、利率、期限、信用等级
	唯一标示：loanId
	
####红岭创投

####陆金所

####点融
	