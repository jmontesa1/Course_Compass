<!--Created by: John Montesa-->
<!-- This is the Account page for Course Compass -->

<template>
<div v-if="userType !== ''">
    <div class="settings-container">

        <div class="container-fluid mt-3">
            <div class="row">
                <!--LEFT SIDE OF PAGE-->
                <div class="col-sm-1 d-flex flex-column align-items-center" style="border-top: 1px solid black;">
                    <span class="material-symbols-outlined" style="font-size: 60px; margin-top: 15px;">
                        settings
                    </span>
                </div>
                <!--RIGHT SIDE OF PAGE-->
                <div class="col d-flex flex-column">
                    <div class="loading-container" v-if="loading">
                        <!-- loading anim -->
                        <v-progress-circular indeterminate :width="5"></v-progress-circular>
                    </div>

                    <div style="padding: 10px;" v-else>
                        <v-row>
                            <v-col cols="8">
                                <h2 style="margin-left: -8px;">Account Details</h2>
                                <p v-if="user.role == 'Instructor'" style="font-size: 17px;"><strong><i>Instructor</i></strong></p>
                                <p v-if="user.role == 'Admin'" style="font-size: 17px;"><strong><i>Admin</i></strong></p>
                                <p v-if="user.role == 'Student'" style="font-size: 17px;"><strong><i>Student</i></strong></p>
                                <br>
                                <p><strong>First Name:</strong> {{ user.firstname }}</p>
                                <p><strong>Last Name:</strong> {{ user.lastname }}</p>
                                <p><strong>Email:</strong> {{ user.email }}</p>
                                <p><strong>Birthdate:</strong> {{ user.dob }}</p>
                                <p v-if="user.role === 'Student'"><strong>Major:</strong> {{ user.major }}</p>
                            </v-col>
                            <v-col cols="4">
                                <v-card class="buttons-container">
                                    <v-card-title>
                                        Options
                                    </v-card-title>
                                    <v-card-text>
                                        <v-dialog v-model="dialog" max-width="500" style="font-family: Poppins;">
                                            <template v-slot:activator="{ props: activatorProps }">
                                                <v-btn v-bind="activatorProps" stacked variant="outlined" style="width:100%;">
                                                <span class="material-symbols-outlined">
                                                    edit
                                                </span>
                                                Edit Profile
                                            </v-btn>
                                            </template>
                                            <!--Pop up -->
                                            <v-card title="Edit Profile Information">
                                                <v-card-text>
                                                    <v-form>
                                                        <v-text-field v-model="editData.firstName" label="First Name"></v-text-field>
                                                        <v-text-field v-model="editData.lastName" label="Last Name"></v-text-field>
                                                        <!--<v-select v-model="editData.major" :items="majorOptions" label="Major"></v-select> -->
                                                        <v-select v-if="user.role === 'Student'" v-model="editData.selectedMajor" :items="majors" item-text="major" item-value="majorID" label="Select your major" return-object required>
                                                            <option value="" disabled>Select your major</option>
                                                            <option v-for="major in majors" :key="major" :value="major">{{ major }}</option>
                                                        </v-select>
                                                    </v-form>
                                                </v-card-text>
                                                <v-card-actions>
                                                    <v-spacer></v-spacer>
                                                    <v-btn text="Cancel" variant="plain" @click="dialog = false"></v-btn>
                                                    <v-btn color="primary" text="Confirm Changes" variant="tonal" @click="updateProfile"></v-btn>
                                                </v-card-actions>
                                            </v-card>
                                        </v-dialog>
                                        <br><br>
                                        <v-dialog v-model="changePasswordDialog" max-width="500" style="font-family: Poppins;">
                                            <template v-slot:activator="{ props: activatorProps }">
                                                <v-btn v-bind="activatorProps" stacked variant="outlined" style="width:100%;" @click="sendEmail">
                                                <span class="material-symbols-outlined">
                                                    Password
                                                </span>
                                                Change Password
                                            </v-btn>
                                            </template>
                                            <!--Pop up -->
                                            <v-card title="Change Password">
                                                <v-card-text>
                                                    An email has been sent to <strong>{{user.email}}</strong> to change your password.
                                                </v-card-text>
                                                <v-card-actions>
                                                    <v-spacer></v-spacer>
                                                    <v-btn text="Close" variant="plain" @click="changePasswordDialog = false"></v-btn>
                                                </v-card-actions>
                                            </v-card>
                                        </v-dialog>                                        
                                        <br><br><br><br><br><br><br><br>
                                        <v-dialog v-model="deleteDialog" max-width="500" style="font-family: Poppins;">
                                            <template v-slot:activator="{ props: activatorProps }">
                                                <v-btn color="red" v-bind="activatorProps" stacked variant="tonal" style="width:100%;border: 1px solid black;">
                                                <span class="material-symbols-outlined" style="color: black;">
                                                    delete_forever
                                                </span>
                                                <span style="color: black;">Delete Account</span>
                                            </v-btn>
                                            </template>
                                            <!--Pop up -->
                                            <v-card title="Delete Account">
                                                <v-card-text>
                                                    Are you sure you would like to delete your account? This cannot be undone.
                                                </v-card-text>
                                                <v-card-actions>
                                                    <v-spacer></v-spacer>
                                                    <v-btn text="Cancel" variant="plain" @click="deleteDialog = false"></v-btn>
                                                    <v-btn color="red" text="Delete" variant="tonal" @click="deleteAccount"></v-btn>
                                                </v-card-actions>
                                            </v-card>
                                        </v-dialog>                                        
                                    </v-card-text>
                                </v-card>
                                <br>
                            </v-col>
                        </v-row>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div> 
<div v-else>
<v-container fluid fill-height>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6">
        <img src="../assets/course compass logo.png" alt="Course Compass Logo" class="mx-auto d-block" style="width: 225px; height:auto;">
        <br>
        <h1 class="text-center" style="font-family: Coolvetica;">You are unauthorized to view this page.</h1>
        <p class="text-center">
            <br>
            Redirect back to <router-link to="/" >Home</router-link> page.
        </p>
      </v-col>
    </v-row>
  </v-container>
</div>
</template>
<script>
    import axios from 'axios';
    
    export default {
        props:{
            userType:{
                type: String,
                required: '',
            }
        },
        data() {
            return {
                user: {
                    firstname: '',
                    lastname: '',
                    email: '',
                    dob: '',
                    major: '',
                    profilePicture: require('../assets/profile-picture.jpg'),
                    role: '',
                },
                editData: {
                    firstName: '',
                    lastName: '',
                    selectedMajor: '',
                },
                dialog: false,
                changePasswordDialog: false,
                deleteDialog: false,
                majors: [],
                error: null,
                loading: false,
            };
        },
        watch: {
            dialog(newVal) {
                if (newVal) {
                    this.editData.firstName = this.user.firstname;
                    this.editData.lastName = this.user.lastname;
                    this.editData.selectedMajor = this.user.major;
                }
            },
        },
        created() {
            this.fetchUserInfo();
        },
        mounted() {
            axios.get('http://127.0.0.1:5000/majors')
                .then(response => {
                    this.majors = response.data.majors;
                })
                .catch(error => {
                    console.error("Failed to fetch majors:", error);
                });
        },
        methods: {
            fetchUserInfo() {
                this.loading = true;
                axios.get('http://127.0.0.1:5000/myaccount', { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }})
                .then(response => {
                    this.user.firstname = response.data.Fname;
                    this.user.lastname = response.data.Lname;
                    this.user.email = response.data.Email;
                    this.user.dob = response.data.DOB;
                    this.user.major = response.data.majorName;
                    this.user.role = response.data.role;
                    console.log('My Account page loaded successfully', response.data);
                    this.loading = false;
                })
                .catch(error => {
                    console.error("Error loading My Account page", error);
                    this.loading = false;
                });        
            },
            updateProfile() {
                const updatedInfo = {
                    firstname: this.editData.firstName,
                    lastname: this.editData.lastName,
                };
                if (this.user.role !== 'Instructor') {
                    updatedInfo.majorID = this.editData.selectedMajor
                }
                axios.post('http://127.0.0.1:5000/editprofile', updatedInfo, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }})
                .then(response => {
                    this.fetchUserInfo(); 
                    this.dialog = false;  
                    console.log('Profile updated successfully');
                })
                .catch(error => {
                    console.error("Error updating profile", error);
                });
            },
            navigateToChangePassword() {
                this.$router.push('/changepassword');
            },
            deleteAccount() {
                if (confirm("Are you sure you would like to delete your account? This cannot be undone.")) {
                    axios.delete('http://127.0.0.1:5000/delete-account', { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }})
                    .then(response => {
                        console.log("Account deleted.");
                        axios.post('http://127.0.0.1:5000/logout', {}, { withCredentials: true })
                            .then(response => {
                                console.log(response.data.message);
                                if (response.status === 200) {
                                    setTimeout(() => {
                                        this.$emit('logout');
                                        this.$router.push('/');
                                    }, 1000);
                                } else {
                                    console.error("Unexpected response during logout: ", response);
                                }
                            })
                            .catch(error => {
                                console.error("Logout error: ", error);
                            });
                        })
                        .catch(error => {
                            console.error("Error deleting account", error);
                        });
                }
            },
            sendEmail(){
                const newDate = new Date().toLocaleDateString('en-US', {
                    month: 'long',
                    day: 'numeric',
                    year: 'numeric',
                });

                const email = {
                    date: newDate,
                    subject: 'Course Compass - Password Change',
                    to: this.user.email, 
                    content: 'You have requested to change your password.\nPlease click the following link to change your password: http://localhost:8080/changepassword',
                };

                axios.post('http://127.0.0.1:5000/send-email', email)
                .then(response => {
                    console.log("Email sent successfully");
                })
                .catch(error => {
                    console.error("Failed to send email: ", error);
                });
            },
        },

    }
</script>

<style scoped>
    h2 {
        text-align: left;
        font-family:coolvetica;
    }

    p{
        font-family: Poppins;
    }

    .settings-container {
        background-color: #ffffff;
        margin: 3% auto;
        padding: 20px;
        width: 70%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 0 px rgba(232, 0, 0, 0.1);
    }
    
    .col{
        border-left: 1px solid #000000;
        border-bottom: 1px solid black;
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

    .account-button {
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

    .loading-container {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 343px;
    }

    .buttons-container{
        border: 1px solid black;
        height: 450px;
        font-family: Poppins;
    }
</style>