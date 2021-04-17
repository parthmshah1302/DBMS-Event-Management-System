create database employee;
use employee;

create table emp(emp_no int primary key , emp_name varchar(50), salary double , manager varchar(50) , dept_no int);

insert into emp
values
 (1,'Malav Doshi', 25000,'Sameep Vani' , 1001),
 (2,'Prachi Kapoor', 27890,'Sameep Vani' , 1002),
 (3,'Parth Patel', 15000,'Sameep Vani' , 1003),
 (4,'Sumit Vyas', 5000,'Sameep Vani' , 1001),
 (5,'Sunil Bhatt', 17000,'Sameep Vani' , 1003),
 (7,'Khushi Gopani', 12500,'Sameep Vani' , 1001),
 (8,'Suchi Pillai', 21000,'Sameep Vani' , 1002);
 
-- desc emp;
drop procedure if exists empdetails;
delimiter $$
create procedure empdetails()
begin
	declare c_end int default 0;
    declare r_empNo int;
	declare c_emp cursor for 
		select emp_no from  emp;
    declare continue handler for not found set c_end=1;
	open c_emp;
	getempdetails: Loop
		fetch c_emp into r_empNo;
		if c_end=1 then
			leave getempdetails;
		end if;
        select * from emp where emp_no = r_empNo;
	end loop;
	close c_emp;
end $$

delimiter ;



