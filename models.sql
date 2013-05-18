create table if not exists `profile`(
    `token` varchar(100),
    `secret` varchar(100),
    `username` varchar(100) UNIQUE,
    `flickr_id` varchar(100) UNIQUE,
    `about_id` varchar(20) UNIQUE,
    `facepp_id` varchar(20) UNIQUE, 
    `avatar_id` varchar(20) UNIQUE,
    PRIMARY KEY (`token`)
) ENGINE = InnoDB DEFAULT CHARSET=utf8;


create table if not exists `record`(
    `yid` varchar(20),
    `be_yid` varchar(20),
    `ctime` int(11),
    `geo` varchar(255),
    PRIMARY KEY (`yid`, `be_yid`, `ctime`)
) ENGINE = InnoDB DEFAULT CHARSET=utf8;
