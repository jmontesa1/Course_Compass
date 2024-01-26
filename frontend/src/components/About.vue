<!--Created by: John Montesa-->
<!-- This is the about page for Course Compass -->
<!-- This page will contain brief information about Course Compass, the team, and why it was created -->

<template>
    <!--About Course Compass-->
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-6">
                <h1>What is Course Compass?</h1>
                <p>Course Compass aims to assist students with their enrollment process and academic progress tracking through its individual-oriented features
                     such as the ability to filter courses by various criteria such as professor ratings, personal and career interests, availability and meeting times,
                      and more. Users will be able to create an account to store relevant information pertaining to their academic life, and will be able to access
                       it at any time to resume planning their educational path. Their major, completed course history, and preferences will enable users to make
                        satisfactory decisions that align with their goals. Users will additionally be able to utilize features such as a calendar, to-do lists,
                         and graphical progress for visualization to stay on top of their responsibilities and maintain a healthy life as a student.
                         The product will largely be accomplished through the use of HTML, Vue.js, Python, Flask, and MySQL.
                </p>
            </div>
            <div class="col-md-6">
                <div class="img-container">
                    <img src="../assets/course compass logo.png" alt="University of Nevada, Reno logo." class="img-fluid">
                </div>
            </div>
        </div>
    </div>

    <!--Why Course Compass?-->
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-6">
                <div class="img-container">
                    <img src="../assets/schedule.png" alt="University of Nevada, Reno logo." class="img-fluid">
                </div>
            </div>    
            <div class="col-md-6">
                <h1>Why Course Compass?</h1>
                <p>The inspiration for this product stems from the team’s personal struggles experienced while attempting to navigate the university’s official course enrollment site, aiming to aleve or outright eliminate any stress or confusion associated with doing so. 
                    Overall, the main goal Course Compass hopes to accomplish is to replace other methods of course selection and discovery with a more streamlined, simplified, and tailored experience that the user can then apply to their university’s official course registration process.
                </p>
            </div>
        </div>
    </div>

    <!--Behind the Team-->
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-6">
                <h1>Behind The Team</h1>
                <p>Course Compass was created by <b>Team 38</b>: <i>John Montesa</i>, <i>Lucas Videtto</i>, and <i>Jose Urrutia</i>. We are 
                    Computer Science & Engineering Undergraduates attending the University of Nevada, Reno. This application is our
                    Capstone Project for graduation, developed during Fall 2023 and Winter 2024.<br>
                    <br>External Advisor: Syreeta Williams
                    <br>Instructors for Fall 2023: Sara Davis, Vinh Le, and Devrin Lee
                    <br>Instructors for Spring 2024: David Feil-Seifer, Devrin Lee, and Sara Davis
                </p>
            </div>            
            <div class="col-md-6">
                <div class="img-container">
                    <img src="../assets/unrlogo.png" alt="University of Nevada, Reno logo." class="img-fluid">
                </div>
            </div>
        </div>
    </div>



    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
</template>

<script>

</script>

<style scoped>
    p{
        font-family: 'Poppins', sans-serif;
        font-size: 20px;
    }
    h1{
        font-family: 'coolvetica';
        text-align: center;
    }

    img {
        width: 70%;
        height: auto;
    }

    .img-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>