<!--Created by: John Montesa-->
<!-- This is the Change Password page for Course Compass -->

<template>
    <div class="login-container">
            <img class ="logo" src="../assets/course compass logo.png" alt="Course Compass Logo">
            <h2>Change Password</h2>

            <!-- Input fields for email and password -->
            <form @submit.prevent="handleLogin">
                <input type="email" v-model="email" placeholder="Email" required>
                <br>

                <div class="password-container">
                    <input ref="passwordInput" type="password" v-model="password" id="passwordInput" placeholder="Password" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}" title="Passwords contain at least one lowercase and one uppercase letter, one number, one special character, and are atleast 8 or more characters." required>
                    <img class ="eye-icon" :src="eyeIcon()" alt="Password Visibility Eye" @click="toggleVisibility">
                </div>
                <div class="password-container">
                    <input ref="passwordConfirmInput" type="password" v-model="passwordConfirm" id="passwordConfirmInput" placeholder="Confirm Password" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}" title="Passwords contain at least one lowercase and one uppercase letter, one number, one special character, and are atleast 8 or more characters." required>
                    <img class ="eye-icon" :src="eyeIcon2()" alt="Password Visibility Eye" @click="toggleVisibility2">
                </div>
                <br>

                <div class="button-container">
                    <button type="submit">Change Password</button>
                </div>
            </form>
        </div>
</template>

<script>
    export default{
        data(){
            return{
                password: '',
                passwordConfirm: '',
                passwordVis: false,
                passwordConfirmVis: false,

            };
        },
        methods:{
            toggleVisibility(){
                const passwordInput = this.$refs.passwordInput;
                if (passwordInput) {
                    this.passwordVis = !this.passwordVis;
                    passwordInput.type = this.passwordVis ? 'text' : 'password';
                }
            },
            toggleVisibility2(){
                const passwordConfirmInput = this.$refs.passwordConfirmInput;
                if (passwordConfirmInput) {
                    this.passwordConfirmVis = !this.passwordConfirmVis;
                    passwordConfirmInput.type = this.passwordConfirmVis ? 'text' : 'password';
                }
            },
            eyeIcon(){
                return this.passwordVis ? require('../assets/eyeclose.png') : require('../assets/eye.png');
            },
            eyeIcon2(){
                return this.passwordConfirmVis ? require('../assets/eyeclose.png') : require('../assets/eye.png');
            },
        }
    };
</script>

<style scoped>
    h2 {
        margin-left: 30px;
        text-align: left;
        font-family:coolvetica;
    }


    .login-container {
        background-color: #e1e1e1;
        margin: 5% auto;
        padding: 20px;
        max-width: 600px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        align-content: center;
        text-align: center;
    }

    .logo {
        max-width: 100px;
        margin-bottom: 20px;
    }

    input {
        width: 90%;
        padding: 10px;
        margin: 10px 0;
        box-sizing: border-box;
        border: 1px black solid;
    }

    .button-container {
        margin-right: 30px;
        text-align: right;
    }

    button {
        font-family: coolvetica, sans-serif;
        font-size: 25px;
        background-color: #000000;
        color: #ffffff;
        padding: 5px 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s linear, color 0.3s linear;
    }

    button:hover {
        background-color: #555555;
    }

    .signup-link a:hover {
        text-decoration: underline;
    }

    .password-container {
        position: relative;
    }

    .eye-icon {
        position: absolute;
        margin-left: -45px;
        margin-top: 25px;
        width: 30px;
        height: auto;
        cursor: pointer;
    }
</style>