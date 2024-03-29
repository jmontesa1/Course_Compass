create view cs425.vwCourseDetails as
select 
    c.courseID,
    c.courseName,
    c.courseCode,
    m.majorName as courseMajor,
    d.deptName as department,
    cs.Instructor as professor,
    cs.Term as term,
    cs.meetingFormat as format,
    c.Credits as units,
    cs.meetingTimes as meetingTime, 
    cs.Location,
    cs.meetingDays as days
from 
    cs425.tblCourses c
    join cs425.tblCourseMajor cm on c.courseID = cm.courseID
    join cs425.tblMajor m on cm.majorID = m.majorID
    join cs425.tblDepartment d on m.deptID = d.deptID
    left join cs425.tblcourseSchedule cs on c.courseID = cs.courseID
where 
    cs.Instructor is not null;