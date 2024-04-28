<!--Created by: John Montesa-->
<!-- This is the Login page for Course Compass -->
<!-- Users will be prompted with an email and password input. The password input allows users to see what they were typing -->
<!-- They can also be redirected to the signup page if they do not have an account yet-->
<!-- There are specific parameters each form must meet to be able to log in -->

<template>
    <div class="login-container">
        <!--<transition name="fade">
            <div v-if="isVerified" class="alert alert-success">
            Your account has been verified. You may now log in.
            </div>
        </transition>-->
            <img class="logo" src="../assets/course compass logo.png" alt="Course Compass Logo">
            <h2>Log In</h2>

            <!-- Input fields for email and password -->
            <form @submit.prevent="handleLogin" style="font-family: Poppins;">
                <input type="email" v-model="email" placeholder="Email" required>
                <br>

                <div class="password-container">
                    <input ref="passwordInput" type="password" v-model="password" id="passwordInput" placeholder="Password" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}" title="Passwords contain at least one lowercase and one uppercase letter, one number, one special character, and are atleast 8 or more characters." required>
                    <img class ="eye-icon" :src="eyeIcon()" alt="Password Visibility Eye" @click="toggleVisibility">
                </div>
                <br>

                <div class="button-container">
                    <button class="login-button" type="submit">Log In</button>
                </div>
            </form>
            <div class="signup-link">
                <p>Don't have an account? <router-link to="/signup" >Sign Up</router-link></p>
            </div>
            <div class="signup-link">
                <v-dialog v-model="dialog" max-width="500" style="font-family: Poppins;">
                    <template v-slot:activator="{ props: activatorProps }">
                        <p><a v-bind="activatorProps" style="cursor: pointer;">Forgot Password?</a></p>
                    </template>
                    <!--Pop up -->
                    <v-card title="Forgot Password">
                        <v-card-text>
                            Please enter your email:
                            <v-text-field v-model="forgotPassEmail" label="Email" type="email"></v-text-field>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn text="Close" variant="plain" @click="dialog = false"></v-btn>

                            <v-dialog v-model="dialog2" max-width="500" style="font-family: Poppins;">
                                <template v-slot:activator="{ props: activatorProps }">
                                    <v-btn v-bind="activatorProps" color="primary" text="Send" variant="tonal" @click="sendEmail"></v-btn>
                                </template>
                                <!--Pop up -->
                                <v-card title="Email Sent">
                                    <v-card-text>
                                        An email was sent to <strong>{{forgotPassEmail}}</strong> with your password.
                                    </v-card-text>
                                    <v-card-actions>
                                        <v-spacer></v-spacer>
                                        <v-btn text="Close" variant="plain" @click="dialog2 = false; forgotPassEmail = ''; dialog = false;"></v-btn>
                                    </v-card-actions>
                                </v-card>
                            </v-dialog>  

                        </v-card-actions>
                    </v-card>
                </v-dialog>  
            </div>


        </div>
</template>

<script>
    import axios from 'axios';

    export default{
        data(){
            return{
                email: '',
                password: '',
                passwordVis: false,
                isVerified: false,
                dialog: false,
                dialog2: false,
                forgotPassEmail: '',
            };
        },
        mounted() {
            if (this.$route.query.verified === 'true') {
                this.isVerified = true;
                this.$emit("show-toast", { message: "Your account has been verified. You may now log in.", color: '#51da6e' });
                setTimeout(() => {
                    this.isVerified = false;
                }, 4000);
            }

            const tag = this.$route.params.tag || this.$route.query.tag;
            if (tag === 'verified=true') {
                this.isVerified = true;
                this.$emit("show-toast", { message: "Your account has been verified. You may now log in.", color: '#51da6e' });
                setTimeout(() => {
                    this.isVerified = false;
                }, 3000);
            }

            this.handleLogin = this.determineLoginHandler();
        },
        methods:{
            toggleVisibility(){
                const passwordInput = this.$refs.passwordInput;
                if (passwordInput) {
                    this.passwordVis = !this.passwordVis;
                    passwordInput.type = this.passwordVis ? 'text' : 'password';
                }
            },
            eyeIcon(){
                return this.passwordVis ? require('../assets/eyeclose.png') : require('../assets/eye.png');
            },

            determineLoginHandler() {
                const tag = this.$route.params.tag;
                if (tag === 'verified=true') {
                    return this.handleLoginVerify;
                }
                return this.handleDefaultLogin;
            },

            handleDefaultLogin(){
                const loginData = {
                    email: this.email,
                    password: this.password
                };
                axios.post('http://127.0.0.1:5000/login', loginData, { withCredentials: true })
                .then(response => {
                    console.log(response.data.message);
                    if (response.status === 200) {
                        localStorage.setItem('access_token', response.data.access_token);
                        this.$emit("show-toast", { message: "Login successful. Welcome back!", color: '#51da6e' });

                        const userType = response.data.role;
                        console.log('User type:', userType);

                        this.$emit('update-user-type', userType);

                        switch(userType) {
                            case 'Student':
                                this.$router.push('/dashboard');
                                break;
                            case 'Instructor':
                                this.$router.push('/instructor-dashboard');
                                break;
                            case 'Admin':
                                this.$router.push('/admin-dashboard');
                                break;
                            default:
                                this.$router.push('/');
                        }

                        this.$emit('login-status-changed', true);

                    } else{
                        console.error("Unexpected response during login: ", response);
                        this.$emit("show-toast",{ message: "An error occurred during login. Please try again."});
                    }
                })
                .catch(error => {
                    if (error.response && error.response.status === 401) {
                        this.$emit("show-toast",{ message: "Invalid email or password."});
                    } 
                    else if (error.response && error.response.status === 403) {
                        this.$emit("show-toast",{ message: "Account not verified. please check your email."});
                    }
                    else {
                        console.error("Login error: ", error);
                        this.$emit("show-toast",{ message: "An error occurred during login."});
                    }
                    });
            },

            handleLoginVerify(){
                const loginData = {
                    email: this.email,
                    password: this.password
                };
                axios.post('http://127.0.0.1:5000/login-verify', loginData, { withCredentials: true })
                .then(response => {
                    console.log(response.data.message);
                    if (response.status === 200) {
                        localStorage.setItem('access_token', response.data.access_token);
                        this.$emit("show-toast", { message: "Login successful. Welcome back!", color: '#51da6e' });
                        const userType = response.data.role;
                        console.log('User type:', userType);
                        this.$emit('update-user-type', userType);
                        switch(userType) {
                            case 'Student':
                                this.$router.push('/dashboard');
                                break;
                            case 'Instructor':
                                this.$router.push('/instructor-dashboard');
                                break;
                            case 'Admin':
                                this.$router.push('/admin-dashboard');
                                break;
                            default:
                                this.$router.push('/');
                        }
                        this.$emit('login-status-changed', true);
                    } else{
                        console.error("Unexpected response during login: ", response);
                        this.$emit("show-toast",{ message: "An error occurred during login. Please try again."});
                    }
                })
                .catch(error => {
                    if (error.response && error.response.status === 401) {
                        this.$emit("show-toast",{ message: "Invalid email or password."});
                    } 
                    else if (error.response && error.response.status === 403) {
                        this.$emit("show-toast",{ message: "Account not verified. please check your email."});
                    }
                    else {
                        console.error("Login error: ", error);
                        this.$emit("show-toast",{ message: "An error occurred during login."});
                    }
                    });
            },

            sendEmail(){
                const newDate = new Date().toLocaleDateString('en-US', {
                    month: 'long',
                    day: 'numeric',
                    year: 'numeric',
                });

                const email = {
                    date: newDate,
                    subject: 'Course Compass - Forgot Password',
                    to: this.forgotPassEmail, 
                    content: 'You have requested that you forgot your password.\nYour password is: ',
                };

                axios.post('http://127.0.0.1:5000/send-email', email)
                .then(response => {
                    console.log("Email sent successfully");
                })
                .catch(error => {
                    console.error("Failed to send email: ", error);
                });
            },
        }
    };
</script>

<style scoped>
    .fade-enter-active, fade-leave-active {
        transition: opacity 3s;
    }
    .fade-enter, .fade-leave-to {
        opacity: 0;
    }
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
        border: 1px solid black;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        align-content: center;
        text-align: center;
    }

    .logo {
        position: relative;
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

    .login-button {
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

    .login-button:hover {
        background-color: #555555;
    }

    .signup-link {
        margin-top: 20px;
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

    p{
        font-family: Poppins;
    }
</style>