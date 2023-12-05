
--Major table
create table cs425.tblMajor(
    majorID int not null primary key unique,
    majorName varchar(100) not null
);


insert into cs425.tblMajor (majorID, majorName)
values
(1, 'Computer Science & Engineering'),
(2, 'Civil Engineering'),
(3, 'Physics'),
(4, 'Accounting');


--User table
create table cs425.tblUser(
    userID int not null primary key auto_increment unique,
    Fname varchar(100) not null,
    Lname varchar(100) not null,
    DOB date,
    Email varchar(256) unique,
    Passwd varchar(100) not null,
    majorID int,
    foreign key (majorID) references tblMajor(majorID)
);



--tblUser insert command
insert into cs425.tblUser (Fname, Lname, DOB, Email, Passwd)
values ('Dave', 'Smith', '1901-12-23', 'DSmith@gmail.com', 'passEx123');


select * from cs425.tblUser;



--Authentication table
create table cs425.tblAuthentication(
    tokenID int not null primary key auto_increment unique,
    tblUser_userID int,
    foreign key (tblUser_userID) references tblUser(userID),
    Token varchar(256)
);


--User Session table
create table cs425.tblUserSession(
    sessionID int not null primary key auto_increment unique,
    tblUser_userID int,
    foreign key (tblUser_userID) references tblUser(userID),
    sessionToken varchar(256),
    expirationDate datetime
);



--Courses table
create table cs425.tblCourses(
    courseID int not null primary key auto_increment unique,
    tblUser_userID int,
    foreign key (tblUser_userID) references tblUser(userID),
    courseCode varchar(50) not null,
    courseName varchar(100) not null,
    instructor varchar(100)
);



--Enrollment table
create table cs425.tblEnrollment(
    enrollmentID int not null primary key auto_increment,
    tblUser_userID int,
    foreign key (tblUser_userID) references tblUser(userID),
    tblCourses_courseID int,
    foreign key (tblCourses_courseID) references tblCourses(courseID),
    enrollmentStatus enum('enrolled', 'dropped') default 'enrolled'
);
