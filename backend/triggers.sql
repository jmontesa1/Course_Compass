delimiter //
create trigger set_title
before insert on tblRoles
for each row
begin
    if new.roleCode = 'STU' then 
		set NEW.title = 'Student';
    elseif new.roleCode = 'INST' then
        set new.title = 'Instructor';
    elseif new.roleCode = 'ADV' then
		set new.title = 'Advisor';
	elseif new.roleCode = 'ADM' then
		set new.title = 'Admin';
    end if;
end;
//
delimiter ;


delimiter //
create trigger set_majorName
before insert on tblStudents
for each row
begin
    if new.majorID = 100 then 
		set new.majorName = 'Computer Science';
    elseif new.majorID = 200 then
        set new.majorName = 'Civil Engineering';
	elseif new.majorID = 300 then
        set new.majorName = 'Physics';
	elseif new.majorID = 400 then
        set new.majorName = 'Accounting';
	elseif new.majorID = 500 then
        set new.majorName = 'Chemistry';
	elseif new.majorID = 600 then
        set new.majorName = 'Finance';
	elseif new.majorID = 700 then
        set new.majorName = 'Biology';
	elseif new.majorID = 800 then
        set new.majorName = 'Psychology';
	elseif new.majorID = 900 then
        set new.majorName = 'Business';
    end if;
end;
//
delimiter ;