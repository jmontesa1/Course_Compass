<!--Page that appears when the user tries to navigate to a page that does not exist through browser search bar -->
<template>
    <div>
        <h1>Sorry!</h1>
        <p>The page you are looking for does not exist.</p>
        <button @click="goBack">Go back</button>
    </div>
</template>

<script>
export default {
    methods: {
        goBack() {
            window.history.back();
        }
    }
}
</script>

<style scoped>
    h1 {
        font-family: Coolvetica;
        font-size: 48pt;
        text-align: center;
    }
    p {
        font-family: Poppins;
        font-size: 14pt;
        text-align: center;
    }
    div {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 60vh;
    }
    button {
        font-family: Poppins;
        background: none;
        border: none;
        color: blue;
        font-size: 12pt;
        text-decoration: underline;
        cursor: pointer;
        margin-top: 20px;
    }
    button:hover {
        text-decoration: none;
    }
</style>
