<!--Created by: John Montesa-->
<!-- This is the courses page for Course Compass -->
<!-- This page prompts the user to select courses based on filters they choose -->
<!-- Courses will have a popup menu that gives details about it -->

<template>   
    <div class="top-row">
        <div class="row">
            <div class="col-sm-2 d-flex flex-column">
                <h1>Courses</h1>
            </div>
            <div class="col d-flex flex-column">
                <!--Courses Search Row-->
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
                <!--Department Search Row-->
                <div class="input-group mb-3">
                    <span class="input-group-text" id="department-search">Department</span>
                    <input type="text" class="form-control" v-model="departmentSearch" placeholder="Enter Department Name">
                </div>
            </div>
            <div class="col d-flex flex-column">
                <!--Professor Search Row-->
                <div class="input-group mb-3">
                    <span class="input-group-text" id="professor-search">Professor</span>
                    <input type="text" class="form-control" v-model="professorSearch" placeholder="Enter Professor Name">
                </div>
            </div>
            <div class="col-sm-2 d-flex flex-column"></div>
        </div>

    </div>

    <div class="row">
        <div class="col-sm-2 d-flex flex-column"></div>

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

            <div class="form-check mb-3">
                <label class="form-check-label" for="sortMajorRequirements">
                    <span class="ml-1">Show Courses from Major</span>
                </label>
                <input class="form-check-input" type="checkbox" v-model="sortByMajorRequirements" @change="handleFilterSelected('Show Courses from Major')" id="sortMajorRequirements"/>
            </div>
        </div>

        <!--RIGHT SIDE OF PAGE-->
        <div class="col-md-8 d-flex flex-column">
            <div class="course-list">
                <CourseList :courses="displayCourses" @addToSchedule="addToSchedule"></CourseList>
            </div>
            <v-pagination :length="totalPages" v-model="currentPage" style="font-family: Poppins"></v-pagination>
        </div>

        <div class="col-md-2 flex-column">
            <div class="enrolled">
                <p>Cart:</p>
                <v-chip class="form-control" v-for="course in schedule" :key="course.id" color="darkgrey" closable @click:close="removeFromSchedule(course)">
                        <div class="chip-text">{{ course.name }}</div>
                </v-chip>
                <v-divider></v-divider>

                <v-dialog v-model="dialog" max-width="500" style="font-family: Poppins;">
                    <template v-slot:activator="{ props: activatorProps }">
                        <div class="enroll-container">
                            <btn v-bind="activatorProps" class="enroll-button">Enroll</btn>
                        </div>
                    </template>
                    <!--Pop up -->
                    <v-card title="Are you sure you want to enroll in:">
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
                            <v-btn color="primary" text="Yes" variant="tonal" @click="enrollCourses()"></v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </div>
        </div>
    </div>
<br>
<br>
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
                            code: department.courseCode,
                            department: department.courseMajor,
                            professor: department.professor,
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
                            professor: course.professor,
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

            async enrollCourses() {
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
                this.dialog = false;
            }
        },
        mounted() {
            this.fetchDepartments();
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
        font-family: 'coolvetica', coolvetica;
        text-align: left;
        margin-top: -11px;
        margin-left: 16px;
    }
    h2{
        font-family: 'coolvetica', coolvetica;
        text-align: left;
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
        font-family: coolvetica;
        background-color: #000000;
        color: #ffffff;
        padding: 5px 10px;
        font-size: 15px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s linear, color 0.3s linear;
        text-decoration: none;
    }

    .enroll-button:hover {
        background-color: #ffffff;
        color: #000000;
    }

</style>