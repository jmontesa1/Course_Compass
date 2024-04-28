<!-- Created by: John Montesa -->
<!-- This component details a specific course a user has interacted with -->
<!-- It will popup a screen for the user to see more indepth information about the course and student's opinions on it -->
<!-- The user faces two buttons where they can either close the popup screen or add it to their schedule -->
<!-- If the user adds it to their schedule, it will add it to a schedule array -->

<template>
    <div class="popup" @click="closePopup">
        <!--Pop up Screen with details of course-->
        <div class="popup-content" @click.stop>
            <button class="close-btn" @click="closePopup">
                <span class="material-icons" style="color:black">close</span>
            </button>
            <h2>Course Details</h2>
            <div class="container" v-if="course">
                <div class="row">
                    <!--Left Side of Popup Page, Reveals Course Details-->
                    <div class="col-lg left-column">
                        <p><strong>Department:</strong> {{ course.department || 'N/A' }}</p>
                        <p><strong>Name:</strong> {{ course.name || 'N/A' }}</p>
                        <p><strong>Code:</strong> {{ course.code || 'N/A' }}</p>
                        <p><strong>Professor:</strong> {{ course.professor || 'N/A' }}</p>
                        <br>
                        <p><strong>Format:</strong> {{ course.format || 'N/A' }}</p>
                        <p><strong>Term:</strong> {{ course.term || 'N/A' }}</p>
                        <p><strong>Units:</strong> {{ course.units || 'N/A' }}</p>
                        <p><strong>Section:</strong> {{ course.section || 'N/A' }}</p>
                        <br>
                        <p><strong>Class Capacity:</strong> {{ course.classCapacity || 'N/A' }}</p>
                        <p><strong>Enrollment Total:</strong> {{ course.enrollmentTotal || 'N/A' }}</p>
                        <p><strong>Available Seats:</strong> {{ course.availableSeats || 'N/A' }}</p>
                        <br>
                        <p><strong>Meeting Details:</strong></p>
                        <p><strong>Location:</strong> {{ course.location || 'N/A' }}</p>
                        <p><strong>Days:</strong> {{ course.days && course.days.length > 0 ? course.days.join(' | ') : 'Information not available' }}</p>
                        <p><strong>Meeting Time:</strong> {{ course.meetingTime || 'N/A' }}</p>
                    </div>

                    <div class="col-lg left-column" style="border-right: none;" v-if="editMode === true">
                        <div class="edit-form">
                            <p style="margin-right: 10px;"><strong>Department:</strong></p>
                            <input type="text" class="form-control" v-model="newDepartment" style="height: 20px; margin-bottom: -1px;">
                        </div>
                        <div class="edit-form">
                            <p style="margin-right: 10px;"><strong>Name:</strong></p>
                            <input type="text" class="form-control" v-model="newName" style="height: 20px; margin-bottom: -1px;">
                        </div>
                        <div class="edit-form">
                            <p style="margin-right: 10px;"><strong>Code:</strong></p>
                            <input type="text" class="form-control" v-model="newCode" style="height: 20px; margin-bottom: -1px;">
                        </div>
                        <div class="edit-form">
                            <p style="margin-right: 5px;"><strong>Professors:</strong></p>

                            <div v-for="(professor, index) in newProfessor" :key="index">
                                <input type="text" class="form-control" v-model="newProfessor[index]" style="height: 20px; margin-bottom: -1px; margin-right: 5px;">
                            </div>
                            <v-btn size="extra-small" variant="plain" @click="addProfessor" :disabled="newProfessor.length > 6">
                                <span class="material-icons" style="color:black">person_add</span>
                            </v-btn>
                            <v-btn size="extra-small" variant="plain" @click="removeProfessor" :disabled="newProfessor.length === 1">
                                <span class="material-icons" style="color:black">remove</span>
                            </v-btn>
                        </div>
                        <br>
                        <div class="edit-form">
                            <p style="margin-right: 10px;"><strong>Format:</strong></p>
                            <input type="text" class="form-control" v-model="newFormat" style="height: 20px; margin-bottom: -1px;">
                        </div>
                        <div class="edit-form">
                            <p style="margin-right: 10px;"><strong>Term:</strong></p>
                            <input type="text" class="form-control" v-model="newTerm" style="height: 20px; margin-bottom: -1px;">
                        </div>
                        <div class="edit-form">
                            <p style="margin-right: 10px;"><strong>Units:</strong></p>
                            <input type="text" class="form-control" v-model="newUnits" style="height: 20px; margin-bottom: -1px;">
                        </div>
                        <br>
                        <div class="edit-form">
                            <p style="display: inline-block; width: 200px;"><strong>Class Capacity:</strong></p>
                            <input type="text" class="form-control" v-model="newCapacity" style="height: 20px; margin-bottom: -1px;">
                        </div>
                        <div class="edit-form">
                            <p style="display: inline-block; width: 230px;"><strong>Enrollment Total:</strong></p>
                            <input type="text" class="form-control" v-model="newEnrollmentTotal" style="height: 20px; margin-bottom: -1px;">
                        </div>
                        <div class="edit-form">
                            <p style="display: inline-block; width: 200px;"><strong>Available Seats:</strong></p>
                            <input type="text" class="form-control" v-model="newAvailablity" style="height: 20px; margin-bottom: -1px;">
                        </div>
                        <br>
                        <p><strong>Meeting Details:</strong></p>
                        <div class="edit-form">
                            <p style="margin-right: 10px;"><strong>Location:</strong></p>
                            <input type="text" class="form-control" v-model="newLocation" style="height: 20px; margin-bottom: -1px;">
                        </div>
                        <div class="edit-form">
                            <p style="margin-right: 10px;"><strong>Days:</strong></p>
                            <input type="text" class="form-control" v-model="newDays" style="height: 20px; margin-bottom: -1px;">
                        </div>
                        <div class="edit-form">
                            <p style="display: inline-block; width: 200px;"><strong>Meeting Time:</strong></p>
                            <input type="text" class="form-control" v-model="newMeetingTime" style="height: 20px; margin-bottom: -1px;">
                        </div>
                    </div>
                    
                    <!--Right Side of Popup Page, Shows User Thoughts-->
                    <div class="col-lg" v-if="editMode === false">
                        <p><strong>What Students Think:</strong></p>
                        <p>{{ course.frequentTags && course.frequentTags.length > 0 ? course.frequentTags.join(', ') : 'Information not available' }}</p>
                        <p><strong>Student Rating:</strong> {{ course.averageRating || '0' }}/5</p>
                        <hr>
                        <p><strong>What Students Say:</strong></p>
                        <p>{{ course.keywords && course.keywords.length > 0 ? course.keywords.join(', ') : 'Information not available' }}</p>
                    </div>
                    <div class="w-100"></div>
                </div>
            </div>
            <div v-else>
                <p>Course information unavailable.</p>
            </div>
            <br>
            <div class="button-container" v-if="userType === 'Admin' && editMode === false">
                    <button class="schedule-button2" @click="editMode = true">Edit Course Details</button>
            </div>


            <div class="button-container" v-if="editMode === false">
                    <button class="schedule-button" @click="addToSchedule">Add Course to Cart</button>
            </div>

            <div class="button-container" v-if="editMode === true">
                    <button class="schedule-button2" @click="editMode = false">Cancel</button>
            </div>

            <div class="button-container" v-if="editMode === true">
                    <button class="schedule-button" @click="editCourseDetails">Save</button>
            </div>

        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                editMode: false,
                newDepartment: '',
                newName: '',
                newCode: '',
                newSection: '',
                newProfessor: [''],
                newFormat: '',
                newTerm: '',
                newUnits: '',
                newCapacity: '',
                newEnrollmentTotal: '',
                newAvailablity: '',
                newLocation: '',
                newDays: '',
                newMeetingTime:'',

            };
        },

        props: {
            course: Object,

            userType:{
                type: String,
                required: '',
            },
        },
        methods: {
            closePopup() {
                this.$emit('close');
                },
            addToSchedule() {
                this.$emit('addToSchedule', this.course);
                },

            editCourseDetails(){
                //backend stuff here

                this.editMode = false;
                this.newDepartment = '';
                this.newName = '';
                this.newCode = '';
                this.newSection = '';
                this.newProfessor = '';
                this.newFormat = '';
                this.newTerm = '';
                this.newUnits = '';
                this.newCapacity = '';
                this.newEnrollmentTotal = '';
                this.newAvailablity = '';
                this.newLocation = '';
                this.newDays = '';
                this.newMeetingTime = '';
            },

            addProfessor(){
                this.newProfessor.push('');
            },

            removeProfessor(index){
                this.newProfessor.pop();
            },
            

        },
    };
    </script>

<style scoped>
    .popup {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index:2;
    }

    .popup-content {
        background: #ffffff;
        padding: 25px;
        border-radius: 8px;
        min-width: 800px;
    }

    .left-column {
        border-right: 1px solid #000000;
    }

    .close-btn {
        margin-left: auto;
    }

    img {
        width: 100%;
        height: auto;
    }

    h2{
        font-family: 'Poppins';
        font-size: 20px;
        text-align: center;
        color:#000000;
        margin-top: -5px;
    }
    p{
        font-family: Poppins, sans-serif;
        font-size: 15px;
        margin-bottom: -1px;
    }

    .button-container {
        margin: 0;
        padding: 0;
        overflow: hidden;
        display: flex;
        justify-content: center;
    }

    .schedule-button {
        font-family: Poppins;
        background-color: #000000;
        color: #ffffff;
        padding: 5px 25px;
        font-size: 15px;
        border: none;
        cursor: pointer;
        display: inline-block;
        transition: background-color 0.3s linear, color 0.3s linear;
        text-decoration: none;
    }

    .schedule-button2 {
        font-family: Poppins;
        background-color: #ffffff;
        color: #000000;
        padding: 5px 25px;
        font-size: 15px;
        cursor: pointer;
        display: inline-block;
        transition: background-color 0.3s linear, color 0.3s linear;
        text-decoration: none;
        margin-bottom: 10px;
        border: 1px solid black;
        align-content: flex-start;
    }

    .schedule-button:hover {
        background-color: #ffffff;
        color: #000000;
    }

    .schedule-button2:hover {
        background-color: #000000;
        color: #ffffff;
    }

    .form-control{
        font-family: 'Poppins', sans-serif;
        font-size: 14px;
        margin-bottom: 5px;
    }

    .edit-form{
        display: flex;
        align-items: center;
    }

</style>