
/*Get users courses with their email for their Major progress*/
delimiter //
create procedure GetCoursesForProgress(
    in userEmail varchar(255)
)
begin
    select c.courseID, c.courseName, c.courseCode, c.Credits, c.Level, m.majorName, m.creditsReq, 
           coalesce(ucc.isCompleted, 0) as isCompleted --coalesce returns completed as 1 or 0 if null
    from tblCourses c
    join tblMajor m on c.majorID = m.majorID
    left join tblUserCompletedCourses ucc on c.courseID = ucc.courseID and m.majorID = ucc.majorID and ucc.Email = userEmail
    where m.majorID = (
        select majorID
        from tblUser
        where Email = userEmail
    );
end //
delimiter ;


/*use case*/
call GetCoursesForProgress('jose@gmail.com');

---------------------------------------------------------------------------------------------------------------------------------------------------
/*Post a course as completed */
delimiter //
create procedure MarkCourseCompleted(
    in userEmail varchar(150),
    in courseCode varchar(25)
)
begin
    declare v_courseID int;
    declare v_majorID int;
    declare v_fname varchar(100);
    declare v_lname varchar(100);

    -- find courseID and majorID by courseCode
    select c.courseID, c.majorID into v_courseID, v_majorID
    from cs425.tblCourses c
    where c.courseCode = courseCode
    limit 1;

    -- get users name 
    select Fname, Lname into v_fname, v_lname
    from cs425.tblUser
	where Email = userEmail
    limit 1;

            -- check if a record already exists
    if (select count(*) from cs425.tblUserCompletedCourses where Email = userEmail and courseID = v_courseID) > 0 then

        update cs425.tblUserCompletedCourses
        set isCompleted = 1, completionDate = curdate()
        where Email = userEmail and courseID = v_courseID;
    else
        insert into cs425.tblUserCompletedCourses (Email, Fname, Lname, courseID, courseCode, isCompleted, completionDate, majorID)
        values (userEmail, v_fname, v_lname, v_courseID, courseCode, 1, curdate(), v_majorID);
    end if;
end //
delimiter ;

call MarkCourseCompleted('jose@gmail.com', 'CS 365')
/*for multiple courses at a time iterate through a list of courses in the endpoint to call it once for each course*/


---------------------------------------------------------------------------------------------------------------------------------------------------
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

---------------------------------------------------------------------------------------------------------------------------------------------------

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
---------------------------------------------------------------------------------------------------------------------------------------------------









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

--------------------------------------------------------------------------------------------------------------------------------------------------------
/*stored procedure for searching departments*/
delimiter //
create procedure SearchDepartments(in search_term varchar(255))
begin
    select distinct courseName, courseCode, courseMajor, department, professor, term, format, units, meetingTime, Location, days
    from vwCourseDetails
    where courseMajor LIKE concat(search_term, '%')
    order by 
        cast(substring(courseCode, locate(' ', courseCode) + 1) AS unsigned),
        substring(courseCode, 1, locate(' ', courseCode) - 1);
end //
delimiter ;
---------------------------------------------------------------------------------------------------------------------------------------------------------