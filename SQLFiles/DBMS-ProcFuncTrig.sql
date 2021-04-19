use dbmsEventManagement;
-- PROCEDURE


-- #1 TO filter acc to venue
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



-- #2 Procedure for extracting 
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



-- #3 Procedure to Calculate 
drop procedure if exists total_collection;
delimiter $$
create procedure total_collection(p_fees int,p_event_name varchar(20))
begin
	declare c_end int default 0;
    declare r_eventname varchar(20);
    declare r_count int;
	declare ans int;
	select count(r.customer_name) from registration r left join event_table e on e.event_no=r.event_no where e.event_name=p_event_name into r_count;
	set ans=r_count*p_fees;
    select r_eventname as "Event name";
    select ans as "Total Collection";
end $$
delimiter ;
call total_collection(500,'Zoomcast');


-- #4 CREATE PROCEDURE CONTACT US
drop procedure if exists contact_us;
delimiter $$
create procedure contact_us (dept_name varchar(20))
begin 
	select department_name,team_member_id,member_name, mob_num, position from team where department_name=dept_name;
end$$
delimiter ;
	
    
-- #5 Create a procedure to return reviews of the event and Keyword for it which displays the sentiment of the feedback in single word powered by IBM Watson 
drop procedure if exists event_feedback;
delimiter $$
create procedure event_feedback()
begin
	declare c_end int default 0;
    declare r_event_no varchar(50);
    declare r_email varchar(50);
    declare r_event_name varchar(50);
    declare c_eventfeedback cursor for select distinct event_no,email from registration order by event_no;
	declare continue handler for not found set c_end=1;
    open c_eventfeedback;
		getfeedback: loop
			fetch c_eventfeedback into r_event_no,r_email ;
				if c_end=1 then
					leave getfeedback;
				end if;
			select event_name from event_table where event_no=r_event_no into r_event_name ;
            -- select r.email, f.title, f.message, f.Date, f.time, f.sentiment from registration r right join on feedback f on f.email=r.email where e.event_name=r_event_name;
			select distinct r_event_name as "Event Name",r.customer_name, f.title, f.message, f.Date, f.time, f.sentiment from  feedback f left join registration r on r.email=f.email where f.email=r_email and r_event_no=f.event_no;
		end loop;
	close c_eventfeedback;
end$$
delimiter ;


-- #6 Procedure to display bill of a user --TO BE CHECKED
drop procedure if exists customer_bill;
delimiter $$
create procedure customer_bill(p_email varchar(50),p_pass varchar(20))
begin
	declare c_end int default 0;
    declare r_bill varchar(50);
    declare r_email varchar(50);
    declare c_bill cursor for select distinct email from bill;
	declare continue handler for not found set c_end=1;
    open c_bill;
		getbill: loop
			fetch c_bill into r_bill ;
				if c_end=1 then
					leave getbill;
				end if;
			select * from bill where email=r_bill and login.pass=p_pass;
		end loop;
	close c_bill;
end$$
delimiter ;


-- #7 Procedure for extracting 

drop procedure if exists sponsor_event;
delimiter $$
create procedure sponsor_event()
    begin
        declare c_end int default 0;
        declare r_eventsp varchar(50);
        declare count_var int;
        declare c_sponsor cursor for select distinct event_no from event_table order by event_name;
        declare continue handler for not found set c_end=1;
        open c_sponsor;
        getsp: loop
            fetch c_sponsor into r_eventsp ;
                if c_end=1 then
                    leave getsp;
                end if;
                    select e.event_name from event_table e where e.event_no = r_eventsp;
                    select s.sponsors_name from event_table e left join sponsors s on e.event_no=s.event_no
					where e.event_no=r_eventsp ;
            end loop;
        close c_sponsor;
    end$$
delimiter ;
call sponsor_event();


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

-- Search function to calculate total sponsors of searched event
drop function if exists event_spcount ;
delimiter $$
 create function event_spcount(r_event_name varchar(20)) returns int deterministic
    begin 
        declare totnum int default 0;
        select count(sponsors_name) from sponsors s left join event_table e on e.event_no=s.event_no 
		where e.event_name=r_event_name into totnum;
        return totnum;
    end$$
delimiter ;

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
			set message_text="Email is invalid/duplicate. Please try again!";
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
			set message_text="Email is invalid/duplicate. Please try again!";
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

-- DELETE TRIGGERS:

-- Trigger for event deleted from event table then delete it from registration and sponsors:

drop trigger if exists event_delete;
delimiter $$
	create trigger event_delete before delete on event_table for each row
		begin 
			delete from registration where event_no=old.event_no;
            delete from sponsors where event_no=old.event_no;
		end $$
	delimiter ;
delete from event_table where event_name='Quaxo';

-- Triggers to delete in Login Table

drop trigger if exists login_delete;
delimiter $$
	create trigger login_delete before delete on login for each row
		begin 
			delete from registration where email=old.email;
			delete from feedback where email=old.email;
			delete from bill where email=old.email;
		end $$
	delimiter ;

-- Trigger to delete in sponsor_type 

drop trigger if exists sponsor_package_delete;
delimiter $$
	create trigger sponsor_package_delete before delete on sponsorship_package for each row
		begin 
			delete from sponsors where sponsor_type=old.sponsor_type;
		end $$
	delimiter ;

-- Trigger to delete in department

drop trigger if exists department_delete;
delimiter $$
	create trigger department_delete before delete on department for each row
		begin 
			delete from vendors where vendor_name=old.vendor_relation;
            delete from team where department_name=old.department_name;
		end $$
	delimiter ;

-- Trigger to update values in tables:

-- Trigger for event deleted from event table then delete it from regisration and sponsors

-- Trigger To Update 
drop trigger if exists event_update;
delimiter $$
	create trigger event_update after update on event_table for each row
		begin 
			update registration set event_no=new.event_no where event_no=old.event_no;
			update sponsors set event_no=new.event_no where event_no=old.event_no;
			update feedback set event_no=new.event_no where event_no=old.event_no;
		end $$
delimiter ;
-- update event_table set event_no=100 where event_no=1;
-- 7
drop trigger if exists login_update;
delimiter $$
    create trigger login_update after update on login for each row
        begin 
            update registration set email=new.email where email=old.email;
            update feedback set email=new.email where email=old.email;
            update bill set email=new.email where email=old.email;
        end $$
delimiter ;




-- Trigger to assignnent 
-- TRIGGER TO ASK FOR FEEDBACK 
-- drop trigger if exists add_feedback;
-- delimiter $$
-- 	create trigger add_feedback after delete on event_table for each row
-- 	begin
-- 		insert into feedback values 
