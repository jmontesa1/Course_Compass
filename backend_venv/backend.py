# Created by Lucas Videtto
# Backend connection for Course Compass

from flask import Flask, jsonify, request, session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from mysql.connector import connect, Error
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt


# Under construction !!!
app = Flask(__name__)
app.secret_key = '12345'
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


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
                
                access_token = create_access_token(identity={"email": user['Email'], "userID": user['userID']})
                print("LOGIN SUCCESSFUL")
                return jsonify({"access_token": access_token, "message": "Login successful"}), 200
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
            
            cursor.execute("INSERT INTO tblUser (Fname, Lname, DOB, Email, Passwd) VALUES (%s, %s, %s, %s, %s)", (fname, lname, dob, email, hashed_pw))
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


@app.route('/getUserInfo', methods=['GET'])
@jwt_required()
def getUserInfo():
    user_email = get_jwt_identity()
    if not user_email:
        return jsonify({"error": "User not logged in"}), 401
    
    connection = connectToDB()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT Fname, Lname, Email, majorName FROM cs425.tblUser WHERE Email = %s", (user_email,))
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
     


#route for fetching majors
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

app.run(debug=True)