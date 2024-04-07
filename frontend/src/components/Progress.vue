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
                        <h1>Progress</h1>
                        <div class="container-fluid mt-3">
                            <div class="row">
                                <div class="col-md d-flex flex-column" style="border-right: 1px solid black;">
                                    <h2>Career</h2>
                                    <p>
                                    <strong>Major: </strong>
                                    <span v-if="dataLoaded">{{ majorName }}</span>
                                    <span v-else> </span>
                                    </p>
                                    <p><strong>Term:</strong> {{ currentTerm }}</p>
                                    <p>
                                    <strong>Class Standing: </strong>
                                    <span v-if="dataLoaded">{{ calculateClassStanding }}</span>
                                    <span v-else> </span>
                                    </p>
                                    <p><strong>Current GPA:</strong> {{ currentGPA }}</p>
                                    <p><strong>Current Credits:</strong> {{ currentCredits }}</p>
                                    <p><strong>Dean's List?:</strong> N/A</p>
                                    <p><strong>Academic Standing:</strong> Good Standing</p>
                                    <p><strong>Credits Completed:</strong> {{ unitsCompleted }}/{{ major.units }}</p>
                                    <v-btn class="save-changes-btn" color="success" @click="confirmationDialog = true" size="small">Save Progress</v-btn>
                                </div>
                                <div class="col-md-6 d-flex flex-column">
                                    <h2>Courses</h2>
                                    <div class="scroll"> 
                                        <div v-for="(course, index) in major.courses" :key="index">
                                            <div class="course-container">
                                                <input type="checkbox" v-model="course.completed" @change="course.changed = true" :disabled="isCourseSaved(course)" />
                                                <v-expansion-panels>
                                                    <v-expansion-panel>
                                                        <v-expansion-panel-title>
                                                            <label>{{ course.name }}</label>
                                                        </v-expansion-panel-title>
                                                        <v-expansion-panel-text>
                                                            <p>Credits: {{ course.credits }}</p>
                                                            <div>
                                                                <label>Tags:</label>
                                                                <div class="tag-container">
                                                                    <span
                                                                        v-for="(tag, tagIndex) in availableTags"
                                                                        :key="tagIndex"
                                                                        class="tag"
                                                                        :class="{ selected: isTagSelected(course, tag), disabled: course.tags.length === 4 && !isTagSelected(course, tag) }"
                                                                        @click="toggleTag(course, tag)"
                                                                    >
                                                                        {{ tag.name }}
                                                                    </span>
                                                                    <label>Your Rating:</label>
                                                                        <v-rating
                                                                        v-model="course.studentRating"
                                                                        :length="5"
                                                                        color="yellow darken-3"
                                                                        background-color="grey lighten-1"
                                                                        empty-icon="$ratingEmpty"
                                                                        hover
                                                                        @input="course.changed = true"
                                                                        ></v-rating>
                                                                </div>
                                                            </div>
                                                            <br>
                                                            <p v-if="course.review">Your Review: {{ course.review }}</p>
                                                            <v-textarea
                                                            v-model="course.review"
                                                            label="Your Thoughts"
                                                            placeholder="Enter your review for this course"
                                                            @input="course.changed = true"
                                                            ></v-textarea>
                                                        </v-expansion-panel-text>
                                                    </v-expansion-panel>
                                                </v-expansion-panels>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <v-dialog v-model="confirmationDialog" max-width="500" style="font-family: Poppins;">
                      <v-card>
                        <v-card-title class="headline">Confirm Changes</v-card-title>
                        <v-card-text>Are you sure you want to save your progress?</v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn text @click="confirmationDialog = false">Cancel</v-btn>
                            <v-btn color="primary" text @click="saveAllChanges">Save</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                    
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
                    <v-container class="grade-calculator">
                            <v-row>
                                <h1 class="calculator-heading">Final Grade Calculator</h1>
                            </v-row>

                            <v-row class="calculator-subheading">
                                <v-col>Course</v-col>
                                <v-col>Credits</v-col>
                                <v-col>Grade</v-col>
                            </v-row>

                            <v-form ref="form">
                                <v-row style="height:70px;">
                                    <v-col>
                                        <v-text-field v-model="currentGrade" label="Your Current Grade">
                                        </v-text-field>
                                    </v-col>
                                    <v-col>                
                                        <v-text-field v-model="targetGrade" label="Target Grade"></v-text-field>
                                    </v-col>
                                    <v-col>
                                        <v-text-field v-model="finalExamWeight" label="Final Exam Weight"></v-text-field>
                                    </v-col>
                                </v-row>

                                <v-row>
                                    <v-col cols="2">
                                    </v-col>
                                    <v-col></v-col>
                                    <v-col cols="2">
                                        <v-btn @click="calculateFinalGrade">Calculate</v-btn>
                                    </v-col>
                                </v-row>
                            </v-form>

                            <v-row>
                                <p class="gpa-text">To achieve your target grade, you need a {{ finalGradeCalculation }}% on the final exam.</p>
                            </v-row>
                        </v-container>
                        <br>
                </div>

                <div class="analytics-page" v-if="this.analytics === true">

                </div>

            </v-col>
    </v-row>
    
    
    
</template>

<script>
    import axios from 'axios'

    export default {
        data() {
            return {
                confirmationDialog: false,
                tab: 'progress',
                progress: true,
                calculators: false,
                analytics: false,
                classStanding: '',
                dataLoaded: false,
                studentRating: 0,
                currentTerm: '',
                currentCredits: 0,
                currentGPA: 0,

                unitsCompleted: 0,
                user: {
                    firstname: '',
                    lastname: '',
                    email: '',
                    major: '',
                },
                majors: [
                {
                    name: '',
                    units: 0,
                    courses: [],
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

                //Final Grade Calculator
                currentGrade: null,
                targetGrade: null,
                finalExamWeight: null,
                finalGradeCalculation: 0,
                majorName: '',

                availableTags: [],

            };
        },

        methods:{
            handleToast(toastData) {

            console.log(toastData.message);
            },

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

            calculateFinalGrade(){
                const currentGrade = parseFloat(this.currentGrade);
                const targetGrade = parseFloat(this.targetGrade);
                const finalExamWeight = parseFloat(this.finalExamWeight) / 100;

                const finalGrade = (targetGrade - (1 - finalExamWeight) * currentGrade) / finalExamWeight;
                this.finalGradeCalculation = finalGrade.toFixed(2);
            },

            async fetchUserCourses() {
                try {
                    const response = await axios.get('http://127.0.0.1:5000/getCourseProgress', {
                        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                    });

                    let majorToUpdate = this.majors.find(major => major.name === this.user.major);

                    if (majorToUpdate) {
                        majorToUpdate.courses = response.data.user_courses.map(course => ({
                            name: `${course.courseCode}: ${course.courseName}`,
                            completed: course.isCompleted === 1,
                            changed: false,
                            credits: course.credits,
                            review: course.review || '',
                            saved: course.isCompleted === 1,
                            tags: course.tags || [], //empty array of tags
                            studentRating: course.studentRating || 0,
                        }));

                        majorToUpdate.units = response.data.totalCreditsReq;
                    }
                    this.dataLoaded = true;
                } catch (error) {
                    console.error("Error fetching user courses", error.message);
                }
            },

            async fetchCareerProgress() {
                try {
                    const response = await axios.get('http://127.0.0.1:5000/getCareerProgress', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                    });
                    this.majorName = response.data.majorName;
                    this.currentTerm = response.data.Term;
                    this.currentCredits = response.data.totalCredits;
                    this.currentGPA = response.data.cumulativeGPA;
                } catch (error) {
                    console.error("Error fetching career progress", error.message);
                }
            },

            async saveAllChanges() {
                const updatePromises = this.majors.flatMap(major =>
                    major.courses.filter(course => course.changed).map(course => {
                        course.saved = course.completed;
                        return axios.post('http://127.0.0.1:5000/markCourseCompleted', {
                            courseCode: course.name.split(':')[0],
                            completed: course.completed ? 1 : 0,
                            review: course.review,
                            tags: course.tags.map(tag => tag.id), //send tagID values
                            studentRating: course.studentRating, //send rating integer(star)
                        }, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } });
                    })
                );

                try {
                    await Promise.all(updatePromises);
                    console.log('All changes saved successfully');
                    this.$emit('show-toast', { message: 'Progress saved.', color: '#51da6e' });
                    this.confirmationDialog = false;
                } catch (error) {
                    console.error('Error saving changes:', error);
                    this.$emit('show-toast', { message: 'Error saving progress. Please try again.', color: '#da6e51' });
                }
            },

            toggleTag(course, tag) {
                const index = course.tags.findIndex(t => t.id === tag.id);
                if (index > -1) {
                    course.tags.splice(index, 1);
                    course.changed = true;
                } else {
                    if (course.tags.length < 4) {
                        course.tags.push({ id: tag.id });
                        course.changed = true;
                    }
                }
            },

            async fetchTags() {
                try {
                    const response = await axios.get('http://127.0.0.1:5000/getTags');
                    this.availableTags = response.data.tags;
                } catch (error) {
                    console.error('Error fetching tags:', error);
                }
            },

            isTagSelected(course, tag) {
                return course.tags && course.tags.some(t => t.id === tag.id);
            },
        },
    
        created() {
            this.selectedMajor = this.user.major; 
            this.fetchUserCourses();
            this.fetchTags();
            this.fetchCareerProgress();
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
                        completedUnits += course.credits; //using the credits value of each course
                    }
                });

                const totalUnits = this.majors.find((major) => major.name === this.user.major).units;
                this.unitsCompleted = completedUnits;
                return (completedUnits / totalUnits) * 100;
            },

            isCourseSaved() {
                return (course) => course.saved;
            },

            calculateClassStanding() {
                if (this.unitsCompleted >= 90) {
                return 'Senior';
                } else if (this.unitsCompleted >= 60) {
                return 'Junior';
                } else if (this.unitsCompleted >= 30) {
                return 'Sophomore';
                } else {
                return 'Freshman';
                }
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
        background-color:#e2e2e25d;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-left: 35px;
        margin-right: 5px;
    }

    .gpa-text{
        margin-top: 9px;
        font-size: 22px;
    }

    .grade-calculator{
        font-family: Poppins;
        border-radius: 8px;
        min-height: 250px;
        background-color:#e2e2e234;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-left: 35px;
        margin-right: 5px;
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
        display: flex;
        align-items: center;
        align-items: center;
        display: flex;
        align-items: center;
        display: flex;
        margin-bottom: 8px;
    }

    .course-container input[type="checkbox"] {
        margin-right: 8px;
    }

    .scroll {
        overflow-x: auto;
        width: 100%;
        height: 50vh;
    }

    .v-tab{
        font-family: Poppins;
    }

    .selected-tab{
        background-color: rgb(224, 224, 224);
    }

    .save-changes-btn{
        font-family: Poppins;
        max-width: 20%;
    }

    .tag-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 8px;
    }

    .tag {
        background-color: #e0e0e0;
        border-radius: 16px;
        padding: 4px 12px;
        cursor: pointer;
        user-select: none;
        transition: background-color 0.3s, color 0.3s;
    }

    .tag.selected {
        background-color: #364db3;
        color: white;
    }

    .tag.disabled {
        background-color: #e0e0e0;
        color: #a0a0a0;
        cursor: not-allowed;
    }
</style>
