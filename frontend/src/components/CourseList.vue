<!-- Created by: John Montesa -->
<!-- This component creates the courses list that the user will interact with -->
<!-- Classes are displayed in a list matter, where the background color alternates from each course to provide better readability -->
<!-- Each item is shown as their course department, course number, and name of course -->


<template>
    <!--Loading animation-->
    <div class="loading" v-if="courses.length === 0">
        <v-progress-circular indeterminate :width="5"></v-progress-circular>
    </div>
    <!-- Display the courses in a list -->
    <div class="course-list">
        <v-dialog v-model="dialog" max-width="1000">
            <template v-slot:activator="{ props: activatorProps }">
                <div v-bind="activatorProps" v-for="(course, index) in courses" :key="index" class="course-item" @click="handleCourseClick(course)">
                    {{ course.code }}: {{ course.name }}
                    <span class="material-icons" style="color:black;">north_east</span>
                </div>
            </template>
            <!--Pop up pulled from CourseDetailsPopup component-->
            <CourseDetailsPopup :userType="userType" v-if="selectedCourse" :course="selectedCourse" @close="closePopup" @addToSchedule="addToSchedule" /> 
        </v-dialog>
    </div>
</template>

<script>
    import CourseDetailsPopup from '@/components/CourseDetailsPopup.vue';
    export default {
        //the courses are passed in as a prop array
        props: {
            courses: Array,
            userType:{
                type: String,
                required: '',
            },
        },
        data() {
            return {
                selectedCourse: null,
                schedule: [],
                notification: null,
                dialog: false,
            };
        },
        methods: {
            //Chooses selected course
            handleCourseClick(course) {
                this.selectedCourse = course;
            },
            
            //handles popup closing
            closePopup() {
                this.selectedCourse = null;
                this.notification = null;
                this.dialog = false;
            },

            //Adds course to user schedule
            addToSchedule(course) {
                this.$emit("addToSchedule", course);
                if (!this.schedule.some((c) => c.name === course.name)) {
                    this.schedule.push(course);
                    this.selectedCourse = null; // Close the popup after adding to the schedule
                    this.notification = null; // Clear any existing notifications
                }
                this.dialog = false;
            },
            
            //Shows popup
            showNotification(message, isError = false) {
                this.notification = {
                    message,
                    isError,
                };
            },

            //Closes popup
            clearNotification() {
                this.notification = null;
            },

        },
        components: {
            CourseDetailsPopup,
            },
        };
</script>

<style scoped>
    .course-list {
        width: 100%;
        flex-direction: column;
    }

    .course-item {
        font-family: coolvetica;
        font-size: 25px;
        padding: 8px;
        box-sizing: border-box;
        border-radius: 0px;
        border: 1px solid #000000;
        color: #000000;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .course-item:hover{
        color: rgb(61, 61, 61);
    }
    
    .course-item:nth-child(even) {
        background: #ffffff;
    }

    .course-item:nth-child(odd) {
        background: #e7e7e7; 
    }

    .full-screen-notification {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .notification-content {
        font-family: Popins, sans-serif;
        font-size: 20px;
        font-style: bold;
        color: #ffffff;
        background: rgb(130, 0, 0.7);
        padding: 20px;
        border: solid 1px #000000;
        border-radius: 5px;
        text-align: center;

    }

    .close-btn {
        margin-top: 10px;
        padding: 10px;
        border: transparent;
        background: transparent;
        cursor: pointer;
        width: 50px;
        height: 50px;
    }

    img {
        width: 100%;
        height: auto;
    }

    h2{
        font-family: 'coolvetica', coolvetica;
        color:#000000;
    }

    .loading{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
</style>