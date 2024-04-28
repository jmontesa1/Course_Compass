<!-- Created by: John Montesa -->
<!-- This component creates the navigation bar that the user will interact with -->
<!-- There are 5 buttons, and one is a drop down menu that directs the user to log in, sign up, or check their profile settings-->

<template>
    <v-banner v-if="isBannerVisible" color="grey-darken-1" lines="two">
        <div class="loading" v-if="upcomingNotification === null">
            <v-progress-linear color="white" indeterminate :height="5" rounded></v-progress-linear>
        </div>
        <template v-slot:prepend>
            <span class="material-icons" style="color:white; margin-top:5px;">notifications</span>
        </template>
        <v-banner-text class="notification-text" v-if="upcomingNotification">
            <b> {{ upcomingNotification.announceDate }} </b> {{ upcomingNotification.source }} - {{ upcomingNotification.message }}
        </v-banner-text>

        <v-banner-actions class="notification-actions">
            <v-btn class ="notification-button" @click="dismissBanner">
                <span class="material-icons" style="color:white">close</span>
            </v-btn>
        </v-banner-actions>
    </v-banner>

    <!--<div v-if="$route.path === '/admin-dashboard'">
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                <router-link to="/" class="navbar-brand">
                    <img src="../assets/course compass logo.png" alt="Course Compass Logo">
                </router-link>
            </div>
        </nav>
    </div>-->

    <div v-if="isLoggedIn">
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                    <router-link to="/" class="navbar-brand">
                        <img src="../assets/course compass logo.png" alt="Course Compass Logo">
                    </router-link>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                        <!-- right-aligned menu items -->
                        <li class="nav-item" @click="dashboardRefresh">
                            <a class="nav-link" style="cursor:pointer;">{{this.userType}} Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <router-link to="/courses" class = "nav-link">Courses</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/schedule" class = "nav-link">Schedule</router-link>
                        </li>
                        <li class="nav-item" v-if="this.userType === 'Student'">
                            <router-link to="/progress" class = "nav-link">Progress</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/about" class = "nav-link">About</router-link>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                Account
                            </a>
                            <ul class="dropdown-menu">
                                <li>
                                <router-link to="/myaccount" class = "dropdown-item">My Account</router-link></li>
                                <li><a href="#" class="dropdown-item" @click.prevent="handleLogout">Log Out</a></li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </div>
    

    <!--NAV BAR WHEN LOGGED OUT-->
    <div v-else>
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                    <router-link to="/" class="navbar-brand">
                        <img src="../assets/course compass logonav.png" alt="Course Compass Logo">
                    </router-link>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <router-link to="/about" class = "nav-link">About</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/login" class = "nav-link">Log In</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/signup" class = "nav-link">Sign Up</router-link>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </div>
</template>

<script>
    import axios from 'axios';

    export default{

        props:{
            isLoggedIn: {
                type: Boolean,
                required: true, //login
            },

            userType:{
                type: String,
                required: '',
            }
        },
        data(){
            return{
                isBannerVisible: true,
                upcomingNotification: null,
            };
        },

        /*computed:{
             upcomingNotification(){
                //this.currentDate = new Date('2024-03-03'); //USE THIS AS A TEST CASE TO CHECK DIFFERENT DAYS, THIS SHOWS IT WORKS WHEN A DAY PASSES FOR A NOTIF
                this.currentDate = new Date(); //get current day
                const upcomingNotifications = this.notifications.filter(notification => new Date(notification.date) > this.currentDate).sort((a, b) => new Date(a.date) - new Date(b.date));
                return upcomingNotifications.length > 0 ? upcomingNotifications[0] : null;
            }, 
        },*/

        created() {
            this.fetchNotifications();
        },

        methods:{
            fetchNotifications() {
                axios.get('http://localhost:5000/notifications')
                    .then(response => { 
                    if (response.status === 200) {
                        this.upcomingNotification = response.data;
                    } else {
                        console.error('Failed to fetch notifications:', response.status);
                    }
                    })
                    .catch(error => {
                    console.error('Error fetching notifications:', error);
                    });
            },


            dashboardRefresh() {
                if (this.$route.path === '/dashboard' && this.userType === 'Student') {
                    this.$router.go();
                } else if(this.userType === 'Student'){
                    this.$router.push('/dashboard');
                }

                if (this.$route.path === '/instructor-dashboard' && this.userType === 'Instructor') {
                    this.$router.go();
                } else if(this.userType === 'Instructor'){
                    this.$router.push('/instructor-dashboard');
                }

                if (this.$route.path === '/admin-dashboard' && this.userType === 'Admin') {
                    this.$router.go();
                } else if(this.userType === 'Admin'){
                    this.$router.push('/admin-dashboard');
                }

            },

            dismissBanner(){
                this.isBannerVisible = false;
            },
            
            handleLogout() {
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
            },

            formatDate(dateString) {
                const options = { year: 'numeric', month: 'long', day: 'numeric' };
                return new Date(dateString).toLocaleDateString(undefined, options);
            },

            /*checkLoginStatus() {
                axios.get('http://127.0.0.1:5000/check_login', { withCredentials: true })
                    .then(response => {
                        if (response.status === 200) {
                            this.isLoggedIn = response.data.logged_in;
                            console.log('User is logged in');
                        } else if (response.status === 401) {
                            this.isLoggedIn = false;
                            console.log('User is not logged in');
                        }
                    })
                    .catch(error => {
                        console.error("Check login error: ", error);
                    });
                },*/
        },

    };
</script>

<style scoped>
    .navbar {
        background-color: #ffffff; 
        border-bottom: 1px solid #000000;
    }

    .navbar-brand img {
        max-width: 74px;
        height: auto;
        margin: -8px auto;
    }

    .nav-link {
        font-family: 'coolvetica';            
        font-size: 25px;
        color: #160e0e;
        margin-right: 10px;
    }


    .nav-link:hover {
        color: #ffffff;
        background-color: #000000;
    }

    .dropdown-menu {
        font-family: 'coolvetica';
        background-color: #ffffff00;
        border: 1px solid transparent;
        text-align: center;
        font-size: 15px;
        min-width: 130px;
    }

    .dropdown-item {
        color: #000000;
        border: 1px solid #000000;
        text-align: center;
        background-color: #ffffff;
    }

    .dropdown-item:hover {
        color: #ffffff;
        background-color: #000000;
    }

    .v-banner{
        margin-top: -5px; 
        margin-bottom: -20px;
        background-color: rgb(53, 53, 53);
    }

    .notification-actions{
        margin-left: auto;
    }

    .notification-button:hover{
        background-color:rgb(157, 157, 157);
    }

    .notification-text{
        font-family: Poppins;
        color: rgb(185, 185, 185);
        margin-top: 6px;
    }

    .notification-button{
        transform: translate(-15px, -22px);
    }

    .loading{
        position: absolute;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 88%;
        margin-bottom: 12px;
    }
</style>