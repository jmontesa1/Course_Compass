# Created by Lucas Videtto
# Backend functionality for Course Compass

from flask import Flask, jsonify, request, session, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from mysql.connector import connect, Error
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import logging, json
from urllib.parse import unquote
from flask_mail import Mail, Message


app = Flask(__name__, template_folder='templates')
app.secret_key = '123456789' # Change key to secure value for production environment
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'coursecompassunr@gmail.com'
app.config['MAIL_PASSWORD'] = 'rlse btgk aelx uxlk'
mail = Mail(app)


# User class to store user information
class User:
    def __init__(self, userID=None, Fname=None, Lname=None, DOB=None, Email=None, majorName=None, majorID=None, studentID=None, role=None):
        self.userID = userID
        self.Fname = Fname
        self.Lname = Lname
        self.DOB = DOB
        self.Email = Email
        self.majorName = majorName
        self.majorID = majorID
        self.studentID = studentID
        self.role = role

    @staticmethod
    def get_user_by_email(email):
        connection = connectToDB()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT u.userID, u.Fname, u.Lname, u.DOB, u.Email, u.role, s.majorID, m.majorName, s.studentID
                FROM tblUser u
                LEFT JOIN tblStudents s ON u.userID = s.userID
                LEFT JOIN tblMajor m ON s.majorID = m.majorID
                WHERE u.Email = %s
            """, (email,))
            user_data = cursor.fetchone()
            print("FETCHED USER DATA FROM GETUSERBYEMAIL", user_data)
            if user_data:
                user = User(**user_data)
                return user
            return None
        except Exception as e:
            print(e)
            return None
        finally:
            cursor.close()
            connection.close()

    def conv_to_json(self):
        return {
            "userID": self.userID,
            "Fname": self.Fname,
            "Lname": self.Lname,
            "DOB": self.DOB.strftime('%Y-%m-%d') if self.DOB else None,
            "Email": self.Email,
            "majorID": self.majorID,
            "majorName": self.majorName,
            "studentID": self.studentID,
            "role": self.role
        }
        
    def get_major_courses(self):
        connection = connectToDB()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT
                    c.courseID,
                    c.courseCode,
                    c.courseName,
                    c.description,
                    c.Credits,
                    c.Level,
                    c.Requirements
                FROM
                    cs425.tblUser u
                JOIN
                    cs425.tblMajor m ON u.majorID = m.majorID
                JOIN
                    cs425.tblMajorCourses mc ON m.majorID = mc.majorID
                JOIN
                    cs425.tblCourses c ON mc.courseID = c.courseID
                WHERE
                    u.Email = %s
            """, (self.Email,))
            courses = cursor.fetchall()
            return courses
        except Exception as e:
            print(e)
            return []
        finally:
            cursor.close()
            connection.close()
            
    def courses_to_json(self):
        return {
            "courses": self.get_major_courses()
        }
        

# Login functionality for backend
# Check backend development notes (Lucas)
# Included print statements for terminal reference
@app.route('/login', methods=['POST'])
def login(): 
    # if request.method == 'POST':
    #     email = request.json.get('email')
    #     password = request.json.get('password')
        
    #     if not email or not password:
    #         print("MISSING EMAIL OR PASSWORD")
    #         return jsonify({"message": "Missing email or password"}), 400
        
    #     try:
    #         connection = connectToDB()
    #         cursor = connection.cursor(dictionary=True)
    #         cursor.execute("SELECT userID, Email, Passwd, role, verified FROM tblUser WHERE Email = %s", (email,))
    #         user = cursor.fetchone()
            
    #         # if not user['verified']:
    #         #     print("EMAIL NOT VERIFIED")
    #         #     return jsonify({"message": "Unverified email."})
            
    #         if user and bcrypt.check_password_hash(user['Passwd'], password):
    #             session['email'] = email
                
    #             print("LOGIN SUCCESSFUL")

    #             role = user['role']
                
    #             access_token = create_access_token(identity={"email": user['Email'], "userID": user['userID'], "role": role})
    #             return jsonify({"message": "Login successful", "access_token": access_token, "role": role}), 200
    #         else:
    #             print("INVALID EMAIL OR PASSWORD")
    #             return jsonify({"message": "Invalid email or password"}), 401
    #     except Error as err:
    #         print(err)
    #         return jsonify({"message": "An error occurred"}), 500
        
    #     finally:
    #         cursor.close()
    #         connection.close()
    # else:
    #     print("INVALID REQUEST")
    #     return jsonify({"message": "Invalid request"}), 400
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        
        if not email or not password:
            print("MISSING EMAIL OR PASSWORD")
            return jsonify({"message": "Missing email or password"}), 400
        
        try:
            connection = connectToDB()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT userID, Email, Passwd, role, verified FROM tblUser WHERE Email = %s", (email,))
            user = cursor.fetchone()
            
            if not user:
                print("INVALID EMAIL OR PASSWORD")
                return jsonify({"message": "Invalid email or password"}), 401
            
            # if not user['verified']:
            #     print("EMAIL NOT VERIFIED")
            #     return jsonify({"message": "Email not verified. Please check your email to verify your account."}), 403

            if bcrypt.check_password_hash(user['Passwd'], password):
                session['email'] = email
                print("LOGIN SUCCESSFUL")
                role = user['role']
                access_token = create_access_token(identity={"email": user['Email'], "userID": user['userID'], "role": role})
                return jsonify({"message": "Login successful", "access_token": access_token, "role": role}), 200
            else:
                print("INVALID EMAIL OR PASSWORD")
                return jsonify({"message": "Invalid email or password"}), 401
        except Error as err:
            print(err)
            return jsonify({"message": "An error occurred"}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        print("INVALID REQUEST")
        return jsonify({"message": "Invalid request"}), 400
            

# Signup functionality for backend
# Check backend development notes (Lucas)
# Included print statements for terminal reference
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        fname = request.json.get('firstname')
        lname = request.json.get('lastname')
        dob = request.json.get('dateOfBirth')
        email = request.json.get('email')
        pw = request.json.get('password')
        userType = request.json.get('userType')
        majorID = request.json.get('majorID') if userType == 'Student' else None
        majorName = request.json.get('majorName')

        print("Received userType:", userType)

        if userType not in ['Student', 'Instructor']:
            print("INVALID USER TYPE")
            return jsonify({"message": "Invalid user type"}), 400

        if not fname or not lname or not dob or not email or not pw:
            print("MISSING REQUIRED FIELDS")
            return jsonify({"message": "Missing required fields"}), 400

        birthdate = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if age < 17:
            print("MUST BE AT LEAST 17 YEARS OLD TO REGISTER")
            return jsonify({"message": "Must be at least 17 years old to sign up"}), 400

        try:
            connection = connectToDB()
            cursor = connection.cursor(dictionary=True)

            connection.start_transaction() #handle insertion into both tables as one transaction
            
            cursor.execute("SELECT * FROM tblUser WHERE Email = %s", (email,))
            if cursor.fetchone():
                print("EMAIL ALREADY IN USE")
                return jsonify({"message": "Email already exists"}), 409
            
            #insert into user table
            hashed_pw = bcrypt.generate_password_hash(pw).decode('utf-8')
            cursor.execute("INSERT INTO tblUser (Fname, Lname, DOB, Email, Passwd, role) VALUES (%s, %s, %s, %s, %s, %s)", (fname, lname, dob, email, hashed_pw, userType))
            
            #retrieve the new userID
            cursor.execute("SELECT userID FROM tblUser WHERE Email = %s", (email,))
            new_user = cursor.fetchone()

            if userType == 'Student':
                cursor.execute("SELECT majorID, majorName FROM tblMajor WHERE majorName = %s", (majorID,))
                major = cursor.fetchone()
                if not major:
                    print("INVALID MAJOR")
                    connection.rollback()
                    return jsonify({"message": "Invalid major selected"}), 400
                majorID = major['majorID']
                majorName = major['majorName']

                cursor.execute("INSERT INTO tblStudents (userID, Email, majorName, majorID) VALUES (%s, %s, %s, %s)", (new_user['userID'], email,majorName, majorID))
                connection.commit()
            elif userType == 'Instructor':
                cursor.execute("INSERT INTO tblInstructor (userID, Email) VALUES (%s, %s)", (new_user['userID'], email))
                connection.commit()
            
            session['email'] = email
            access_token = create_access_token(identity={"email": email, "userID": new_user['userID']})
            # confirm_url = f"http://localhost:8080/login?token={access_token}"
            confirm_url = f"http://localhost:8080/login?verified=true"
            html = render_template('confirm_template.html', confirm_url=confirm_url)
            msg = Message("Course Compass - Confirm Your Email", sender="coursecompassunr@gmail.com", recipients=[email])
            msg.body = f"Please click on the link to confirm your Course Compass account: {confirm_url}"
            msg.html = html
            mail.send(msg)            
            print("SIGN UP SUCCESSFUL")
            return jsonify({"message": "Signup successful", "access_token": access_token}), 200
        except Error as err:
            print(err)
            connection.rollback()
            return jsonify({"message": "An error occurred"}), 500
        
        finally:
            cursor.close()
            connection.close()
            
    print("INVALID REQUEST")
    return jsonify({"message": "Invalid request"}), 400


@app.route('/resend_confirmation_email', methods=['POST'])
def resend_confirmation_email():
    email = request.json.get('email')
    try:
        connection = connectToDB()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT userID FROM tblUser WHERE Email = %s", (email,))
        user = cursor.fetchone()
        if user:
            access_token = create_access_token(identity={"email": email, "userID": user['userID']})
            confirm_url = f"http://localhost:8080/login?token={access_token}"
            html = render_template('confirm_template.html', confirm_url=confirm_url)
            msg = Message("Course Compass - Confirm Your Email", sender="coursecompassunr@gmail.com", recipients=[email])
            msg.body = f"Please click on the link to confirm your Course Compass account: {confirm_url}"
            msg.html = html
            mail.send(msg)
            return jsonify({"message": "Confirmation email resent"}), 200
        else:
            return jsonify({"message": "Email address not found"}), 404
    except Exception as exc:
        print(exc)
        return jsonify({"message": "Error while resending confirmation email"}), 500
    finally:
        cursor.close()
        connection.close()
        

# Fetch user information
@app.route('/getUserInfo', methods=['GET'])
def getUserInfo():
    if 'user_id' in session and 'email' in session:
        userid = session['user_id']
        useremail = session['email']
        connection = connectToDB()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute("SELECT Fname, Lname, Email, majorName FROM cs425.tblUser WHERE userID = %s AND Email = %s", (userid, useremail))
                user_info = cursor.fetchone()
                if user_info:
                    return jsonify(user_info), 200
                else:
                    return jsonify({"error": "User not found"}), 404
            except Error as err:
                return jsonify({"error": "Error while fetching data: " + str(err)}), 500
            finally:
                cursor.close()
                connection.close()
        else:
            return jsonify({"error": "DB connection failed"}), 500
    else:
        return jsonify({"error": "User not logged in"}), 401
    

# Retrive user schedule
@app.route('/getUserSchedule', methods=['GET'])
@jwt_required()
def user_schedule():
    try:
        identity = get_jwt_identity()
        current_user_email = identity.get('email')

        if not current_user_email:
            logging.warning("JWT identity does not contain email.")
            return jsonify({"error": "Authentication information is incomplete."}), 400

        logging.info(f"Current user email: {current_user_email}") 

        return fetch_user_schedule(current_user_email)
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching the user schedule: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500
    

def fetch_user_schedule(email):
    try:
        with connectToDB() as connection:
            with connection.cursor() as cursor:
                user_schedule = user_schedule_stored_procedure(cursor, email)
                if user_schedule is not None:
                    return jsonify({"user_schedule": user_schedule}), 200
                else:
                    logging.warning(f"Failed to fetch schedule for {email}")
                    return jsonify({"error": "Failed to fetch user schedule"}), 500
    except Exception as e:
        logging.error(f"Error fetching user schedule for {email}: {e}", exc_info=True)
        return jsonify({"error": "An error occurred while fetching the user schedule"}), 500
    

def user_schedule_stored_procedure(cursor, email):
    try:
        cursor.callproc('GetUserSchedule', [email])

        user_schedule = []
        for result in cursor.stored_results():
            user_schedule = result.fetchall()

        schedule_list = []
        for schedule in user_schedule:
            schedule_dict = {
                "courseCode": schedule[0],
                "meetingDays": schedule[1],
                "meetingTimes": schedule[2],
                "startTime": str(schedule[3]),
                "endTime": str(schedule[4]),
                "Location": schedule[5],
                "Term": schedule[6],
                "Credits": schedule[7]
            }
            schedule_list.append(schedule_dict)

        return schedule_list
    except Error as err:
        print("Error while fetching user schedule:", err)
        return None
    

#create a custom schedule
@app.route('/createCustomSchedule', methods=['POST'])
@jwt_required()
def create_custom_schedule():
    try:
        current_user_email = get_jwt_identity()['email']
        user = User.get_user_by_email(current_user_email)
        if not user or not user.studentID:
            return jsonify({"message": "User not found or not a student"}), 400

        data = request.get_json()
        title = data['title']
        option = data['option']

        # Insert the new custom schedule into the database
        connection = connectToDB()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tblCustomSchedules (studentID, title, scheduleOption) VALUES (%s, %s, %s)",
                       (user.studentID, title, option))
        connection.commit()

        # Retrieve the newly created custom schedule from the database
        schedule_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tblCustomSchedules WHERE scheduleID = %s", (schedule_id,))
        schedule_data = cursor.fetchone()

        # Create a dictionary representing the custom schedule
        custom_schedule = {
            'scheduleID': schedule_data[0],
            'title': schedule_data[2],
            'option': schedule_data[3]
        }

        return jsonify({"schedule": custom_schedule}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error creating custom schedule"}), 500
    finally:
        cursor.close()
        connection.close()

#add event to custom schedule
@app.route('/createCustomEvent', methods=['POST'])
@jwt_required()
def create_custom_event():
    try:
        current_user_email = get_jwt_identity()['email']
        user = User.get_user_by_email(current_user_email)
        if not user or not user.studentID:
            return jsonify({"message": "User not found or not a student"}), 400

        data = request.get_json()
        description = data['description']
        color = data['color']
        start_time = data['start']
        end_time = data['end']
        days_of_week = ','.join(data['daysOfWeek'])
        schedule_id = data['scheduleID']

        connection = connectToDB()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO tblCustomEvents (scheduleID, description, color, startTime, endTime, daysOfWeek)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (schedule_id, description, color, start_time, end_time, days_of_week))
        connection.commit()

        return jsonify({"message": "Custom event created successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error creating custom event"}), 500
    finally:
        cursor.close()
        connection.close()

#retrieve user created schedules
@app.route('/getCustomSchedules', methods=['GET'])
@jwt_required()
def get_custom_schedules():
    try:
        current_user_email = get_jwt_identity()['email']
        user = User.get_user_by_email(current_user_email)
        if not user or not user.studentID:
            return jsonify({"message": "User not found or not a student"}), 400

        connection = connectToDB()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT cs.scheduleID, cs.title, cs.scheduleOption, ce.eventID, ce.description, ce.color, ce.startTime, ce.endTime, ce.daysOfWeek
            FROM cs425.tblCustomSchedules cs
            LEFT JOIN cs425.tblCustomEvents ce ON cs.scheduleID = ce.scheduleID
            WHERE cs.studentID = %s
        """, (user.studentID,))

        results = cursor.fetchall()
        custom_schedules = {}

        for row in results:
            schedule_id = row[0]
            if schedule_id not in custom_schedules:
                custom_schedules[schedule_id] = {
                    "scheduleID": schedule_id,
                    "title": row[1],
                    "option": row[2],
                    "events": []
                }

            if row[3]:  # If eventID is not None
                days_of_week = row[8].split(',') if row[8] else []
                custom_schedules[schedule_id]["events"].append({
                    "eventID": row[3],
                    "description": row[4],
                    "color": row[5],
                    "start": row[6],
                    "end": row[7],
                    "daysOfWeek": days_of_week
                })

        return jsonify({"customSchedules": list(custom_schedules.values())}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Error retrieving custom schedules"}), 500

    finally:
        cursor.close()
        connection.close()


#delete custom created schedules
@app.route('/deleteCustomSchedule/<int:schedule_id>', methods=['DELETE'])
@jwt_required()
def delete_custom_schedule(schedule_id):
    try:
        current_user_email = get_jwt_identity()['email']
        user = User.get_user_by_email(current_user_email)
        if not user or not user.studentID:
            return jsonify({"message": "User not found or not a student"}), 400

        connection = connectToDB()
        cursor = connection.cursor()

        # Delete the associated events first
        cursor.execute("DELETE FROM tblCustomEvents WHERE scheduleID = %s", (schedule_id,))

        # Delete the custom schedule
        cursor.execute("DELETE FROM tblCustomSchedules WHERE scheduleID = %s AND studentID = %s", (schedule_id, user.studentID))
        connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Custom schedule deleted successfully"}), 200
        else:
            return jsonify({"message": "Custom schedule not found or not authorized"}), 404

    except Exception as e:
        print(e)
        return jsonify({"message": "Error deleting custom schedule"}), 500
    finally:
        cursor.close()
        connection.close()

#delete event from custom schedule
@app.route('/deleteCustomEvent/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_custom_event(event_id):
    try:
        current_user_email = get_jwt_identity()['email']
        user = User.get_user_by_email(current_user_email)
        if not user or not user.studentID:
            return jsonify({"message": "User not found or not a student"}), 400

        connection = connectToDB()
        cursor = connection.cursor()

        # Delete the custom event
        cursor.execute("DELETE FROM tblCustomEvents WHERE eventID = %s", (event_id,))
        connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Custom event deleted successfully"}), 200
        else:
            return jsonify({"message": "Custom event not found"}), 404

    except Exception as e:
        print(e)
        return jsonify({"message": "Error deleting custom event"}), 500

    finally:
        cursor.close()
        connection.close()


#get user enrolled courses
@app.route('/getEnrolledCourses', methods=['GET'])
@jwt_required()
def get_enrolled_courses():
    try:
        current_user_email = get_jwt_identity()['email']
        user = User.get_user_by_email(current_user_email)
        if not user or not user.studentID:
            return jsonify({"message": "User not found or not a student"}), 400

        connection = connectToDB()
        cursor = connection.cursor()

        query = """
        SELECT 
            cs.scheduleID,
            cs.courseCode AS course,
            c.courseName,
            cs.meetingDays AS days,
            cs.meetingTimes AS time,
            TIME_FORMAT(cs.startTime, '%l:%i %p') AS start,
            TIME_FORMAT(cs.endTime, '%l:%i %p') AS end,
            cs.Location AS location,
            cs.Instructor AS instructor,
            cs.Section,
            c.Credits,
            IFNULL(i.officeHours, 'N/A') AS officeHours,
            IFNULL(i.officeLocation, 'N/A') AS officeLocation
        FROM 
            tblUserSchedule us
        JOIN
            tblcourseSchedule cs ON us.scheduleID = cs.scheduleID
        JOIN 
            tblCourses c ON cs.courseID = c.courseID
        LEFT JOIN 
            tblInstructor i ON cs.instructorID = i.instructorID
        WHERE 
            us.studentID = %s AND cs.semesterID = (
            SELECT semesterID
            FROM tblSemesters
            WHERE startDate < CURDATE()
            ORDER BY startDate ASC
            LIMIT 1
        );
        """
        cursor.execute(query, (user.studentID,))
        result = cursor.fetchall()
        enrolled_courses = [
            {
                'scheduleID': course[0],
                'course': course[1],
                'courseName': course[2],
                'days': course[3].split(',') if course[3] else [],
                'time': course[4],
                'start': course[5],
                'end': course[6],
                'location': course[7],
                'instructor': course[8],
                'Section': course[9],
                'Credits': course[10],
                'officeHours': course[11],
                'officeLocation': course[12]
            }
            for course in result
        ]

        return jsonify({"enrolledCourses": enrolled_courses}), 200
    except Error as e:
        print(e)
        return jsonify({"message": "Error fetching enrolled courses"}), 500
    finally:
        cursor.close()
        connection.close()


#  unenroll from course
@app.route('/unenrollCourse', methods=['POST'])
@jwt_required()
def unenroll_course():
    try:
        current_user_email = get_jwt_identity()['email']
        user = User.get_user_by_email(current_user_email)
        
        if not user or not user.studentID:
            return jsonify({"message": "User not found or not a student"}), 400
        
        schedule_id = request.json.get('scheduleID')
        if not schedule_id:
            return jsonify({"message": "Schedule ID is required"}), 400
        
        connection = connectToDB()
        cursor = connection.cursor()
        
        cursor.callproc('UnenrollCourse', [user.studentID, schedule_id])
        connection.commit()
        
        return jsonify({"message": "Course unenrolled successfully"}), 200
    except Error as e:
        print(e)
        return jsonify({"message": "Error unenrolling course"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
            

#get review tags
@app.route('/getTags', methods=['GET'])
def get_tags():
    connection = connectToDB()
    if not connection:
        return jsonify({"error": "DB connection failed"}), 500
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT tagID, tagName FROM tblTags")
        tags = cursor.fetchall()
        
        tag_list = [{"id": tag[0], "name": tag[1]} for tag in tags]
        
        return jsonify({"tags": tag_list}), 200
    except Error as err:
        return jsonify({"error": f"Error retrieving tags: {err}"}), 500
    finally:
        cursor.close()
        connection.close()


#mark a course as completed
@app.route('/markCourseCompleted', methods=['POST'])
@jwt_required()
def mark_course_completed_endpoint():
    try:
        identity = get_jwt_identity()
        user_email = identity['email']
        data = request.get_json()
        course_code = data.get('courseCode')
        completed = data.get('completed')
        review = data.get('review')
        student_rating = data.get('studentRating')
        tags = data.get('tags')
        letter_grade = data.get('letterGrade')

        app.logger.info(f"Received tags from frontend: {tags}")  #log the received tags
        app.logger.info(f"Received letter grade from frontend: {letter_grade}")  #log the received letter grade

        #check if course has already been reviewed by the student
        reviewed = is_course_reviewed(user_email, course_code)
        if reviewed:
            error_message = f"{course_code} has already been reviewed."
            app.logger.warning(error_message)
            return jsonify({"error": error_message}), 400

        success, message = mark_course_completed(user_email, course_code, completed, review, tags, student_rating, letter_grade)
        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"error": message}), 500
    except Exception as e:
        app.logger.error(f"Error in mark_course_completed_endpoint: {str(e)}")
        return jsonify({"error": "An internal server error occurred"}), 500
    

def mark_course_completed(user_email, course_code, completed, review, tags, student_rating, letter_grade):
    try:
        connection = connectToDB()
        if not connection:
            return False, "DB connection failed"

        cursor = connection.cursor()
        cursor.callproc('MarkCourseCompleted', [user_email, course_code, completed, review, json.dumps(tags), student_rating, letter_grade])
        connection.commit()
        return True, "Course marked as completed successfully"
    except Error as err:
        app.logger.error(f"Error in mark_course_completed: {str(err)}")
        connection.rollback()
        return False, f"Error marking course as completed: {str(err)}"
    finally:
        cursor.close()
        connection.close()

def is_course_reviewed(user_email, course_code):
    try:
        connection = connectToDB()
        if not connection:
            return False

        cursor = connection.cursor()
        query = """
            SELECT COUNT(*) 
            FROM tblRatings r
            JOIN tblCourses c ON r.courseID = c.courseID
            JOIN tblStudents s ON r.studentID = s.studentID
            WHERE s.Email = %s AND c.courseCode = %s
        """
        values = (user_email, course_code)
        cursor.execute(query, values)
        result = cursor.fetchone()
        review_count = result[0]

        return review_count > 0
    except Error as err:
        app.logger.error(f"Error in is_course_reviewed: {str(err)}")
        return False
    finally:
        cursor.close()
        connection.close()

#get tags for reviewed courses
@app.route('/getUserCourseTags', methods=['GET'])
@jwt_required()
def get_user_course_tags():
    try:
        identity = get_jwt_identity()
        user_email = identity['email']

        tags_by_course = fetch_user_course_tags(user_email)
        if tags_by_course is not None:
            return jsonify({"tags_by_course": tags_by_course}), 200
        else:
            return jsonify({"error": "Failed to fetch user course tags"}), 500
    except Exception as e:
        app.logger.error(f"Error in get_user_course_tags: {str(e)}")
        return jsonify({"error": "An internal server error occurred"}), 500

def fetch_user_course_tags(email):
    try:
        with connectToDB() as connection:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT 
                    c.courseCode,
                    GROUP_CONCAT(t.tagID) AS tags,
                    MAX(r.rating) AS rating
                FROM 
                    tblStudents s
                JOIN 
                    tblUser u ON s.userID = u.userID
                JOIN 
                    tblRatings r ON s.studentID = r.studentID
                JOIN
                    tblCourses c ON r.courseID = c.courseID
                JOIN
                    tblRatingTags rt ON r.ratingID = rt.ratingID
                JOIN
                    tblTags t ON rt.tagID = t.tagID
                WHERE 
                    u.Email = %s
                GROUP BY
                    c.courseCode
                """
                cursor.execute(query, (email,))
                results = cursor.fetchall()
                
                tags_by_course = {}
                for result in results:
                    course_code = result['courseCode']
                    tags = result['tags'].split(',') if result['tags'] else []
                    rating = result['rating']
                    tags_by_course[course_code] = {
                        'tags': tags,
                        'rating': rating
                    }

                    # Log the tags and rating for each course
                    app.logger.info(f"Course: {course_code}, Tags: {tags}, Rating: {rating}")

                return tags_by_course
    except Exception as e:
        app.logger.error(f"Error fetching user course tags and ratings: {str(e)}")
        return None


# Retrieve majors
@app.route('/majors', methods=['GET'])
def get_majors():
    connection = connectToDB()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT majorName FROM cs425.tblMajor")
            majors = [row[0] for row in cursor.fetchall()]
            return jsonify({"majors": sorted(majors)}), 200  
        except Error as err:
            return jsonify({"error": "Error while fetching majors: " + str(err)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({"error": "DB connection failed"}), 500
    

#logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  
    print('Logut Successful')
    return jsonify({"message": "Logout successful"}), 200


#Developed by John
#tests to see if the user is logged in for front end usability
@app.route('/check_login', methods=['GET'])
def check_login():
    if 'email' in session:
        return jsonify({'logged_in': True, 'user_id': session['user_id'], 'email': session['email']}), 200
    else:
        return jsonify({'logged_in': False}), 401
    

# User session for dashboard
@app.route('/dashboard', methods=['GET'])
@jwt_required()
def user_dashboard():
    identity = get_jwt_identity()
    current_user_email = identity['email']
    print(f"Extracted email: {current_user_email}")
    user = User.get_user_by_email(current_user_email)
    if user:
        print("STILL LOGGED IN SUCCESS")
        return jsonify(user.conv_to_json()), 200    
    else:
        return jsonify({"message": "User not found"}), 404
    
    
# Load courses page with user-specific course list
@app.route('/courses', methods=['GET'])
@jwt_required()
def loadCourses():
    identity = get_jwt_identity()
    current_user_email = identity['email']
    print(f"Extracted email: {current_user_email}")
    user = User.get_user_by_email(current_user_email)
    if user:
        print("STILL LOGGED IN SUCCESS")
        test = user.courses_to_json()
        print(test)
        return jsonify(user.courses_to_json()), 200
    else:
        return jsonify({"message": "User not found"}), 404
    
    
@app.route('/myaccount', methods=['GET'])
@jwt_required()
def myAccount():
    identity = get_jwt_identity()
    current_user_email = identity['email']
    print(f"Extracted email: {current_user_email}")
    user = User.get_user_by_email(current_user_email)
    if user:
        print("MY ACCOUNT USER SUCCESS")
        return jsonify(user.conv_to_json()), 200
    else:
        return jsonify({"message": "User not found"}), 404
    
    
@app.route('/editprofile', methods=['POST'])
@jwt_required()
def editProfile():
    identity = get_jwt_identity()
    current_user_email = identity['email']
    print(f"Extracted email: {current_user_email}")
    user_information = User.get_user_by_email(current_user_email)
    if not user_information:
        return jsonify({"message": "User not found"}), 404
    user_role = user_information.role
    data = request.get_json()
    if not current_user_email:
        print("AUTH REQUIRED")
        return jsonify({"message": "Authentication required"}), 401
    try:
        connection = connectToDB()
        cursor = connection.cursor(dictionary=True)

        updates = []
        params = []
        if 'firstname' in data:
            updates.append("u.Fname = %s")
            params.append(data['firstname'])
        if 'lastname' in data:
            updates.append("u.Lname = %s")
            params.append(data['lastname'])
        if 'major' in data and user_role != 'Instructor':
            cursor.execute("SELECT majorID, majorName FROM tblMajor WHERE majorName = %s", (data['major'],))
            maj_result = cursor.fetchone()
            majorName = maj_result['majorName']
            print("Fetch result:", maj_result)
            if maj_result:
                updates.append("s.majorName = %s")
                params.append(majorName)
            # updates.append("majorName = %s")
            # params.append(data['major'])
        
        if updates:
            if user_role == 'Instructor':
                joined_updates = ', '.join(updates)
                query = f"""
                UPDATE tblInstructor i
                JOIN tblUser u ON i.userID = u.userID
                SET {joined_updates} WHERE u.Email = %s
                """
                print("AS INSTRUCTOR:")
            else:
                joined_updates = ', '.join(updates)
                query = f"""
                UPDATE tblStudents s
                JOIN tblUser u ON s.userID = u.userID
                SET {joined_updates}
                WHERE u.Email = %s
                """
                print("AS STUDENT:")
            params.append(current_user_email)
            print("Executing query:", query)  
            print("With params:", params)    
            cursor.execute(query, params)
            connection.commit()
            # query = f"UPDATE tblUser SET {', '.join(updates)} WHERE Email = %s"
            # params.append(current_user_email)
            # cursor.execute(query, params)
            # connection.commit()

        return jsonify({"message": "Profile updated successfully"}), 200
    except Error as err:
        print("Error updating profile:", err)
        return jsonify({"message": "An error occurred"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
    
    
@app.route('/changepassword', methods=['POST'])
@jwt_required()
def changePassword():
    try:
        user_identity = get_jwt_identity()
        email = user_identity['email']
        new_password = request.json.get('newPassword')
        if not new_password:
            return jsonify({"message": "New password is required"}), 400
        connection = connectToDB();
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT Passwd FROM tblUser WHERE Email = %s", (email,))
        user_data = cursor.fetchone()
        curr_hashed_pw = user_data['Passwd']
        if bcrypt.check_password_hash(curr_hashed_pw, new_password):
            return jsonify({"message": "New password cannot match old"}), 400
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        update_query = "UPDATE tblUser SET Passwd = %s WHERE Email = %s"
        cursor.execute(update_query, (hashed_password, email))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "User not found"}), 404
        return jsonify({"message": "Password updated successfully"}), 200
    except Error as e:
        print(e)
        return jsonify({"message": "Database connection error"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


#retrieve courses with completion status
@app.route('/getCourseProgress', methods=['GET'])
@jwt_required()
def courses_for_progress_page():
    identity = get_jwt_identity()
    current_user_email = identity['email']
    user = User.get_user_by_email(current_user_email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    connection = connectToDB()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT creditsReq FROM tblMajor WHERE majorName = %s", (user.majorName,))
            total_credits_req = cursor.fetchone()[0]

            cursor.callproc('GetCoursesForProgress', [current_user_email])
            user_courses = []
            for result in cursor.stored_results():
                user_courses = result.fetchall()

            course_list = []
            for courses in user_courses:
                course_dict = {
                    "courseName": courses[1],
                    "courseCode": courses[2],
                    "credits": courses[3],
                    "isCompleted": courses[4],
                }
                course_list.append(course_dict)


            return jsonify({
                #"majorName": user.majorName,
                "totalCreditsReq": total_credits_req,
                "user_courses": course_list
            }), 200
        except Error as err:
            return jsonify({"error": "Error while fetching user's courses: " + str(err)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({"error": "DB connection failed"}), 500
    

#get career variables for progress page (left hand side of page)
@app.route('/getCareerProgress', methods=['GET'])
@jwt_required()
def get_career_progress():
    identity = get_jwt_identity()
    current_user_email = identity['email']
    user = User.get_user_by_email(current_user_email)

    if not user or not user.studentID:
        return jsonify({"error": "User not found or not a student"}), 404

    connection = connectToDB()
    if connection:
        cursor = connection.cursor()
        try:
            query = """
            SELECT 
                SUM(c.Credits) as TotalCredits,
                cs.Term,
                g.cumulativeGPA
            FROM 
                tblUserSchedule us
            JOIN
                tblcourseSchedule cs ON us.scheduleID = cs.scheduleID
            JOIN
                tblCourses c ON cs.courseID = c.courseID
            LEFT JOIN
                (
                    SELECT
                        studentID,
                        cumulativeGPA
                    FROM
                        tblGPA
                    WHERE
                        (studentID, semesterID) IN (
                            SELECT
                                studentID,
                                MAX(semesterID)
                            FROM
                                tblGPA
                            GROUP BY
                                studentID
                        )
                ) g ON us.studentID = g.studentID
            WHERE
                us.studentID = %s
                AND cs.semesterID = (
                    SELECT semesterID
                    FROM tblSemesters
                    WHERE startDate < CURDATE()
                    ORDER BY startDate DESC
                    LIMIT 1
                )
            GROUP BY
                cs.Term, g.cumulativeGPA;
            """
            cursor.execute(query, (user.studentID,))
            result = cursor.fetchone()

            if result:
                total_credits, term, cumulative_gpa = result
                return jsonify({
                    "majorName": user.majorName,
                    "totalCredits": total_credits,
                    "Term": term,
                    "cumulativeGPA": cumulative_gpa if cumulative_gpa is not None else 0.00
                }), 200
            else:
                return jsonify({"error": "No career progress found for the current term"}), 404
        except Error as err:
            return jsonify({"error": "Error while fetching career progress: " + str(err)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({"error": "DB connection failed"}), 500

    
    
# Retrieve courses related to user input at department search
@app.route('/search-departments', methods=['GET'])
@jwt_required()
def search_departments():
    query_param = request.args.get('query', '')
    level_param = request.args.get('level', None)
    start_time_param = request.args.get('startTime', None)
    format_param = request.args.get('format', None)
    location_param = request.args.get('location', None)
    term_param = request.args.get('term', None)
    rating_param = request.args.get('rating', None)
    
    connection = connectToDB()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            query = """
            SELECT
                scheduleID,
                Section,
                courseName,
                courseCode,
                courseMajor,
                department,
                professor,
                term,
                format,
                units,
                meetingTime,
                Location,
                days,
                classCapacity,
                enrollmentTotal,
                availableSeats,
                averageRating,
                courseLevel,
                frequentTags
            FROM (
                SELECT *,
                    ROW_NUMBER() OVER (PARTITION BY courseCode, term ORDER BY scheduleID) AS rn
                FROM vwCourseDetails
                WHERE 1=1
            ) t
            WHERE rn = 1
            """
            
            params = []
            filters_applied = False
            
            if 'query' in request.args and query_param:
                query += " AND courseMajor LIKE %s"
                params.append(f"{query_param}%")
                filters_applied = True
            
            if 'level' in request.args and level_param:
                level = level_param.rstrip('+')
                numeric_level = int(level)
                query += " AND courseLevel = %s"
                params.append(numeric_level)
                filters_applied = True
            
            if 'startTime' in request.args and start_time_param:
                start_time_param = unquote(request.args.get('startTime', ''))
                start_time_range = start_time_param.split('-')
                start_time_lower = datetime.strptime(start_time_range[0].strip() + start_time_range[1][-2:].strip(), '%I%p').time()
                end_time_value = start_time_range[1].strip().split(' ')[0]  # Extract the end time value
                end_time_period = start_time_range[1][-2:].strip()  # Extract AM or PM
                start_time_upper = datetime.strptime(end_time_value + end_time_period, '%I%p').time()
                query += " AND (TIME_FORMAT(LEFT(meetingTime, LOCATE('-', meetingTime) - 1), '%h:%i %p') BETWEEN %s AND %s OR TIME_FORMAT(LEFT(meetingTime, LOCATE('-', meetingTime) - 1), '%H:%i') BETWEEN TIME_FORMAT(%s, '%H:%i') AND TIME_FORMAT(%s, '%H:%i'))"
                params.extend([start_time_lower.strftime('%I:%M %p'), start_time_upper.strftime('%I:%M %p'), start_time_lower, start_time_upper])
                filters_applied = True
            
            if 'format' in request.args and format_param:
                query += " AND format = %s"
                params.append(format_param)
                filters_applied = True
            
            if 'location' in request.args and location_param:
                query += " AND LEFT(Location, LOCATE(' ', Location) - 1) = %s"
                params.append(location_param)
                filters_applied = True

            if 'term' in request.args and term_param:
                query += " AND term = %s"
                params.append(term_param)
                filters_applied = True
            
            if 'rating' in request.args and rating_param:
                query += " AND averageRating >= %s"
                params.append(float(rating_param))
                filters_applied = True
            
            query += " ORDER BY courseLevel, courseCode;"
            
            print("Query Parameters:", params)

            cursor.execute(query, tuple(params))
            result = cursor.fetchall()       
            departments = [{
                'scheduleID': dept['scheduleID'],
                'section': dept['Section'],
                'professor': dept['professor'],
                'courseName': dept['courseName'],
                'courseCode': dept['courseCode'],
                'courseMajor': dept['courseMajor'],
                'department': dept['department'],
                'term': dept['term'],
                'format': dept['format'],
                'units': dept['units'],
                'meetingTime': dept['meetingTime'],
                'Location': dept['Location'],
                'days': dept['days'],
                'classCapacity': dept['classCapacity'],
                'enrollmentTotal': dept['enrollmentTotal'],
                'availableSeats': dept['availableSeats'],
                'averageRating': dept['averageRating'],
                'frequentTags': dept['frequentTags'].split(', ')[:4] if dept['frequentTags'] else [],
            } for dept in result]
        finally:
            cursor.close()
            connection.close()
        return jsonify(departments), 200
    else:
        return jsonify({"message": "Failed to connect to database"}), 500
    
    
# Add courses to user schedule
@app.route('/enrollCourses', methods=['POST'])
@jwt_required()
def enroll_courses():
    try:
        current_user_email = get_jwt_identity()['email']
        user = User.get_user_by_email(current_user_email)

        if not user or not user.studentID:
            return jsonify({"message": "User not found or not a student"}), 400

        schedule_ids = request.json.get('scheduleIDs', [])
        if not schedule_ids:
            return jsonify({"message": "No scheduleIDs provided"}), 400

        connection = connectToDB()
        cursor = connection.cursor()

        print(schedule_ids)

        added_schedule_ids = []

        try:
            cursor.execute("START TRANSACTION")

            for schedule_id in schedule_ids:
                cursor.execute("""
                    SELECT cs.availableSeats, cs.courseCode, cs.startTime, cs.endTime, cs.meetingDays,cs.semesterID
                    FROM tblcourseSchedule cs
                    WHERE cs.scheduleID = %s
                    FOR UPDATE
                """, (schedule_id,))

                result = cursor.fetchone()

                if result:
                    availableSeats, course_code, startTime, endTime, meetingDays, semesterID = result

                    if availableSeats <= 0:
                        raise Exception(f"Course {course_code} has no available seats")

                    #check if the student is already enrolled in the course
                    cursor.execute("""
                        SELECT COUNT(*)
                        FROM tblUserSchedule
                        WHERE studentID = %s AND scheduleID = %s
                    """, (user.studentID, schedule_id))
                    already_enrolled = cursor.fetchone()[0]
                    if already_enrolled:
                        raise Exception(f"You are already enrolled in course {course_code}")
                    
                    #check for time conflicts within the same semester
                    cursor.execute("""
                        SELECT cs.courseCode
                        FROM tblcourseSchedule cs
                        JOIN tblUserSchedule us ON cs.scheduleID = us.scheduleID
                        WHERE us.studentID = %s
                        AND cs.semesterID = %s
                        AND cs.meetingDays LIKE CONCAT('%%', %s, '%%')
                        AND (
                            (ADDTIME(cs.endTime, '00:15:00') > %s AND cs.endTime <= %s)
                            OR (cs.startTime >= %s AND SUBTIME(cs.startTime, '00:15:00') < %s)      /*15 minute buffer between courses*/
                            OR (cs.startTime <= %s AND cs.endTime >= %s)
                        )
                    """, (user.studentID, semesterID, meetingDays, startTime, startTime, endTime, endTime, startTime, endTime))
                    conflicting_courses = cursor.fetchall()
                    if conflicting_courses:
                        conflicting_course_codes = [course[0] for course in conflicting_courses]
                        raise Exception(f"There is a time conflict with course(s): {', '.join(conflicting_course_codes)}")

                    cursor.execute("""
                        INSERT INTO tblUserSchedule (studentID, scheduleID)
                        VALUES (%s, %s)
                    """, (user.studentID, schedule_id))

                    cursor.execute("""
                        UPDATE tblcourseSchedule
                        SET enrollmentTotal = enrollmentTotal + 1,
                            availableSeats = availableSeats - 1
                        WHERE scheduleID = %s
                    """, (schedule_id,))

                    print(f"Course with scheduleID {schedule_id} added to user schedule")
                    added_schedule_ids.append(schedule_id)
                else:
                    print(f"Course with scheduleID {schedule_id} not found in tblcourseSchedule")

            cursor.execute("COMMIT")
            return jsonify({
                "message": "Courses enrollment processed",
                "added_schedule_ids": added_schedule_ids
            }), 200
        except Exception as e:
            cursor.execute("ROLLBACK")
            print(e)
            return jsonify({"message": str(e)}), 400
    except Error as e:
        print(e)
        return jsonify({"message": "Error adding courses"}), 500
    finally:
        cursor.close()
        connection.close()


#retrieve notifications for banner
@app.route('/notifications', methods=['GET'])
def get_today_notification():
    notification, error = get_formatted_notification()
    if error:
        if error == "No notifications retrieved":
            return jsonify({"message": error}), 404
        return jsonify({"error": error}), 500

    return jsonify(notification), 200


def get_formatted_notification():
    notification, error = fetch_todays_notification()
    if error:
        return None, error

    if notification:
        announce_date = notification['announceDate']
        formatted_date = announce_date.strftime("%B %d, %Y")
        notification['announceDate'] = formatted_date
        return notification, None
    return None, "No notifications retrieved" 


def fetch_todays_notification():
    connection = connectToDB()
    if not connection:
        return None, "Failed to connect to the database"
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT announceDate, source, message FROM cs425.tblNotifications WHERE announceDate >= CURDATE() ORDER BY announceDate ASC LIMIT 1")
        return cursor.fetchone(), None
    except Error as err:
        return None, str(err)
    finally:
        cursor.close()
        connection.close()
        
        
@app.route('/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    identity = get_jwt_identity()
    user_email = identity.get('email')
    try:
        connection = connectToDB()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT userID FROM tblUser WHERE Email = %s", (user_email,))
        user_info = cursor.fetchone()
        if not user_info: return jsonify({"message": "User not found"}), 404
        user_id = user_info['userID']
        cursor.execute("DELETE FROM tblInstructor WHERE userID = %s", (user_id,))
        cursor.execute("DELETE FROM tblUser WHERE userID = %s", (user_id,))
        connection.commit()
        print("ACCOUNT DELETED")
        return jsonify({"message:": "Account deleted"}), 200
    except Error as err:
        print(err)
        connection.rollback()
        return jsonify({"message": "Error during account deletion"}), 500
    finally:
        cursor.close()
        connection.close()
        
        
@app.route('/analytics/counts', methods=['GET'])
@jwt_required()
def get_counts():
    connection = connectToDB()
    cursor = connection.cursor(dictionary=True)
    try:
        response = {}
        cursor.execute("SELECT COUNT(*) AS student_count FROM tblStudents")
        student_count = cursor.fetchone()
        response['student_count'] = student_count['student_count'] if student_count else 0
        cursor.execute("SELECT COUNT(*) AS instructor_count FROM tblInstructor")
        instructor_count = cursor.fetchone()
        response['instructor_count'] = instructor_count['instructor_count'] if instructor_count else 0
        
        return jsonify(response), 200
    except Exception as exc:
        print(f"Error fetching counts: {exc}")
        return jsonify({"error": "Error occurred while fetching user counts"}), 500
    finally:
        cursor.close()
        connection.close()
        

@app.route('/analytics/stored-data-counts', methods=['GET'])
@jwt_required()
def get_stored_data_counts():
    connection = connectToDB()
    cursor = connection.cursor(dictionary=True)
    try:
        response = {}
        cursor.execute("SELECT COUNT(*) AS course_count FROM tblCourses")
        course_count = cursor.fetchone()
        response['course_count'] = course_count['course_count'] if course_count else 0
        cursor.execute("SELECT COUNT(*) AS major_count FROM tblMajor")
        major_count = cursor.fetchone()
        response['major_count'] = major_count['major_count'] if major_count else 0
        cursor.execute("SELECT COUNT(*) AS schedule_count FROM tblUserSchedule")
        schedule_count = cursor.fetchone()
        response['schedule_count'] = schedule_count['schedule_count'] if schedule_count else 0
        
        return jsonify(response), 200
    except Exception as exc:
        print(f"Error fetching stored data counts: {exc}")
        return jsonify({"error": "Error occurred while fetching stored data counts"}), 500
    finally:
        cursor.close()
        connection.close()
        

# Connect to database
def connectToDB():
    try:
        connection = connect(
            host= "coursecompass-db-instance.c74q40ekci79.us-east-2.rds.amazonaws.com",
            user = "admin",
            passwd = "CourseCompT38!",
            database = "cs425"
        )
        return connection
    except Error as err:
        print("Error while connecting to database", err)
        return None


# Launch backend development server
if __name__ == '__main__':
    app.run(debug=True)
