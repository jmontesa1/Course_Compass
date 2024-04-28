<!--Created by: John Montesa-->
<!-- This is the Account page for Course Compass -->

<template>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/spinkit/1.2.5/spinkit.min.css">
    </head>
    <div class="settings-container">
        <div class="loading-container" v-if="loading">
            <!-- loading anim -->
            <v-progress-circular indeterminate :width="5"></v-progress-circular>
        </div>
        <div class="container-fluid mt-3" v-else>
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
                        <p v-if="user.role == 'Instructor'" style="font-size: 20px;"><strong><i>Instructor</i></strong></p>
                        <p><strong>First Name:</strong> {{ user.firstname }}</p>
                        <p><strong>Last Name:</strong> {{ user.lastname }}</p>
                        <p><strong>Email:</strong> {{ user.email }}</p>
                        <p><strong>Birthdate:</strong> {{ user.dob }}</p>
                        <p v-if="user.role !== 'Instructor'"><strong>Major:</strong> {{ user.major }}</p>
                        <v-dialog v-model="dialog" max-width="500" style="font-family: Poppins;">
                            <template v-slot:activator="{ props: activatorProps }">
                                <btn class="account-button" v-bind="activatorProps">Edit Profile</btn>
                            </template>
                            <!--Pop up -->
                            <v-card title="Edit Profile Information">
                                <v-card-text>
                                    <v-form>
                                        <v-text-field v-model="editData.firstName" label="First Name"></v-text-field>
                                        <v-text-field v-model="editData.lastName" label="Last Name"></v-text-field>
                                        <!--<v-select v-model="editData.major" :items="majorOptions" label="Major"></v-select> -->
                                        <v-select v-if="user.role !== 'Instructor'" v-model="editData.selectedMajor" :items="majors" item-text="major" item-value="majorID" label="Select your major" return-object required>
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

                        <btn class="account-button" @click="navigateToChangePassword">Change Password</btn>
                        <btn class="account-button" @click="deleteAccount">Delete Account</btn>
                    </div>
                </div>

                <!--<div class="col-md-2 d-flex flex-column">
                    <br>
                    <br>
                    <img class="profile-picture" :src="user.profilePicture" alt="Profile Picture">
                    <p style="text-align:center;"><i>Profile Picture</i></p>
                    <br>
                </div>-->

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
                    role: '',
                },
                editData: {
                    firstName: '',
                    lastName: '',
                    selectedMajor: '',
                },
                dialog: false,
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
        width: 70%;
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

    button:hover {
        background-color: #555555;
    }

    .loading-container {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 343px;
    }
</style>