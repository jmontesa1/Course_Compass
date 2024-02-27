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
                    <p class="selected-filters">Applied Filters: {{ selectedFilters }}</p>
                    <v-chip class="filter-chips" v-for="(filter, index) in selectedFilters" :key="index" color="darkgrey">
                        {{ filter }}
                        <v-icon @click="handleFilterSelected(filter)" class="cancel-icon">
                            <span class="material-icons" style="color:black;">cancel</span>
                        </v-icon>
                    </v-chip>
                </div>
            </div>
        </div>
        <div class="col-sm-2 d-flex flex-column"></div>
    </div>

    <div class="row">
        <!--LEFT SIDE OF PAGE-->
        <div class="col-md-2 d-flex flex-column">
            <!--Sort by Major Requirements Row-->

            <FilterMenu v-model:selectedFilters="selectedFilters" @itemSelected="handleFilterSelected" :open="filterMenuOpen" ></FilterMenu>

            <div class="form-check mb-3">
                <label class="form-check-label" for="sortMajorRequirements">
                    <span class="ml-1">Show Courses from Major</span>
                </label>
                <input class="form-check-input" type="checkbox" v-model="sortByMajorRequirements" @change="handleFilterSelected('Show Courses from Major')" id="sortMajorRequirements"/>
            </div>
        </div>

        <!--RIGHT SIDE OF PAGE-->
        <div class="col d-flex flex-column">
            <CourseList :courses="courseList" @addToSchedule="addToSchedule"></CourseList>
        </div>

        <div class="col-md-2 flex-column">
            <div class="enrolled">
                <p>Enrolled:</p>
                <v-chip class="form-control" v-for="course in schedule" :key="course.id" color="darkgrey" closable @click:close="removeFromSchedule(course)">
                        <div class="chip-text">{{ course.name }}</div>
                </v-chip>
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
        //Import components and Data
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
        },
        data() {
            return {
                courseList: [],
                departmentSearch: '',
                professorSearch: '',
                sortByMajorRequirements: false,
                schedule: [],
                selectedFilters: [],
                filterMenuOpen: ['Filters'],
                //Hardcoded course list for now, will work on getting data from database later
                courseList: [
                        { department: 'CS', name: 'CS 425 - Software Engineering', professor: ['Sara Davis', 'Vinh Le'], rating: 4.5, level: '400+', startTime: '10-11 AM',
                        keywords: ['Attendance', 'Lecture Heavy', 'Textbook Required', 'Projects'], location: 'WPEB 130', format: 'In-Person', requirement: 'N/A',
                        term: 'Fall 2023', program: 'Undergraduate', days: ['Tuesday', 'Thursday'], meetingtime:'10:30 AM - 11:45 AM', units: '3.0',
                        prerequisites: 'CS 446', status: 'Waitlist', section: '1001' },
                    ],
            };
        },

        methods: {
            fetchCourses() {
                axios.get('http://127.0.0.1:5000/courses', { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }})
                .then(response => {
                    this.courseList = response.data.map(course => ({
                    id: course.courseID,
                    code: course.courseCode,
                    name: course.courseName,
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
            addToSchedule(course) {
                if (!this.schedule.some((c) => c.name === course.name)) {
                    this.schedule.push(course);
                }
                else if (this.schedule.some((c) => c.name === course.name)) {
                    this.$emit("show-toast", course.name + " is already added to your schedule.");
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
        },
        created() {
            this.fetchCourses();
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
    }

    .form-control{
        font-family: 'Poppins', sans-serif;
        font-size: 14px;
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
        max-width: 100%; /* Ensure the container doesn't expand beyond the column */
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
</style>
