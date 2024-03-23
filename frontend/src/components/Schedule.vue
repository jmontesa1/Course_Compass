<!--Created by: John Montesa-->
<!-- This is the Schedule page for Course Compass -->
<!-- This page will show the scheudle of the specific user in a time table/ time block style -->

<template>
    <v-row no-gutters>
        <v-col cols="2">
        <v-tabs v-model="tab" direction="vertical" color="primary" selected-class="selected-tab" slider-color="black">
            <v-tab value="class-schedule" @click="chooseClassSchedule">
                <v-icon start>
                    <span class="material-icons" style="color:black">calendar_view_day</span>
                </v-icon>
                Weekly Schedule
            </v-tab>

            <v-tab value="calendar" @click="chooseCalendar()">
                <v-icon start>
                    <span class="material-icons" style="color:black">calendar_month</span>
                </v-icon>
                Calendar
            </v-tab>
        </v-tabs>
        </v-col>

        <v-col>
            <div class="right-side1" v-if="classSchedule">
                <div class="header-container">
                    <div class="row justify-content-center">
                        <div class="col d-flex flex-column">
                            <h1>                            
                                <select>
                                    <option v-for="schedule in userSchedules" :key="schedule" :value="userschedule" >{{ schedule }}</option>
                                </select>
                            </h1>
                        </div>

                        <button class="print-btn" @click="downloadPDF">
                            <img class ="printer" src="../assets/printer.png" alt="Print Button">
                        </button>

                        <v-dialog v-model="dialog" max-width="500" style="font-family: Poppins;">
                            <template v-slot:activator="{ props: activatorProps }">
                                <v-btn class="add-schedule" v-bind="activatorProps">Add A Schedule</v-btn>
                            </template>
                            <!--Pop up -->
                            <v-card title="Add a weekly schedule">
                                <v-card-text>
                                    <v-row dense>
                                        <v-col>  
                                            <v-text-field v-model="scheduleTitle" label="Schedule Title" required></v-text-field>
                                            <v-select v-model="scheduleOption" :items="scheduleOptions" label="Week" required></v-select>
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn text="Close" variant="plain" @click="dialog = false"></v-btn>
                                    <v-btn color="primary" text="Add" variant="tonal" @click="newSchedule()"></v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </div>
                </div>

                <div id="schedule-page" ref="schedulePage" >
                    <div class="container-fluid mt-3" v-if="weekdays">
                        <div class="schedule-days">
                            <!-- This is the very top of the schedule, showing the days -->
                            <div class="row">
                                <div class="col-sm-1"></div>
                                <div v-for="day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']" :key="day" class="col d-flex flex-column">
                                    {{ day }}
                                </div>
                            </div>

                            <!-- This is the rest of the schedule, showing the time and blocks of courses -->
                            <div class="row">
                                <!-- This is the time on the left side -->
                                <div class="col-sm-1">
                                        <div class="time-slot" v-for="time in ['8', '9', '10', '11', '12', '1', '2', '3', '4', '5', '6', 
                                        '7']" :key="time">
                                            <div class="time-slot-hour"><h2> {{ time }} </h2></div> <!-- height of each row-->
                                            <div class="time-slot-bar"></div> <!-- bars for time -->
                                        </div>
                                </div>


                                <div v-for="day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']" :key="day" class="col">
                                            <div class="time-slot" v-for="time in ['8', '9', '10', '11', '12', '1', '2', '3', '4', '5', '6', '7']" :key="time">
                                                <div class="day-slot-hour"></div> <!-- height of each row-->
                                                <div class="day-slot-bar"></div> <!-- bars for time -->
                                                <template v-if="time === '8' && day === 'Monday' || time === '8' && day === 'Tuesday'
                                                        || time === '8' && day === 'Wednesday' || time === '8' && day === 'Thursday'
                                                        || time === '8' && day === 'Friday'">
                                                    <div v-for="classBlock in generateBlocks(day)" :key="classBlock.id" :style="classBlock.style">
                                                        <div class="class-info">
                                                            {{ classBlock.classes.map(item => item.course).join(', ') }}
                                                            <br>
                                                            {{ classBlock.classes[0].time }}
                                                            <br>
                                                            {{ classBlock.classes[0].location }}
                                                        </div>
                                                    </div>
                                                </template>
                                            </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="container-fluid mt-3" v-if="!weekdays">
                        <div class="schedule-days">
                            <!-- This is the very top of the schedule, showing the days -->
                            <div class="row">
                                <div class="col-sm-1"></div>
                                <div v-for="day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']" :key="day" class="col d-flex flex-column">
                                    {{ day }}
                                </div>
                            </div>
                            <!-- This is the rest of the schedule, showing the time and blocks of courses -->
                            <div class="row">
                                <!-- This is the time on the left side -->
                                <div class="col-sm-1">
                                    <div class="time-slot" v-for="time in ['8', '9', '10', '11', '12', '1', '2', '3', '4', '5', '6', 
                                    '7']" :key="time">
                                        <div class="time-slot-hour"><h2> {{ time }} </h2></div> <!-- height of each row-->
                                        <div class="time-slot-bar"></div> <!-- bars for time -->
                                    </div>
                                </div>

                                <div v-for="day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']" :key="day" class="col">
                                    <div class="time-slot" v-for="time in ['8', '9', '10', '11', '12', '1', '2', '3', '4', '5', '6', '7']" :key="time">
                                        <div class="day-slot-hour"></div> <!-- height of each row-->
                                        <div class="day-slot-bar"></div> <!-- bars for time -->
                                        <template v-if="time === '8' && day === 'Monday' || time === '8' && day === 'Tuesday'
                                                || time === '8' && day === 'Wednesday' || time === '8' && day === 'Thursday'
                                                || time === '8' && day === 'Friday'">
                                        </template>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            <br>
            </div>

            <div class="right-side2" v-if="calendar">
                <v-dialog v-model="dialog" max-width="1000" style="font-family: Poppins;">
                    <template v-slot:activator="{ props: activatorProps }">
                        <v-btn class="add-event" v-bind="activatorProps">Add an event</v-btn>
                    </template>
                    <!--Pop up -->
                    <v-card title="Enter event details">
                        <v-card-text>
                        <v-row dense>
                            <v-col cols = "12" md="6">  
                                <v-text-field v-model="eventTitle" label="Event Title" required></v-text-field>
                                <v-select v-model="eventColor" :items="this.colors" label="Color" required></v-select>
                                <v-textarea v-model="eventDescription" label="Event Description" single-line rows="8"></v-textarea>
                                <v-checkbox v-model="allDay" label="Is this event all day?" hint="All day events are blue and square."></v-checkbox>
                            </v-col>
                            <v-col cols="12" md="6">
                                <v-date-picker v-model="eventDate" width="100%"></v-date-picker>
                            </v-col>
                        </v-row>

                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn text="Close" variant="plain" @click="dialog = false"></v-btn>
                            <v-btn color="primary" text="Add" variant="tonal" @click="newEvent()"></v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
                    
                <v-row class="fill-height">
                    <v-col>
                        <v-sheet class="calendar-container">
                            <v-calendar
                            ref="calendar"
                            v-model="today"
                            color="primary"
                            type="month"
                            :events="events"
                            @click:day="(event)=>dateClick(event,true)"
                            ></v-calendar>
                        </v-sheet>
                    </v-col>
                </v-row>
                <br>
            </div>
        </v-col>
    </v-row>
</template>

<script>
    import html2pdf from 'html2pdf.js';
    import axios from 'axios';
    import { useDate } from 'vuetify';
    import { ref } from 'vue';

    export default {
        data:() => ({
            
                tab: 'class-schedule',
                classSchedule: true,
                calendar: false,

                //schedule options
                scheduleTitle: '',
                scheduleOption: 'Weekdays',
                weekdays: true,
                scheduleOptions: ['Weekdays', 'Weekdays and Weekends'],

                user: {
                    firstname: '',
                    lastname: '',
                    major: '',
                },

                schedules: [
                    {option: 'weekdays', title: 'Hi', events:[]}
                ],
                userSchedules:["Class Schedule"],

                schedule: [
/*                      { course: 'CS 135', days: ['Monday','Wednesday','Friday'], time: '10:00 AM - 10:50 AM', start: '10:00 AM', end: '10:50 AM', location: 'SEM 104' },
                    { course: 'CS 425', days: ['Tuesday','Thursday'], time: '10:30 AM - 11:45 AM', start: '10:30 AM', end: '11:45 AM', location: 'WPEB 101' },
                    { course: 'CS 302', days: ['Monday', 'Wednesday'], time: '3:00 PM - 4:15 PM', start: '3:00 PM', end: '4:15 PM', location: 'PSAC 1002' },
                    { course: 'ENG 101', days: ['Monday', 'Wednesday', 'Friday'], time: '6:00 PM - 6:50 PM', start: '6:00 PM', end: '6:50 PM', location: 'MKIC 320' },
                    { course: 'EE 165', days: ['Monday', 'Wednesday', 'Friday'], time: '8:30 AM - 9:45 AM', start: '8:30 AM', end: '9:45 AM', location: 'SLC 102' },
                    { course: 'MUS 123', days: ['Tuesday', 'Thursday'], time: '5:00 PM - 6:50 PM', start: '5:00 PM', end: '6:30 PM', location: 'CFA 102' },
                 */],

                //Every data that involves calendar under this
                today: ref(new Date()),
                focus: '',
                events: [],
                colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey'],
                dialog: false,
                eventTitle: '',
                eventColor: 'blue',
                eventDescription: '',
                allDay: false,
                eventDate: new Date(),

                }),

        mounted() {
            this.fetchUserInfo();
            this.fetchUserSchedule();
            
            const adapter = useDate()
            this.fetchEvents({ start: adapter.startOfDay(adapter.startOfMonth(new Date())), end: adapter.endOfDay(adapter.endOfMonth(new Date())) })
            },

        methods: {
            dateClick(event, Boolean) {
                console.log('Clicked day:', event);
            },
            chooseClassSchedule(){
                this.tab = 'class-schedule';
                this.calendar = false;
                this.classSchedule = true;
            },

            chooseCalendar(){
                this.tab = 'calendar';
                this.classSchedule = false;
                this.calendar = true;
            },

            async downloadPDF() {
                await this.$nextTick();
                const content = this.$refs.schedulePage;

                const pdfSettings = {
                    margin: 1,
                    filename: 'schedule.pdf',
                    image: { type: 'jpeg', quality: 0.98 },
                    html2canvas: { scale: 3 },
                    jsPDF: { unit: 'mm', format: 'a4', orientation: 'landscape' },
                };

                html2pdf().from(content).set(pdfSettings).save();
            },

            async fetchUserInfo() {
                try {
                    const response = await axios.get('http://127.0.0.1:5000/myaccount', {headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }});
                    console.log(response.data.message);
                    if (response.data) {
                        this.user.firstname = response.data.Fname;
                        this.user.lastname = response.data.Lname;
                        this.user.major = response.data.majorName;
                    }
                } catch (error) {
                    console.error("Error fetching info: ", error);
                    this.error = error.response ? error.response.data.error : "Unknown error";
                }
            },

            async fetchUserSchedule() {
                try {
                    const response = await axios.get('http://127.0.0.1:5000/getUserSchedule', {
                        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                    });
                    if (response.data && response.data.user_schedule) {
                        //replace with this.schedule to load, BUT IT DOESNT LOAD YET
                        this.schedule = response.data.user_schedule.map(item => {
                            const daysArray = item.meetingDays.split(',').map(day => day.trim()); //split meeting days string into separate arrays
                            return {
                                course: item.courseCode,
                                days: daysArray, 
                                time: `${item.meetingTimes}`, 
                                start: item.startTime, 
                                end: item.endTime,  
                                location: item.Location,
                                term: item.Term,
                            };
                        });
                    }
                } catch (error) {
                    console.error("Error fetching schedule: ", error.message);
                }
            },

    
            //This is for the class Schedule
            generateBlocks(day) {
                const blocks = [];
                const colors = ['#F1948A', '#AED6F1', '#A3E4D7', '#F9E79F', '#BB8FCE', '#F8C471', '#AEB6BF', '#FADBD8'];

                this.schedule.forEach((course, index) => {
                    if (course.days.includes(day)) {
                        //choose color for colors list, first course gets first course and so on
                        let color;
                        for (let i = 0; i < colors.length; i++) {
                            if (index === 0) {
                                color = colors[0];
                                break;
                            } else {
                                color = colors[(index - 1 + i) % (colors.length - 1) + 1];
                                break;
                            }
                        }
                        const startHour = parseInt(course.start.split(':')[0]); //hours
                        const startMinute = parseInt(course.start.split(':')[1]); //minutes
                        const endHour = parseInt(course.end.split(':')[0]); //hours
                        const endMinute = parseInt(course.end.split(':')[1]); //minutes

                        const blockHeight = ((endHour - startHour) * 60 + (endMinute - startMinute));

                        let yTransformation;


                        if(startHour === 8){
                            yTransformation = 2;
                        }
                        else if(startHour === 9){
                            yTransformation = 58;
                        }
                        else if(startHour === 10){
                            yTransformation = 113;
                        }
                        else if(startHour === 11){
                            yTransformation = 169;
                        }
                        else if(startHour === 12){
                            yTransformation = 224;
                        }
                        else if(startHour === 1){
                            yTransformation = 280;
                        }
                        else if(startHour === 2){
                            yTransformation = 335;
                        }
                        else if(startHour === 3){
                            yTransformation = 391;
                        }
                        else if(startHour === 4){
                            yTransformation = 446;
                        }
                        else if(startHour === 5){
                            yTransformation = 502;
                        }
                        else if(startHour === 6){
                            yTransformation = 558;
                        }
                        else if(startHour === 7){
                            yTransformation = 613;
                        }
                        
                        if(startMinute === 30){
                                yTransformation += 27;
                            }

                        blocks.push({
                            id: course.course + day,
                            style: { 
                                'background-color': color,
                                'border-radius': '8px',
                                'height': `${blockHeight}px`,
                                'width': '100%',
                                'transform': `translateY(${yTransformation}px)`,
                                'position': 'absolute',
                                'top': `0`,
                                'z-index': '1',
                            },
                            classes: [course],
                        });
                    }
                });
                return blocks;
            },


            //Any method under this are for the schedule
            newSchedule(){
                
            },

            //Any method under this are for the calendar
            getEventColor (event) {
                return event.color
            },
            newEvent(){
                const newEvent = {
                    title: this.eventTitle,
                    description: this.eventDescription,
                    start: this.eventDate, 
                    end: this.eventDate,
                    color: this.eventColor,
                    allDay: this.allDay,
                };
                this.events.push(newEvent);
                this.fetchEvents(newEvent);
                this.dialog = false;
            },

            fetchEvents (newEvent) {
                this.events.push();
            },

        },
    };
</script>

<style scoped>
    .body {
        overflow-x: hidden;
    }
    .header-container{
        margin-bottom: -10px;
    }

    h1 {
        white-space: nowrap;
        text-align: left;
        font-family: Poppins;
        font-size: 30px;
        margin-top: 2px;
        margin-bottom: -6px;
        margin-left: 16px;
    }

    .schedule-days { /* outer part of the schedule*/
        font-family: Poppins;
        font-size: 20px;
        text-align: center;
        padding: 10px;
        border: 1px solid #d3d3d3; 
    }

    .col {
        padding: 10px;
    }

    .print-btn {
        border: transparent;
        background: transparent;
        cursor: pointer;
        float: right;
        margin-top: 5px;
        margin-right: 15px;
        width: 35px;
        height: auto;
        transform: translateX(-75%);
    }

    .printer{
        width: 35px;
        height: auto;
    }

    .time-slot {
        position: relative;
    }

    h2{
        position: static;
        text-align: left;
        font-family: Poppins;
        font-size: 23px;
        transform: translateY(-12%);
        margin-top: 2px;
        margin-bottom: -6px;
    }
    
    .time-slot-hour {
        padding-bottom: 32px; /*Height of the time slot box */
    }

    .time-slot-bar {
        position: absolute;
        max-width: 90px; /*time slot black bar*/
        top: 20%;
        left: 30%; /*time slot black bar*/
        right: 0;
        height: 1px;
        background-color: #d3d3d3;
    }

    .day-slot-bar {
        position: absolute;
        max-width: 500px; /*time slot black bar*/
        top: 4%;
        left: 0; /*time slot black bar*/
        right: 0;
        height: 1px;
        background-color: #00000036;
        z-index: 0;
    }

    .day-slot-hour {
        padding-bottom: 55.5px; /*Height of the day slot box */
    }

    .class-info {
        font-size: 16px;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: #000000;
        line-height: 1;
        position: relative;
        overflow: hidden;
        white-space: nowrap; 
        top: 50%; /* The last three make the text in the middle of the block*/
        left: 50%;
        transform: translate(-50%, -50%);
    }

    @media (max-width: 768px) {
        .class-info {
            font-size: 12px; 
        }
    }

    .right-side1{
        border-left: 1px solid black;
    }

    .right-side2{
        border-left: 1px solid black;
    }

    .calendar-container{
        margin-left: 10px;
        margin-right: 10px;
        font-family: Poppins;
    }

    .v-tab{
        font-family: Poppins;
    }

    select {
        width: 40%;
        height: 45px;
        margin-bottom: 5px;
        box-sizing: border-box;
        border: 1px solid rgba(0, 0, 0, 0.089);
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="%23000000"><path d="M1 5h14L8 12z"/></svg>');
        background-position: right 10px center;
        background-size: 15px;
        cursor: pointer;
        padding-left: 8px;
    }

    .add-event{
        position: absolute;
        right: 10px;
        top: 165px;
        font-family: Poppins;
        color: white;
        background-color: black;
        box-shadow: none;
    }

    .add-schedule{
        width: 150px;
        margin-top: 17px;
        margin-right: 25px;
        font-family: Poppins;
        color: rgb(255, 255, 255);
        background-color: rgb(0, 0, 0);
        box-shadow: none;
    }

    .selected-tab{
        background-color: rgb(224, 224, 224);
    }
</style>