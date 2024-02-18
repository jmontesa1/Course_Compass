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
            <div>
                <p class="selected-filters">Applied Filters: {{ selectedFilters }}</p>
            </div>
        </div>
        <div class="col-sm-2 d-flex flex-column"></div>
    </div>

    <div class="row">
        <!--LEFT SIDE OF PAGE-->
        <div class="col-md-2 d-flex flex-column">
            <!--Sort by Major Requirements Row-->

            <FilterMenu :selected="selectedFilters" @itemSelected="handleFilterSelected" :open="filterMenuOpen" ></FilterMenu>

            <div class="form-check mb-3">
                <label class="form-check-label" for="sortMajorRequirements">
                    <span class="ml-1">Only Show Courses from Major</span>
                </label>
                <input class="form-check-input" type="checkbox" v-model="sortByMajorRequirements" @change="handleFilterSelected('Only Show Courses from Major')" id="sortMajorRequirements"/>
            </div>
        </div>

        <!--RIGHT SIDE OF PAGE-->
        <div class="col d-flex flex-column">
            <CourseList :courses="courseList" @addToSchedule="addToSchedule"></CourseList>
        </div>

        <div class="col-md-2 flex-column">
            <div class="enrolled">
                <h2>Enrolled:</h2>
                <div v-for="(course, index) in schedule" :key="index" class="schedule-item">
                    {{ course.name }}
                </div>
            </div>
        </div>

    </div>

    <br>
    <br>
</template>

<script>
    import FilterMenu from '@/components/FilterMenu.vue'
    import CourseList from '@/components/CourseList.vue'


    export default{
        //Import components and Data
        name: 'Courses',
        components:
        {
            FilterMenu,
            CourseList
        },
        data() {
            return {
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
        
                        { name: 'this is a projected course'},
                        { name: 'this is a projected course' },
                        { name: 'this is a projected course' },
                        { name: 'this is a projected course' },
                        { name: 'this is a projected course' },
                        { name: 'this is a projected course' },
                        { name: 'this is a projected course' },
                        { name: 'this is a projected course' },
                        { name: 'this is a projected course' },
                        { name: 'this is a projected course' },
                        { name: 'this is a projected course' },
                        { name: 'this is a projected course' },
                        { name: 'this is a projected course' },
                        { name: 'this is a projected course' },
                        { name: 'this is a projected course' },
                        //Add more courses as needed
                    ],
            };
        },

        methods: {
            addToSchedule(course) {
                if (!this.schedule.some((c) => c.name === course.name)) {
                    this.schedule.push(course);
                }
            },
            handleFilterSelected(item) {
                // Check if the item is already in the selectedFilters array
                const index = this.selectedFilters.indexOf(item);

                if (index !== -1) {
                    // If the item is already selected, remove it
                    this.selectedFilters.splice(index, 1);
                } else {
                    // If the item is not selected, add it
                    this.selectedFilters.push(item);
                }
            },
            
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
        font-size: 20px;
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
        margin-left: -15px;
    }
</style>