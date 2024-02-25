import pytest
from flask import Flask, session
from app.backend import app, connectToDB, bcrypt

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client
        with app.app_context():
            pass
        
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

        
def test_valid_login(client):
    email = "lucastestingemail@gmail.com"
    password = "Test1.0$"
    hashed_password = hash_password(password)
    
    connection = connectToDB()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tblUser (Email, Passwd) VALUES (%s, %s)", (email, hashed_password))
    connection.commit()
    
    response = client.post('/login', json={'email': email, 'password': password})
    
    assert response.status_code == 200
    assert b"Login successful" in response.data
    
    cursor.execute("DELETE FROM tblUser WHERE Email = %s", (email,))
    connection.commit()
    cursor.close()
    connection.close()
        