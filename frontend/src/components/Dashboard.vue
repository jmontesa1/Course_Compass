<!--Created by: John Montesa-->
<!-- This is dashboard page for Course Compass -->
<!-- This page will contain brief information -->

<template>
    <v-row v-if="user && user.firstname">
        <h1 class="welcome-text">
            <v-avatar size="50" >
                <v-img :src="user.avatar" alt="User profile picture"></v-img>
            </v-avatar>
            Welcome, {{ user.firstname }}
        </h1>
    </v-row>

    <v-container class="dashboard-container">
        <v-row>
            <v-col>
                <p>Today: {{ currentDate }}</p>
                <v-container class="upcoming-container">
                    <p>Classes Today:</p>

                    <v-container class="class-block">
                        <v-row class="class-rows" no-gutters v-for="(course, index) in retrieveSchedule" :key="index">
                            <v-col class="class-block-left" cols="2">
                                <v-sheet class="pa-2 ma-2">
                                    {{ course.course }}
                                </v-sheet>
                            </v-col>
                            <v-col class="class-block-right">
                                <v-sheet class="pa-2 ma-2">
                                    {{ course.time }} - {{ course.location }}
                                </v-sheet>
                            </v-col>
                        </v-row>
                    </v-container>

                    <p>Classes Tomorrow:</p>
                        <v-container class="class-block">
                            <v-row class="class-rows" no-gutters v-for="(course, index) in retrieveScheduleTomorrow" :key="index">
                                <v-col class="class-block-left" cols="2">
                                    <v-sheet class="pa-2 ma-2">
                                        {{ course.course }}
                                    </v-sheet>
                                </v-col>
                                <v-col class="class-block-right">
                                    <v-sheet class="pa-2 ma-2">
                                        {{ course.time }} - {{ course.location }}
                                    </v-sheet>
                                </v-col>
                            </v-row>
                        </v-container>
                </v-container>
            </v-col>

            <v-col cols="3">
                <br>
                <v-container class="deadlines-container">
                    <p>Deadlines:</p>
                    <v-expansion-panels>
                        <v-expansion-panel class="deadline-title" v-for="(notification, i) in upcomingNotifications" :key="i" :title="`${notification.source} - ${notification.date}`" :text="notification.message">
                        </v-expansion-panel>
                    </v-expansion-panels>

                </v-container>
            </v-col>
        </v-row>


    </v-container>

    <v-container class="dashboard-container2">
        <v-row>
            <h1 class="header-text">Enrolled Courses</h1>
        </v-row>

        <v-row>
            <v-card class="enrolled-cards" v-for="(course, index) in schedule" :key="index" :title="course.course" :subtitle="course.location">
                <v-card-text>
                    {{ formatDays(course.days) }}<br>
                    {{ course.time }}
                </v-card-text>
                <v-card-actions>
                    <v-dialog v-model="dialog[index]" max-width="500" style="font-family: Poppins;">
                        <template v-slot:activator="{ props: activatorProps }">
                            <v-btn v-bind="activatorProps">View Details</v-btn>
                        </template>
                        <!--Pop up -->
                        <v-card title="Course Details">
                            <v-card-text>
                                <v-row dense>
                                    <v-col cols = "12" md="6">
                                        Add information
                                    </v-col>
                                </v-row>
                            </v-card-text> 

                            <v-card-actions>
                                <v-btn text="Close" variant="plain" @click="dialog[index] = false"></v-btn>
                                <v-spacer></v-spacer>
                                <v-btn color="dark-grey" text="Unenroll" variant="tonal" @click="enrollCourses()"></v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-card-actions>
            </v-card>
        </v-row>
        <br>
    </v-container>

    <!--<v-container class="dashboard-container3">
        <v-row>
            <h1 class="header-text">Major Progress</h1>
        </v-row>
        <br>
        <br>
        <br>
        <br>
    </v-container>-->

</template>

<script>
    import axios from 'axios';
    
    export default {
        data() {
            return {
                dialog: [],
                currentDate: null,
                user: {
                    firstname: '',
                    lastname: '',
                    dob: '',
                    major: '',
                    term: 'Spring 2024',
                    avatar: require('@/assets/profile-picture.jpg'),
                },

                schedule: [
                    { course: 'CS 135', days: ['Monday','Wednesday','Friday'], time: '10:00 AM - 10:50 AM', start: '10:00 AM', end: '10:50 AM', location: 'SEM 104' },
                    { course: 'CS 425', days: ['Tuesday','Thursday'], time: '10:30 AM - 11:45 AM', start: '10:30 AM', end: '11:45 AM', location: 'WPEB 101' },
                    { course: 'CS 302', days: ['Monday', 'Wednesday'], time: '3:00 PM - 4:15 PM', start: '3:00 PM', end: '4:15 PM', location: 'PSAC 1002' },
                    { course: 'ENG 101', days: ['Monday', 'Wednesday', 'Friday'], time: '6:00 PM - 6:50 PM', start: '6:00 PM', end: '6:50 PM', location: 'MKIC 320' },
                    { course: 'EE 165', days: ['Monday', 'Wednesday', 'Friday'], time: '8:30 AM - 9:45 AM', start: '8:30 AM', end: '9:45 AM', location: 'SLC 102' },
                    { course: 'MUS 123', days: ['Tuesday', 'Thursday', 'Friday'], time: '1:00 PM - 1:50 PM', start: '1:00 PM', end: '1:50 PM', location: 'CFA 102' },
                ],

                notifications: [
                    {date: '5/15/2024', source: 'UNR', message: 'Instruction Ends'},
                    {date: '3/1/2024', source: 'UNR', message: 'Deadline to apply for May graduation'},
                    {date: '3/25/2024', source: 'Professor Mike', message: 'Hello Students, hw 1 is due in the next few weeks, and there is an exam tomorrow about coffee.'},
                    {date: '3/1/2024', source: 'UNR', message: 'Deadline to apply for May graduation'},
                    {date: '3/18/2024', source: 'UNR', message: 'Summer Session registration starts'},
                    {date: '3/19/2024', source: 'UNR', message: 'Final fee payment due for those on a payment plan'},
                    {date: '3/23/2024', source: 'UNR', message: 'Spring Break (campus open; no classes)'},
                    {date: '4/1/2024', source: 'UNR', message: 'Fall semester enrollment begins'},
                    {date: '4/2/2024', source: 'UNR', message: 'No dropping of individual classes after this deadline'},
                    {date: '5/8/2024', source: 'UNR', message: 'Prep Day'},
                    {date: '5/9/2024', source: 'UNR', message: 'Finals week begins'},
                    {date: '5/15/2024', source: 'UNR', message: 'Instruction Ends'},
                    {date: '5/16/2024', source: 'UNR', message: 'On-campus residence hall move-out (11 a.m.)'},
                    {date: '5/16/2024', source: 'UNR', message: 'Commencement'},
                    {date: '5/20/2024', source: 'UNR', message: 'Faculty to post final grades in MyNEVADA by 5 p.m.'},
                    {date: '5/20/2024', source: 'UNR', message: 'Spring semester ends, last day faculty on campus for spring semester'},
                ],
            };
        },
        methods: {
            formatDays(days){
                return days.map(day => day.slice(0,3)).join('');
            },

            fetchDashboardData() {
                axios.get('http://127.0.0.1:5000/dashboard', { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }})
                .then(response => {
                    this.user.firstname = response.data.Fname;
                    this.user.lastname = response.data.Lname;
                    this.user.major = response.data.majorName;
                    this.user.dob = response.data.DOB;
                    console.log('Dashboard loaded successfully', response.data);
                })
                .catch(error => {
                    console.error("Error fetching dashboard data", error);
                });
            },
            goToDashboard() {
                this.$router.push('/dashboard')
            }
        },
        beforeRouteUpdate(to, from, next) {
            if (to.path === '/dashboard') {
                this.fetchDashboardData();
            }
            next();
        },

        
        computed:{
            currentDate(){
                const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
                this.currentDate = new Date().toLocaleDateString('en-US', options);
                return this.currentDate;
            },
               
            upcomingNotifications() {
                const currentDate = new Date();
                //const currentDate = new Date('2024-03-03'); test case
                const upcomingNotifications = this.notifications
                    .filter(notification => new Date(notification.date) > currentDate)
                    .sort((a, b) => new Date(a.date) - new Date(b.date));
                return upcomingNotifications.length > 0 ? upcomingNotifications : null;
            },

            //retrieves todays and tomorrows classes
            retrieveSchedule(){
                const currentDayIndex = new Date().getDay();
                const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
                const currentDay = daysOfWeek[currentDayIndex];

                return this.schedule.filter(course => {
                    const courseDay = course.days.includes(currentDay);
                    return courseDay;
                }).sort((a, b) => {
                    const getTime = time => {
                        const [hours, minutes] = time.split(':').map(Number);
                        const paddedHours = hours.toString().padStart(2, '0');
                        return parseInt(`${paddedHours}${minutes}`, 10);
                    };

                    const timeComparison = getTime(a.start) - getTime(b.start);

                    if (a.start.includes('AM') && b.start.includes('PM')) {
                        return -1;
                    } else if (a.start.includes('PM') && b.start.includes('AM')) {
                        return 1;
                    }
                    return timeComparison;
                });
            },

            retrieveScheduleTomorrow(){
                const tomorrow = new Date();
                tomorrow.setDate(tomorrow.getDate() + 1); //Tomorrow

                const nextDayIndex = tomorrow.getDay();
                const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
                const nextDay = daysOfWeek[nextDayIndex];


                return this.schedule.filter(course => {
                    const courseDay = course.days.includes(nextDay);
                    return courseDay;
                }).sort((a, b) => {
                    const getTime = time => {
                        const [hours, minutes] = time.split(':').map(Number);
                        const paddedHours = hours.toString().padStart(2, '0');
                        return parseInt(`${paddedHours}${minutes}`, 10);
                    };

                    const timeComparison = getTime(a.start) - getTime(b.start);

                    if (a.start.includes('AM') && b.start.includes('PM')) {
                        return -1;
                    } else if (a.start.includes('PM') && b.start.includes('AM')) {
                        return 1;
                    }
                    return timeComparison;
                });
            },
        },

        mounted(){
            this.dialog = new Array(this.schedule.length).fill(false);

            if (!localStorage.getItem('access_token')) {
                this.$router.push('/login');
            } else {
                this.fetchDashboardData();
            }
        },
    }
</script>

<style scoped>
    p{
        font-family: Poppins;
        font-size: 15px;
        margin: 0px;
    }

    .class-rows{
        margin-bottom: 14px;
    }
    .class-block{
        position: relative;
    }

    .class-block-left{
        border-top: 1px solid black;
        border-right: 1px solid black;
        border-bottom: 1px solid black;
    }

    .class-block-right{
        border-top: 1px solid black;
    }

    .welcome-text{
        font-family: coolvetica;
        position: relative;
        left: 3%;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .dashboard-container{
        margin: 10px auto;
        position: relative;
        max-width: 90%;
        border-radius: 1px;
        border-top: 1px solid black;
        border-left: 1px solid black;
    }

    .dashboard-container2{
        margin: 10px auto;
        position: relative;
        max-width: 90%;
        border-radius: 1px;
        border-top: 1px solid black;
        border-right: 1px solid black;
    }

    .dashboard-container3{
        margin: 10px auto;
        position: relative;
        max-width: 90%;
        border-radius: 1px;
        border-top: 1px solid black;
        border-left: 1px solid black;
    }

    .deadlines-container{
        margin-left: -15px;
        max-height: 500px;
        overflow-y: auto;
    }

    .deadline-title {
        font-family: Poppins;
        display: inline-block;
    }

    .header-text{
        font-family: Coolvetica;
        font-size: 25px;
    }

    .enrolled-cards{
        margin-right: 6px;
        font-family: Poppins;
        background-color: rgb(236, 236, 236);

    }
</style>