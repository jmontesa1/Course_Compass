<!--Created by: John Montesa-->
<!-- This is the Schedule page for Course Compass -->
<!-- This page will show the scheudle of the specific user in a time table/ time block style -->

<template>
<div v-if="userType !== ''">
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
                                <v-row>                            
                                    <!--<select v-model="selectedScheduleTitle" @change="handleScheduleChange">
                                        <option v-for="schedule in userSchedules" :key="schedule.title" :value="schedule.title">{{ schedule.title }}</option>
                                    </select>-->
                                    <v-col cols="9">
                                        <v-select
                                            v-model="selectedScheduleTitle"
                                            :items="userSchedules"
                                            item-value="title"
                                            item-text="customText"
                                            label="Select Schedule"
                                            variant="outlined"
                                            style="margin-bottom: -125px;"
                                            >
                                            <template #prepend-inner>
                                                <span class="material-symbols-outlined">calendar_today</span>
                                            </template>
                                        </v-select>
                                    </v-col>
                                    <v-dialog v-model="dialog" max-width="500" style="font-family: Poppins;">
                                        <template v-slot:activator="{ props: activatorProps }">
                                            <v-btn class="add-schedule" size="small" v-bind="activatorProps" style="max-width: 41px; height:41px; margin-top:18px;">
                                                <span class="material-symbols-outlined" style="font-size: 41px;">calendar_add_on</span>
                                            </v-btn>
                                        </template>
                                        <!--Pop up -->
                                        <v-card title="Add a weekly schedule">
                                            <v-card-text>
                                                <v-row dense>
                                                    <v-col>  
                                                        <v-text-field v-model="scheduleTitle" label="Schedule Title" required></v-text-field>
                                                        <v-select v-model="newScheduleOption" :items="scheduleOptions" label="Week" required></v-select>
                                                    </v-col>
                                                </v-row>
                                            </v-card-text>
                                            <v-card-actions>
                                                <v-spacer></v-spacer>
                                                <v-btn text="Close" variant="plain" @click="dialog = false"></v-btn>
                                                <v-btn color="primary" text="Add" variant="tonal" @click="createCustomSchedule">ADD</v-btn>
                                            </v-card-actions>
                                        </v-card>
                                    </v-dialog>

                                    <v-dialog v-model="dialog_delete_schedule" max-width="500" style="font-family: Poppins;" v-if="scheduleOption === 'Weekdays and Weekends' || scheduleOption === 'Weekdays'">
                                        <template v-slot:activator="{ props: activatorProps }">
                                            <v-btn class="add-schedule" size="small"  v-bind="activatorProps" style="max-width: 41px; height:41px; margin-top:18px;">
                                                <span class="material-symbols-outlined" style="font-size: 41px;">delete</span>
                                            </v-btn>
                                        </template>
                                        <!--Pop up -->
                                        <v-card title="Delete Schedule">
                                            <v-card-text>
                                                <v-row dense>
                                                    <p>Are you sure you want to delete schedule <strong>{{this.selectedScheduleTitle}}</strong>?</p>
                                                    <p>This will delete all of your weekly events.</p>
                                                </v-row>
                                            </v-card-text>
                                            <v-card-actions>
                                                <v-spacer></v-spacer>
                                                <v-btn text="Close" variant="plain" @click="dialog_delete_schedule = false"></v-btn>
                                                <v-btn color="#da4d4d" text="Delete" variant="tonal" @click="deleteSchedule()"></v-btn>
                                            </v-card-actions>
                                        </v-card>
                                    </v-dialog>
                                </v-row>
                            </h1>
                        </div>

                        <div class="col d-flex flex-column">
                            <v-btn class="add-schedule" @click="downloadPDF" size="small" style="max-width: 46px; height:46px; margin-top:6px; margin-left: auto; margin-right: 10px;">
                                <span class="material-symbols-outlined" style="font-size: 46px;">print</span>
                            </v-btn>
                        </div>
                        <!--<button class="print-btn" @click="downloadPDF">
                            <img class ="printer" src="../assets/printer.png" alt="Print Button">
                            <span class="material-symbols-outlined" style="font-size: 41px;">print</span>
                        </button>-->


                        <!--WEEKDAYS AND WEEKENDS ADD EVENTS POPUP-->
                        <v-dialog v-model="dialog_event" max-width="900" style="font-family: Poppins;" v-if="scheduleOption === 'Weekdays and Weekends'">
                            <template v-slot:activator="{ props: activatorProps }">
                                <v-btn class="add-weekly-event" v-bind="activatorProps">Add An Event</v-btn>
                            </template>
                            <!--Pop up -->
                            <v-card title="Add a weekly event">
                                <v-card-text>
                                    <v-row dense>
                                        <v-col>  
                                            <v-text-field v-model="weeklyEventDesc" label="Event Description" required ></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row dense>
                                        <v-col auto>
                                            <v-select v-model="eventColor" :items="this.scheduleColors" label="Color" required></v-select>
                                        </v-col>
                                        <v-col auto>        
                                            <v-text-field v-model="weeklyEventStart" placeholder="00:00 AM" hint="8:00 AM - 7:00 PM" label="Start Time" type="time" :rules="[timeValidation]"></v-text-field>
                                        </v-col>
                                        <v-col auto>
                                                <v-text-field v-model="weeklyEventEnd" placeholder="00:00 PM" hint="Maximum End Time: 7:59 PM" label="End Time" type="time" :rules="[timeValidation]"></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row dense>
                                        <v-col v-for="(day, index) in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']" :key="index" cols="auto">
                                            <v-checkbox v-model="daysOfWeek[day]" :label="day" style="font-size: 16px;"></v-checkbox>
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn text="Close" variant="plain" @click="dialog_event = false"></v-btn>
                                    <v-btn color="primary" text="Add" variant="tonal" @click="createCustomEvent()" :disabled="!timeValid"></v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>

                        <!--POP UP FOR WEEKDAYS EVENT ADD-->
                        <v-dialog v-model="dialog_weekdaysevent" max-width="700" style="font-family: Poppins;" v-if="scheduleOption === 'Weekdays'">
                            <template v-slot:activator="{ props: activatorProps }">
                                <v-btn class="add-weekly-event" v-bind="activatorProps">Add An Event</v-btn>
                            </template>
                            <!--Pop up -->
                            <v-card title="Add a weekly event">
                                <v-card-text>
                                    <v-row dense>
                                        <v-col>  
                                            <v-text-field v-model="weeklyEventDesc" label="Event Description" required></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row dense>
                                        <v-col auto>
                                            <v-select v-model="eventColor" :items="this.scheduleColors" label="Color" required></v-select>
                                        </v-col>
                                        <v-col auto>        
                                            <v-text-field v-model="weeklyEventStart" placeholder="00:00 AM" hint="8:00 AM - 7:00 PM" label="Start Time" type="time" :rules="[timeValidation]"></v-text-field>
                                        </v-col>
                                        <v-col auto>
                                                <v-text-field v-model="weeklyEventEnd" placeholder="00:00 PM" hint="Maximum End Time: 7:59 PM" label="End Time" type="time" :rules="[timeValidation]"></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row dense>
                                        <v-col v-for="(day, index) in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']" :key="index" cols="auto">
                                            <v-checkbox v-model="daysOfWeek[day]" :label="day" style="font-size: 16px;"></v-checkbox>
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn text="Close" variant="plain" @click="dialog_weekdaysevent = false"></v-btn>
                                    <v-btn color="primary" text="Add" variant="tonal" @click="createCustomEvent()" :disabled="!timeValid"></v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                        
                    </div>
                </div>

                <!-- delete event from schedule pop up -->
                <v-dialog v-model="dialog_event_popup" max-width="500" style="font-family: Poppins;">
                    <v-card>
                        <v-card-title>Event Details</v-card-title>
                        <v-card-text>
                        <v-row dense>
                            <v-col>
                            <p><strong>Description:</strong> {{ selectedEvent.description }}</p>
                            <p><strong>Start Time:</strong> {{ selectedEvent.start }}</p>
                            <p><strong>End Time:</strong> {{ selectedEvent.end }}</p>
                            <p><strong>Days:</strong> {{ selectedEvent.daysOfWeek.join(', ') }}</p>
                            </v-col>
                        </v-row>
                        </v-card-text>
                        <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn text="Close" variant="plain" @click="dialog_event_popup = false"></v-btn>
                        <v-btn color="#da4d4d" text="Delete" variant="tonal" @click="dialog_delete_event = true"></v-btn>
                        </v-card-actions>
                    </v-card>
                    </v-dialog>

                    <!-- confirnm deletion pop up-->
                    <v-dialog v-model="dialog_delete_event" max-width="500" style="font-family: Poppins;">
                    <v-card>
                        <v-card-title>Confirm Delete</v-card-title>
                        <v-card-text>
                        <p>Are you sure you want to delete the event "{{ selectedEvent.description }}"?</p>
                        </v-card-text>
                        <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn text="Cancel" variant="plain" @click="dialog_delete_event = false"></v-btn>
                        <v-btn color="#da4d4d" text="Delete" variant="tonal" @click="confirmDeleteEvent"></v-btn>
                        </v-card-actions>
                    </v-card>
                    </v-dialog>

                <!--DISPLAYS OF WEEKDAY SCHEDULE OPTION-->
                <div id="schedule-page" ref="schedulePage" >
                    <div class="loading" v-if="schedule.length === 0">
                        <v-progress-circular indeterminate :width="5"></v-progress-circular>
                    </div>
                    <div class="container-fluid mt-3" v-if="scheduleOption === 'Weekdays' || scheduleOption === 'Class Schedule' && schedule.length > 0">
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
                                            <div v-if="scheduleOption === 'Class Schedule'">
                                                <div v-for="classBlock in generateBlocks(day)" :key="classBlock.id" :style="classBlock.style">
                                                    <div class="class-info">
                                                        {{ classBlock.classes.map(item => item.course).join(', ') }}
                                                        <br>
                                                        {{ classBlock.classes[0].time }}
                                                        <br>
                                                        {{ classBlock.classes[0].location }}
                                                    </div>
                                                </div>
                                            </div>
                                            <div v-if="scheduleOption === 'Weekdays'">
                                                <div v-for="eventBlock in generateWeeklyBlocks(day)" :key="eventBlock.id" :style="eventBlock.style" @click="openEventPopup(eventBlock.events[0])">
                                                    <div class="class-info">
                                                        {{ eventBlock.events[0].description }}
                                                        <br>
                                                        {{ eventBlock.events[0].start }} - {{ eventBlock.events[0].end }}
                                                    </div>
                                                </div>
                                            </div>
                                        </template>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>



                    <!--DISPLAYS OF WEEKDAYS AND WEEKENDS SCHEDULE OPTION-->
                    <div class="container-fluid mt-3" v-if="scheduleOption === 'Weekdays and Weekends'">
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
                                        <template v-if="time === '8' && day === 'Sunday' || time === '8' && day === 'Monday' || time === '8' && day === 'Tuesday'
                                                || time === '8' && day === 'Wednesday' || time === '8' && day === 'Thursday'
                                                || time === '8' && day === 'Friday' || time === '8' && day === 'Saturday'">
                                            <div v-if="scheduleOption === 'Weekdays and Weekends'">
                                                <div v-for="eventBlock in generateWeeklyBlocks(day)" :key="eventBlock.id" :style="eventBlock.style" @click="openEventPopup(eventBlock.events[0])">
                                                    <div class="class-info">
                                                        {{ eventBlock.events[0].description }}
                                                        <br>
                                                        {{ eventBlock.events[0].start }} - {{ eventBlock.events[0].end }}
                                                    </div>
                                                </div>
                                            </div>
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
                <v-dialog v-model="dialog_events" max-width="800" style="font-family: Poppins;">
                    <template v-slot:activator="{ props: activatorProps }">
                        <v-btn class="add-event2" v-bind="activatorProps">Events</v-btn>
                    </template>
                    <!--Pop up -->
                    <v-card title="Manage Events">
                        <v-card-text>
                            <v-row dense>
                                <v-col cols = "12">
                                    <v-expansion-panels>
                                        <v-expansion-panel>
                                            <v-expansion-panel-title>
                                                <v-row no-gutters>
                                                    <v-col class="d-flex justify-start">
                                                        <p>Your events: ({{events.length}})</p>
                                                    </v-col>
                                                </v-row>
                                            </v-expansion-panel-title>
                                            <v-expansion-panel-text>
                                                <v-row no-gutters v-for="(event, index) in events" :key="index">
                                                    <v-col cols="10">
                                                        <p><strong>{{events[index].title}}</strong> (<em>{{events[index].date}}</em>) - {{events[index].description}}</p>
                                                    </v-col>
                                                    <v-col cols="1">
                                                        <v-dialog v-model="dialog_events_remove[index]" max-width="500" style="font-family: Poppins;">
                                                            <template v-slot:activator="{ props: activatorProps }">
                                                                <v-btn v-bind="activatorProps" icon="$close" variant="plain">
                                                                    <span class="material-symbols-outlined">
                                                                        delete
                                                                    </span>
                                                                </v-btn>
                                                            </template>
                                                            <!--Pop up -->
                                                            <v-card title="Are you sure you want to delete event:">
                                                                <v-card-text>
                                                                    <br>
                                                                    <p><strong>{{events[index].title}}</strong> (<em>{{events[index].date}}</em>) - {{events[index].description}}</p>
                                                                </v-card-text> 
                                                                <v-card-actions>
                                                                    <v-spacer></v-spacer>
                                                                    <v-btn text="Close" variant="plain" @click="dialog_events_remove[index] = false"></v-btn>
                                                                    <v-btn color="#da4d4d" text="Delete" variant="tonal" @click="removeCalendarEvent(index)"></v-btn>
                                                                </v-card-actions>
                                                            </v-card>
                                                        </v-dialog> 
                                                    </v-col>
                                                    <v-col cols="1">
                                                        <v-dialog v-model="dialog_events_share[index]" max-width="500" style="font-family: Poppins;">
                                                            <template v-slot:activator="{ props: activatorProps }">
                                                                <v-btn v-bind="activatorProps" icon="$close" variant="plain">
                                                                    <span class="material-symbols-outlined">
                                                                        share
                                                                    </span>
                                                                </v-btn>
                                                            </template>
                                                            <!--Pop up -->
                                                            <v-card title="Are you sure you want to export event:">
                                                                <v-card-text>
                                                                    <br>
                                                                    <p><strong>{{events[index].title}}</strong> (<em>{{events[index].date}}</em>) - {{events[index].description}}</p>
                                                                </v-card-text> 
                                                                <v-card-actions>
                                                                    <v-spacer></v-spacer>
                                                                    <v-btn text="Close" variant="plain" @click="dialog_events_share[index] = false"></v-btn>
                                                                    <v-btn color="primary" text="Export" variant="tonal" @click="generateSingleICSEvent(index)"></v-btn>
                                                                </v-card-actions>
                                                            </v-card>
                                                        </v-dialog> 
                                                    </v-col>
                                                    <v-divider class="instructor-divider"></v-divider>
                                                </v-row>
                                            </v-expansion-panel-text>
                                        </v-expansion-panel>
                                    </v-expansion-panels>  
                                </v-col>
                            </v-row>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn text="Export Calendar" color="success" @click="generateAllICSEvents" variant="tonal" :disabled="events.length === 0"></v-btn>
                            <v-spacer></v-spacer>
                            <v-btn text="Close" variant="plain" @click="dialog_events = false"></v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>

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
                            @contextmenu:day="dateClick"
                            ></v-calendar>
                        </v-sheet>
                    </v-col>
                </v-row>
                <br>
            </div>
        </v-col>
    </v-row>
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
    import html2pdf from 'html2pdf.js';
    import axios from 'axios';
    import { useDate } from 'vuetify';
    import { ref } from 'vue';
    import { createEvent } from 'ics';

    export default {
        props:{
            userType:{
                type: String,
                required: '',
            }
        },
        data:() => ({
            
                tab: 'class-schedule',
                classSchedule: true,
                calendar: false,
                selectedEvent: null,
                dialog_event_popup: false,
                dialog_delete_event: false,

                user: {
                    firstname: '',
                    lastname: '',
                    major: '',
                },

                dialog: false,
                dialog_events: false,
                dialog_events_remove: [],
                dialog_events_share: [],
                dialog_event: false,
                dialog_weekdaysevent: false,
                dialog_delete_schedule: false,

                //Every data that involves schedule under this
                menuStart: false,
                scheduleTitle: '',
                selectedScheduleTitle: 'Class Schedule',
                newScheduleOption: 'Weekdays',
                scheduleOption: 'Class Schedule',
                weekdays: true,
                scheduleOptions: ['Weekdays', 'Weekdays and Weekends'],
                userSchedules: [
                    {option: 'Class Schedule', title: 'Class Schedule', weeklyEvents:[]},
                ],
                schedule: [],
                scheduleColors: ['aliceblue', 'beige', 'darkgrey', 'darksalmon', 'honeydew', 'lightblue', 'darkseagreen','plum', 'springgreen', 'lightyellow','pink'],

                weeklyEventDesc: '',
                weeklyEventStart: '',
                weeklyEventEnd: '',
                daysOfWeek: {
                    Sunday: false,
                    Monday: false,
                    Tuesday: false,
                    Wednesday: false,
                    Thursday: false,
                    Friday: false,
                    Saturday: false
                },
                timeValid: false,

                //Every data that involves calendar under this
                today: ref(new Date()),
                focus: '',
                events: [],
                colors: ['aliceblue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey','red', 'brown', 'yellow','black'],
                eventTitle: '',
                eventColor: '',
                eventDescription: '',
                allDay: false,
                eventDate: new Date(),

                }),

        watch:{
            selectedScheduleTitle(){
                this.handleScheduleChange();
            }
        },

        computed: {
            timeValidation() {
                return () => {
                const minTime = "08:00";
                const maxTime = "19:00";
                const maxTimeEnd = "19:59";
                const startTime = this.weeklyEventStart;
                const endTime = this.weeklyEventEnd;
                
                const withinRange = startTime >= minTime && startTime <= maxTime && endTime <= maxTimeEnd;

                const validOrder = startTime < endTime;

                this.timeValid = withinRange && validOrder;
                
                if (!withinRange) {
                    return "Start time must be between 08:00 AM and 7:00 PM, and end before 7:59 PM";
                }

                if (!validOrder) {
                    return "Start time must be before end time";
                }

                return this.timeValid || "Invalid times";
                };
            },
        },
        mounted() {
            this.fetchUserInfo();
            this.fetchUserSchedule();
            
            const adapter = useDate()
            this.fetchEvents({ start: adapter.startOfDay(adapter.startOfMonth(new Date())), end: adapter.endOfDay(adapter.endOfMonth(new Date())) })

            this.fetchCustomSchedules();
            },

        methods: {
            dateClick(date) {
                console.log('Clicked day', date);
            },
            chooseClassSchedule(){
                this.tab = 'class-schedule';
                this.calendar = false;
                this.classSchedule = true;
            },

            openEventPopup(event) {
                this.selectedEvent = event;
                this.dialog_event_popup = true;
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

                        //check the user's role
                        if (response.data.role === 'Admin') {
                            this.calendar = true;
                            this.classSchedule = false;
                        } else {
                            this.fetchUserSchedule(); //if the user is not an admin, fetch the user schedule
                        }
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
                        
                        const startHour = parseInt(course.start.split(':')[0]);
                        const startMinute = parseInt(course.start.split(':')[1]);
                        const endHour = parseInt(course.end.split(':')[0]);
                        const endMinute = parseInt(course.end.split(':')[1]);

                        const blockHeight = ((endHour - startHour) * 56.3 + (endMinute - startMinute));

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
                        else if(startHour === 13){
                            yTransformation = 280;
                        }
                        else if(startHour === 14){
                            yTransformation = 335;
                        }
                        else if(startHour === 15){
                            yTransformation = 391;
                        }
                        else if(startHour === 16){
                            yTransformation = 446;
                        }
                        else if(startHour === 17){
                            yTransformation = 502;
                        }
                        else if(startHour === 18){
                            yTransformation = 558;
                        }
                        else if(startHour === 19){
                            yTransformation = 613;
                        }
                        yTransformation += 0.9 * startMinute;

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
                                'border': '1px solid black',
                            },
                            classes: [course],
                        });
                    }
                });
                return blocks;
            },


            //Any method under this are for the schedule

            async deleteSchedule() {
                const scheduleToDelete = this.userSchedules.find(schedule => schedule.title === this.selectedScheduleTitle);

                if (scheduleToDelete && scheduleToDelete.scheduleID) {
                    try {
                        await axios.delete(`http://127.0.0.1:5000/deleteCustomSchedule/${scheduleToDelete.scheduleID}`, {
                            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                    });
                        // Remove the deleted schedule from the userSchedules array
                        const scheduleIndex = this.userSchedules.findIndex(schedule => schedule.title === this.selectedScheduleTitle);
                        this.userSchedules.splice(scheduleIndex, 1);

                        this.dialog_delete_schedule = false;
                        this.selectedScheduleTitle = 'Class Schedule';
                        this.scheduleOption = 'Class Schedule';
                    } catch (error) {
                        console.error('Error deleting custom schedule:', error);
                    }
                }
            },

            createWeeklyEvent(){
                const selectedDays = Object.keys(this.daysOfWeek).filter(day => this.daysOfWeek[day]);
                this.newWeeklyEvent(selectedDays);
                console.log("selected days", selectedDays);
            },

            newWeeklyEvent(selectedDays){
                const selectedSchedule = this.userSchedules.find(schedule => schedule.title === this.selectedScheduleTitle);
                console.log("selected schedule", selectedSchedule);
                const newEvent = {
                    description: this.weeklyEventDesc,
                    color: this.eventColor,
                    start: this.weeklyEventStart,
                    end: this.weeklyEventEnd,
                    daysOfWeek: {},
                };

                // Set the selected days in the event object
                selectedDays.forEach(day => {
                    newEvent.daysOfWeek[day] = true;
                });

                // Add the new event to the selected schedule
                selectedSchedule.weeklyEvents.push(newEvent);

                this.weeklyEventDesc = '';
                this.eventColor = '';
                this.weeklyEventStart = '';
                this.weeklyEventEnd = '';
                this.daysOfWeek = {
                    Sunday: false,
                    Monday: false,
                    Tuesday: false,
                    Wednesday: false,
                    Thursday: false,
                    Friday: false,
                    Saturday: false,
                };

                this.dialog_event = false;
                this.dialog_weekdaysevent = false;                
            },

            async confirmDeleteEvent() {
                await axios.delete(`http://127.0.0.1:5000/deleteCustomEvent/${this.selectedEvent.eventID}`, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                });

                this.fetchCustomSchedules();
                this.dialog_delete_event = false;
                this.dialog_event_popup = false;
            },
            
            generateWeeklyBlocks(day) {
                const blocks = [];
                const selectedSchedule = this.userSchedules.find(schedule => schedule.title === this.selectedScheduleTitle);
                if (selectedSchedule && selectedSchedule.events) {
                    // Proceed only if the selected schedule is found and it has weekly events
                    selectedSchedule.events.forEach(event => {
                        if (event.daysOfWeek && event.daysOfWeek.includes(day)) {
                            //event.start === 8:00 AM
                            const startTimeParts = event.start.split(':'); //[hours, minutes, am/pm]
                            const endTimeParts = event.end.split(':');

                            let startHour = parseInt(startTimeParts[0]);
                            const startMinute = parseInt(startTimeParts[1].slice(0, 2));
                            const startAmPm = startTimeParts[1].slice(-2);

                            let endHour = parseInt(endTimeParts[0]);
                            const endMinute = parseInt(endTimeParts[1].slice(0, 2));
                            const endAmPm = endTimeParts[1].slice(-2);
                            
                            if(startAmPm === 'PM' && startHour < 12){
                                startHour += 12; //convert to 24 hour format
                            }

                            if(endAmPm === 'PM' && endHour < 12){
                                endHour += 12; //convert to 24 hour format
                            }

                            let startMinutes = (startHour * 60) + startMinute;
                            let endMinutes = (endHour * 60) + endMinute;

                            let durationInMinutes = (endMinutes - startMinutes)/60;

                            let blockHeight = durationInMinutes * 56.3;

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
                            else if(startHour === 13){
                                yTransformation = 280;
                            }
                            else if(startHour === 14){
                                yTransformation = 335;
                            }
                            else if(startHour === 15){
                                yTransformation = 391;
                            }
                            else if(startHour === 16){
                                yTransformation = 446;
                            }
                            else if(startHour === 17){
                                yTransformation = 502;
                            }
                            else if(startHour === 18){
                                yTransformation = 558;
                            }
                            else if(startHour === 19){
                                yTransformation = 613;
                            }
                            yTransformation += 0.9 * startMinute;
                        


                            blocks.push({
                                id: event.eventID + day,
                                style: {
                                    'background-color': event.color,
                                    'border-radius': '8px',
                                    'height': `${blockHeight}px`,
                                    'width': '100%',
                                    'transform': `translateY(${yTransformation}px)`,
                                    'position': 'absolute',
                                    'top': `0`,
                                    'z-index': '1',
                                    'cursor': 'pointer',
                                    'border': '1px solid black',
                                },
                                events: [event]
                            });
                        }
                    });
                }
                return blocks;
            },

            handleScheduleChange() {
                this.selectedSchedule = this.userSchedules.find(schedule => schedule.title === this.selectedScheduleTitle);
                this.scheduleOption = this.selectedSchedule.option;
                console.log("selected:", this.selectedSchedule);
            },

            //Any method under this are for the calendar
            getEventColor (event) {
                return event.color
            },

            generateSingleICSEvent(index) {
                const eventExport = this.events[index];

                const startDate = new Date(eventExport.start);
                const endDate = new Date(eventExport.end);
                endDate.setHours(endDate.getHours() + 1);

                const event = {
                    start: [startDate.getFullYear(), startDate.getMonth() + 1, startDate.getDate(), startDate.getHours(), startDate.getMinutes()],
                    end: [endDate.getFullYear(), endDate.getMonth() + 1, endDate.getDate(), endDate.getHours(), endDate.getMinutes()],
                    title: eventExport.title,
                    description: eventExport.description,
                    location: '', 
                    categories: ['Course Compass'],
                };

                createEvent(event, (error, value) => {
                    if (error) {
                        console.error(error);
                        return;
                    }
                    const blob = new Blob([value], { type: 'text/calendar;charset=utf-8' });

                    const link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.setAttribute('download', eventExport.title + ' Event.ics');
                    document.body.appendChild(link);
                    link.click();

                    document.body.removeChild(link);
                });
                this.dialog_events_share = false;
            },

            generateAllICSEvents() {
                const icsData = [];

                this.events.forEach(eventExport => {
                    const startDate = new Date(eventExport.start);
                    const endDate = new Date(eventExport.end);
                    endDate.setHours(endDate.getHours() + 1);

                    const event = {
                        start: [startDate.getFullYear(), startDate.getMonth() + 1, startDate.getDate(), startDate.getHours(), startDate.getMinutes()],
                        end: [endDate.getFullYear(), endDate.getMonth() + 1, endDate.getDate(), endDate.getHours(), endDate.getMinutes()],
                        title: eventExport.title,
                        description: eventExport.description,
                        location: '', 
                        categories: ['Course Compass'],
                    };

                    createEvent(event, (error, value) => {
                        if (error) {
                            console.error(error);
                            return;
                        }
                        icsData.push(value);
                    });
                });

                const allEventsICS = icsData.join('\r\n');

                const blob = new Blob([allEventsICS], { type: 'text/calendar;charset=utf-8' });

                const link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.setAttribute('download', 'Course Compass Calendar.ics');
                document.body.appendChild(link);
                link.click();

                document.body.removeChild(link);
            },

            newEvent(){
                const reformatDate = new Date(this.eventDate).toLocaleDateString('en-US', {
                    month: 'long',
                    day: 'numeric',
                    year: 'numeric',
                });

                const newEvent = {
                    title: this.eventTitle,
                    description: this.eventDescription,
                    start: this.eventDate, 
                    end: this.eventDate,
                    color: this.eventColor,
                    allDay: this.allDay,
                    date: reformatDate,
                };

                this.events.push(newEvent);
                this.dialog = false;
                this.eventDate = new Date();
                this.eventColor = '';
                this.eventTitle ='';
                this.eventDescription ='';
            },

            fetchEvents (newEvent) {
                this.events.push();
            },

            removeCalendarEvent(index){
                this.events.splice(index, 1);
                this.dialog_events_remove[index] = false;
            },

            //format Time - John
            formatTime(time){
                const [hours, minutes] = time.split(':');
                const formattedHours = parseInt(hours, 10) > 12 ? parseInt(hours, 10) - 12 : parseInt(hours, 10); //if hours is greater than 12, minus 12 to achieve PM
                const ampm = parseInt(hours, 10) >= 12 ? 'PM' : 'AM'; //if hours is greater or equal to 12, choose PM, otherwise AM

                return `${formattedHours}:${minutes} ${ampm}`; //ex: 2:44 AM            
            },

            //created by Jose
            async createCustomSchedule() {
                try {
                    const response = await axios.post('http://127.0.0.1:5000/createCustomSchedule', {
                        title: this.scheduleTitle,
                        option: this.newScheduleOption,
                    }, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                    });
                    if (response.status === 200) {
                        const newSchedule = response.data.schedule;
                        newSchedule.title = this.scheduleTitle;
                        this.userSchedules.push(newSchedule);
                        this.dialog = false;
                        this.scheduleTitle = '';
                        await this.fetchCustomSchedules();
                        //this.selectedScheduleTitle = newSchedule.title; //set the selected schedule to the new schedule
                    }
                } catch (error) {
                    if (error.response && error.response.data && error.response.data.error) {
                    this.$emit('show-toast', { message: error.response.data.error, color: '#da6e51' });
                    } else {
                    console.error('Error creating custom schedule:', error);
                    this.$toast.error('An error occurred while creating the custom schedule. Please try again.');
                    }
                }
            }, //-- end

            async createCustomEvent() {
                const selectedSchedule = this.userSchedules.find(schedule => schedule.title === this.selectedScheduleTitle);

                const selectedDays = Object.keys(this.daysOfWeek).filter(day => this.daysOfWeek[day]);
                const eventStartTime = this.formatTime(this.weeklyEventStart); //03:00 --> 3:00 AM
                const eventEndTime = this.formatTime(this.weeklyEventEnd); //16:40 --> 4:40 PM
                console.log('start', eventStartTime);
                console.log('end', eventEndTime);
                const newEvent = {
                    description: this.weeklyEventDesc,
                    color: this.eventColor,
                    start: eventStartTime,
                    end: eventEndTime,
                    daysOfWeek: selectedDays,
                    scheduleID: selectedSchedule.scheduleID, // Include the scheduleID
                };

                try {
                    await axios.post('http://127.0.0.1:5000/createCustomEvent', newEvent, {
                        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                    });
                    this.weeklyEventDesc = '';
                    this.eventColor = '';
                    this.weeklyEventStart = '';
                    this.weeklyEventEnd = '';
                    this.daysOfWeek = {
                        Sunday: false,
                        Monday: false,
                        Tuesday: false,
                        Wednesday: false,
                        Thursday: false,
                        Friday: false,
                        Saturday: false,
                    };
                    this.dialog_event = false;
                    this.dialog_weekdaysevent = false;
                    this.fetchCustomSchedules();
                } catch (error) {
                    console.error('Error creating custom event:', error);
                }
            },

            async fetchCustomSchedules() {
                try {
                    const response = await axios.get('http://127.0.0.1:5000/getCustomSchedules', {
                        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                    });
                    if (response.data && response.data.customSchedules) {
                        const updatedSchedules = [
                            {
                                option: 'Class Schedule',
                                title: 'Class Schedule',
                                events: []
                            },
                            ...response.data.customSchedules.map(schedule => ({
                                ...schedule,
                                events: schedule.events || [],
                            }))
                        ];
                        this.userSchedules = updatedSchedules;
                    }
                } catch (error) {
                    console.error('Error fetching custom schedules:', error);
                }
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
        text-align: left;
        font-family: Poppins;
        margin-top: 2px;
        margin-bottom: -6px;
        margin-left: 14px;
    }

    .schedule-days { /* outer part of the schedule*/
        font-family: Poppins;
        font-size: 20px;
        text-align: center;
        padding: 10px;
        border-radius: 5px;
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
        font-size: 14px;
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
        width: 320px;
        height: 45px;
        margin-bottom: 5px;
        box-sizing: border-box;
        border: 1px solid rgba(0, 0, 0, 0.089);
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="%23000000"><path d="M1 5h14L8 12z"/></svg>');
        background-position: right 5px center;
        background-size: 15px;
        cursor: pointer;
        padding-left: 8px;
        padding-right: 15px;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
    }

    .add-event{
        position: absolute;
        right: 10px;
        margin-top: 25px;
        font-family: Poppins;
        color: white;
        background-color: black;
        box-shadow: none;
    }

    .add-event2{
        position: absolute;
        right: 180px;
        margin-top: 25px;
        font-family: Poppins;
        color: rgb(0, 0, 0);
        background-color: rgb(255, 255, 255);
        box-shadow: none;
        border: black 1px solid;
    }

    .add-weekly-event{
        width: 150px;
        margin-top: 19px;
        margin-right: 25px;
        font-family: Poppins;
        color: rgb(255, 255, 255);
        background-color: rgb(0, 0, 0);
        box-shadow: none;
    }
    
    .add-schedule{
        margin-left: 5px;
        margin-bottom: 4px;
        font-family: Poppins;
        box-shadow: none;
    }

    .selected-tab{
        background-color: rgb(224, 224, 224);
    }

    .custom-label .v-label{
        font-size: 5px;
    }

    .color-square {
        width: 20px;
        height: 20px;
        display: inline-block;
        margin-right: 10px;
        vertical-align: middle;
        background-color: pink;
    }

    .loading{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
</style>