<!-- Created by: John Montesa-->
<!-- This is the home page for Course Compass, which includes the navigation bar, a description of the website, and a button to get started-->
<!-- This is the first page the user will see -->

<template>
    <div class="image-container">
    <img src="@/assets/unrskyline2.png" alt="Unr whole campus with skyline">
        <div class="button-container">
            <router-link to="/signup">
                <button class="get-started-button">Get Started</button>
            </router-link>
        </div>
    </div>
</template>

<script>
</script>

<style scoped>
    .image-container {
        position: relative;
    }

    img {
        width: 100%;
        height: auto;
        border-bottom:#000000 2px solid;
    }

    .button-container {
        position: absolute;
        top: 75%;
        left: 48%;
        transform: translate(-50%, -50%);
        text-align: center;
    }

    .get-started-button {
        font-family: akira;
        background-color: #00000000;
        color: #ffffff;
        padding: 5% 10%;
        font-size: 2vw;
        border: white 3px solid;
        cursor: pointer;
        display: inline-block;
        transition: background-color 0.3s linear, color 0.3s linear;
        text-decoration: none;
        white-space: nowrap;
        box-shadow: 0 12px 10px rgba(0, 0, 0, 0.992);
    }

    .get-started-button:hover {
        background-color: #ffffff;
        color: #000000;
    }

    @media screen and (max-width: 600px) {
        .get-started-button {
            padding: 8% 15%;
            font-size: 4vw;
        }
    }
</style>