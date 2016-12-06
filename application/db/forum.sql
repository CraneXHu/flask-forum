drop table if exists user;
create table user (
  id int primary key auto_increment,
  username varchar(20) not null,
  email varchar(30) not null,
  password varchar(32) not null,
  avatar varchar(50),
  create_at datetime default now()
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;

drop table if exists social_account;
create table social_account (
  id int primary key auto_increment,
  user_id int not null,
  github varchar(32),
  weibo varchar(32),
  twitter varchar(50),
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;

drop table if exists reset_password;
create table reset_info (
  user_id int primary key,
  expiration_time datetime not null,
  md5 varchar(32) not null,
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;

drop table if exists article;
create table article (
  id int primary key auto_increment,
  username varchar(20) not null,
  tag varchar(20) not null,
  title varchar(100) not null,
  content varchar(4000),
  comment_count int default 0,
  create_at datetime default now()
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;

drop table if exists comment;
create table comment (
  id int primary key auto_increment,
  articleId int not null,
  username varchar(20) not null,
  content varchar(1000),
  create_at datetime default now()
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;