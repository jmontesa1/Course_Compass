<!--Created by: John Montesa-->
<!-- This is the Schedule page for Course Compass -->
<!-- This page will show the scheudle of the specific user in a time table/ time block style -->

<template>
        <div class="header-container">
            <div class="row justify-content-end">
                <div class="col-6"><h1>{{ user.firstname }} {{ user.lastname }}'s Schedule | {{ user.term }}</h1></div>
                <div class="col-3">
                    <button class="print-btn" @click="downloadPDF">
                        <img class ="printer" src="../assets/printer.png" alt="Print Button">
                    </button>
            </div>
            </div>
        </div>

    <div id="schedule-page">
        <div class="container-fluid mt-3">
            <div class="schedule-days">
                <div class="row">
                    <div class="col-sm-1"></div>
                    <div v-for="day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']" :key="day" class="col d-flex flex-column">
                        {{ day }}
                    </div>
                </div>

                <div class="row">
                    <div class="col-sm-1">
                            <div class="time-slot" v-for="time in ['7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', 
                            '7 PM']" :key="time">
                                <div class="time-slot-hour">{{ time }}</div>
                                <div class="time-slot-half-hour"></div>
                            </div>
                    </div>
                    <div v-for="day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']" :key="day" class="col d-flex flex-column"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import html2pdf from 'html2pdf.js';

    export default {
        methods: {
            async downloadPDF() {
            const content = document.getElementById('schedule-page');


            const pdfOptions = {
                margin: 1,
                filename: 'schedule.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 1 },
                jsPDF: { unit: 'mm', format: 'a4', orientation: 'landscape' },
            };

            html2pdf().from(content).set(pdfOptions).save();
            },
        },

        data() {
            return {
            user: {
                firstname: 'John',
                lastname: 'Montesa',
                major: 'Computer Science & Engineering',
                term: 'Fall 2023',
            },

            schedule: [
                { course: 'CS 135', day: 'Monday', time: '10:00 AM - 10:50 AM', location: 'SEM 104' },
                { course: 'CS 425', day: 'Monday', time: '10:30 AM - 11:45 AM', location: 'WPEB 101' },
                { course: 'CS 302', day: 'Monday', time: '3:00 PM - 4:15 PM', location: 'PSAC 1002' },
                // Add more events as needed
            ],
            };
        },
    };
</script>

<style scoped>
    .header-container{
        margin-bottom: -10px;
    }
    h1 {
        text-align: center;
        font-family: coolvetica;
        font-size: 30px;
        margin-top: 2px;
        margin-bottom: -6px;
    }

    .schedule-days {
        font-family: coolvetica;
        font-size: 20px;
        text-align: center;
        padding: 10px;
        border: 1px solid #000000;
        border-radius: 8px;
    }

    .col {
        padding: 10px;
        border: 1px solid #eee;
    }

    .print-btn {
        border: transparent;
        background: transparent;
        cursor: pointer;
        float: right;
        margin-top: 5px;
        margin-right: 15px;
    }

    .printer{
        width: 35px;
        height: auto;
    }

    .time-slot {
        border-bottom: 1px solid #eee;
        position: relative;
    }

    .time-slot-hour {
        padding-bottom: 20px;
    }

    .time-slot-half-hour {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background-color: #333;
    }
</style>