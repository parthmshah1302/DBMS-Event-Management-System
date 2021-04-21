create database dbmsEventManagement;

use dbmsEventManagement;

-- drop table feedback;
-- drop table inventory;
-- drop table team;
-- drop table department;
-- drop table vendors;
-- drop table sponsors;
-- drop table sponsorship_package;
-- drop table registration;
-- drop table account_table;
-- drop table bill;
-- drop table event_table;
-- drop table login;

create table login(email varchar(50) primary key, pass varchar(50));
create table event_table(
  event_no int auto_increment unique,
  primary key(event_no),
  event_name varchar(50),
  event_date date,
  venue varchar(50),
  event_time time,
  event_type varchar(50),
  index (event_name)
);


create table bill(
  bill_no int auto_increment unique,
  order_no int,
  amount double,
  tax double,
  del_charge double,
  final_amt double,
  bill_date date,
  email varchar(50),
  foreign key(email) references login(email),
  primary key(bill_no, order_no)
);


create table account_table(
  balance double,
  misc_charges double,
  receipt_name varchar(50),
  account_date date,
  bill_no int,
  foreign key(bill_no) references bill(bill_no),
  tot_amt double,
  paid_amt double
);
create table registration(
  fees double,
  customer_name varchar(50),
  mob_name varchar(50),
  email varchar(50),
  foreign key(email) references login(email),
  payment_mode varchar(50),
  sr_no varchar(50),
  college_name varchar(50),
  register_receipt varchar(50),
  event_name varchar(50),
  event_no int,
  foreign key(event_no) references event_table(event_no),
  primary key(event_no, sr_no)
);
create table sponsorship_package(
  sponsor_type varchar(50),
  deliverables varchar(50),
  primary key(sponsor_type)
);
create table sponsors(
  sponsors_name varchar(50),
  address varchar(50),
  amount double,
  mob_num int,
  sponsor_type varchar(50),
  foreign key(sponsor_type) references sponsorship_package(sponsor_type),
  event_no int,
  foreign key(event_no) references event_table(event_no),
  event_name varchar(50),
  foreign key(event_name) references event_table(event_name),
  primary key(sponsors_name, mob_num)
);
create table vendors(
  products_taken varchar(50),
  amount double,
  invoice_no varchar(50),
  vendor_name varchar(50),
  index (vendor_name),
  primary key(invoice_no)
);
create table department(
  department_name varchar(50),
  vendor_relation varchar(50),
  foreign key(vendor_relation) references vendors(vendor_name) on update cascade on delete cascade,
  work_scope varchar(50),
  primary key(department_name)
);
create table team (
  member_name varchar(50),
  mob_num int,
  department_name varchar(50),
  foreign key(department_name) references department (department_name) on update cascade on delete cascade,
  email varchar(50),
  team_member_id int,
  position varchar(50),
  primary key(team_member_id)
);
alter table team modify mob_num varchar(10);
create table inventory(
  item_code varchar (50),
  item_name varchar(50),
  quantity int,
  primary key(item_name, item_code)
);
create table feedback (
  email varchar(50),
  foreign key(email) references login(email) on update cascade on delete cascade,
  title varchar(50),
  message varchar(50),
  Date date,
  time time
);
alter table feedback modify message varchar(5000);
alter table feedback add Sentiment varchar(50);
alter table account_table add primary key(receipt_name);
alter table sponsors drop primary key;
alter table sponsors add primary key(sponsors_name,event_no);
alter table sponsors modify mob_num varchar(10);
