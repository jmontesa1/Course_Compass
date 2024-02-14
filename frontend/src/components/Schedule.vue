<!--Created by: John Montesa-->
<!-- This is the Schedule page for Course Compass -->
<!-- This page will show the scheudle of the specific user in a time table/ time block style -->

<template>
    <div class="header-container">
        <div class="row justify-content-center">
            <div class="col d-flex flex-column"><h1>{{ user.firstname }} {{ user.lastname }}'s Schedule | {{ user.term }}</h1></div>
                <button class="print-btn" @click="downloadPDF">
                    <img class ="printer" src="../assets/printer.png" alt="Print Button">
                </button>
        </div>
    </div>

    <div id="schedule-page" ref="schedulePage">
        <div class="container-fluid mt-3">
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
    </div>

</template>

<script>
    import html2pdf from 'html2pdf.js';

    export default {
        data() {
            return {
            user: {
                firstname: 'John',
                lastname: 'Montesa',
                major: 'Computer Science & Engineering',
                term: 'Fall 2023',
            },

            schedule: [
                { course: 'CS 135', days: ['Monday','Wednesday','Friday'], time: '10:00 AM - 10:50 AM', start: '10:00', end: '10:50', location: 'SEM 104' },
                { course: 'CS 425', days: ['Tuesday','Thursday'], time: '10:30 AM - 11:45 AM', start: '10:30', end: '11:45', location: 'WPEB 101' },
                { course: 'CS 302', days: ['Monday', 'Wednesday'], time: '3:00 PM - 4:15 PM', start: '3:00', end: '4:15', location: 'PSAC 1002' },
                { course: 'ENG 101', days: ['Monday', 'Wednesday', 'Friday'], time: '6:00 PM - 6:50 PM', start: '6:00', end: '6:50', location: 'MKIC 320' },
                { course: 'EE 165', days: ['Monday', 'Wednesday', 'Friday'], time: '8:30 PM - 9:45 PM', start: '8:30', end: '9:45', location: 'SLC 102' },
                { course: 'MUS 123', days: ['Tuesday', 'Thursday', 'Friday'], time: '1:00 PM - 1:50 PM', start: '1:00', end: '1:50', location: 'CFA 102' },
                // Add more events as needed
            ],

            };
        },

        methods: {
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
                                'transform': `translateY(${yTransformation}px)`, // Apply Y transformation
                                'position': 'absolute',
                                'top': `0`,
                            },
                            classes: [course],
                        });
                    }
                });
                return blocks;
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
        text-align: center;
        font-family: coolvetica;
        font-size: 30px;
        margin-top: 2px;
        margin-bottom: -6px;
    }

    .schedule-days { /* outer part of the schedule*/
        font-family: coolvetica;
        font-size: 20px;
        text-align: center;
        padding: 10px;
        border: 1px solid #000000; 
        border-radius: 8px;
    }

    .col {
        padding: 10px;
        border: 1px solid #eeeeee72;
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
        font-family: coolvetica;
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
        left: 20%; /*time slot black bar*/
        right: 0;
        height: 1px;
        background-color: #333;
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
        white-space: nowrap; /* Optional: Prevent text from wrapping if it exceeds the width */
        top: 50%; /* The last three make the text in the middle of the block*/
        left: 50%;
        transform: translate(-50%, -50%);
    }

@media (max-width: 768px) {
    .class-info {
        font-size: 12px; /* Adjust the font size for smaller screens */
    }
}
</style>