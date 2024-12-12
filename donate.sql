 CREATE TABLE requests_blood (date date, address text, id integer, phone character varying, blood_group_id integer, email character varying, name character varying, city character varying);
 CREATE TABLE blood_groups (id integer, name character varying);
 CREATE TABLE donors (ready_to_donate boolean, blood_group_id integer, username character varying, date_of_birth date, password character varying, email character varying, address text, phone character varying, id integer, last_name character varying, gender character varying, city character varying, first_name character varying);
 CREATE TABLE users (username character varying, password character varying, email character varying, id integer);


