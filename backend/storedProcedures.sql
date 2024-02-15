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