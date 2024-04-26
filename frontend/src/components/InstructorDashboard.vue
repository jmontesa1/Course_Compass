<!--Created by: John Montesa-->
<!-- This is dashboard page for Course Compass -->
<!-- This page will contain brief information -->

<template>
    <br>
    <div class="top-container">
        <v-row v-if="user && user.firstname">
            <h1 class="welcome-text">
                <!--<v-avatar size="37" >
                    <v-img :src="user.avatar" alt="User profile picture"></v-img>
                </v-avatar>-->
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
                            <v-col class="class-block-left2" cols="2" :class="{'class-block-left': index === 0}">
                                <v-sheet class="pa-2 ma-2">
                                    {{ course.course }}
                                </v-sheet>
                            </v-col>
                            <v-col class="class-block-right2" :class="{'class-block-right': index === 0}">
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
                                <v-col class="class-block-left2" cols="2" :class="{'class-block-left': index === 0}">
                                    <v-sheet class="pa-2 ma-2">
                                        {{ course.course }}
                                    </v-sheet>
                                </v-col>
                                <v-col class="class-block-right2" :class="{'class-block-right': index === 0}">
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
                    <v-row style="padding-bottom: 15px;">
                        <p style="margin-top: 3px;">Deadlines:</p>
                        <v-spacer></v-spacer>
                        <v-dialog v-model="dialogNotifications" max-width="420" style="font-family: Poppins;">
                            <template v-slot:activator="{ props: activatorProps }">
                                <v-btn size="extra-small" v-bind="activatorProps" variant="plain" style="position: relative;">
                                    <span class="material-symbols-outlined" v-if="notificationsActive === false">
                                        notifications_off
                                    </span>
                                    <span class="material-symbols-outlined" v-if="notificationsActive === true">
                                        notifications_active
                                    </span>
                                </v-btn>
                            </template>
                            <!--Pop up -->
                            <v-card title="Notification Center">
                                <v-card-text>
                                    <v-row>
                                        <v-col cols="auto">
                                            <v-switch
                                                v-model="notificationsActive"
                                                color="primary"
                                                label="Turn on email notifications"
                                                style="margin-top: -10px; margin-bottom: -35px; color: black;"
                                            ></v-switch>
                                        </v-col>
                                    </v-row>
                                    <v-row v-if="notificationsActive === true">
                                        <v-col cols="auto">
                                            <p>Remind me <strong style="color: red">{{daysBeforeNotification}}</strong> days before a deadline.<br><span style="font-size: 12px; color: gray;">(Sent to <em>{{user.email}}</em>)</span></p>
                                        </v-col>
                                        <v-col cols="1">
                                            <v-btn :disabled="daysBeforeNotification === 1" size="extra-small" v-bind="activatorProps" variant="plain" style="position: relative;" @click="daysBeforeNotification--">
                                                <span class="material-symbols-outlined">
                                                    remove
                                                </span>
                                            </v-btn>
                                        </v-col>
                                        <v-col cols="1">
                                            <v-btn :disabled="daysBeforeNotification === 7" size="extra-small" v-bind="activatorProps" variant="plain" style="position: relative;" @click="daysBeforeNotification++">
                                                <span class="material-symbols-outlined">
                                                    add
                                                </span>
                                            </v-btn>
                                        </v-col>
                                    </v-row>
                                    <v-row v-if="notificationsActive === true">
                                        <v-col cols="auto">
                                            <p>Select your notification sources:</p>
                                        </v-col>
                                    </v-row>
                                    <v-row v-if="notificationsActive === true" style="margin-top: -10px; margin-bottom: -55px;">
                                        <v-col cols="6">
                                            <v-checkbox v-model="selectedNotificationSources" label="UNR" value="UNR"></v-checkbox>
                                        </v-col>
                                        <v-col cols="6">
                                            <v-checkbox v-model="selectedNotificationSources" label="Instructors" value="Instructor"></v-checkbox>
                                        </v-col>
                                    </v-row>
                                    <v-row v-if="notificationsActive === true" style="margin-top: -20px; margin-bottom: -55px;">
                                        <v-col cols="6">
                                            <v-checkbox v-model="selectedNotificationSources" label="Admins" value="Admin"></v-checkbox>
                                        </v-col>
                                        <v-col cols="6">
                                            <v-checkbox v-model="selectedNotificationSources" label="User Deadlines" :value="user.firstname + ' ' + user.lastname"></v-checkbox>
                                        </v-col>
                                    </v-row>
                                </v-card-text> 
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn text="Close" variant="plain" @click="dialogNotifications = false"></v-btn>
                                    <v-btn color="primary" text="Save" variant="tonal" @click="turnOnEmailNotifications()"></v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog> 
                    </v-row>
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
                                    <p><strong>{{instructorNotifications[index].date}}</strong> {{instructorNotifications[index].source}} - {{instructorNotifications[index].description}}</p>
                                    <br><p>Sent to: {{instructorNotifications[index].courses}}</p>
                                </v-col>
                                <v-col cols="1">
                                    <v-dialog v-model="deleteNotificationDialog[index]" max-width="800" style="font-family: Poppins;">
                                        <template v-slot:activator="{ props: activatorProps }">
                                            <v-btn v-bind="activatorProps" icon="$close" variant="plain">
                                                <span class="material-symbols-outlined">
                                                delete
                                                </span>
                                            </v-btn>
                                        </template>
                                        <!--Pop up -->
                                        <v-card title="Are you sure you want to delete announcement:">
                                            <v-card-text>
                                                <br>
                                                <p><strong>{{instructorNotifications[index].date}}</strong> {{instructorNotifications[index].source}} - {{instructorNotifications[index].description}}</p>
                                                <br><p>Sent to: {{instructorNotifications[index].courses}}</p>
                                            </v-card-text> 
                                            <v-card-actions>
                                                <v-spacer></v-spacer>
                                                <v-btn text="Cancel" variant="plain" @click="deleteNotificationDialog[index] = false"></v-btn>
                                                <v-btn color="red" text="Delete" variant="tonal" @click="deleteNotification(index)"></v-btn>
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
                            <v-btn  v-bind="activatorProps" class="announcement-btn" variant="outlined">
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
                            <v-btn color="dark-grey" variant="tonal" v-bind="activatorProps">View Details</v-btn>
                        </template>
                        <!--Pop up -->
                        <v-card title="Course Details">
                            <v-card-text>
                                <v-row dense>
                                    <v-col cols="auto">
                                        <strong>Course Name: </strong> {{ course.courseName }}<br>
                                        <strong>Instructor: </strong> {{ course.instructor }}<br>
                                        <strong>Credits: </strong> {{ course.Credits }}<br>
                                        <strong>Section: </strong> {{ course.Section }}<br>
                                        <strong>Office Hours: </strong> {{ course.officeHours }}<br>
                                        <strong>Office Hours Location: </strong> {{ course.officeLocation }}<br>
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

                <v-card-actions>
                    <v-dialog v-model="officeHoursDialog[index]" max-width="700" style="font-family: Poppins;">
                        <template v-slot:activator="{ props: activatorProps }">
                            <v-btn variant="outlined" v-bind="activatorProps">Office Hours</v-btn>
                        </template>
                        <!--Pop up -->
                        <v-card title="Adjust Office Hours">
                            <v-card-text>
                                <v-row dense>
                                    <v-col cols="auto">
                                        Current Office Hours: 11:00 AM - 12:15 PM, Mon We Fr, SEM 314
                                    </v-col>
                                </v-row>
                                <br>
                                <v-row dense>
                                    <v-col auto>
                                            <v-text-field v-model="officeHoursStart" type="time" :rules="[timeValidation]" label="Start Time"></v-text-field>
                                    </v-col>
                                    <v-col auto>
                                            <v-text-field v-model="officeHoursEnd" type="time" :rules="[timeValidation]" label="End Time"></v-text-field>
                                    </v-col>
                                    <v-col auto>
                                            <v-text-field v-model="officeHoursLocation" label="Location"></v-text-field>
                                    </v-col>
                                </v-row>

                                <v-row dense>
                                    <p>Choose which days to change to:</p>
                                    <div class="checkboxes-container">
                                        <v-checkbox v-for="(day, index) in daysOfWeek.slice(1,6)" :key="index" :label="daysOfWeek[index + 1]" v-model="chosenOfficeHoursDays[index]" style="margin-bottom: -35px;"></v-checkbox>
                                    </div>
                                </v-row>
                            </v-card-text> 
                            <v-card-actions>
                                <v-btn text="Close" variant="plain" @click="officeHoursDialog[index] = false"></v-btn>
                                <v-spacer></v-spacer>
                                <v-btn color="dark-grey" text="Change" variant="tonal" @click="confirmOfficeHours(course.scheduleID, index)" :disabled="!timeValid"></v-btn>
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

        <v-dialog v-model="officeHoursConfirmDialog" max-width="500" style="font-family: Poppins;">
            <v-card>
                <v-card-title class="headline">Confirm Office Hours Changes</v-card-title>
                <v-card-text>Are you sure you want to change Office Hours details?</v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="dark-grey" variant="tonal" text @click="officeHoursConfirmDialog = false">Cancel</v-btn>
                    <v-btn color="primary" variant="tonal" text @click="changeOfficeHours">Confirm</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        </div>
    </v-container>

    <v-container class="dashboard-container4">
        <div class="inner-container">
        <v-row>
            <h1 class="header-text">Recent Student Reviews</h1>
        </v-row>
        <p v-if="courseReviews.length === 0"><br>No recent student reviews</p>
            <v-card  style="height: 620px; overflow-y: auto;">
                <v-list lines="auto" style="font-family: Poppins;">
                    <div v-for="(course,indexTitle) in courseReviews" :key="indexTitle">
                        <v-list-item v-for="(review,index) in courseReviews[indexTitle].reviews" :key="index">
                            <template v-slot:title>
                                {{courseReviews[indexTitle].course}} - {{courseReviews[indexTitle].reviews[index].date}}
                            </template>
                            <template v-slot:subtitle>
                                <strong>Anonymous</strong> &mdash; {{courseReviews[indexTitle].reviews[index].text}}
                            </template>
                            <v-divider></v-divider>
                        </v-list-item>
                    </div>
                </v-list>
            </v-card>
        </div>
    </v-container>
</template>

<script>
    import axios from 'axios';
    
    export default {
        data() {
            return {
                daysOfWeek: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],

                unenrollScheduleID: null,
                currentDate: null,
                user: {
                    firstname: '',
                    lastname: '',
                    dob: '',
                    major: '',
                    term: 'Spring 2024',
                    avatar: require('@/assets/profile-picture.jpg'),
                    email: '',
                },

                showUnenrollDialog: false,
                officeHoursDialog: [],
                officeHoursConfirmDialog: false,
                dialog: [],
                notificationDialog: false,
                deleteNotificationDialog: [],

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
                    {date: '4/26/2024', source: 'Professor Mike', message: 'Hello Students, hw 1 is due in the next few weeks, and there is an exam tomorrow about coffee.'},
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

                emailNotifications:[],

                //Office Hours
                officeHoursStart: '',
                officeHoursEnd: '',
                timeValid: false,
                officeHoursLocation: '',
                chosenOfficeHoursDays: [],

                //notifications on/off
                notificationsActive: false,
                dialogNotifications: false,
                daysBeforeNotification: 1,
                selectedNotificationSources: [],

                //student reviews
                courseReviews: [
                    {course: 'MATH 182',
                        reviews: [
                            { text: 'The course material was outdated and not helpful.', date: 'Jan 12th, 2016' },
                            { text: 'The lectures were confusing and poorly structured.', date: 'Feb 23rd, 2015' },
                            { text: 'Didn\'t find the course engaging or informative.', date: 'Aug 7th, 2023' },
                            { text: 'The content was too basic and not worth the price.', date: 'May 15th, 2018' },
                            { text: 'I expected more from the course but was disappointed.', date: 'Apr 29th, 2024' }
                        ],
                    },

                    {course: 'ENG 100',
                        reviews: [
                            { text: 'Great course content, very informative!', date: 'Apr 9th, 2017' },
                            { text: 'Enjoyed the interactive lessons and quizzes.', date: 'Jan 4th, 2022' },
                            { text: 'Highly recommend for anyone new to the subject.', date: 'Jul 18th, 2019' },
                            { text: 'Excellent instructors, clear explanations.', date: 'Oct 25th, 2016' },
                            { text: 'Practical exercises were really helpful.', date: 'Mar 8th, 2020' }
                        ],
                    },
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
                    this.user.email = response.data.Email;
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

            confirmOfficeHours(scheduleID, index) {
                //this.unenrollScheduleID = scheduleID;
                this.officeHoursConfirmDialog = true;
                this.officeHoursDialog[index] = false;
            },

            changeOfficeHours(){
                //NEEDS IMPLEMENTATION TO CHANGE OFFICE HOURS FROM

                this.officeHoursStart = '';
                this.officeHoursEnd = '';
                this.officeHoursLocation = '';
                this.chosenOfficeHoursDays = [];
                this.officeHoursConfirmDialog = false;
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
                    source: this.source,
                    description: this.user.firstname + ' ' + this.user.lastname + ' - ' + this.notificationDescription,
                    courses: reformatCourses,
                    deadline: this.notificationDeadline,
                };

                if(this.notificationDeadline === true){
                    const notification2 = {
                        date: reformatDate2,
                        source: this.source,
                        message: this.user.firstname + ' ' + this.user.lastname + ' - ' + this.notificationDescription,
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

            deleteNotification(index){
                const deletedNotification = this.instructorNotifications[index];
                this.instructorNotifications.splice(index, 1);
                
                //find notification under deadlines
                const deadlineNotification = this.notifications.findIndex(notification =>
                    notification.date === deletedNotification.date &&
                    notification.message === deletedNotification.description);

                this.notifications.splice(deadlineNotification, 1);
                this.deleteNotificationDialog[index] = false;
            },
            turnOnEmailNotifications(){
                const currentDate = new Date();
                const grabNotifications = JSON.parse(JSON.stringify(this.notifications));//copy this.notifcations

                let filteredNotifications = grabNotifications.filter(notification => {
                    const notificationDate = new Date(notification.date);

                    const isSelectedSource = this.selectedNotificationSources.includes(notification.source);

                    const isFutureDate = notificationDate > currentDate;

                    const sendNotificationDate = new Date(notificationDate);
                    sendNotificationDate.setDate(sendNotificationDate.getDate() - this.daysBeforeNotification);

                    notification.date = sendNotificationDate.toISOString().split('T')[0];

                    return isSelectedSource && isFutureDate;
                });

                filteredNotifications.sort((a, b) => new Date(a.date) - new Date(b.date)); //filter by date

                this.emailNotifications = filteredNotifications;
                this.daysBeforeNotification = 1;
                this.dialogNotifications = false;
                console.log('Filtered Notifications', filteredNotifications);                
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
                const currentDay = this.daysOfWeek[currentDayIndex];

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
                const nextDay = this.daysOfWeek[nextDayIndex];

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

            timeValidation() {
                return () => {
                const startTime = this.officeHoursStart;
                const endTime = this.officeHoursEnd;
                
                const validOrder = startTime < endTime;

                this.timeValid = validOrder;

                if (!validOrder) {
                    return "Start time must be before end time";
                }

                return this.timeValid || "Invalid times";
                };
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

    .class-block-left2{
        border-right: 1px solid black;
        border-bottom: 1px solid black;
    }

    .class-block-right{
        border-top: 1px solid black;
        position: relative;
        top: 1px;
    }

    .class-block-right2{
        margin-top: -1px;
        border-top: 1px solid black;
    }

    .welcome-text{
        font-family: coolvetica;
        position: relative;
        margin-top: 16px;
        margin-left: 10px;
        font-size: 32px;
        left:1%;
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

    .dashboard-container4{
        margin: 10px auto;
        position: relative;
        max-width: 90%;
        border-radius: 1px;
        border-top: 1px solid black;
        border-right: 1px solid black;
    }

    .deadlines-container{
        max-height: 500px;
        overflow-y: auto;
        overflow-x: hidden;
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