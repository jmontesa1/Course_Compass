<!--Created by: John Montesa-->
<!-- This is the courses page for Course Compass -->
<!-- This page prompts the user to select courses based on filters they choose -->
<!-- Courses will have a popup menu that gives details about it -->

<template>
    <h1>Courses</h1>

    <div class="coursepage-container">

        <div class="row">
            <!--LEFT SIDE OF PAGE-->
            <div class="col-md-2 d-flex flex-column">
                <!--Department Search Row-->
                <div class="input-group mb-3">
                    <span class="input-group-text" id="department-search">Department</span>
                    <input type="text" class="form-control" v-model="departmentSearch" placeholder="Enter Department Name">
                </div>
                <!--Professor Search Row-->
                <div class="input-group mb-3">
                    <span class="input-group-text" id="professor-search">Professor</span>
                    <input type="text" class="form-control" v-model="professorSearch" placeholder="Enter Professor Name">
                </div>
                <!--Sort by Major Requirements Row-->
                <div class="form-check mb-3">
                    <label class="form-check-label" for="sortMajorRequirements">
                        <span class="ml-1">Only Show Courses from Major</span>
                    </label>
                    <input class="form-check-input" type="checkbox" v-model="sortByMajorRequirements" id="sortMajorRequirements">
                </div>
                <FilterMenu></FilterMenu>
            </div>

            <!--RIGHT SIDE OF PAGE-->
            <div class="col d-flex flex-column">
                <CourseList :courses="courseList"></CourseList>
            </div>

            <div class="col-md-2 flex-column">
                    <div class="schedule">
                    <h2>Enrolled:</h2>
                        <div v-for="(course, index) in schedule" :key="index" class="schedule-item">
                            {{ course.name }}
                        </div>
                    </div>
            </div>

        </div>
    </div>
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
    }
</script>

<style scoped>

    .coursepage-container{
        position: relative;
        left: 50%;
        transform: translateX(-50%);
        max-width: 94%;
        border-radius: 1px;
        border-left: 1px solid black;
        border-top: 1px solid black;
    }
    p{
        font-family: 'Poppins', sans-serif;
        font-size: 20px;
    }
    h1{
        font-family: 'coolvetica', coolvetica;
        text-align: left;
        margin-left: 13px;
    }
    h2{
        font-family: 'coolvetica', coolvetica;
        text-align: left;
    }

    .input-group-text{
        font-family: 'Poppins', sans-serif;
        font-size: 15px;
    }
    .form-control{
        font-family: 'Poppins', sans-serif;
        font-size: 15px;
    }
    .form-check-label{
        font-family: 'Poppins', sans-serif;
        font-size: 15px;
    }
</style>