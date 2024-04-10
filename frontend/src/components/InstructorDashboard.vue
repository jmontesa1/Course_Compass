<!--Created by: John Montesa-->
<!-- This is dashboard page for Course Compass -->
<!-- This page will contain brief information -->

<template>
    <br>
    <div class="top-container">
        <v-row v-if="user && user.firstname">
            <h1 class="welcome-text">
                <v-avatar size="37" >
                    <v-img :src="user.avatar" alt="User profile picture"></v-img>
                </v-avatar>
                Welcome, {{ user.firstname }}
            </h1>
        </v-row>
    </div>

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
                        <p v-if="retrieveSchedule.length === 0">No classes scheduled for today!</p>
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
                            <p v-if="retrieveScheduleTomorrow.length === 0">No classes scheduled for tomorrow!</p>
                        </v-container>
                </v-container>
            </v-col>

            <v-col cols="3">
                <br>
                <v-container class="deadlines-container">
                    <p>Deadlines:</p>
                    <v-expansion-panels>
                        <v-expansion-panel class="deadline-title" v-for="(notification, index) in upcomingNotifications" :key="index" :title="`${notification.date} - ${notification.source}`" :text="notification.message" :class="{'upcoming': index === 0}">
                        </v-expansion-panel>
                    </v-expansion-panels>

                </v-container>
            </v-col>
        </v-row>
    </v-container>

    <v-container class="dashboard-container2">
        <div class="inner-container">
            <v-row>
                <h1 class="header-text">Announcements</h1>
            </v-row>
            <v-row>
                <v-expansion-panels>
                    <v-expansion-panel>
                        <v-expansion-panel-title>
                            <v-row no-gutters>
                                <v-col class="d-flex justify-start">
                                    <p>Your active announcements ({{instructorNotifications.length}})</p>
                                </v-col>
                            </v-row>
                        </v-expansion-panel-title>
                        <v-expansion-panel-text>
                            <v-row  no-gutters v-for="(notification, index) in instructorNotifications" :key="index">
                                <v-col cols="11">
                                    <p class="row-text"><strong>{{instructorNotifications[index].date}}</strong> {{instructorNotifications[index].source}} - {{instructorNotifications[index].description}}</p>
                                    <br><p>Sent to: {{instructorNotifications[index].courses}}</p>
                                </v-col>
                                <v-col cols="1">
                                    <v-dialog v-model="removeNotificationDialog[index]" max-width="800" style="font-family: Poppins;">
                                        <template v-slot:activator="{ props: activatorProps }">
                                            <v-btn v-bind="activatorProps" icon="$close" variant="plain">
                                                <span class="material-symbols-outlined">
                                                delete
                                                </span>
                                            </v-btn>
                                        </template>
                                        <!--Pop up -->
                                        <v-card title="Are you sure you want to remove announcement:">
                                            <v-card-text>
                                                <br>
                                                <p><strong>{{instructorNotifications[index].date}}</strong> {{instructorNotifications[index].source}} - {{instructorNotifications[index].description}}</p>
                                                <br><p>Sent to: {{instructorNotifications[index].courses}}</p>
                                            </v-card-text> 
                                            <v-card-actions>
                                                <v-spacer></v-spacer>
                                                <v-btn text="No" variant="plain" @click="removeNotificationDialog[index] = false"></v-btn>
                                                <v-btn color="primary" text="Yes" variant="tonal" @click="removeNotification(index)"></v-btn>
                                            </v-card-actions>
                                        </v-card>
                                    </v-dialog> 
                                </v-col>
                                <v-divider class="instructor-divider"></v-divider>
                            </v-row>
                        </v-expansion-panel-text>
                    </v-expansion-panel>
                </v-expansion-panels>
            </v-row>

            <v-row>
                <v-col cols="10">
                </v-col>
                <v-col cols="2" class="d-flex justify-end align-center">
                    <v-dialog v-model="notificationDialog" max-width="1000" style="font-family: Poppins;">
                        <template v-slot:activator="{ props: activatorProps }">
                            <v-btn  v-bind="activatorProps" class="announcement-btn" variant="outlined" @click="handleLogout">
                                <p>Send announcement</p>
                            </v-btn>
                        </template>
                        <!--Pop up -->
                        <v-card title="Send An Announcement">
                            <v-card-text>
                                <v-row dense>
                                    <v-col cols = "12" md="6">  
                                        <br>
                                        <p>Choose courses to send to:</p>
                                        <div class="checkboxes-container">
                                            <v-checkbox v-for="(course, index) in schedule" :key="index" :label="course.course" v-model="chosenCourses[index]" style="margin-bottom: -35px;"></v-checkbox>
                                        </div>
                                        <br>
                                        <v-textarea v-model="notificationDescription" label="Announcement Description" single-line rows="7"></v-textarea>
                                        <br>
                                        <v-checkbox v-model="notificationDeadline" label="Add announcement to your dashboard" hint="This announcement will appear under your deadlines."></v-checkbox>
                                    </v-col>
                                    <v-col cols="12" md="6">
                                        <v-date-picker v-model="notificationDate" width="100%"></v-date-picker>
                                    </v-col>
                                </v-row>
                            </v-card-text> 
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn text="Close" variant="plain" @click="notificationDialog = false"></v-btn>
                                <v-btn color="primary" text="Send" variant="tonal" @click="sendNotification()"></v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>

                </v-col>
            </v-row>
        </div>
    </v-container>



    <v-container class="dashboard-container3">
        <div class="inner-container">
        <v-row>
            <h1 class="header-text">Courses Taught</h1>
        </v-row>

        <p v-if="schedule.length === 0"><br>No courses taught, please visit the <a href="../courses">Courses</a> page to add courses!</p>

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
                                        <strong>Course Name: </strong> {{ course.courseName }}<br>
                                        <strong>Instructor: </strong> {{ course.instructor }}<br>
                                        <strong>Credits: </strong> {{ course.Credits }}<br>
                                        <strong>Section: </strong> {{ course.Section }}<br>
                                    </v-col>
                                </v-row>
                            </v-card-text> 

                            <v-card-actions>
                                <v-btn text="Close" variant="plain" @click="dialog[index] = false"></v-btn>
                                <v-spacer></v-spacer>
                                <v-btn color="dark-grey" text="Unenroll" variant="tonal" @click="confirmUnenrollment(course.scheduleID, index)"></v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-card-actions>
            </v-card>
        </v-row>
        <br>
        <v-dialog v-model="showUnenrollDialog" max-width="500" style="font-family: Poppins;">
            <v-card>
                <v-card-title class="headline">Confirm Unenrollment</v-card-title>
                <v-card-text>Are you sure you want to unenroll from this course?</v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="dark-grey" variant="tonal" text @click="showUnenrollDialog = false">Cancel</v-btn>
                    <v-btn color="primary" variant="tonal" text @click="unenrollCourse">Confirm</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        </div>
    </v-container>
</template>

<script>
    import axios from 'axios';
    
    export default {
        data() {
            return {
                unenrollScheduleID: null,
                currentDate: null,
                user: {
                    firstname: '',
                    lastname: '',
                    dob: '',
                    major: '',
                    term: 'Spring 2024',
                    avatar: require('@/assets/profile-picture.jpg'),
                },

                showUnenrollDialog: false,
                dialog: [],
                notificationDialog: false,
                removeNotificationDialog: [],

                schedule: [],

                //send announcement vars under
                source: "Instructor",
                chosenCourses: [],
                notificationDate: new Date(),
                notificationDeadline: false,
                notificationDescription: '',

                instructorNotifications:[],
                notifications: [
                    {date: '5/15/2024', source: 'UNR', message: 'Instruction Ends'},
                    {date: '4/25/2024', source: 'Professor Mike', message: 'Hello Students, hw 1 is due in the next few weeks, and there is an exam tomorrow about coffee.'},
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
            },

            async fetchEnrolledCourses() {
                try {
                    const response = await axios.get('http://127.0.0.1:5000/getEnrolledCourses', {
                        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                    });
                    this.schedule = response.data.enrolledCourses.map(course => ({
                        ...course,
                        scheduleID: course.scheduleID
                    }));
                } catch (error) {
                    console.error("Error fetching enrolled courses:", error);
                }
            },

            async unenrollCourse() {
                try {
                    const response = await axios.post('http://127.0.0.1:5000/unenrollCourse', {
                        scheduleID: this.unenrollScheduleID
                    }, {
                        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                    });

                    if (response.status === 200) {
                        this.schedule = this.schedule.filter(course => course.scheduleID !== this.unenrollScheduleID);
                        console.log('Course unenrolled successfully');
                        this.showUnenrollDialog = false;
                        this.$emit('show-toast', { message: 'Course unenrolled.', color: '#51da6e' });
                    }
                } catch (error) {
                    console.error("Error unenrolling course:", error);
                }
            },


            confirmUnenrollment(scheduleID, index) {
                this.unenrollScheduleID = scheduleID;
                this.showUnenrollDialog = true;
                this.dialog[index] = false;
            },

            sendNotification(){
                //Month Date, Year
                const reformatDate = new Date(this.notificationDate).toLocaleDateString('en-US', {
                    month: 'long',
                    day: 'numeric',
                    year: 'numeric',
                });

                //Month/Date/Year
                const reformatDate2 = new Date(this.notificationDate).toLocaleDateString('en-US', {
                    month: 'numeric',
                    day: 'numeric',
                    year: 'numeric',
                });
                const selectedCourses = this.schedule.filter((course, index) => this.chosenCourses[index]);
                const reformatCourses = selectedCourses.map(course => course.course).join(', ');

                const notification = {
                    date: reformatDate,
                    source: this.source + ' ' + this.user.firstname + ' ' + this.user.lastname,
                    description: this.notificationDescription,
                    courses: reformatCourses,
                    deadline: this.notificationDeadline,
                };

                if(this.notificationDeadline === true){
                    const notification2 = {
                        date: reformatDate2,
                        source: this.source + ' ' + this.user.firstname + ' ' + this.user.lastname,
                        message: this.notificationDescription,
                    }

                    this.notifications.push(notification2);
                }

                this.instructorNotifications.push(notification);

                this.notificationDate = new Date();
                this.notificationDescription ='';
                this.chosenCourses = [];
                this.notificationDeadline = false;
                this.notificationDialog = false;
            },

            removeNotification(index){
                const removedNotification = this.instructorNotifications[index];
                this.instructorNotifications.splice(index, 1);
                
                //find notification under deadlines
                const deadlineNotification = this.notifications.findIndex(notification =>
                    notification.date === removedNotification.date &&
                    notification.message === removedNotification.description);

                this.notifications.splice(deadlineNotification, 1);
                this.removeNotificationDialog[index] = false;
            },
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
                    return course.days.some(day => day.trim() === currentDay);
                }).sort((a, b) => {
                    const getTime = time => {
                        const [hours, minutes] = time.split(' - ')[0].split(':').map(Number);
                        const paddedHours = hours.toString().padStart(2, '0');
                        return parseInt(`${paddedHours}${minutes}`, 10);
                    };

                    const timeComparison = getTime(a.time) - getTime(b.time);

                    if (a.time.includes('AM') && b.time.includes('PM')) {
                        return -1;
                    } else if (a.time.includes('PM') && b.time.includes('AM')) {
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
                    return course.days.some(day => day.trim() === nextDay);
                }).sort((a, b) => {
                    const getTime = time => {
                        const [hours, minutes] = time.split(' - ')[0].split(':').map(Number);
                        const paddedHours = hours.toString().padStart(2, '0');
                        return parseInt(`${paddedHours}${minutes}`, 10);
                    };

                    const timeComparison = getTime(a.time) - getTime(b.time);

                    if (a.time.includes('AM') && b.time.includes('PM')) {
                        return -1;
                    } else if (a.time.includes('PM') && b.time.includes('AM')) {
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
                this.fetchEnrolledCourses(); //enrolled courses data
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
        margin-top: 14px;
        margin-bottom: 10px;
        font-size: 32px;
        left:1.5%;
    }

    .top-container{
        top: -1.7px;
        margin: 10px auto;
        position: relative;
        max-width: 90%;
        border-radius: 1px;
        border-top: 1px solid black;
        border-left: 1px solid black;
        border-right: 1px solid black;
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

    .upcoming{
        font-weight: bold;
        background-color: rgba(255, 0, 0, 0.168);
    }

    .announcement-btn{
        left: 11px;
        font-size: 0px;
        min-width: 170px;
    }

    .inner-container {
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 96%;
        margin: 0 auto;
    }

    .v-date-picker{
        margin-top: -29px;
        margin-bottom: -38px;
    }

    .checkboxes-container {
        display: flex;
        flex-wrap: wrap;
    }

</style>