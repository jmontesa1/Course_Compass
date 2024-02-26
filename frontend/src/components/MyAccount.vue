<!--Created by: John Montesa-->
<!-- This is the Account page for Course Compass -->

<template>
    <div class="settings-container">
        <div class="container-fluid mt-3">
            <div class="row">
                <!--LEFT SIDE OF PAGE-->
                <div class="col-md-1 d-flex flex-column">
                    <img class="gear" src="../assets/gear.png" alt="Settings Icon">
                </div>



                <!--RIGHT SIDE OF PAGE-->
                <div class="col d-flex flex-column">
                    <h2>My Account</h2>

                    <div>
                        <br>
                        <br>
                        <p><strong>First Name:</strong> {{ user.firstname }}</p>
                        <p><strong>Last Name:</strong> {{ user.lastname }}</p>
                        <p><strong>Email:</strong> {{ user.email }}</p>
                        <p><strong>Birthdate:</strong> {{ user.dob }}</p>
                        <p><strong>Major:</strong> {{ user.major }}</p>
                        <!-- Add other user information fields as needed -->
                        <button type="submit">Edit Profile</button>
                        <button type="submit">Change Password</button>
                    </div>
                </div>

                <div class="col-md-2 d-flex flex-column">
                    <br>
                    <br>
                    <img class="profile-picture" :src="user.profilePicture" alt="Profile Picture">
                    <p style="text-align:center;"><i>Profile Picture</i></p>
                    <br>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    
    export default {
        data() {
            return {
                user: {
                    firstname: '',
                    lastname: '',
                    email: '',
                    dob: '',
                    major: '',
                    profilePicture: require('../assets/profile-picture.jpg'),
                },
                error: null,
            };
        },
        created() {
            this.fetchUserInfo();
        },
        methods: {
            fetchUserInfo() {
                axios.get('http://127.0.0.1:5000/myaccount', { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }})
                .then(response => {
                    this.user.firstname = response.data.Fname;
                    this.user.lastname = response.data.Lname;
                    this.user.email = response.data.Email;
                    this.user.dob = response.data.DOB;
                    this.user.major = response.data.majorName;
                    console.log('My Account page loaded successfully', response.data);
                })
                .catch(error => {
                    console.error("Error loading My Account page", error);
                });        
            }
        }
    }
</script>

<style scoped>
    h2 {
        text-align: left;
        font-family:coolvetica;
    }

    p{
        font-family: Poppins, sans-serif;
    }

    .settings-container {
        background-color: #e1e1e1;
        margin: 3% auto;
        padding: 20px;
        width: 80%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 0 px rgba(232, 0, 0, 0.1);
    }
    
    .col{
        border-left: 2px solid #000000;
    }

    .gear {
        min-width: 30px;
        max-width: 60px;
    }

    .profile-picture {
        margin-left:auto;
        margin-right:auto;
        max-width: 100px;
        border-radius: 50%; 
        margin-bottom: 10px;
    }

    button {
        font-family: coolvetica, sans-serif;
        font-size: 25px;
        background-color: #000000;
        color: #ffffff;
        padding: 5px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s linear, color 0.3s linear;
        margin-right: 40px;
    }

    button:hover {
        background-color: #555555;
    }

</style>