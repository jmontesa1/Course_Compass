<template>
    <div>
        <router-link to="/">
            <img src="../assets/course compass logo.png" alt="Course Compass Logo" class="logo" />
        </router-link>
        <br>
        <h1>Course Compass Instructor Home Page</h1>
        <br>
        <br>
        <br>
        <div class="instructor-options">
            <h2>What would you like to do?</h2>
            <br>
            <ul>
                <li @click="showModal('viewCourses')">View courses</li>
                <li @click="showModal('reviseCourseInfo')">Revise course information</li>
                <li @click="showModal('studentReviews')">Student reviews</li>
                <li @click="showModal('instructorAnalytics')">Analytics</li>
            </ul>
        </div>
        <div v-if="modals.viewCourses" class="modal">
            <div class="modal-content">
                <span class="close" @click="closeModal">&times;</span>
                <h3>View Courses</h3>
                <p>No currently assigned courses.</p>
            </div>
        </div>
        <div v-if="modals.reviseCourseInfo" class="modal">
            <div class="modal-content">
                <span class="close" @click="closeModal">&times;</span>
                <h3>Revise Course Information</h3>
                <p>No currently assigned courses.</p>
            </div>
        </div>
        <div v-if="modals.studentReviews" class="modal">
            <div class="modal-content">
                <span class="close" @click="closeModal">&times;</span>
                <h3>Student Reviews</h3>
                <p>None.</p>
            </div>
        </div>
        <div v-if="modals.instructorAnalytics" class="modal">
            <div class="modal-content">
                <span class="close" @click="closeModal">&times;</span>
                <h3>View Courses</h3>
                <p>No currently assigned courses or student reviews.</p>
            </div>
        </div>
        <br>
    </div>
</template>

<script>
export default {
    data() {
        return {
            modals: {
                viewCourses: false,
                reviseCourseInfo: false,
                studentReviews: false,
                instructorAnalytics: false
            }
        }
    },
    methods: {
        showModal(modalKey) {
            Object.keys(this.modals).forEach(key => {
                this.modals[key] = false;
            });
            this.modals[modalKey] = true;
        },
        closeModal() {
            Object.keys(this.modals).forEach(key => {
                this.modals[key] = false;
            });
        }
    }
}
</script>

<style>
h1 {
    font-family: Poppins;
    font-size: 28pt;
    text-align: center;
    font-weight: bold
}
.instructor-options {
    padding-top: 5px;
    border: 2px solid black;
    width: 50%;
    margin-left: auto;
    margin-right: auto;
}
.instructor-options h2 {
    padding-top: 10px;
    font-family: Poppins;
    font-size: 20pt;
    text-align: center
}
.instructor-options ul {
    list-style-type: none;
    padding: 0;
    padding-left: 8px
}
.instructor-options ul li {
    margin: 10px 0;
    font-family: Poppins;
    cursor: pointer;
    text-align: left
}
.modal {
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    display: flex;
    justify-content: center;
    align-items: center
}
.modal-content {
    margin: 15% auto;
    padding: 20px;
    border: 1px solid black;
    width: 50%;
    background-color: white;
}
.close {
    float: right;
    font-size: 20px;
    font-weight: bold
}
.close:hover,
.close:focus {
    text-decoration: none;
    cursor: pointer;
}
.logo {
    position: absolute;
    top: 0;
    left: 0;
    width: 85px;
    height: auto;
    margin: 10px;
}
</style>