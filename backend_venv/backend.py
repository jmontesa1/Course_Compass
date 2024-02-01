# Created by Lucas Videtto
# Backend connection for Course Compass

from flask import Flask, jsonify, request, session
from flask_cors import CORS
from mysql.connector import connect, Error
from datetime import datetime, timedelta
import hashlib
import os
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = '12345'
CORS(app)
bcrypt = Bcrypt(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    
    demo_email = '425demo@example.com' # For demo showcase / plan b
    demo_pw = 'Password1!'
    
    if email == demo_email and password == demo_pw:
        print("User logged in and session started") # Print check for testing purposes
        session['user_email'] = email
        return jsonify({"message": "Demo login successful"}), 200
    
    connection = connectToDB()
    if connection is not None:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM cs425.tblUser WHERE Email = %s", (email,))
            user = cursor.fetchone()
            if user and user['Passwd'] == password:
                session['user_email'] = email
                return jsonify({"message": "Login successful"}), 200
            else:
                return jsonify({"error": "Invalid email or password"}), 401
        except Error as err:
            print("Error while authenticating user", err)
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500
    
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    password = data['password']
    majorID = data['majorID']
    userId = 100 - len(firstname) - len(lastname)
    
    connection = connectToDB()
    if connection is not None:
        cursor = connection.cursor()
        try:
            insertQuery = """INSERT INTO cs425.tblUser (userID, Fname, Lname, Email, Passwd) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(insertQuery, (userId, firstname, lastname, email, password))
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
def getUserInfo():
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({"error": "User not logged in"}), 401
    
    connection = connectToDB()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT Fname, Lname, Email, majorID FROM cs425.tblUser WHERE Email = %s", (user_email,))
            user_info = cursor.fetchone()
            if user_info:
                major_id = user_info['majorID']
                cursor.execute("SELECT majorName FROM cs425.tblMajor WHERE majorID = %s", (major_id,))
                major = cursor.fetchone()
                if major:
                    user_info['major'] = major['majorName']
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