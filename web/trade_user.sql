DROP TABLE if exists`alipay`.`trade`;
DROP TABLE if exists`alipay`.`user`;
create table user(
`userid` varchar(255),
`name` varchar(255),
`sfz` varchar(255),
`zfb` varchar(255),
`phone` varchar(255),
primary key(userid)
)ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;
CREATE TABLE trade(
`user`varchar(255), 
`trade_no` varchar(255),
`out_trade_no` varchar(255),
`trade_status` varchar(255),
`code` varchar(255),
`total_amount` varchar(255),
`receipt_amount` varchar(255),
`buyer_logon_id` varchar(255),
`gmt_payment` varchar(255),
primary key(trade_no),
foreign key(user) references user(userid)
)ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;