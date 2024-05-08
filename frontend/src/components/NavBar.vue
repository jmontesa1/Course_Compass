<!-- Created by: John Montesa -->
<!-- This component creates the navigation bar that the user will interact with -->
<!-- There are different buttons based on user type or if they are logged in -->
<!-- Redirects users to the various different pages -->
<!-- Contains the dynamic notifciation bar at the top the changes based on days as well. -->

<template>
    <v-banner v-if="isBannerVisible" color="grey-darken-1" lines="two">
        <!-- Loading animation when gathering announcements -->
        <div class="loading" v-if="notifications.length === 0">
            <v-progress-linear color="white" indeterminate :height="5" rounded></v-progress-linear>
        </div>
        <template v-slot:prepend>
            <span class="material-icons" style="color:white; margin-top:5px;">notifications</span>
        </template>
        <v-banner-text class="notification-text" v-if="notifications.length > 0">
            <b> {{ formatDate(notifications[currentNotificationIndex].announceDate) }} </b> {{ notifications[currentNotificationIndex].source }} - {{ notifications[currentNotificationIndex].message }}
        </v-banner-text>

        <!-- Close announcement bar at the top of page -->
        <v-banner-actions class="notification-actions">
            <v-btn class ="notification-button" @click="dismissBanner">
                <span class="material-icons" style="color:white">close</span>
            </v-btn>
        </v-banner-actions>
    </v-banner>

    <!-- Navigation bar if logged in -->
    <div v-if="isLoggedIn">
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                    <!-- Logo -->
                    <router-link to="/" class="navbar-brand">
                        <img src="../assets/course compass logo.png" alt="Course Compass Logo">
                    </router-link>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                        <!-- right-aligned menu items, each item redirects depending on page and user type -->
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
        emits: ['logout'],
        data(){
            return{
                isBannerVisible: true,
                notifications: [],
                currentNotificationIndex: 0,
                notificationDisplayInterval: null,
                upcomingNotificatins: null,
            };
        },

        created() {
            this.fetchNotifications();
        },

        methods:{
            //get notifications from DB
            fetchNotifications() {
                axios.get('http://127.0.0.1:5000/active-notifications', { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }})
                .then(response => { 
                    if (response.status === 200 && response.data.length > 0) {
                        this.notifications = response.data;
                        this.setUpNotificationRotation();
                    } else {
                        console.error('No active notifications');
                        this.isBannerVisible = false; 
                    }
                })
                .catch(error => {
                    console.error('Error fetching notifications:', error);
                    this.isBannerVisible = false; 
                });
            },

            //Rotates notifications every ten seconds
            setUpNotificationRotation() {
                if(this.notifications.length > 1) {
                    this.notificationDisplayInterval = setInterval(() => {
                        this.currentNotificationIndex = (this.currentNotificationIndex + 1) % this.notifications.length;
                        this.upcomingNotification = this.notifications[this.currentNotificationIndex];
                    }, 10000); 
                }
            },

            //change dashboard routing based on user type
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

            //remove announcement bar
            dismissBanner(){
                this.isBannerVisible = false;
                clearInterval(this.notificationDisplayInterval);
            },
            
            //logout users
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

            //reformat date for announcements
            formatDate(dateString) {
                const options = { year: 'numeric', month: 'long', day: 'numeric' };
                const date = new Date(dateString);
                date.setDate(date.getDate() + 1);
                return date.toLocaleDateString(undefined, options);
            },
        },

        beforeDestroy() {
            if (this.notificationDisplayInterval) {
                clearInterval(this.notificationDisplayInterval);
            }
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
        margin-bottom: -41px;
    }
</style>