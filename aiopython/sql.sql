DROP TABLE IF EXISTS users;
CREATE TABLE users(
    id INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL DEFAULT '',
    email VARCHAR(256) NOT NULL DEFAULT '',
    city VARCHAR(256) NOT NULL DEFAULT '',
    PRIMARY KEY(id)
) ENGINE=INNODB;
INSERT INTO users(name, email, city) VALUES ('test name1', 'abcf@mail.ru', 'Moscow');
INSERT INTO users(name, email, city) VALUES ('test name2', 'notreplay@joom.ru', 'London');
INSERT INTO users(name, email, city) VALUES ('test name3', '123@oops.com','Yekaterinburg');

DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts(
    id INT(11) NOT NULL AUTO_INCREMENT,
    email VARCHAR(256) NOT NULL DEFAULT '',
    fname VARCHAR(256) NOT NULL DEFAULT '',
    sname VARCHAR(256) NOT NULL DEFAULT '',
    status VARCHAR(256) NOT NULL DEFAULT '',
    country VARCHAR(256) NOT NULL DEFAULT '',
    city VARCHAR(256) NOT NULL DEFAULT '',
    phone VARCHAR(256) NOT NULL DEFAULT '',
    sex VARCHAR(256) NOT NULL DEFAULT '',
    joined INT(11) NOT NULL DEFAULT 0,
    birth INT(11) NOT NULL DEFAULT 0,
    ext_id INT(11) NOT NULL DEFAULT 0,
    PRIMARY KEY(id)
) ENGINE=INNODB;
INSERT INTO accounts(fname, sname) VALUES ('tets2', 'test2');

CREATE TABLE accounts_like(
    id INT(11)  NOT NULL AUTO_INCREMENT,
    like_id INT(11),
    like_ts INT(11),
    acc_id INT(11),
    PRIMARY KEY(id),
    FOREIGN KEY(acc_id) REFERENCES accounts(ext_id) ON DELETE CASCADE
) ENGINE=INNODB; 

CREATE TABLE accounts_premium(
    id INT(11)  NOT NULL AUTO_INCREMENT,
    start INT(11),
    finish INT(11),
    acc_id INT(11),
    FOREIGN KEY(acc_id) REFERENCES accounts(ext_id)
) ENGINE=INNODB; 

CREATE TABLE accounts_int(11)erest(
    id INT(11)  NOT NULL AUTO_INCREMENT,
    int(11)erest VARCHAR(256),
    acc_id INT(11),
    FOREIGN KEY(acc_id) REFERENCES accounts(ext_id)
) ENGINE=INNODB; 