# Created by Lucas Videtto
# Backend functionality for Course Compass

from flask import Flask, jsonify, request, session
from flask_jwt_extended import JWTManager,create_access_token
from flask_cors import CORS
from mysql.connector import connect, Error
from datetime import datetime
from flask_bcrypt import Bcrypt


# Under construction !!!
app = Flask(__name__)
app.secret_key = '123456789'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# Login functionality for backend
# Under construction !!!
# Check backend development notes (Lucas)
# Included print statements for terminal reference
@app.route('/login', methods=['POST'])
def login(): 
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        
        if not email or not password:
            print("MISSING EMAIL OR PASSWORD")
            return jsonify({"message": "Missing email or password"}), 400
        
        try:
            connection = connectToDB()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tblUser WHERE Email = %s", (email,))
            user = cursor.fetchone()
            
            if user and bcrypt.check_password_hash(user['Passwd'], password):
                session['user_id'] = user['userID']
                session['email'] = user['Email']
                
                #access_token = create_access_token(identity={"email": user['Email'], "userID": user['userID']})
                print("LOGIN SUCCESSFUL")
                return jsonify({"message": "Login successful"}), 200
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
# Under construction !!!
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
        majID = request.json.get('majorID')
        
        if not fname or not lname or not dob or not email or not pw or not majID:
            print("MISSING REQUIRED FIELDS")
            return jsonify({"message:" "Missing required fields"}), 400
        
        birthdate = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if age < 17:
            print("MUST BE AT LEAST 17 YEARS OLD TO REGISTER")
            return jsonify({"message": "Must be at least 17 years old to sign up"}), 400
        
        try:
            connection = connectToDB()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tblUser WHERE Email = %s", (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                print("EMAIL ALREADY IN USE")
                return jsonify({"message": "Email already exists"}), 409
            
            hashed_pw = bcrypt.generate_password_hash(pw).decode('utf-8')
            
            cursor.execute("INSERT INTO tblUser (Fname, Lname, DOB, Email, Passwd, majorName) VALUES (%s, %s, %s, %s, %s, %s)", (fname, lname, dob, email, hashed_pw, majID))
            connection.commit()
            
            cursor.execute("SELECT * FROM tblUser WHERE Email = %s", (email,))
            new_user = cursor.fetchone()
            
            access_token = create_access_token(identity={"email": new_user['Email'], "userID": new_user['userID']})
            
            session['user_id'] = new_user['userID']
            session['email'] = new_user['Email']
            
            print("SIGN UP SUCCESSFUL")
            return jsonify({"access_token": access_token, "message": "Sign up successful"}), 200
        except Error as err:
            print(err)
            return jsonify({"message": "An error occurred"}), 500
        
        finally:
            cursor.close()
            connection.close()
            
    print("INVALID REQUEST")
    return jsonify({"message": "Invalid request"}), 400

#fetch user information
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


# Retrieve majors
@app.route('/majors', methods=['GET'])
def get_majors():
    connection = connectToDB()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT majorName FROM cs425.tblMajor")
            majors = [row[0] for row in cursor.fetchall()]
            return jsonify({"majors": majors}), 200  
        except Error as err:
            return jsonify({"error": "Error while fetching majors: " + str(err)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({"error": "DB connection failed"}), 500
    

#fetch course information, not finished
@app.route('/getCourseInfo', methods=['GET'])
def get_courses():
    connection = connectToDB()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM cs425.tblCourses")
            courses = cursor.fetchall()

            courses_list = []
            for course in courses:
                course_dict = {
                    "courseCode" : course[1],
                    "courseName" : course[2],
                    "description" : course[4],
                    "Room" : course[14],
                    "instructor" : course[15],
                    "section" : course[13]
                }
                courses_list.append(course_dict)
            return jsonify({"courses": courses_list}), 200  
        except Error as err:
            return jsonify({"error": "Error while fetching courses: " + str(err)}), 500
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
    if 'user_id' in session and 'email' in session:
        return jsonify({'logged_in': True, 'user_id': session['user_id'], 'email': session['email']}), 200
    else:
        return jsonify({'logged_in': False}), 401
    
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

# Launch development server
app.run(debug=True)


