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
            
    
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    firstname = data['firstname']
    lastname = data['lastname']
    dateOfBirth = data['dateOfBirth']
    email = data['email']
    password = data['password']
    majorID = data['majorID']

    passwordHash = bcrypt.generate_password_hash(password).decode('utf-8')

    
    connection = connectToDB()
    if connection is not None:
        cursor = connection.cursor()
        try:
            insertQuery = """INSERT INTO cs425.tblUser (Fname, Lname, DOB, Email, Passwd) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(insertQuery, (firstname, lastname, dateOfBirth, email, passwordHash))
            connection.commit()
            session['user_email'] = email
            return jsonify({"message": "Signup successful"}), 200
        except Error as err:
            print("Error while inserting data into database", err)
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500


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