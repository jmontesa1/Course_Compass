<!--Created by: John Montesa-->
<!-- This is the courses page for Course Compass -->
<!-- This page prompts the user to select courses based on filters they choose -->
<!-- Courses will have a popup menu that gives details about it -->

<template> 
    <div v-if="userType === 'Student' || userType === 'Admin'">
        <div class="top-row">
        <div class="row">
            <div class="col-sm-2 d-flex flex-column justify-content-end">
                <p style="font-size: 20px; position:relative; top:-4px;" class="text-end">Search:</p>
            </div>
            <div class="col d-flex flex-column">
            <v-row>
                <v-col cols="6">
                    <!--Courses Search Row-->
                    <div class="input-group mb-3">
                        <input type="text" class="form-control" v-model="courseSearch" placeholder="Enter Course Name">
                    </div>                    
                </v-col>
                <v-col cols="3">
                    <!--Department Search Row-->
                    <div class="input-group mb-3">
                        <input type="text" class="form-control" v-model="departmentSearch" placeholder="Enter Department Name">
                    </div>
                </v-col>
                <v-col cols="3">
                    <!--Professor Search Row-->
                    <div class="input-group mb-3">
                        <input type="text" class="form-control" v-model="professorSearch" placeholder="Enter Professor Name">
                    </div>
                </v-col>

            </v-row>
            </div>
            <div class="col-sm-2 d-flex flex-column"></div>
        </div>
            <!--<div class="row">
                <div class="col-sm-2 d-flex flex-column">
                </div>
                <div class="col d-flex flex-column">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="course-search">Course</span>
                        <input type="text" class="form-control" v-model="courseSearch" placeholder="Enter Course Name">
                    </div>
                </div>
                <div class="col-sm-2 d-flex flex-column"></div>
            </div>

            <div class="row">
                <div class="col-sm-2 d-flex flex-column">
                </div>
                <div class="col d-flex flex-column">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="department-search">Department</span>
                        <input type="text" class="form-control" v-model="departmentSearch" placeholder="Enter Department Name">
                    </div>
                </div>
                <div class="col d-flex flex-column">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="professor-search">Professor</span>
                        <input type="text" class="form-control" v-model="professorSearch" placeholder="Enter Professor Name">
                    </div>
                </div>
                <div class="col-sm-2 d-flex flex-column"></div>
            </div>-->
        </div>

        <div class="row">
            <div class="col d-flex flex-column">
                <div class="filter-row">
                    <div class="filter-chips-container">
                        <v-chip class="filter-chips" v-for="(filter, index) in selectedFilters" :key="index" color="darkgrey">
                            {{ filter }}
                        </v-chip>
                    </div>
                </div>
            </div>
            <div class="col-sm-2 d-flex flex-column"></div>
        </div>

        <div class="row">
            <!--LEFT SIDE OF PAGE-->
            <div class="col-md-2 d-flex flex-column">
                <FilterMenu v-model:selectedFilters="selectedFilters" @itemSelected="handleFilterSelected" :open="filterMenuOpen" ></FilterMenu>

                <div class="form-check mb-3" v-if="userType === 'Student'">
                    <label class="form-check-label" for="sortMajorRequirements">
                        <span class="ml-1">Show Courses from Major</span>
                    </label>
                    <input class="form-check-input" type="checkbox" v-model="sortByMajorRequirements" @change="handleFilterSelected('Show Courses from Major')" id="sortMajorRequirements"/>
                </div>
            </div>

            <!--RIGHT SIDE OF PAGE-->
            <div class="col-md-8 d-flex flex-column">
                <div class="course-list">
                    <CourseList :userType="userType" :courses="displayCourses" @addToSchedule="addToSchedule"></CourseList>
                </div>
                <v-pagination :length="totalPages" v-model="currentPage" style="font-family: Poppins"></v-pagination>
            </div>

            <div class="col-md-2 flex-column">
                <div class="enrolled">
                    <v-select
                        :items="instructors"
                        v-model="selectedInstructor"
                        item-value="id"
                        item-title="name"
                        return-object
                        variant="underlined"
                        density="compact"
                        label="Select an Instructor"
                        v-if="userType === 'Admin'"
                        style="margin-top: 10px; color: black; font-family: Poppins;"
                    ></v-select>
                    <p style="font-size: 16px">Cart:</p>
                    <v-chip class="form-control" v-for="course in schedule" :key="course.id" color="darkgrey">
                            <div class="chip-text">{{ course.name }}</div>
                            <v-btn size="extra-small" @click="removeFromSchedule(course)" variant="plain" style="position: relative;">
                                <span class="material-symbols-outlined">
                                    close
                                </span>
                            </v-btn>
                    </v-chip>
                    <v-divider></v-divider>

                    <v-dialog v-model="dialog" max-width="500" style="font-family: Poppins;">
                        <template v-slot:activator="{ props: activatorProps }">
                            <div class="enroll-container">
                                <btn v-bind="activatorProps" class="enroll-button">Enroll</btn>
                            </div>
                        </template>
                        <!--Pop up -->
                        <v-card>
                            <v-card-title v-if="userType === 'Student'">
                                Are you sure you want to enroll in:
                            </v-card-title>
                            <v-card-title v-if="userType === 'Admin'">
                                Are you sure you want to enroll <strong>{{selectedInstructor?.name}}</strong> in:
                            </v-card-title>
                            <v-card-text>
                                <v-row dense>
                                    <v-col>
                                        <v-row v-for="course in schedule" :key="course.id">-{{ course.name }}</v-row>
                                    </v-col>
                                </v-row>
                            </v-card-text> 
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn text="No" variant="plain" @click="dialog = false"></v-btn>
                                <v-btn color="primary" text="Yes" variant="tonal" @click="enrollCourses(selectedInstructor)"></v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </div>
            </div>
        </div>
    <br>
    <br>
    </div>

    <div v-if="userType ==='Instructor'">
        <v-row no-gutters>
            <v-col cols="2">
                <h2 class="welcome-text">
                    Courses Taught 
                </h2>
                <v-divider></v-divider>
                <v-tabs v-model="tab" direction="vertical" color="primary" selected-class="selected-tab" slider-color="black">
                    <v-tab v-for="(course, index) in instructorSchedule" :key="index" :title="course.course" value="tab" @click="chooseTab(index)">
                        {{course.course}}
                    </v-tab>
                </v-tabs>
            </v-col>


            <v-col>
                <div class="course-page" v-if="this.tab===null">
                    <h3 class="course-heading" v-if="this.instructorSchedule.length > 0">Please select a course from the menu.</h3>
                    <h4 class="course-heading" v-if="this.instructorSchedule.length === 0">Please wait for an administrator to enroll you into your taught courses.</h4>
                </div>

                <div class="course-page" v-if="this.coursePage[this.tab] === true">
                    <h3 class="course-heading">{{instructorSchedule[this.tab].course}}</h3>
                    <v-container>
                        <v-row>
                            <v-col cols="8">
                                <v-card style="border: 1px solid black; height: 420px;">
                                    <v-card-title style="font-family:Poppins;">Course Details</v-card-title>
                                    <v-card-text>
                                        <v-divider></v-divider>
                                            <v-sparkline
                                                :key="sparklineKey"
                                                :auto-line-width="false"
                                                :gradient="['#da4d4d', '#51da6e']"
                                                :gradient-direction="'left'"
                                                :line-width="'10'"
                                                :smooth="0"
                                                :model-value="gradeAnalytics"
                                                :padding="'5'"
                                                :type="'bar'"
                                                auto-draw
                                                style="font-family: Poppins;"
                                            >
                                            <template v-slot:label="item">
                                                {{ grades[grades.length - 1 - item.index].grade }}: {{ item.value }}
                                            </template>
                                            </v-sparkline>
                                        <v-divider></v-divider>
                                        <p>Average Grade Distribution: {{courseGradeAverage}}</p>
                                        <br>
                                        <p>S/U Grade Distribution: {{ tallyS }}/{{ tallyU }}</p>
                                </v-card-text>
                                </v-card>
                            </v-col>

                            <v-col cols="4">
                                <v-card style="border: 1px solid black; height: 420px; overflow-y: auto;">
                                    <v-card-title style="font-family:Poppins;">Recent Course Reviews</v-card-title>
                                    <v-card-text>
                                        <v-divider></v-divider>
                                        <v-list lines="auto" style="font-family: Poppins;">
                                            <v-list-header>{{instructorSchedule[this.tab].course}}</v-list-header>
                                            <v-list-item v-for="(review,index) in courseStudents[this.tab].reviews" :key="index">
                                                <template v-slot:title>
                                                    {{courseStudents[this.tab].reviews[index].date}}
                                                </template>
                                                <template v-slot:subtitle>
                                                    <strong>Anonymous</strong> &mdash; {{courseStudents[this.tab].reviews[index].text}}
                                                </template>
                                                <v-divider></v-divider>
                                            </v-list-item>
                                        </v-list>
                                    </v-card-text>
                                </v-card>                            
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="12">
                                <v-card style="border: 1px solid black; min-height: 120px;">
                                    <v-card-title style="font-family:Poppins;">Students</v-card-title>
                                    <v-card-text>
                                        <v-divider></v-divider>
                                        <v-expansion-panels>
                                            <v-expansion-panel>
                                                <v-expansion-panel-title>
                                                        <v-row no-gutters>
                                                            <v-col class="d-flex justify-start" cols="4">
                                                                Students enrolled in {{instructorSchedule[this.tab].course}} ({{this.courseStudents[this.tab].students.length}})
                                                            </v-col>
                                                        </v-row>
                                                </v-expansion-panel-title>
                                                <v-expansion-panel-text>
                                                    <v-row  no-gutters v-for="(student, index) in retrieveCourseStudents" :key="index">
                                                        <v-col cols="11">
                                                            <p class="row-text"><strong>{{ student.name }}</strong>: 
                                                            <span v-if="student.isGraded === false" style="color:#da4d4d;">No grade</span>
                                                            <span v-if="student.isGraded === true" style="color:#51da6e;">Grade: {{student.courseGrade}}</span>
                                                            </p>
                                                        </v-col>
                                                        <v-col cols="1">
                                                            <v-dialog v-model="studentDialog[index]" max-width="500" style="font-family: Poppins;">
                                                                <template v-slot:activator="{ props: activatorProps }">
                                                                    <v-btn v-bind="activatorProps" icon="$close" variant="plain">
                                                                        <span class="material-symbols-outlined">
                                                                            more_horiz
                                                                        </span>
                                                                    </v-btn>
                                                                </template>
                                                                <!--Pop up -->
                                                                <v-card>
                                                                    <v-card-title>
                                                                        <strong>{{instructorSchedule[this.tab].course}}:</strong> {{student.name}}
                                                                    </v-card-title>
                                                                    <v-card-text>
                                                                        <v-row>
                                                                            <v-col cols="auto">
                                                                                <p style="margin-top: 13px;">Grade</p>
                                                                            </v-col>
                                                                            <v-col cols="8">
                                                                                <v-select
                                                                                    clearable
                                                                                    density="compact"
                                                                                    label="Select grade"
                                                                                    v-model="studentGradeSelection"
                                                                                    :items="grades.map(item => item.grade)"
                                                                                ></v-select>
                                                                            </v-col>
                                                                            <v-col cols="auto">
                                                                                <v-dialog v-model="studentGradeDialog[index]" max-width="400" style="font-family: Poppins;">
                                                                                    <template v-slot:activator="{ props: activatorProps }">
                                                                                        <v-btn v-bind="activatorProps" icon="$close" variant="plain">
                                                                                            <span class="material-symbols-outlined">
                                                                                                save
                                                                                            </span>
                                                                                        </v-btn>
                                                                                    </template>
                                                                                    <!--Pop up -->
                                                                                    <v-card title="Save grade">
                                                                                        <v-card-text>
                                                                                            Are you sure you want to save <strong>{{student.name}}'s</strong> grade as <strong>{{this.studentGradeSelection}}</strong>?
                                                                                            <br>
                                                                                        </v-card-text> 
                                                                                        <v-card-actions>
                                                                                            <v-spacer></v-spacer>
                                                                                            <v-btn text="Cancel" variant="plain" @click="studentGradeDialog[index] = false"></v-btn>
                                                                                            <v-btn text="Save" variant="tonal" color="#51da6e" @click="saveStudentGrade(index)"></v-btn>
                                                                                        </v-card-actions>
                                                                                    </v-card>
                                                                                </v-dialog>
                                                                            </v-col>
                                                                        </v-row>
                                                                        <br>
                                                                    </v-card-text> 
                                                                    <v-card-actions>
                                                                        <v-dialog v-model="studentRemoveDialog[index]" max-width="400" style="font-family: Poppins;">
                                                                            <template v-slot:activator="{ props: activatorProps }">
                                                                                <v-btn v-bind="activatorProps" text="Remove Student" variant="tonal" color="red"></v-btn>
                                                                            </template>
                                                                            <!--Pop up -->
                                                                            <v-card title="Remove student">
                                                                                <v-card-text>
                                                                                    Are you sure you want to remove <strong>{{student.name}}</strong> from <strong>{{instructorSchedule[this.tab].course}}</strong>?
                                                                                    <br>
                                                                                </v-card-text> 
                                                                                <v-card-actions>
                                                                                    <v-spacer></v-spacer>
                                                                                    <v-btn text="Cancel" variant="plain" @click="studentRemoveDialog[index] = false"></v-btn>
                                                                                    <v-btn text="Remove" variant="tonal" color="#da4d4d" @click="studentRemoveDialog[index] = false"></v-btn>
                                                                                </v-card-actions>
                                                                            </v-card>
                                                                        </v-dialog>
                                                                        <v-spacer></v-spacer>
                                                                        <v-btn text="Close" variant="plain" @click="studentDialog[index] = false"></v-btn>
                                                                    </v-card-actions>
                                                                </v-card>
                                                            </v-dialog> 
                                                        </v-col>
                                                        <v-divider class="instructor-divider"></v-divider>
                                                    </v-row>
                                                </v-expansion-panel-text>
                                            </v-expansion-panel>
                                        </v-expansion-panels>
                                    </v-card-text>
                                </v-card>                          
                            </v-col>
                        </v-row>
                    </v-container>
                </div>
            </v-col>
        </v-row>       
    </div>
</template>

<script>
    import FilterMenu from '@/components/FilterMenu.vue'
    import CourseList from '@/components/CourseList.vue'
    import axios from 'axios';

    export default{
        name: 'Courses',
        components:
        {
            FilterMenu,
            CourseList,
        },

        props: {
            selectedFilters: {
            type: Array,
            default: () => [],
            },
            userType:{
                type: String,
                required: '',
            },
        },
        watch: {
            selectedFilters(newFilters) {
            this.selectedFilters = newFilters;
            this.fetchDepartments();
            },
            departmentSearch() {
                this.fetchDepartments();
            },
            
            courseSearch() {
                this.fetchCourseCodes();
            }
        },
        data() {
            return {
                courseList: [],
                courseSearch: '',
                departmentSearch: '',
                professorSearch: '',
                sortByMajorRequirements: false,
                schedule: [],
                selectedFilters: [],
                filterMenuOpen: ['Filters'],
                dialog: false,

                //pagination
                currentPage: 1,
                itemsPerPage: 15,

                //instructor page
                instructorSchedule: [],
                tab: null,
                coursePage: [],
                studentDialog: [],
                studentGradeDialog: [],
                studentRemoveDialog: [],
                studentGradeSelection: '',
                courseStudents: [
                    {course: 'COURSE 1', students: [
                        { name: 'Rhys Little', isGraded: false, courseGrade: null },
                        { name: 'Dawson Mahoney', isGraded: false, courseGrade: null },
                        { name: 'Esmee Velazquez', isGraded: false, courseGrade: null },
                        { name: 'Michael Harmon', isGraded: false, courseGrade: null },
                        { name: 'Maariyah Coleman', isGraded: false, courseGrade: null },
                        { name: 'Ricky Kim', isGraded: false, courseGrade: null },
                        { name: 'Gethin Bond', isGraded: false, courseGrade: null },
                        { name: 'Mohamad Gomez', isGraded: false, courseGrade: null },
                        { name: 'Elsa Flynn', isGraded: false, courseGrade: null },
                        { name: 'Kelsie Richards', isGraded: false, courseGrade: null }
                        ],
                        reviews: [
                            { text: 'The course material was outdated and not helpful.', date: 'Jan 12th, 2016' },
                            { text: 'The lectures were confusing and poorly structured.', date: 'Feb 23rd, 2015' },
                            { text: 'Didn\'t find the course engaging or informative.', date: 'Aug 7th, 2023' },
                            { text: 'The content was too basic and not worth the price.', date: 'May 15th, 2018' },
                            { text: 'I expected more from the course but was disappointed.', date: 'Apr 29th, 2024' }
                        ],
                    },

                    {course: 'COURSE 2', students:[
                        { name: 'Miah Serrano', isGraded: false, courseGrade: null },
                        { name: 'Jesse Cook', isGraded: false, courseGrade: null },
                        { name: 'Zohaib Dominguez', isGraded: false, courseGrade: null },
                        { name: 'Ana Carver', isGraded: false, courseGrade: null },
                        { name: 'Jennifer Shepard', isGraded: false, courseGrade: null },
                        { name: 'Mathilda Quinn', isGraded: false, courseGrade: null },
                        { name: 'Keiran Ford', isGraded: false, courseGrade: null },
                        { name: 'Ahmad Lara', isGraded: false, courseGrade: null },
                        { name: 'Brenda Hartman', isGraded: false, courseGrade: null },
                        { name: 'Kathleen Mayo', isGraded: false, courseGrade: null }
                        ],
                        reviews: [
                            { text: 'Great course content, very informative!', date: 'Apr 9th, 2017' },
                            { text: 'Enjoyed the interactive lessons and quizzes.', date: 'Jan 4th, 2022' },
                            { text: 'Highly recommend for anyone new to the subject.', date: 'Jul 18th, 2019' },
                            { text: 'Excellent instructors, clear explanations.', date: 'Oct 25th, 2016' },
                            { text: 'Practical exercises were really helpful.', date: 'Mar 8th, 2020' }
                        ],
                    },
                ],

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

                sparklineKey: 0,
                gradeAnalytics: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], //U S F D- D D+ C- C C+ B- B B+ A- A
                courseGradeAverage: 0,
                tallyS: 0,
                tallyU: 0,


                //Admin variables
                instructors: [],
                selectedInstructor: null,
            };
        },

        computed:{
            //pagination functions
            totalPages(){
                //rounds to highest number for pages
                return Math.ceil(this.courseList.length / this.itemsPerPage);
            },
            displayCourses() {
                const firstCourse = (this.currentPage - 1) * this.itemsPerPage;
                const lastCourse = firstCourse + this.itemsPerPage;
                return this.courseList.slice(firstCourse, lastCourse);
            },
            searchParams() {
                const params = {};

                if (this.selectedFilters.some(filter => /^\d+00\+$/.test(filter))) {
                params.level = this.selectedFilters.find(filter => /^\d+00\+$/.test(filter));
                }

                if (this.selectedFilters.some(filter => /^\d+-\d+\s(?:AM|PM)$/.test(filter))) {
                params.startTime = this.selectedFilters.find(filter => /^\d+-\d+\s(?:AM|PM)$/.test(filter));
                }

                if (this.departmentSearch.trim() !== '') {
                params.query = this.departmentSearch.trim();
                }

                if (this.selectedFilters.some(filter => /^(?:SEM|WPEB)$/.test(filter))) {
                    params.location = this.selectedFilters.find(filter => /^(?:SEM|WPEB|AB|MS|DMSC|PSAC|SLH)$/.test(filter));
                }

                if (this.selectedFilters.some(filter => /^(?:Fall|Winter|Spring|Summer)$/.test(filter))) {
                    const currentYear = new Date().getFullYear();
                    params.term = `${currentYear} ${this.selectedFilters.find(filter => /^(?:Fall|Winter|Spring|Summer)$/.test(filter))}`;
                }
                return params;
            },

            retrieveCourseStudents(){
                const retrieveStudents = this.courseStudents[this.tab].students;
                return retrieveStudents;
            },
        },

        created() {
            this.fetchInstructors();
        },

        methods: {
            fetchCourses() {
                axios.get('http://127.0.0.1:5000/courses', { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }})
                .then(response => {
                    this.courseList = response.data.map(course => ({
                    id: course.courseID,
                    code: course.courseCode,
                    name: course.courseName,
                    department: course.courseMajor,
                    description: course.description,
                    credits: course.Credits,
                    level: course.Level,
                    requirements: course.Requirements,
                    }));
                    console.log('My Account page loaded successfully', response.data)
                })
                .catch(error => {
                console.error("Failed to load:", error);
                });
            },
            /* handleLevelSelection(selectedLevel) {
            const isLevel = /^\d+00$/.test(selectedLevel);
            if (isLevel) {
                this.fetchDepartments(selectedLevel);
            }
            }, */
            fetchDepartments() {
                let baseUrl = 'http://127.0.0.1:5000/search-departments';
                let queryParts = [];

                const selectedLevel = this.selectedFilters.find(filter => /^\d+00$/.test(filter));
                const selectedStartTime = this.selectedFilters.find(filter => /^\d+-\d+\s(?:AM|PM)$/.test(filter));
                const selectedFormat = this.selectedFilters.find(filter => /^(In Person|Online|Hybrid)$/.test(filter));
                const selectedLocation = this.selectedFilters.find(filter => /^(?:SEM|WPEB|AB|MS|DMSC|PSAC|SLH)$/.test(filter));
                const selectedTerm = this.selectedFilters.find(filter => /^(?:Fall|Winter|Spring|Summer)$/.test(filter));
                const selectedRating = this.selectedFilters.find(filter => /^\d+\+\sStars$/.test(filter));

                if (selectedLevel) {
                    queryParts.push(`level=${encodeURIComponent(selectedLevel)}`);
                }

                if (selectedStartTime) {
                    queryParts.push(`startTime=${encodeURIComponent(selectedStartTime)}`);
                }

                if (selectedRating) {
                    const ratingValue = parseInt(selectedRating.split('+')[0]);
                    queryParts.push(`rating=${encodeURIComponent(ratingValue)}`);
                }

                if (selectedFormat) {
                    queryParts.push(`format=${encodeURIComponent(selectedFormat)}`);
                }

                if (this.departmentSearch.trim() !== '') {
                    queryParts.push(`query=${encodeURIComponent(this.departmentSearch.trim())}`);
                }

                if (selectedLocation) {
                    queryParts.push(`location=${encodeURIComponent(selectedLocation)}`);
                }

                if (selectedTerm) {
                    const currentYear = new Date().getFullYear();
                    queryParts.push(`term=${encodeURIComponent(`${currentYear} ${selectedTerm}`)}`);
                }

                let url = queryParts.length > 0 ? `${baseUrl}?${queryParts.join('&')}` : baseUrl;

                axios.get(url, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }})
                    .then(response => {
                        this.courseList = response.data.map(department => ({
                            scheduleID: department.scheduleID,
                            name: department.courseName,
                            section: department.section,
                            code: `${department.courseCode}.${department.section}`,
                            department: department.courseMajor,
                            professor: department.professors,
                            format: department.format,
                            term: department.term,
                            units: department.units,
                            meetingTime: department.meetingTime,
                            location: department.Location,
                            days: department.days ? department.days.split(', ') : [],
                            classCapacity: department.classCapacity,
                            enrollmentTotal: department.enrollmentTotal,
                            availableSeats: department.availableSeats,
                            averageRating: department.averageRating,
                            frequentTags: department.frequentTags,
                        }));
                    })
                    .catch(error => {
                        console.error("Failed to load departments:", error);
                        this.courseList = [];
                    });
            },


            fetchCourseCodes() {
                let baseUrl = 'http://127.0.0.1:5000/search-courses';
                let queryParts = [];

                const selectedLevel = this.selectedFilters.find(filter => /^\d+00$/.test(filter));
                const selectedStartTime = this.selectedFilters.find(filter => /^\d+-\d+\s(?:AM|PM)$/.test(filter));
                const selectedFormat = this.selectedFilters.find(filter => /^(In Person|Online|Hybrid)$/.test(filter));
                const selectedLocation = this.selectedFilters.find(filter => /^(?:SEM|WPEB|AB|MS|DMSC|PSAC|SLH)$/.test(filter));
                const selectedTerm = this.selectedFilters.find(filter => /^(?:Fall|Winter|Spring|Summer)$/.test(filter));
                const selectedRating = this.selectedFilters.find(filter => /^\d+\+\sStars$/.test(filter));

                if (selectedLevel) {
                    queryParts.push(`level=${encodeURIComponent(selectedLevel)}`);
                }

                if (selectedStartTime) {
                    queryParts.push(`startTime=${encodeURIComponent(selectedStartTime)}`);
                }

                if (selectedRating) {
                    const ratingValue = parseInt(selectedRating.split('+')[0]);
                    queryParts.push(`rating=${encodeURIComponent(ratingValue)}`);
                }

                if (selectedFormat) {
                    queryParts.push(`format=${encodeURIComponent(selectedFormat)}`);
                }

                if (this.courseSearch.trim() !== '') {
                    queryParts.push(`courseCode=${encodeURIComponent(this.courseSearch.trim())}`);
                }

                if (selectedLocation) {
                    queryParts.push(`location=${encodeURIComponent(selectedLocation)}`);
                }

                if (selectedTerm) {
                    const currentYear = new Date().getFullYear();
                    queryParts.push(`term=${encodeURIComponent(`${currentYear} ${selectedTerm}`)}`);
                }

                let url = queryParts.length > 0 ? `${baseUrl}?${queryParts.join('&')}` : baseUrl;

                axios.get(url, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }})
                    .then(response => {
                        this.courseList = response.data.map(course => ({
                            scheduleID: course.scheduleID,
                            name: course.courseName,
                            code: course.courseCode,
                            department: course.courseMajor,
                            professor: course.professors,
                            format: course.format,
                            term: course.term,
                            units: course.units,
                            meetingTime: course.meetingTime,
                            location: course.Location,
                            days: course.days ? course.days.split(', ') : [],
                            classCapacity: course.classCapacity,
                            enrollmentTotal: course.enrollmentTotal,
                            availableSeats: course.availableSeats,
                            averageRating: course.averageRating,
                            frequentTags: course.frequentTags,
                        }));
                    })
                    .catch(error => {
                        console.error("Failed to load courses:", error);
                        this.courseList = [];
                    });
            },

            addToSchedule(course) {
                if (!this.schedule.some((c) => c.name === course.name)) {
                    this.schedule.push(course);
                }
                else if (this.schedule.some((c) => c.name === course.name)) {
                    this.$emit("show-toast", { message: course.name + " is already added to your cart."});
                }
            },

            removeFromSchedule(course){
                const index = this.schedule.indexOf(course);
                if(index !== -1){
                    this.schedule.splice(index, 1);
                }
            },

            handleFilterSelected(filter) {
                const index = this.selectedFilters.indexOf(filter);
                if (index !== -1) {
                    this.selectedFilters.splice(index, 1);
                } else {
                    this.selectedFilters.push(filter);
                }
            },

            async enrollCourses(instructor) {
                if(this.userType === 'Student' || this.userType ==='Instructor'){
                    try {
                        const scheduleIDs = this.schedule.map(course => course.scheduleID);

                        const response = await axios.post('http://127.0.0.1:5000/enrollCourses', {
                            studentID: localStorage.getItem('studentID'),
                            scheduleIDs: scheduleIDs
                        }, {
                            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                        });

                        if (response.status === 200) {
                            this.$emit("show-toast", { message: "Courses added to schedule!", color: '#51da6e' });
                            this.schedule = [];
                        }
                    } catch (error) {
                        console.error("Failed to add courses to schedule.", error);
                        let errorMessage = "Failed to add course to schedule."; //default message
                        if (error.response && error.response.data && error.response.data.message) {
                            errorMessage = error.response.data.message; //use  server's error message
                        }
                        this.$emit("show-toast", { message: errorMessage, color: '#da5151' });
                    }
                }
                else if (this.userType === 'Admin') {
                try {
                const scheduleIDs = this.schedule.map(course => course.scheduleID);
                const Instructor = this.selectedInstructor;

                const response = await axios.post('http://127.0.0.1:5000/assignInstructors', {
                    courseId: scheduleIDs[0],
                    instructorIds: [Instructor.id]
                }, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                });

                if (response.status === 200) {
                    const message = response.data.message;
                    if (message.includes("assigned successfully")) {
                    this.$emit("show-toast", { message: "Instructor assigned successfully!", color: '#51da6e' });
                    } else if (message.includes("already assigned")) {
                    this.$emit("show-toast", { message: "Instructor is already assigned to the course.", color: '#da5151' });
                    }
                    this.schedule = [];
                    this.selectedInstructor = null;
                }
                } catch (error) {
                    console.error("Failed to assign instructor.", error);
                    let errorMessage = "Failed to assign instructor.";
                    if (error.response && error.response.data && error.response.data.message) {
                        errorMessage = error.response.data.message;
                    }
                    this.$emit("show-toast", { message: errorMessage, color: '#da5151' });
                    }
                }

                this.dialog = false;
            },

            //instructor page functions
            async fetchEnrolledCourses() {
                try {
                    const response = await axios.get('http://127.0.0.1:5000/getEnrolledCourses', {
                        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                    });
                    this.instructorSchedule = response.data.enrolledCourses.map(course => ({
                        ...course,
                        scheduleID: course.scheduleID
                    }));
                } catch (error) {
                    console.error("Error fetching enrolled courses:", error);
                }
            },

            chooseTab(index){
                this.tab = index;
                this.coursePage[this.tab] = true;
                this.getGradeAnalytics();
            },

            saveStudentGrade(index){
                this.courseStudents[this.tab].students[index].isGraded = true;
                this.courseStudents[this.tab].students[index].courseGrade = this.studentGradeSelection;

                this.studentGradeSelection = '';
                this.studentGradeDialog[index] = false;
                this.getGradeAnalytics();
            },

            getGradeAnalytics(){
                const tallyGrades = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; //U S F D- D D+ C- C C+ B- B B+ A- A
                let tally = 0;
                let sCount = 0;
                let uCount = 0;
                let totalWeight = 0;
                const currentCourse = this.courseStudents[this.tab];

                if (currentCourse) {
                    currentCourse.students.forEach(student => {
                        if (student.isGraded && student.courseGrade !== null) {
                            switch (student.courseGrade) {
                                case 'U':
                                    tallyGrades[0]++;
                                    uCount++;
                                    break;
                                case 'S':
                                    tallyGrades[1]++;
                                    sCount++;
                                    break;
                                case 'F':
                                    tallyGrades[2]++;
                                    tally++;
                                    break;
                                case 'D-':
                                    tallyGrades[3]++;
                                    tally++;
                                    totalWeight += 0.67;
                                    break;
                                case 'D':
                                    tallyGrades[4]++;
                                    tally++;
                                    totalWeight += 1.0;
                                    break;
                                case 'D+':
                                    tallyGrades[5]++;
                                    tally++;
                                    totalWeight += 1.33;
                                    break;
                                case 'C-':
                                    tallyGrades[6]++;
                                    tally++;
                                    totalWeight += 1.67;
                                    break;
                                case 'C':
                                    tallyGrades[7]++;
                                    tally++;
                                    totalWeight += 2.0;
                                    break;
                                case 'C+':
                                    tallyGrades[8]++;
                                    tally++;
                                    totalWeight += 2.33;
                                    break;
                                case 'B-':
                                    tallyGrades[9]++;
                                    tally++;
                                    totalWeight += 2.67;
                                    break;
                                case 'B':
                                    tallyGrades[10]++;
                                    totalWeight += 3.0;
                                    break;
                                case 'B+':
                                    tallyGrades[11]++;
                                    tally++;
                                    totalWeight += 3.33;
                                    break;
                                case 'A-':
                                    tallyGrades[12]++;
                                    tally++;
                                    totalWeight += 3.67;
                                    break;
                                case 'A':
                                    tallyGrades[13]++;
                                    tally++;
                                    totalWeight += 4.0;
                                    break;
                            }
                        }
                    });
                }

                if(tally!=0){this.courseGradeAverage = (totalWeight/tally).toFixed(2);}
                else{this.courseGradeAverage = 0}
                this.tallyS = sCount;
                this.tallyU = uCount;
                this.sparklineKey++;
                this.gradeAnalytics = tallyGrades;
            },

            async fetchInstructors() {
                try {
                    const response = await axios.get('http://127.0.0.1:5000/getInstructors', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                    });
                    this.instructors = response.data.instructors.map(instructor => ({
                    id: instructor.instructorID,
                    name: instructor.name
                    }));
                    console.log("Instructors data:", this.instructors);
                } catch (error) {
                    console.error("Error fetching instructors:", error);
                }
            },
        },

        mounted() {
            this.coursePage = new Array(this.instructorSchedule.length).fill(false);

            this.fetchDepartments();
            this.fetchEnrolledCourses(); //enrolled courses data
        },
    }
</script>

<style scoped>

    .coursepage-container{
        position: relative;
        left: 50%;
        transform: translateX(-50%);
        max-width: 94%;
        border-radius: 1px;
    }

    p{
        font-family: 'Poppins', sans-serif;
        font-size: 14px;
    }
    h1{
        font-family: 'Coolvetica';
        text-align: left;
        margin-top: -11px;
        margin-left: 16px;
    }


    .chip-text{
        width: 165px;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .input-group-text{
        font-family: 'Poppins', sans-serif;
        font-size: 14px;
        height: 35px;
    }

    .form-control{
        font-family: 'Poppins', sans-serif;
        font-size: 14px;
        margin-bottom: 5px;
    }

    .form-check-label{
        font-family: 'Poppins', sans-serif;
        font-size: 14px;
    }

    .form-check-input{
        margin-left: 0px;
    }

    .selected-filters{
        font-family: Poppins;
        font-size: 14px;
    }
    
    .top-row{
        margin-top: 15px;
    }

    .enrolled{
        margin-left: -7px;
        max-width: 210px;
        border-top: black 1px solid;

    }

    .filter-row {
        max-width: 100%;
    }

    .filter-chips-container {
        flex-wrap: nowrap;
        overflow-x: auto;
        width: 100%;
    }

    .filter-chips {
        margin-right: 5px;
        margin-bottom: 5px;
        white-space: nowrap;
    }

    .cancel-icon{
        margin-left: 6px;
    }

    .enroll-container{
        display:flex;
        justify-content: space-between;
    }
    .enroll-button {
        margin-left:auto;
        position: relative;
        font-family: Poppins;
        background-color: #000000;
        color: #ffffff;
        padding: 5px 10px;
        font-size: 15px;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s linear, color 0.3s linear;
        text-decoration: none;
    }

    .enroll-button:hover {
        background-color: #ffffff;
        color: #000000;
    }



    /*Instructors Page */
    .v-tab{
        font-family: Poppins;
    }

    .selected-tab{
        background-color: rgb(224, 224, 224);
    }

    .welcome-text{
        font-family: Poppins;
        font-size: 28px;
        margin-left: 10px;
        margin-top: 13px;
    }

    .course-page{
        border-left: 1px solid black;
        height: 100% ;
    }

    .course-heading{
        font-family: Poppins;
        position: relative;
        top: 12px;
        margin-left: 10px;
        font-size: 24px;
    }

    .row-text{
        margin-top: 15px;
    }
</style>