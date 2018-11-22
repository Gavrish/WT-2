drop user root;
create user root with password 'root';
grant all privileges on all tables in schema public to root;
drop database quizon;
create database quizon;
\c quizon

create table users(id serial, username varchar(30) primary key, overall float);

create table quiz(qid serial primary key, qname varchar(15));  

create table user_quiz(uqid serial primary key, qid int, username varchar(30), result float, FOREIGN KEY(username) REFERENCES users(username), FOREIGN KEY(qid) REFERENCES quiz(qid));

insert into users (username,overall) values ('g',0);
insert into quiz (qname) values ('celebrity');
insert into quiz (qname) values ('G.K');
insert into user_quiz (qid,username,result) values (1,'g',5);
insert into user_quiz (qid,username,result) values (2,'g',4);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO root;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO root;
