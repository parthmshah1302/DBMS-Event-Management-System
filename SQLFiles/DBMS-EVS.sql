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
 insert into login values ('m@g.com','123'),('b@g.com','123');
 insert into login values ('parthmshah1302@gmail.com','123'),('malavdoshi312@gmail.com','123');

insert into event_table (event_no, event_name, event_date, venue, event_time, event_type) values (1, 'Kamba', '2020-07-10', 'Shebunino', '15:22:10', 'Stronghold');
insert into event_table (event_no, event_name, event_date, venue, event_time, event_type) values (2, 'Yodoo', '2021-01-24', 'Abilay', '3:17:11', 'Aerified');
insert into event_table (event_no, event_name, event_date, venue, event_time, event_type) values (3, 'Zoomcast', '2020-07-15', 'Isnos', '6:57:29', 'Temp');
insert into event_table (event_no, event_name, event_date, venue, event_time, event_type) values (4, 'Quaxo', '2020-08-07', 'Paratunka', '14:55:36', 'Latlux');
insert into event_table (event_no, event_name, event_date, venue, event_time, event_type) values (5, 'Midel', '2021-02-25', 'Morro do ChapÃ©u', '22:25:36', 'Zaam-Dox');

insert into registration values 
(500,'Parth' ,'91932419f','parthmshah1302@gmail.com','Cash','A103','AU','g','Zoomcast',3),
(500,'Pnot' ,'91542919','m@g.com','Cash','A104','AU','g','Quaxo',4),
(500,'Malav' ,'91919439','malavdoshi312@gmail.com','Cheque','A106','AU','g','Zoomcast',3),
(500,'Parth' ,'91932419','parthmshah1302@gmail.com','Cash','A105','AU','g','Yoodo',2),
(500,'Pusrshotam' ,'919191919','b@g.com','Cash','A106','AU','g','Kamba',1),
(500,'Malav' ,'91919439','malavdoshi312@gmail.com','Cheque','A102','AU','g','Yoodo',2);

insert into sponsorship_package values ('GOLD' ,'sample');
insert into sponsorship_package values ('PLATINIUM' ,'sample');
insert into sponsorship_package values ('SILVER' ,'sample');
insert into sponsors values ('Manikchand','Muh mai',10000,'9999999','GOLD',1,'Kamba'),
							('RMD','Yeh bhi Muh mai',10000,'9999999','SILVER',2,'Yodoo'),
							('Old monk','Liver mai',10000,'9999999','PLATINIUM',4,'Quaxo'),
							('Parth Industires','Bhrigu lake',10000,'9999999','GOLD',1,'Kamba');
-- TO DISPLAY MY EVENTS
-- select event_name , email from registration where email=login.email; -- YOu MIGHT SHOW A REGISTERED AND TICK BESIDE 
-- TO FILTER USING PROCEDURE



-- PROCEDURE


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


-- Procdeure for extracting 

drop procedure if exists registeredusers;
delimiter $$
create procedure registeredusers()
	begin
		declare c_end int default 0;
		declare r_eventreg varchar(50);
        declare count_var int;
		declare c_registeredpeps cursor for select distinct event_name from registration order by event_name;
		declare continue handler for not found set c_end=1;
        open c_registeredpeps;
        getmailinglist: loop
			fetch c_registeredpeps into r_eventreg ;
				if c_end=1 then
					leave getmailinglist;
				end if;
               select distinct r_eventreg as "Event Name";
					select email,customer_name from registration where registration.event_name=r_eventreg ;
					-- select count(email), fees from registration where registration.event_name = r_eventreg into count_var;
            end loop;
		close c_registeredpeps;
	end$$
delimiter ;
call registeredusers();

-- Total collection on basis of event
drop procedure if exists event_collection;
delimiter $$;
create procedure event_collection(event_fee int)
begin 
    declare amt double default 0.0;
	declare reg_users int default 0;
	
    end loop;
    return amount;

end $$
delimiter ;


-- CREATE PROCEDURE CONTACT US
-- drop procedure if exists contact_us;
-- delimiter $$;
-- create procedure contact_us (dept_name varchar(20))
-- begin 
-- 	select 
		
        
        
-- FUNCTION   



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


-- calculate total amt in trigger
drop function if exists totalamt;
delimiter $$
create function totalamt(b_no int) returns double deterministic
	begin
		declare c_end int default 0;
		declare r_totalamt varchar(50);
        declare total_amount double default 0.0;
        declare amt double default 0.0;
        declare t1 double default 0.0;
        declare del double default 0.0;
		declare c_bills cursor for select amount from bill where bill.bill_no=b_no;
		declare continue handler for not found set c_end=1;
        open c_bills;
        gettotamt: loop
			fetch c_bills into r_totalamt ;
				if c_end=1 then
					leave gettotamt;
				end if;
			select amount from bill where bill.bill_no=b_no into amt  ;
			select tax from bill where bill.bill_no=b_no into t1 ;
			select del_charge from bill where bill.bill_no=b_no into del ;
            set total_amount=amt+(amt*t1/100)+del;
		end loop;
        return total_amount;
        end$$
	delimiter ;
    INSERT INTO `dbmseventmanagement`.`bill` (`bill_no`, `order_no`, `amount`, `tax`, `del_charge`, `bill_date`, `email`) VALUES ('1', '101', '200', '18', '33', '2021-04-13', 'malavdoshi312@gmail.com');
    select totalamt("1") as "Ans";

-- Function to return all the events of specific type
drop function if exists search_eventtype ;
delimiter $$
 create function search_eventtype (eventtype varchar(20)) returns table (event_type)
		

-- TRIGGER


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


-- Trigger to check email while login
drop trigger if exists validemail_i;
delimiter $$
	create trigger validemail_i before insert on login for each row
    begin
		if new.email not like '%@%' then
			signal sqlstate value '91302'
			set message_text = 'The email you entered is invalid';
		elseif char_length(new.email) <5 then
			signal sqlstate value '91605'
			set message_text = 'The email you entered is invalid lenght';
		end if;
    end$$
delimiter ;

-- Trigger to check email while login -- TO DO: CHECK FIRST if email exists
drop trigger if exists validemail_u;
delimiter $$
	create trigger validemail_u before update on login for each row
    begin
		if new.email not like '%@%' then
			signal sqlstate value '93102'
				set message_text = 'The email you updated is invalid';
		elseif char_length(new.email) <5 then
			signal sqlstate value '92001'
			set message_text = 'The email you entered is invalid length';
		end if;
    end$$
delimiter ;

-- Trigger for event deleted from event table then delete it from regisration and sponsors
drop trigger if exists event_delete;
delimiter $$
	create trigger event_delete before delete on event_table for each row
		begin 
			delete from registration where event_no=old.event_no;
            delete from sponsors where event_no=old.event_no;
		end $$
	delimiter ;
delete from event_table where event_name='Zoomcast';


-- TRIGGER TO ASK FOR FEEDBACK 
-- drop trigger if exists add_feedback;
-- delimiter $$
-- 	create trigger add_feedback after delete on event_table for each row
-- 	begin
-- 		insert into feedback values 