<!--Created by: John Montesa-->
<!-- This is the Signup page for Course Compass -->
<!-- Users will be prompted with an email and password input. -->
<!-- They can also be redirected to the login page if they already have an account -->
<!-- They must also confirm their email and password to make sure they are correct -->
<!-- They are also able to choose a major from a major list -->

<template>
    <div class="signup-container">
        <div class="left-section">

            <h2>Sign Up</h2>

            <form @submit.prevent="handleSubmit">

                <div>
                    <v-row no-gutters>
                        <v-col cols="9">
                            <div class="name-container">
                                <input v-model="firstname" type="text" placeholder="First Name" required>
                                <input v-model="lastname" type="text" placeholder="Last Name" required>
                            </div>
                        </v-col>
                        <v-col style="margin-left: 9px; font-family: Poppins;">
                            <select required>
                                <option :value="role">Student</option>
                                <option :value="role">Instructor</option>
                            </select>
                        </v-col>
                    </v-row>
                </div>
                <input v-model="email" type="email" placeholder="Email" required>
                <br>
                <input v-model="confirmEmail" type="email" placeholder="Confirm Email" required>
                <br>
                <br>

                <input v-model="dateOfBirth" type="date" placeholder="Date of Birth" required>
                <br>
                <br>

                <div class="password-container">
                    <input v-model="password" ref="passwordInput" type="password" id="passwordInput" placeholder="Password" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}" title="Passwords contain at least one lowercase and one uppercase letter, one number, one special character, and are at least 8 or more characters." required/>
                    <img class="eye-icon" :src="eyeIcon('passwordInput')" alt="Password Visibility Eye" @click="toggleVisibility('passwordInput')" />
                </div>
                <div class="password-container">
                    <input v-model="confirmPass" ref="confirmPasswordInput" type="password" id="confirmPasswordInput" placeholder="Confirm Password" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}" title="Passwords contain at least one lowercase and one uppercase letter, one number, one special character, and are at least 8 or more characters." required/>
                    <img class="eye-icon" :src="eyeIcon('confirmPasswordInput')" alt="Confirm Password Visibility Eye" @click="toggleVisibility('confirmPasswordInput')" />
                </div>
                <br>

                <div>
                    <label for="major">Select Your Major:</label>
                    <select v-model="selectedMajor" id="major" required>
                        <option value="" disabled></option>
                        <option v-for="major in majors" :key="major" :value="major">{{ major }}</option>
                    </select>
                </div>



                <div class="button-container">
                    <button type="submit">Sign Up</button>
                </div>
            </form>


            <div>
                <p>Already have an account? <router-link to="/login">Log In</router-link></p>
            </div>
        </div>
    

        <div class="right-section">
            <img src="@/assets/background-img.png" alt="Background Image" />
        </div>
    </div>

</template>

<script>
    import axios from 'axios';

    export default {
        data() {
            return {
            firstname: '',
            lastname: '',
            dateOfBirth:'',
            email: '',
            confirmEmail: '',
            password: '',
            confirmPass: '',
            passwordVis: false,
            confirmPassVis: false,
            selectedMajor: '',
            majors: [] 
            };
        },

        mounted() {
            //fetch majors from the backend API endpoint
            axios.get('http://127.0.0.1:5000/majors')
                .then(response => {
                    this.majors = response.data.majors;
                })
                .catch(error => {
                    console.error("Failed to fetch majors:", error);
                });
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

        validateForm() {
            if (this.email !== this.confirmEmail || this.password !== this.confirmPass) {
                this.$emit("show-toast", "Emails and Passwords must match.");
                return false;
            }
            return true;
        },

        // handleSubmit method implemented by Lucas Videtto
        handleSubmit() {
            if (this.validateForm() &&this.validateAge()) {
                const userData = {
                    firstname: this.firstname,
                    lastname: this.lastname,
                    dateOfBirth: this.dateOfBirth,
                    email: this.email,
                    password: this.password,
                    majorID: this.selectedMajor
                };

                axios.post('http://127.0.0.1:5000/signup', userData)
                    .then(response => {
                        console.log(response.data.message);
                        if(response.status === 200){
                        this.$emit("show-toast", "Welcome to Course Compass!", "#51da6e");
                        setTimeout(() => {
                            this.$router.push('/login');
                        }, 2500);
                    }
                    })
                    .catch(error => {
                        if (error.response && error.response.status ===409){
                            this.$emit("show-toast","Signup failed: " + error.response.data.message);
                        }
                        else{
                            console.error("A problem has ocurred: Unable to sign up:", error);
                            this.$emit("show-toast","Signup failed: " + error.message);
                        }
                    });
            }
        },


        validateAge() {
        const today = new Date();
        const birthDate = new Date(this.dateOfBirth);
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }

        const minimumAge = 18;

        if (age < minimumAge) {
            this.$emit("show-toast", "You must be at least 18 years old to sign up.");
            return false;
        }
        return true;


    },


        
    },
};
</script>

<style scoped>
    .name-container {
        display: flex;
        gap: 10px;
    }
    .signup-container {
        display: flex;
        height: 100vh;
    }

    .left-section {
        flex: 1;
        padding: 20px;
        border-right: 1px solid #000000;
    }

    .right-section {
        flex: 1;
        overflow: hidden;
    }

    img {
        height: 100%;
        width: auto;
        object-fit: cover;
    }

    :placeholder-shown{
        font-family: Poppins, sans-serif;
    }

    option {
        font-family: Poppins, sans-serif;
    }
    h2 {
        text-align: left;
        font-family:coolvetica;
    }

    p{
        font-family: Poppins, sans-serif;
    }

    .logo {
        max-width: 100px;
        margin-bottom: 20px;
    }

    input {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        box-sizing: border-box;
        border: 1px black solid;

    }

    label{
        font-family: Poppins, sans-serif;
        font-size: 18px;
    }

    .button-container {
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



    .signup-link a {
        color: #1292e7;
        text-decoration: none;
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

    select {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        box-sizing: border-box;
        border: 1px black solid;
        overflow-y: auto;
        max-height: 100px;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="%23000000"><path d="M1 5h14L8 12z"/></svg>');
        background-position: right 10px center;
        background-size: 15px;
        cursor: pointer;
        }

    option{
        max-height: 20vh;
    }

</style>