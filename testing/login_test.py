# Author: Lucas Videtto
# Course Compass
# Unit tests for login functionality

import pytest
from flask import Flask, session
from app.backend import app, connectToDB, bcrypt


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client
            
            
@pytest.fixture
def db():
    connection = connectToDB()
    yield connection
    connection.close()
        

@pytest.fixture
def test_user(db):
    email = "team38testemail@gmail.com"
    password = "Test0.0$"
    hashed_password = hash_password(password)
    cursor = db.cursor()
    cursor.execute("INSERT INTO tblUser (Email, Passwd) VALUES (%s, %s)", (email, hashed_password))
    db.commit()
    cursor.close()
    return {"email": email, "password": password, "hashed_password": hashed_password}

        
# hashes user password for test cases
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


# test for valid email and password
def test_valid_login(client, db, test_user):
    response = client.post('/login', json={'email': test_user['email'], 'password': test_user['password']})
    assert response.status_code == 200
    assert b"Login successful" in response.data
    cursor = db.cursor()
    cursor.execute("DELETE FROM tblUser WHERE Email = %s", (test_user['email'],))
    db.commit()
    cursor.close()
    

# test for invalid email
def test_invalid_email(client, db, test_user):
    invalid_email = "userNotInDB@gmail.com"
    response = client.post('/login', json={'email': invalid_email, 'password': test_user['password']})
    assert response.status_code == 401
    assert b"Invalid email or password" in response.data
    cursor = db.cursor()
    cursor.execute("DELETE FROM tblUser WHERE Email = %s", (test_user['email'],))
    db.commit()
    cursor.close()
    
    
# test for incorrect password
def test_incorrect_password(client, db, test_user):
    incorrect_password = "incorrectPw1$"
    response = client.post('/login', json={'email': test_user['email'], 'password': incorrect_password})
    assert response.status_code == 401
    assert b"Invalid email or password" in response.data
    cursor = db.cursor()
    cursor.execute("DELETE FROM tblUser WHERE Email = %s", (test_user['email'],))
    db.commit()
    cursor.close()
    