
/*Department table*/
create table cs425.tblDepartment(
    deptID int primary key,
    deptName varchar(50),
    deptCode varchar(20),
    deptDesc text,
    officeLocation varchar(50),
    officePhone varchar(20), 
    headOfDept varchar(50)
);

/*Major table*/
create table cs425.tblMajor(
    majorID int primary key auto_increment,
    deptID int,
    majorCode varchar(15),
    majorName varchar(50),
    majorDesc text,
    degreeType varchar(50),
    creditsReq int,
    foreign key (deptID) references tblDepartment (deptID)
);

/*User table*/
create table cs425.tblUser(
    userID int primary key auto_increment,
    Fname varchar(100) not null,
    Lname varchar(100) not null,
    DOB date,
    Email varchar(150) unique,
    Passwd varchar(100) not null
);

/*Roles table*/
create table cs425.tblRoles(
    roleID int primary key auto_increment,
    userID int unique,
    roleCode enum('STU', 'INST', 'ADV', 'ADM'),
    title varchar(20),
    foreign key(userID) references tblUser(userID)
);

/*UserSettings table*/
create table cs425.tblUserSettings(
    settingID int primary key,
    userID int,
    notifyEnabled tinyint(1),
    dateFormats varchar(20),
    foreign key (userID) references tblUser(userID)
);

/*ContactInfo table*/
create table cs425.tblContactInfo(
    contactID int primary key,
    userID int,
    phoneNum varchar(20),
    streetAddr varchar(200),
    city varchar(50),
    state varchar(2),
    zipCode varchar(10),
    foreign key (userID) references tblUser(userID)
);

/*Students table*/
create table cs425.tblStudents(
    studentID int primary key,
    userID int unique,
    username varchar(30),
    majorID int,
    majorName varchar(50),
    GPA decimal(3,2),
    foreign key (userID) references tblUser(userID),
    foreign key (majorID) references tblMajor(majorID)
);

/*Instructor table*/
create table cs425.tblInstructor(
    instructorID int primary key,
    userID int unique,
    email varchar (75),
    deptID int,
    officeLocation varchar(100),
    phoneNum varchar(20),
    officeHours varchar (100),
    foreign key (userID) references tblUser(userID),
    foreign key (deptID) references tblDepartment(deptID)
);

/*Advisor table*/
create table cs425.tblAdvisors(
    advisorID int primary key,
    userID int,
    deptID int,
    bio text,
    officeAdv varchar(100),
    officeHours varchar(100),
    phoneNum varchar(20),
    foreign key (userID) references tblUser(userID),
    foreign key (deptID) references tblDepartment(deptID)
);

/*Admin table*/
create table cs425.tblAdmin(
    adminID int primary key,
    userID int unique,
    deptID int,
    officeLocation varchar(75),
    phoneNum varchar(20),
    responsilities text,
    hireDate date,
    foreign key (deptID) references tblDepartment(deptID)
);

/*Courses table*/
CREATE TABLE cs425.tblCourses (
    courseID int PRIMARY KEY auto_increment,
    courseCode varchar(25) NOT NULL,
    courseName varchar(100) NOT NULL,
    status varchar(10),
    credits int,
    Description TEXT,
    majorID int,
    meetingDays varchar(15),
    startTime TIME,
    endTime TIME,
    meetingTimes varchar(30),
    Requirements text,
    classAttributes varchar(256),
    FOREIGN KEY (majorID) REFERENCES tblMajor(majorID),
    Section int,
    Room varchar(10),
    instructor varchar(50),
    startDate date,
    endDate date,
    classCapacity int,
    enrollmentTotal int,
    availableSeats int,
    waitList int,
    materials varchar(50)
);

/*CourseSchedule table*/
create table cs425.tblCourseSchedule(
    scheduleID int primary key,
    studentID int,
    daysOfWeek varchar (10),
    startTime time,
    endTime time,
    semester varchar(50),
    building varchar(50),
    room varchar(50),
    instructor varchar(100),
    foreign key (studentID) references tblStudents(studentID)
);

/*CourseOffering table*/
create table cs425.tblCourseOffering(
    offerID int primary key,
    courseID int,
    Section int,
    meetDays varchar (20),
    courseLocation varchar(30),
    enrollCapacity int,
    enrollCount int,
    courseStatus varchar(20),
    instructorID int,
    foreign key (courseID) references tblCourses(courseID),
    foreign key (instructorID) references tblInstructor(instructorID)
);

/*Semesters table*/
create table cs425.tblSemesters(
    semesterID int primary key,
    semesterName varchar(50),
    startDate date,
    endDate date,
    academicYear year,
    regStartDate date,
    regEndDate date,
    notes text
);

/*Prerequisites table*/
create table cs425.tblPrerequisites(
    prereqID int primary key,
    courseID int,
    minGrade varchar(3),
    completionStatus varchar(20),
    foreign key (courseID) references tblCourses(courseID)
);

/*Grades table*/
create table cs425.tblGrades(
    gradeID int primary key,
    studentID int,
    courseID int,
    grade varchar(3),
    semesterID int,
    instructorID int,
    comments text,
    submissionDate date,
    foreign key(studentID) references tblStudents(studentID),
    foreign key(courseID) references tblCourses(courseID),
    foreign key(semesterID) references tblSemesters(semesterID),
    foreign key(instructorID) references tblInstructor(instructorID)
);

/*GPA table*/
create table cs425.tblGPA(
    gpaID int primary key,
    studentID int,
    cumulativeGPA decimal(3,2),
    creditsEarned int,
    semesterCredits decimal(3,2),
    semesterGPA decimal(3,2),
    lastUpdate datetime,
    foreign key (studentID) references tblStudents(studentID)
);

/*Enrollment table*/
create table cs425.tblEnrollment(
    enrollmentID int primary key,
    studentID int,
    courseID int,
    enrollmentStatus enum('Unable', 'Enrolled', 'Dropped'),
    enrollDate date,
    foreign key (studentID) references tblStudents(studentID),
    foreign key (courseID) references tblCourses(courseID)
);

/*Review table*/
create table cs425.tblReviews(
    reviewID int primary key,
    studentID int,
    courseID int,
    rating int,
    ratingText text,
    reviewDate date,
    upVotes int,
    downVotes int,
    foreign key (studentID) references tblStudents(studentID),
    foreign key (courseID) references tblCourses(courseID)
);

/*Payments table*/
create table cs425.tblPayments(
    paymentID int primary key,
    studentID int,
    amount decimal (8,2),
    paymentDate datetime,
    paymentStatus varchar(20),
    paymentMethod varchar(30),
    decription text,
    billAdress text,
    confirmationNum varchar(20),
    foreign key (studentID) references tblStudents(studentID)
);

/*Announcements table*/
create table cs425.tblAnnouncements(
    announcementID int primary key,
    title varchar(200),
    content text,
    announceDate date,
    createDate timestamp,
    lastModify timestamp
);

/*Internships table*/
create table cs425.tblInternships(
    internshipID int primary key,
    studentID int,
    companyName varchar (75),
    startDate date,
    endDate date,
    position varchar(50),
    foreign key (studentID) references tblStudents(studentID)
);