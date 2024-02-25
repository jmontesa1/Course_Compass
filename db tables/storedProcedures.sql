
/*Get users courses with their email for their Major progress*/
delimiter //
create procedure GetCoursesForProgress(
    in userEmail varchar(255)
)
begin
    select c.courseID, c.courseName, c.courseCode, c.Credits, c.Level, m.majorName, m.creditsReq, m.deptName
    from tblCourses c
    join tblMajor m on c.majorID = m.majorID
    where m.majorID = (
        select majorID
        from tblUser
        where Email = userEmail
    );
end //
delimiter ;


/*use case*/
call GetCoursesForProgress('jose@gmail.com');

---------------------------------------------------------
delimiter //
create procedure `GetMajorCompletionStatus`(
    in userEmail varchar(150)
)
begin
    select 
        c.courseID, 
        c.courseName, 
        c.courseCode,
        c.Credits,
        (ucc.courseID is not null) as isCompleted -- 1 (true) if completed, 0 (false) if not
    from 
        tblCourses c
    join 
        tblMajor m on c.majorID = m.majorID
    left join 
        tblUserCompletedCourses ucc on c.courseID = ucc.courseID and ucc.Email = userEmail
    where 
        m.majorID = (
            select majorID 
            from tblUser 
            where Email = userEmail
        );
end//
delimiter ;


/*use case*/

call GetMajorCompletionStatus('jose@gmail.com')

----------------------------------------------------------------------

/*Retrives a user's current courses witht their email as argument*/
delimiter //
create procedure `GetUserSchedule`(
    in userEmail varchar(150)
)
begin
    select 
        u.Email, 
        u.Fname, 
        u.Lname, 
        cs.courseCode, 
        cs.Section, 
        cs.Credits, 
        cs.Term, 
        cs.startDate, 
        cs.endDate, 
        cs.meetingDays, 
        cs.meetingTimes, 
        cs.Location, 
        cs.Instructor, 
        cs.meetingFormat
    from 
        cs425.tblUserSchedule us
    join 
        cs425.tblcourseSchedule cs on us.scheduleID = cs.scheduleID
    join 
        cs425.tblUser u on us.Email = u.Email
    where 
        u.Email = userEmail
    and 
        cs.startDate <= curdate() 
    and 
        cs.endDate >= curdate();
end //
delimiter ;


/*use case*/
call GetUserSchedule('jose@gmail.com')
---------------------------------------------------------------------------------------------------









/*Get users by major*/
delimiter //
create procedure GetUsersByMajor (
    in p_majorName varchar(50)
)
begin
    select U.userID, U.Fname, U.Lname, S.username, S.majorName
    from cs425.tblUser U
    join cs425.tblStudents S on U.userID = S.userID
    where S.majorName = p_majorName;
end //
delimiter ;

/*Use case*/
call GetUsersByMajor('Computer Science')

/*Get users by role*/
delimiter //
create procedure GetUsersByRole (
    in p_roleTitle varchar(50)
)
begin
    select U.userID, U.Fname, U.Lname, R.title
    from cs425.tblUser U
    join cs425.tblRoles R on U.userID = R.userID
    where R.title = p_roleTitle;
end //
delimiter ;

/*Use case*/
call GetUsersByRole('Student')

/*Get students major*/
delimiter //
create procedure GetStudentsMajor (
    in p_Fname varchar(100),
    in p_Lname varchar(100)
)
begin
    select U.Fname, U.Lname, S.majorName
    from cs425.tblUser U
    join cs425.tblStudents S on U.userID = S.userID
    where U.Fname = p_Fname and U.Lname = p_Lname;
end //
delimiter ;

/*Use case*/
call GetStudentsMajor('Jose', 'Urrutia')

/*Update user email*/
delimiter //
create procedure UpdateUserEmail (
    in p_userID int,
    in p_newEmail varchar(150)
)
begin
    update cs425.tblUser
    set Email = p_newEmail
    where userID = p_userID;
end //
delimiter ;

/*Use case*/
call UpdateUserEmail(1, 'newemail@gmail.com');


/* get user information for My Account page */
delimiter //
create procedure GetUserInfo(IN userEmail VARCHAR(150))
begin
    select
        user.Fname AS FirstName,
        user.Lname AS LastName,
        user.Email,
        user.majorName AS Major
    from
        cs425.tblUser user
    where
        user.Email = userEmail;
end //
delimiter;