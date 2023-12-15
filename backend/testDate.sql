use cs425;

/*insert majors*/
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




/*insert users*/
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



/*set roles*/
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



/*insert students*/
insert into cs425.tblStudents(studentID, userID, username, majorID, majorName, GPA)
values
(123123123, 1, 'urrutia123', 100, 'Computer Science', 3.5),
(123456789, 3, 'userexample', 200, 'Civil Engineering', 3.6),
(351651165, 5, 'anotheruser', 900, 'Business', 4.0),
(254887148, 6, 'user123', 500, 'Chemistry', 3.8),
(452412214, 7, 'example123', 800, 'Physchology', 3.4);





/*search for student by major*/
select * from cs425.tblUser join cs425.tblStudents on cs425.tblUser.userID = cs425.tblStudents.userID
where majorName = 'Computer Science';