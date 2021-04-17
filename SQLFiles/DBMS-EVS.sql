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
insert into event_table values
 (1,'Event1','05-05-21','Ahmedabad','12:00:00','A'),
 (2,'Event2','05-05-21','Baroda','12:00:00','A'),
 (3,'Event3','05-05-21','Ahmedabad','12:00:00','A'),
 (4,'Event4','05-05-21','Baroda','12:00:00','A');
-- TO DISPLAY MY EVENTS
-- select event_name , email from registration where email=login.email; -- YOu MIGHT SHOW A REGISTERED AND TICK BESIDE 
-- TO FILTER USING PROCEDURE
drop procedure if exists filtervenue ;
delimiter $$
create procedure filtervenue()
	begin
		declare c_end int default 0;
		declare r_cityname varchar(50);
		declare count_event int;
		declare c_event cursor for select venue from event_table;
		declare continue handler for not found set c_end=1;

        open c_event;
        getvenuename: LOOP
        fetch c_event into r_cityname;
      --  select event_count;
			if c_end=1 then
				leave getvenuename;
			end if;
            select event_count(r_cityname) into count_event ;
			select r_cityname as "VENUE:", count_event as "Total Events";
            select event_name as "Event",date_format(event_date,"%M %d %Y") as "Date",event_time as "Time" from event_table
            where venue=r_cityname;
		end loop;
		close c_event;
	end$$
delimiter ;
-- select count(*) from event_table;

-- create function event_count
drop function if exists event_count ;
delimiter $$
 create function event_count(city_name varchar(20)) returns int deterministic
	begin 
		declare totnum int default 0;
        select count(event_no) from event_table where event_table.venue=city_name into totnum;-- as "Upcoming Events";
       -- call filtervenue();
        return totnum;
	end$$
delimiter ;
insert into login values ('m@g.com','123'),('b@g.com','123');
-- Trigger for checking if the email id exists or not
drop trigger if exists check_login;
delimiter $$
	create trigger check_login before insert on login for each row
		begin
        declare old_email varchar(50);
        select email from login where email=new.email into old_email;
		if old_email is not null then
			signal sqlstate '66666'
			set message_text="Lodu pachu kem nakhe che";
        end if;
	end $$
delimiter ;	

-- Trigger for checking if the email id exists or not
drop trigger if exists check_loginup;
delimiter $$
	create trigger check_loginup before update on login for each row
		begin
        declare old_email varchar(50);
        select email from login where email=new.email into old_email;
		if old_email is not null then
			signal sqlstate '66667'
			set message_text="Already exists Dafod Chal chal biju lai";
			end if;
	end $$
delimiter ;	

-- TRIGGER TO ASK FOR FEEDBACK 
drop trigger if exists bhar_feedback;
delimiter $$
	create trigger bhar_feedback before insert on login for each row
		begin 
			


