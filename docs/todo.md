##ToDo List
* 按天计息的数据处理，借款单位也是天
* Detail页面的数据的抓取,如果设置Detail的数据抓取任务
* 服务器部署
* 处理过的数据标记 loan_items
* 修改P2P项目状态码，参考HttpStatus Code的规则，100，200预留标志位
* 前端的数据API设计&开发
* 已经收录网站的Summary信息统计：网站名称、总项目、成功、募资总额、逾期总额....
* 人人贷网站List数据抓取代码改写
* 红岭创投的DetailURL缺少路径信息

##ChangeLog
###2013/09/05
* 修改P2P项目状态码，参考HttpStatus Code的规则，100，200预留标志位； 包括all_loan_itmes的item_status字段长度；
* 增加FullLoanItem的类定义，当贷款进度更新或者筹款总额变动时自动更新状态编码
* 增加点融的数据抓取