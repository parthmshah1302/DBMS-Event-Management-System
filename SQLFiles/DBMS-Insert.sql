use dbmsEventManagement;

 insert into login values ('m@g.com','123'),('b@g.com','123');
 insert into login values ('parthmshah1302@gmail.com','123'),('malavdoshi312@gmail.com','123');

insert into event_table (event_no, event_name, event_date, venue, event_time, event_type) values (1, 'Kamba', '2020-07-10', 'Shebunino', '15:22:10', 'Stronghold');
insert into event_table (event_no, event_name, event_date, venue, event_time, event_type) values (2, 'Yodoo', '2021-01-24', 'Abilay', '3:17:11', 'Aerified');
insert into event_table (event_no, event_name, event_date, venue, event_time, event_type) values (3, 'Zoomcast', '2020-07-15', 'Isnos', '6:57:29', 'Temp');
insert into event_table (event_no, event_name, event_date, venue, event_time, event_type) values (4, 'Quaxo', '2020-08-07', 'Paratunka', '14:55:36', 'Latlux');
insert into event_table (event_no, event_name, event_date, venue, event_time, event_type) values (5, 'Midel', '2021-02-25', 'Morro do Chapéu', '22:25:36', 'Zaam-Dox');

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
