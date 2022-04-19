insert into customers (id, first_name, last_name, date_of_birth) values (1, 'Sile', 'Lesurf', '1980-11-09 00:00:00+00');
insert into customers (id, first_name, last_name, date_of_birth) values (2, 'Jerrie', 'Martynka', '1997-05-08 00:00:00+00');
insert into customers (id, first_name, last_name, date_of_birth) values (3, 'Kaylil', 'Pardue', '1982-04-03 00:00:00+00');
insert into customers (id, first_name, last_name, date_of_birth) values (4, 'Bobinette', 'Hayfield', '1986-10-26 00:00:00+00');
insert into customers (id, first_name, last_name, date_of_birth) values (5, 'Aristotle', 'Shadrack', '1986-08-26 00:00:00+00');
insert into customers (id, first_name, last_name, date_of_birth) values (6, 'Kareem', 'Stockin', '1980-11-09 01:00:00+00');
insert into customers (id, first_name, last_name, date_of_birth) values (7, 'Alva', 'Swanbourne', '1997-05-08 01:00:00+00');
insert into customers (id, first_name, last_name, date_of_birth) values (8, 'Kass', 'Llywarch', '1982-04-03 01:00:00+00');
insert into customers (id, first_name, last_name, date_of_birth) values (9, 'Kaycee', 'Quirk', '1986-10-26 01:00:00+00');
insert into customers (id, first_name, last_name, date_of_birth) values (10, 'Guenna', 'Angus', '1986-08-26 01:00:00+00');

select
  date_part('year', age(date_of_birth))
from
  customers;