# Author: Lucas Videtto
# Course Compass
# Unit tests for login functionality

import pytest
from flask import Flask, session
from app.backend import app, connectToDB, bcrypt


@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client
            
            
@pytest.fixture(scope="module")
def db():
    connection = connectToDB()
    yield connection
    connection.close()
        

@pytest.fixture(scope="module")
def test_user(db):
    email = "team38testemail@gmail.com"
    password = "Test0.0$"
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO tblUser (Email, Passwd) VALUES (%s, %s)", (email, hashed_password))
        db.commit()
        yield {"email": email, "password": password, "hashed_password": hashed_password}
    finally:
        cursor.execute("DELETE FROM tblUser WHERE Email = %s", (email,))
        db.commit()
        cursor.close()


# test for valid email and password
def test_valid_login(client, test_user):
    response = client.post('/login', json={'email': test_user['email'], 'password': test_user['password']})
    assert response.status_code == 200
    assert b"Login successful" in response.data
    

# test for invalid email
def test_invalid_email(client, test_user):
    invalid_email = "userNotInDB@gmail.com"
    response = client.post('/login', json={'email': invalid_email, 'password': test_user['password']})
    assert response.status_code == 401
    assert b"Invalid email or password" in response.data
    
    
# test for incorrect password
def test_incorrect_password(client, test_user):
    incorrect_password = "incorrectPw1$"
    response = client.post('/login', json={'email': test_user['email'], 'password': incorrect_password})
    assert response.status_code == 401
    assert b"Invalid email or password" in response.data
    
    
# test for empty email field
def test_email_field(client, test_user):
    response = client.post('/login', json={'email': '', 'password': test_user['password']})
    assert response.status_code == 400
    assert b"Missing email or password" in response.data


# test for empty password field
def test_password_field(client, test_user):
    response = client.post('/login', json={'email': test_user['email'], 'password': ''})
    assert response.status_code == 400
    assert b"Missing email or password" in response.data
    
    
# test for preventing SQL injection
def test_sql_injection(client, db):
    cursor = db.cursor()
    cursor.execute(("CREATE TEMPORARY TABLE IF NOT EXISTS temp_tblUser LIKE tblUser;"))
    db.commit()
    injection = "'; DROP TABLE temp_tblUser; --"
    response = client.post('/login', json={'email': injection, 'password': 'validPasswd1$'})
    assert response.status_code == 401
    assert b"Invalid email or password" in response.data
    