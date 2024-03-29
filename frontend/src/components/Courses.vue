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
                                <v-col cols = "12" md="6">
                                    <v-row v-for="course in schedule" :key="course.id">{{ course.name }}</v-row>
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
            },
            departmentSearch() {
                this.fetchDepartments();
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
                courseList: [],
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
            fetchDepartments() {
                if (this.departmentSearch.trim() === '') {
                    this.courseList = [];
                    return;
                }

                axios.get(`http://127.0.0.1:5000/search-departments?query=${encodeURIComponent(this.departmentSearch)}`, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }})
                .then(response => {
                    this.courseList = response.data.map(department => ({
                        name: department.courseName,
                        code: department.courseCode,
                        department: department.courseMajor,
                        professor: department.professor,
                        format: department.format,
                        term: department.term,
                        units: department.units,
                        meetingTime: department.meetingTime,
                        location: department.Location,
                        days: department.days ? department.days.split(', ') : []
                    }));
                })
                .catch(error => {
                    console.error("Failed to load departments:", error);
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
                    const courseCodes = this.schedule.map(course => course.courseCode);

                    const response = await axios.post('http://127.0.0.1:5000/enrollCourses', {
                        email: localStorage.getItem('userEmail'),
                        courses: courseCodes
                    }, {
                        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                    });

                    if (response.status === 200) {
                        this.$emit("show-toast", { message: "Courses added to schedule!", color: '#51da6e' });
                        this.schedule = [];
                    }
                } catch (error) {
                        console.error("Failed to add courses to schedule.", error);
                        this.$emit("show-toast", { message: "Failed to add courses to schedule.", color: '#da5151' });
                }
            }
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