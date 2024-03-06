USE cs425;

ALTER TABLE tblCourseNames ADD format VARCHAR(16);

UPDATE tblCourseNames SET format = 'In-person';