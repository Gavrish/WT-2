drop user root;
create user root with password 'root';
grant all privileges on all tables in schema public to root;
drop database quizon;
create database quizon;
\c quizon

create table users(username varchar(30) primary key, email varchar(30));

create table quiz(qid serial primary key, qname varchar(15));  

create table user_quiz(uqid serial primary key, qid int, username varchar(30), result int, FOREIGN KEY(username) REFERENCES users(username), FOREIGN KEY(qid) REFERENCES quiz(qid));

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO root;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO root;
