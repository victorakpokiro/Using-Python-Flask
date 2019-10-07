
create table if not EXISTS  blogtbl (
    id int primary key, 
    title varchar(40) not null,
    status Text not null,
    filename varchar(50),
    date_created datetime  
)
