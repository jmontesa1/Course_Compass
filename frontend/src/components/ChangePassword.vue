<!--Created by: John Montesa-->
<!-- This is the Change Password page for Course Compass -->

<template>
    <div class="login-container">
        <img class="logo" src="../assets/course compass logo.png" alt="Course Compass Logo">
        <h2>Change Password</h2>
        <!-- Input fields for email and password -->
        <form @submit.prevent="changePassword">
            <div class="password-container">
                <input ref="passwordInput" type="password" v-model="password" id="passwordInput" placeholder="Password"
                    pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}"
                    title="Passwords contain at least one lowercase and one uppercase letter, one number, one special character, and are at least 8 or more characters."
                    required>
                <img class="eye-icon" :src="eyeIcon('passwordInput')" alt="Password Visibility Eye" @click="toggleVisibility('passwordInput')">
            </div>
            <div class="password-container">
                <input ref="passwordConfirmInput" type="password" v-model="passwordConfirm" id="passwordConfirmInput"
                    placeholder="Confirm Password" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}"
                    title="Passwords contain at least one lowercase and one uppercase letter, one number, one special character, and are at least 8 or more characters."
                    required>
                <img class="eye-icon" :src="eyeIcon('passwordConfirmInput')" alt="Password Visibility Eye" @click="toggleVisibility('passwordConfirmInput')">
            </div>
            <br>
            <div class="button-container">
                <button type="submit">Change Password</button>
            </div>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            password: '',
            passwordConfirm: '',
            passwordVis: false,
            confirmPassVis: false,
        };
    },
    methods: {
        toggleVisibility(refName) {
            const inputField = this.$refs[refName];
            if (inputField) {
                if (refName === 'passwordInput') {
                this.passwordVis = !this.passwordVis;
                inputField.type = this.passwordVis ? 'text' : 'password';
                } else if (refName === 'confirmPasswordInput') {
                this.confirmPassVis = !this.confirmPassVis;
                inputField.type = this.confirmPassVis ? 'text' : 'password';
                }
            }
        },

        eyeIcon(refName) {
            return refName === 'passwordInput'
                ? this.passwordVis
                ? require('../assets/eyeclose.png')
                : require('../assets/eye.png')
                : this.confirmPassVis
                ? require('../assets/eyeclose.png')
                : require('../assets/eye.png');
        },

        changePassword() {
            if (this.password !== this.passwordConfirm) {
                this.$emit("show-toast", { message: "Passwords do not match."});
                return;
            }
            const passwordPattern = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}/;
            if (!passwordPattern.test(this.password)) {
                this.$emit("show-toast", { message: "Password does not the requirements."}); // may have to remove, check frontend 
                return;
            }
            axios.post('http://127.0.0.1:5000/changepassword', {
                newPassword: this.password
            }, {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
            })
                .then(response => {
                    this.$emit("show-toast", { message: "Password successfully changed.", color: '#51da6e' });
                    this.$router.push('/myaccount');
                    this.password = '';
                    this.passwordConfirm = '';
                })
                .catch(error => {
                    console.error("Failed to change password:", error);
                    this.$emit("show-toast", { message: "New password can not match old password."});
                });
        }
    }
};
</script>

<style scoped>
h2 {
    margin-left: 30px;
    text-align: left;
    font-family: coolvetica;
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