<!-- Created by: John Montesa-->
<!-- This is the home page for Course Compass, which includes the navigation bar, a description of the website, and a button to get started-->
<!-- This is the first page the user will see -->

<template>
<!--    <div class="image-container">
    <img src="@/assets/unrskyline2.png" alt="Unr whole campus with skyline">
        <div class="button-container">
            <router-link to="/signup">
                <button class="get-started-button">Get Started</button>
            </router-link>
        </div>
    </div>
-->
        <div class="home-container">
            <div class="text1-container">
                <h1 class="hero">Remove the clutter of your college experience.<br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Use Course Compass. </h1>
            </div>
            <div class="text2-container">
                <p>Refine, enhance, and restructure your college experience with
                    our intuitive course system, sleek graphics, and innovative features designed to customize your journey for success.
                </p>
            </div>
            <img class="laptop" src="@/assets/laptop with unr logo.png" alt="laptop with UNR logo as a sticker">
            <div class="button-container">
                <router-link to="/signup">
                    <button>
                        Get Started
                    </button>
                </router-link>
            </div>
        </div>

        <br>
        <div class="roles-container">
            <div class="text3-container">
                <h1 class="hero2">Students</h1>
            </div>
            <br>
            <p>Enroll in classes from your university and view schedules based on your courses. Receive messages and alerts from the school and your professors.
                Fine tune your enrollment by filtering classes specific to your needs. Utilize scheduling, progress trackers, and to-do lists to meet deadlines and
                visualize your success.
            </p>
        </div>

        <br>
        <br>
        <div class="roles-container2">
            <div class="text4-container">
                <h1 class="hero2">Professors</h1>
            </div>
            <br>
            <p>Send alerts and messages to students enrolled in your classes. Advertise your office hours and personal website to your students.
                Stay on top of your schedule and receive feedback from courses you are teaching. Utilize a to-do list to track your work and deadlines.
            </p>
        </div>

        <br>
        <h1 class="hero3">Features:</h1>

        <div class="features-container">
            <v-card>
                <v-tabs v-model="tab" bg-color="transparent" color="white" grow>
                    <v-tab v-for="item in items" :key="item.value" :value="item.value"
                        :class="{ 'features-tab': true, 'features-tab--active': tab === item.value }" style="font-family: Poppins;">
                        {{ item.label }}
                    </v-tab>
                </v-tabs>

                <v-window v-model="tab">
                    <v-window-item v-for="item in items" :key="item.value" :value="item.value">
                        <div class="flex-container">
                            <v-card-text class="text-container">
                                <h1 class="hero3">{{ item.header }}</h1>
                                <p>{{ item.text }}</p>
                            </v-card-text>
                            <v-img v-if="item.image" :src="item.image" alt="Feature Image" class="image-container" />
                        </div>
                    </v-window-item>
                </v-window>
            </v-card>
        </div>

        <br>
        <br>
        <br>
</template>

<script setup>
    import { ref } from 'vue'
import About from './About.vue';

    const tab = ref('Features')

    const items = [
        { label: 'Courses', header:'Fine Tune Your Needs', value: 'Courses', text: 'Filter courses to your specific needs and enroll in classes that fit your requirements. Explore a wide range of courses offered by your university, and easily navigate through various categories.', image: require('@/assets/unrlibrary.png') },
        { label: 'Schedule', header:'Prepare Your Schedule', value: 'Schedule', text: 'View your classes, plan your weekly schedule, and print out your customized schedule. Stay organized and keep track of your classes, exams, and other important events with Course Compass\'s intuitive scheduling feature.', image: require('@/assets/unrlibrary.png') },
        { label: 'Progress', header:'Visualize Your Success', value: 'Progress', text: 'Monitor your academic progress and achievements with Course Compass. Get insights into your completed courses and overall progress. Use visualizations and progress trackers to stay motivated and achieve your academic goals.', image: require('@/assets/unrlibrary.png') },
        { label: 'Planner', header:'Stay Up To Date', value: 'Planner', text: 'Keep yourself organized and up-to-date with Course Compass\'s planner feature. Set reminders for assignments, exams, and other important deadlines. Customize your planner to align with your goals and stay on top of your academic and personal commitments.', image: require('@/assets/unrlibrary.png') },
    ];
</script>

<script>
    export default {
  components: { About },
        data () {
        return {
            tab: 'Features',
            items: [
            'Features', 'Entrees', 'Deserts', 'Cocktails',
            ],
            text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
        }
        },
    }
</script>


<style scoped>
    .features-tab {
        background-color: white;
        border: 1px solid black;
        color: black;
    }

    .features-tab--active {
        background-color: black;
        color: white;
    }

    .features-card {
        background-color: white;
        color: black;
        padding: 20px;
    }

    .flex-container {
    display: flex;
    }

    .text-container,
    .image-container {
        flex: 1;
    }

    .v-img {
        width: 100%;
        height: auto;
        border-left: 1px solid black;
    }

    p{
        font-family:Poppins;
        font-size: 16px;
        margin-left: 8px;
        margin-right: 8px;
    }
    
    .roles-container{
        background-color: white;
        position: relative;
        left: 50%;
        transform: translateX(-50%);
        max-width: 86%;
        border-radius: 1px;
        border-top: 1px solid black;
        border-right: 1px solid black;
        border-bottom: 1px solid black;
        margin-bottom: 18px;
    }

    .roles-container2{
        background-color: white;
        position: relative;
        left: 50%;
        transform: translateX(-50%);
        max-width: 86%;
        border-radius: 1px;
        border-top: 1px solid black;
        border-left: 1px solid black;
        border-bottom: 1px solid black;
        margin-bottom: 18px;

    }

    .features-container{
        background-color: white;
        position: relative;
        left: 50%;
        transform: translateX(-50%);
        max-width: 86%;
        border-radius: 1px;
        border-left: 1px solid black;
        border-right: 1px solid black;
    }

    .home-container{
        position: relative;
        height: 50vh;
        width: 100vw;
        margin-bottom: 28px;
    }

    hr{
        border: 1px solid rgb(0, 0, 0);
    }
    
    .hero{
        font-family: Coolvetica;
        font-size: 2.5vw;
    }

    .hero2{
        font-family: Coolvetica;
        text-align: center;
        font-size: 25px;
    }

    .hero3{
        font-family: Coolvetica;
        text-align: center;
        font-size: 40px;
    }


    .text1-container{
        position:relative;
        top: 7%;
        left: 45%;
        z-index: 2;
    }

    .text2-container{
        position:absolute;
        width:47%;
        right: 8%;
        top: 50%;
        z-index: 2;
    }

    .text3-container{
        position: absolute;
        height: 30px;
        width: 110px;
        background: rgb(255, 255, 255);
        top: -17px;
        left: 20px;
    }

    .text4-container{
        position: absolute;
        height: 30px;
        width: 120px;
        background: rgb(255, 255, 255);
        top: -17px;
        right: 20px;
    }


    button {
        font-family: coolvetica, sans-serif;
        font-size: 25px;
        background-color: #364db3;
        color: #ffffff;
        padding: 5px 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s linear, color 0.3s linear;
    }

    button:hover {
        background-color: black;/*#555555;*/
    }

    .laptop{
        position: absolute;
        height:300px;
        width: auto;
        z-index: 1;
        top:10%;
        left: 7%;
        border-left:1px solid black;
        border-top: 1px solid black;
    }
    .success-container{
        position: relative;
    }

    img {
        width: 50%;
        height: auto;
    }

    .button-container {
        position: absolute;
        top: 75%;
        right: 8%;
    }



    @media screen and (max-width: 1000px) {
        .hero{
            font-size: 20px;
        }
        .laptop{
            height:150px;
            width:auto;
        }
    }

</style>