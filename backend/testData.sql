use cs425;


/*insert majors*/
Insert into cs425.tblMajor (majorID, majorName)
values
(100, 'Accounting'),
(200, 'Agricultural Science'),
(300, 'Anthropology'),
(400, 'Art'),
(500, 'Biochemistry'),
(600, 'Biology'),
(700, 'Business Administration'),
(800, 'Chemistry'),
(900, 'Civil Engineering'),
(1000, 'Computer Science'),
(1100, 'Criminal Justice'),
(1200,'Economics'),
(1300,'Electrical Engineering'),
(1400, 'English'),
(1500, 'Environmental Science'),
(1600, 'Finance'),
(1700, 'Geography'),
(1800, 'History'),
(1900, 'Journalism'),
(2000, 'Management'),
(2100, 'Marketing'),
(2200, 'Mathematics'),
(2300, 'Mechanical Engineering'),
(2400, 'Music'),
(2500, 'Nursing'),
(2600, 'Nutrition'),
(2700, 'Philosophy'),
(2800, 'Physics'),
(2900, 'Political Science'),
(3000, 'Psychology'),
(3100, 'Social Work'),
(3200, 'Sociology'),
(3300, 'Spanish'),
(3400, 'Statistics'),
(3500, 'Theatre'),
(3600, 'Wildlife Ecology and Conservation');


/*set roles*/

/*Insert majors*/
insert into cs425.tblMajor(majorID, majorName)
values
(100, 'Computer Science & Engineering'),
(200, 'Civil Engineering'),
(300, 'Physics'),
(400, 'Accounting'),
(500, 'Chemistry'), 
(600, 'Finance'),
(700, 'Biology'),
(800, 'Psychology'),
(900, 'Business');

/*Insert users*/
insert into cs425.tblUser(Fname, Lname, DOB, Email, Passwd)
values
('Cindy', 'Portillo', '1989-12-23', 'potilloc89@gmail.com', 'djgh$kjj785'),
('Dave', 'Smith', '1901-12-23', 'DSmith@gmail.com', 'SD23dg$'),
('Jose', 'Urrutia', '1950-10-15', 'jurrutia@gmail.com', 'passEx123'),
('Jessica', 'Aquil', '1980-11-11', 'aquil@gmail.com', 'urrutia45'),
('John Nathan', 'Montesa', NULL, 'mediapop0@gmail.com', 'Password1234!'),
('testing', 'lesting', NULL, 'test2@gmail.com', 'Lucky123#'),
('Hossein', 'Demo', NULL, 'Bill.gate@microsoft.com', 'Password1234!'),
('Lucas', 'Test', NULL, 'test@gmail.com', 'Testing1234!'),
('lucas', 'video', NULL, 'lucaj@gmail.com', 'Testing123!'),
('Lucas', 'Videtto', NULL, 'lucasjohnvidetto@gmail.com', 'Ozark21!'),
('Jose', 'Urrutia', NULL, 'jose@gmail.com', '$2b$12$JTep2nnJpp5Rm9MTSVS14umnSqxOdNmJP.ML6V3wkAySIiDJhWfRe'),
('Jose', 'Urrutia', NULL, 'jose12@gmail.com', 'solikj65');

/*Set roles*/

insert into cs425.tblRoles(userID, roleCode)
values 
(1, 'STU'),
(2, 'INST'),
(3, 'STU'),
(4, 'ADM'),
(5, 'STU'),
(6, 'STU'),
(7, 'STU'),
(8, 'ADM');

/*Insert students*/
insert into cs425.tblStudents(studentID, userID, username, majorID, majorName, GPA)
values
(123123123, 1, 'urrutia123', 100, 'Computer Science', 3.5),
(123456789, 3, 'userexample', 200, 'Civil Engineering', 3.6),
(351651165, 5, 'anotheruser', 900, 'Business', 4.0),
(254887148, 6, 'user123', 500, 'Chemistry', 3.8),
(452412214, 7, 'example123', 800, 'Physchology', 3.4),
(561452135, 8, 'testtest', 100, 3.7),
(124578325, 9, 'user4245', 100, 3.7),
(245412154, 10, 'user7515', 200, 4.0);