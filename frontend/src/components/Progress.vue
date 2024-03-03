<!-- Created by: John Montesa -->
<!-- This is the Progress page for Course Compass -->
<!-- This page will show the progress of the specific user's college career in a progress bar style -->
<!-- The progress bar will be based on the courses that the user has completed -->
<!-- The user can check off the courses that they have completed and the progress bar and units completed will update accordingly -->

<template>
    <v-row no-gutters>
            <v-col cols="2">
            <v-tabs v-model="tab" direction="vertical" color="primary" selected-class="selected-tab" slider-color="black">
                <v-tab value="progress" @click="chooseProgress">
                    <v-icon start>
                        <span class="material-icons" style="color:black">task_alt</span>
                    </v-icon>
                    Progress
                </v-tab>

                <v-tab value="calculators" @click="chooseCalculators()">
                    <v-icon start>
                        <span class="material-icons" style="color:black">calculate</span>
                    </v-icon>
                    Grade Calculators
                </v-tab>

                <v-tab value="analytics" @click="chooseAnalytics()">
                    <v-icon start>
                        <span class="material-icons" style="color:black">analytics</span>
                    </v-icon>
                    Analytics
                </v-tab>
            </v-tabs>
            </v-col>

            <v-col>
                <div class="progress-page" v-if="this.progress === true">
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
                    <br>
                </div>


                <div class="calculators-page" v-if="this.calculators === true">
                    <br>
                    <v-container class="gpa-calculator">
                        <v-row>
                            <h1 class="calculator-heading">GPA Calculator</h1>
                        </v-row>

                        <v-row class="calculator-subheading">
                            <v-col>Course</v-col>
                            <v-col>Credits</v-col>
                            <v-col>Grade</v-col>
                            <v-col cols="1"></v-col>
                        </v-row>

                        <v-form ref="form">
                            <v-row style="height:70px;" v-for="(courseGPA, index) in coursesGPA" :key="index">
                                <v-col>
                                    <v-text-field v-model="courseGPA.name" label="Course Name (Optional)"></v-text-field>
                                </v-col>
                                <v-col>                
                                    <v-text-field v-model="courseGPA.credits" label="Credits"></v-text-field>
                                </v-col>
                                <v-col>
                                <v-select v-model="courseGPA.grade" :items="grades.map(item => item.grade)" label="Grade" required></v-select>
                                </v-col>
                                <v-col cols="1">
                                    <v-btn class="close-btn" @click="removeCourseGPA">
                                        <span class="material-icons" style="color:black">close</span>
                                    </v-btn>
                                </v-col>
                            </v-row>

                            <v-row>
                                <v-col cols="2">
                                    <v-btn @click="addCourseGPA">Add a course</v-btn>
                                </v-col>
                                <v-col></v-col>
                                <v-col cols="2">
                                    <v-btn @click="calculateGPA">Calculate</v-btn>
                                </v-col>
                            </v-row>
                        </v-form>

                        <v-row>
                            <p class="gpa-text">Your GPA is: {{GPA}}</p>
                        </v-row>
                    </v-container>

                    <br>
                    <v-container class="exam-calculator">
                            <v-row>
                                <h1 class="calculator-heading">Final Grade Calculator</h1>
                            </v-row>

                            <v-row class="calculator-subheading">
                                <v-col>Course</v-col>
                                <v-col>Credits</v-col>
                                <v-col>Grade</v-col>
                                <v-col cols="1"></v-col>
                            </v-row>

                            <v-form ref="form">
                                <v-row style="height:70px;" v-for="(courseGPA, index) in coursesGPA" :key="index">
                                    <v-col>
                                        <v-text-field v-model="courseGPA.name" label="Course Name (Optional)"></v-text-field>
                                    </v-col>
                                    <v-col>                
                                        <v-text-field v-model="courseGPA.credits" label="Credits"></v-text-field>
                                    </v-col>
                                    <v-col>
                                    <v-select v-model="courseGPA.grade" :items="grades.map(item => item.grade)" label="Grade" required></v-select>
                                    </v-col>
                                    <v-col cols="1">
                                        <v-btn class="close-btn" @click="removeCourseGPA">
                                            <span class="material-icons" style="color:black">close</span>
                                        </v-btn>
                                    </v-col>
                                </v-row>

                                <v-row>
                                    <v-col cols="2">
                                        <v-btn @click="addCourseGPA">Add a course</v-btn>
                                    </v-col>
                                    <v-col></v-col>
                                    <v-col cols="2">
                                        <v-btn @click="calculateGPA">Calculate</v-btn>
                                    </v-col>
                                </v-row>
                            </v-form>

                            <v-row>{{GPA}}</v-row>
                        </v-container>
                        <br>
                </div>

                <div class="analytics-page" v-if="this.analytics === true">

                </div>

            </v-col>
    </v-row>
    
    
    
</template>

<script>
    export default {
        data() {
            return {
                tab: 'progress',
                progress: true,
                calculators: false,
                analytics: false,

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
                grades:[
                    { grade: 'A', weight: 4.0 },
                    { grade: 'A-', weight: 3.67 },
                    { grade: 'B+', weight: 3.33 },
                    { grade: 'B', weight: 3.0 },
                    { grade: 'B-', weight: 2.67 },
                    { grade: 'C+', weight: 2.33 },
                    { grade: 'C', weight: 2.0 },
                    { grade: 'C-', weight: 1.67 },
                    { grade: 'D+', weight: 1.33 },
                    { grade: 'D', weight: 1.0 },
                    { grade: 'D-', weight: 0.67 },
                    { grade: 'F', weight: 0.0 },
                    { grade: 'S', weight: 0.0 },
                    { grade: 'U', weight: 0.0 }
                ],

                coursesGPA:[
                    {name:'', credits:'', grade:''},
                    {name:'', credits:'', grade:''},
                    {name:'', credits:'', grade:''},
                    {name:'', credits:'', grade:''},
                ],

                GPA: 0,
            };
        },

        methods:{
            chooseProgress(){
                this.tab = 'progress';
                this.calculators = false;
                this.analytics = false;
                this.progress = true;
            },

            chooseCalculators(){
                this.tab = 'calculators';
                this.progress = false;
                this.analytics = false;
                this.calculators = true;
            },

            chooseAnalytics(){
                this.tab = 'analytics';
                this.calculators = false;
                this.progress = false;
                this.analytics = true;
            },

            addCourseGPA(){
                this.coursesGPA.push({name:'', credits:'', grade:''});
                this.$refs.form.reset()
            },

            removeCourseGPA(index){
                this.coursesGPA.splice(index, 1);
                this.$refs.form.reset()
            },

            calculateGPA(){
            let totalCredits = 0;
                let totalWeightedPoints = 0;

                this.coursesGPA.forEach((course) => {
                const credits = parseFloat(course.credits);
                const gradeInfo = this.grades.find((item) => item.grade === course.grade);

                if (!isNaN(credits) && gradeInfo) {
                    totalCredits += credits;
                    totalWeightedPoints += credits * gradeInfo.weight;
                }
                });

                if (totalCredits > 0) {
                this.GPA = totalWeightedPoints / totalCredits;
                } else {
                this.GPA = 0;
                }
            },
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
    .calculators-page{
        border-left: 1px solid black;
    }

    .calculator-heading{
        font-family: Poppins;
        font-size: 25px;
        margin-left: 9px;
    }

    .calculator-subheading{
        margin-top: -13px;
    }

    .gpa-calculator{
        font-family: Poppins;
        border-radius: 8px;
        min-height: 400px;
        background-color:#e2e2e234;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .gpa-text{
        margin-top: 9px;
        font-size: 22px;
    }

    .exam-calculator{
        font-family: Poppins;
        border-radius: 8px;
        min-height: 400px;
        background-color:#e2e2e234;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    h2 {
        font-family: Poppins;
        text-align: left;
    }

    h1{
        font-family: Poppins;
        text-align: left;
        margin-left: 9px;
    }

    p{
        font-family: Poppins;
        margin-left: 10px;
    }

    .progress-page {
        width: 100%;
        border-left: 1px solid black;
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
        font-family: Poppins;
        font-size: 25px;
        color: #000;
        margin-left: 10px;
    }

    .footer { 
        position: relative;
        bottom: 0; 
        left: 0;
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

    .v-tab{
        font-family: Poppins;
    }

    .selected-tab{
        background-color: rgb(224, 224, 224);
    }
</style>
