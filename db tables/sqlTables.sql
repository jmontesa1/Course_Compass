/*Department table*/
create table cs425.tblDepartment(
    deptID int primary key auto_increment,
    deptName varchar(75),
    deptDesc text,
    officeLocation varchar(75),
    officePhone varchar(20), 
    deptChair varchar(50)
);


/*Major table*/
create table cs425.tblMajor(
    majorID int primary key auto_increment,
    deptID int,
    deptName varchar(75),
    program varchar(75),
    majorName varchar(50),
    majorDesc text,
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
    Passwd varchar(100) not null,
    majorName varchar(60),
    majorID int,
    foreign key (majorID) references tblMajor (majorID)
);

/*Advisor table*/
create table cs425.tblAdvisors(
    advisorID int primary key auto_increment,
    deptID int,
    Fname varchar(75),
    Lname varchar(75),
    Email varchar(150) unique,
    office varchar(100),
    officeHours varchar(100),
    phoneNum varchar(20),
    isAdmin boolean,
    foreign key (deptID) references tblDepartment(deptID)
);

/*Instructor table*/
create table cs425.tblInstructor(
    instructorID int primary key auto_increment,
    Fname varchar(75),
    Lname varchar(75),
    Email varchar(150) unique,
    deptID int,
    officeLocation varchar(100),
    phoneNum varchar(20),
    officeHours varchar (100),
    isAdmin boolean,
    foreign key (deptID) references tblDepartment(deptID)
);


/*Admin table*/
create table cs425.tblAdmin(
    adminID int primary key auto_increment,
    Fname varchar(75),
    Lname varchar(75),
    Email varchar(150) unique,
    deptID int,
    officeLocation varchar(75),
    phoneNum varchar(20),
    jobDesc text,
    foreign key (deptID) references tblDepartment(deptID)
);


/*Students table*/
create table cs425.tblStudents(
    studentID int primary key auto_increment,
    userID int unique,
    Email varchar(150) unique,
    majorName varchar(50),
    currentCredits int,
    creditsEarned int,
    GPA decimal(3,2),
    enrollmentStatus varchar(75),
    advisorID int,
    foreign key (Email) references tblUser(Email),
    foreign key (advisorID) references tblAdvisors(advisorID)
);



/*UserSettings table*/
create table cs425.tblUserSettings(
    settingID int primary key auto_increment,
    userID int,
    Email varchar(100),
    notifyEnabled tinyint(1),
    emailNotif tinyint(1),
    homeNotif tinyint(1),
    dateFormats varchar(20),
    foreign key (Email) references tblUser(Email)
);


/*ContactInfo table*/
create table cs425.tblContactInfo(
    contactID int primary key auto_increment,
    userID int,
    Email varchar(100),
    phoneNum varchar(20),
    streetAddr varchar(200),
    city varchar(50),
    state varchar(2),
    zipCode varchar(10),
    foreign key (Email) references tblUser(Email)
);

/* Course Info table*/
create table cs425.tblCourses(
    courseID int primary key auto_increment,
    deptID int,
    majorID int,
    courseCode varchar(25),
    courseName varchar(100) not null,
    description text,
    Credits int,
    Level varchar(25),
	Requirements text,
    foreign key (majorID) references tblMajor(majorID)
);

/* Junction table for many-to-many relationship */
CREATE TABLE cs425.tblMajorCourses(
    majorID INT,
    courseID INT,
    primary key (majorID, courseID),
    foreign key (majorID) references tblMajor(majorID),
    foreign key (courseID) references tblCourses(courseID)
);

/*Course Schedule*/
create table cs425.tblcourseSchedule(
    scheduleID int primary key auto_increment,
    courseCode varchar(25),
    courseID int,
    Section int,
    Credits int,
	startDate date,
    endDate date,
    Term varchar(75),
    meetingDays varchar(75),
    startTime time,
    endTime time,
    meetingTimes varchar(30),
    Location varchar(10),
    Instructor varchar(75),
    meetingFormat varchar(75),
    status varchar(10),
    classCapacity int,
    enrollmentTotal int,
    availableSeats int,
    waitList int,
    Rating decimal(3,1),
    classAttributes varchar(256),
    materials varchar(150),
    foreign key (courseID) references tblCourses(courseID)
);


/*Enrollment table*/
create table cs425.tblUserSchedule(
    enrollmentID int primary key auto_increment,
    scheduleID int,
    Email varchar(150),
    courseCode varchar(25),
    Section int,
    Credits int,
    Term varchar(75),
    startDate date,
    endDate date,
    meetingDays varchar(75),
    meetingTimes varchar(30),
    Location varchar(25),
    Instructor varchar(75),
    meetingFormat varchar(75),
    Grade varchar(5),
    paymentStatus varchar(50),
    foreign key (Email) references tblUser(Email),
    foreign key (scheduleID) references tblcourseSchedule(scheduleID)
);

/*course History*/
CREATE TABLE cs425.tblUserCompletedCourses(
    completionID int primary key auto_increment,
    Email varchar(150),
    Fname varchar(100),
    Lname varchar(100),
    courseID int,
    courseCode varchar(25),
    isCompleted boolean default false,
    completionDate date,
    grade varchar(5),
    majorID int,
    foreign key (Email) references tblUser(Email),
    foreign key (courseID) references tblCourses(courseID),
    foreign key (majorID) references tblMajor(majorID),
    unique (Email, courseID)
);

/*Review table*/
create table cs425.tblRatings(
    ratingsID int primary key auto_increment,
    courseID int,
    courseCode varchar(25),
    rating int,
    ratingText text,
    ratingDate date,
    Keywords varchar(256),
    upVotes int,
    downVotes int,
    foreign key (courseID) references tblCourses(courseID)
);

/*Planer table*/
create table cs425.tblPlanner(
	plannerID int primary key auto_increment,
    Email varchar(100),
    Title varchar(100),
    Priority varchar(20),
    Date date,
    Notes text,
    status varchar(30),
    Attachments varchar(255),
    reminderDatetime datetime,
    foreign key (Email) references tblUser(Email)
);

/*Course Shopping Cart table*/
create table cs425.tblshoppingCart(
    cartID int primary key auto_increment,
    Email varchar(100),
    scheduleID int,
    courseID int,
	courseCode varchar(25),
    enrollmentStatus varchar(25),
    enrollDate date,
    dropDate date,
	foreign key (Email) references tblUser(Email),
    foreign key (scheduleID) references tblcourseSchedule(scheduleID)
);



/*Announcements table*/
create table cs425.tblNotifications(
    notificationID int primary key auto_increment,
    instructorID int,
	announceDate date,
    source varchar(50),
    message text,
    createDate date,
    lastModify date,
    expireDate date,
    foreign key (instructorID) references tblInstructor(instructorID)
);

/*Semesters table*/
create table cs425.tblSemesters(
    semesterID int primary key auto_increment,
    semesterName varchar(75),
    startDate date,
    endDate date,
    academicYear year,
    regStartDate date,
    regEndDate date,
    notes text
);

/*Grades table*/
create table cs425.tblGrades(
    gradeID int primary key auto_increment,
    studentID int,
    courseID int,
    grade varchar(5),
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
    gpaID int primary key auto_increment,
    studentID int,
    cumulativeGPA decimal(3,2),
    creditsEarned int,
    semesterCredits decimal(3,2),
    semesterGPA decimal(3,2),
    lastUpdate datetime,
    foreign key (studentID) references tblStudents(studentID)
);

create table cs425.tblCourseNames (
    courseID int primary key auto_increment,
    courseName varchar(100),
    courseCode varchar(25),
    courseMajor varchar(100)
);
