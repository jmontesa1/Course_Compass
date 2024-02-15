<!-- Created by: John Montesa -->
<!-- This component creates the navigation bar that the user will interact with -->
<!-- There are 5 buttons, and one is a drop down menu that directs the user to log in, sign up, or check their profile settings-->

<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
                <router-link to="/" class="navbar-brand">
                    <img src="../assets/course compass logo.png" alt="Course Compass Logo">
                </router-link>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <!-- right-aligned menu items -->
                    <li class="nav-item">
                        <router-link to="/courses" class = "nav-link">Courses</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/schedule" class = "nav-link">Schedule</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/progress" class = "nav-link">Progress</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/about" class = "nav-link">About</router-link>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Account
                        </a>
                        <ul class="dropdown-menu">
                            <li><router-link to="/login" class = "dropdown-item">Log in</router-link></li>
                            <li><router-link to="/signup" class = "dropdown-item">Sign Up</router-link></li>
                            <li><router-link to="/myaccount" class = "dropdown-item">My Account</router-link></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>

</script>

<style scoped>
    .navbar {
        background-color: #ffffff; 
        border-bottom: 1px solid #000000;
    }

    .navbar-brand img {
        max-width: 85px;
        height: auto;
        margin: -8px auto;
    }

    .nav-link {
        font-family: 'coolvetica';            
        font-size: 25px;
        color: #160e0e;
        margin-right: 10px;
    }

    .nav-link:hover {
        color: #ffffff;
        background-color: #000000;
        margin-top: -5px;
        margin-bottom: -5px;
    }

    .dropdown-menu {
        font-family: 'coolvetica';
        background-color: #ffffff00;
        border: 1px solid transparent;
        text-align: center;
        font-size: 15px;
        min-width: 130px;
    }

    .dropdown-item {
        color: #000000;
        border: 1px solid #000000;
        text-align: center;
        background-color: #ffffff;
    }

    .dropdown-item:hover {
        color: #ffffff;
        background-color: #000000;
    }
</style>
