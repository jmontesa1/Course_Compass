<!-- Created by: John Montesa -->
<!-- This is the Progress page for Course Compass -->
<!-- This page will show the progress of the specific user's college career in a progress bar style -->
<!-- The progress bar will be based on the courses that the user has completed -->
<!-- The user can check off the courses that they have completed and the progress bar and units completed will update accordingly -->

<template>
    <div class="progress-page">
        <div v-for="(major, index) in filteredMajors" :key="index">
        <h1>{{ major.name }}</h1>
        <div class="container-fluid mt-3">
            <div class="row">
            <div class="col-md d-flex flex-column">
                <br>
                <h2>Career</h2>
                <p><strong>Units Completed:</strong> {{ unitsCompleted }}/{{ major.units }}</p>
            </div>
            <div class="col-md-5 d-flex flex-column">
                <br>
                <h2>Courses</h2>
                <div class="scroll">
                    <div class="course-container" v-for="(course, courseIndex) in major.courses" :key="courseIndex">
                        <input type="checkbox" v-model="course.completed" />
                        <label>{{ course.name }}</label>
                    </div>
                </div>
            </div>
            </div>
        </div>
        </div>
    </div>

    <div class="footer">
        <div class="container-fluid mt-3">
            <div class="row">
                <div v-if="selectedMajor === user.major" class="col-sm-2 d-flex">
                    <div class="completion-text">Progress:</div>
                </div>

                <div class="col d-flex flex-column">
                    <div class="progress-container">
                        <div v-if="selectedMajor === user.major" class="progress-bar" :style="{ width: `${progressPercentage}%` }">
                            <span class="progress-text">{{ Math.round(progressPercentage) }}%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    export default {
        data() {
            return {
                unitsCompleted: 0,
                user: {
                    firstname: 'John',
                    lastname: 'Montesa',
                    email: '',
                    major: 'Computer Science & Engineering',
                },
                majors: [
                {
                    name: 'Computer Science & Engineering',
                    units: 120.0,
                    courses: [
                        { name: 'CS 135: Introduction to Computing', completed: false },
                        { name: 'CS 202: Computing II', completed: false },
                        { name: 'CS 219: Storage Management', completed: false },
                        { name: 'CS 302: Data Structures', completed: false },
                        { name: 'CS 365: Math to Computer Science', completed: false },
                        { name: 'CS 425: Senior Projects I', completed: false },
                        { name: 'CS 426: Senior Projects II', completed: false },
                        { name: 'CS 446: Principles of Data', completed: false },
                        { name: 'CS 456: Automata and Formal Languages', completed: false },
                        { name: 'CS 477: Analysis of Algorithms', completed: false },
                    ],
                },
                {
                    name: 'Electrical Engineering',
                    units: 120.0,
                    courses: [
                        { name: 'EE 101', completed: false },
                        { name: 'EE 202', completed: false },
                        { name: 'EE 303', completed: false },
                    ],
                },
                ],

                selectedMajor: null,
            };
        },
    
        created() {
            this.selectedMajor = this.user.major; 
        },

        computed: {
            filteredMajors() {
                return this.majors.filter((major) => major.name === this.user.major);
            },
            progressPercentage() {
                const selectedMajorCourses = this.majors.find((major) => major.name === this.user.major).courses;
                let completedUnits = 0;

                selectedMajorCourses.forEach((course) => {
                    if (course.completed) {
                        completedUnits += 3; // Assuming each course is 3 units
                    }
                });

                const totalUnits = this.majors.find((major) => major.name === this.user.major).units;
                this.unitsCompleted = completedUnits;
                return (completedUnits / totalUnits) * 100;
            },
        },
    };
</script>

<style scoped>
    h2 {
        font-family: 'coolvetica', coolvetica;
        text-align: left;
    }

    h1{
        font-family: 'coolvetica', coolvetica;
        text-align: center;
    }

    p{
        font-family: Poppins;
        margin-left: 10px;
    }

    .progress-page {
        width: 100%;
        margin: 10px auto;
    }

    input[type="checkbox"] {
        margin-right: 8px;
    }

    .progress-container {
        height: 25px;
        display: flex;
        border: 2px solid #000000;
        border-radius: 10px;
        margin-right: 15px;
        margin-top: 10px;
    }

    .progress-bar {
        height: 100%;
        background: #54ff59;
        position: relative;
        transition: width 0.3s ease;
        border-radius: 10px;
    }

    .progress-text {
        position: absolute;
        font-family:'Poppins';
        color: #000;
        margin-left: 5px;
    }

    .completion-text {
        font-family: coolvetica;
        font-size: 25px;
        color: #000;
        margin-left: 10px;
    }

    .footer { 
        position: absolute;
        bottom: 0; 
        left: 0;
        padding: 10px;
        width: 100%;
    }

    .course-container {
        font-family: 'Poppins';
        align-items: center;
        display: flex;
        margin-bottom: 8px;
        padding: 8px;
        max-width: 100%;
        max-height: 50px;
        border: 2px solid #000000;
        border-radius:5px;
    }

    .scroll {
        overflow-x: auto;
        height: 60%;
        width: 100%;
    }

</style>
