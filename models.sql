create table if not exists `profile`(
    `yid` varchar(20),
    `ytoken` varchar(100),
    `about_id` varchar(20),
    `facepp_id` varchar(20), 
    `avatar_id` varchar(20),
    PRIMARY KEY (`yid`)
) ENGINE = InnoDB DEFAULT CHARSET=utf8;


create table if not exists `record`(
    `yid` varchar(20),
    `be_yid` varchar(20),
    `ctime` int(11),
    `geo` varchar(255),
    PRIMARY KEY (`yid`, `be_yid`, `ctime`)
) ENGINE = InnoDB DEFAULT CHARSET=utf8;
