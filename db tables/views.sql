create view cs425.vwCourseDetails as
select
    cs.scheduleID as scheduleID,
    cs.Section as Section,
    c.courseName as courseName,
    c.courseCode as courseCode,
    m.majorName as courseMajor,
    d.deptName as department,
    cs.Instructor as professor,
    cs.Term as term,
    cs.meetingFormat as format,
    c.Credits as units,
    cs.meetingTimes as meetingTime,
    cs.Location as Location,
    cs.meetingDays as days,
    cs.classCapacity as classCapacity,
    cs.enrollmentTotal as enrollmentTotal,
    cs.availableSeats as availableSeats,
    round(coalesce(avg(r.rating), 0), 1) as averageRating,
    c.Level as courseLevel,
    tf.frequentTags as frequentTags,
    tf.tagCount as tagCount
from
    tblCourses c
    join tblCourseMajor cm on c.courseID = cm.courseID
    join tblMajor m on cm.majorID = m.majorID
    join tblDepartment d on m.deptID = d.deptID
    left join tblcourseSchedule cs on c.courseID = cs.courseID
    left join tblRatings r on c.courseID = r.courseID
    left join (
        select
            c.courseID,
            c.courseCode,
            c.courseName,
            group_concat(distinct t.tagName order by tag_count desc separator ', ') as frequentTags,
            sum(tag_count) as tagCount
        from
            tblCourses c
            left join (
                select
                    r.courseID,
                    rt.tagID,
                    count(*) as tag_count
                from
                    tblRatings r
                    join tblRatingTags rt on r.ratingID = rt.ratingID
                group by
                    r.courseID, rt.tagID
            ) as tag_counts on c.courseID = tag_counts.courseID
            left join tblTags t on tag_counts.tagID = t.tagID
        group by
            c.courseID, c.courseCode, c.courseName
    ) as tf on c.courseID = tf.courseID
where
    cs.Instructor is not null
group by
    cs.scheduleID,
    cs.Section, 
    c.courseName,
    c.courseCode,
    m.majorName,
    d.deptName,
    cs.Instructor,
    cs.Term,
    cs.meetingFormat,
    c.Credits,
    cs.meetingTimes,
    cs.Location,
    cs.meetingDays,
    cs.classCapacity,
    cs.enrollmentTotal,
    cs.availableSeats,
    c.Level,
    tf.frequentTags,
    tf.tagCount;