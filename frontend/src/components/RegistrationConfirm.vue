<!--Created by: John Montesa-->
<!-- This is the page after registering for Course Compass -->
<!-- This page will prompt the user for the next step in the sign up process -->

<template>
  <v-container fluid fill-height>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6">
        <img src="../assets/course compass logo.png" alt="University of Nevada, Reno logo." class="mx-auto d-block" style="width: 225px; height:auto;">
        <br>
        <h1 class="text-center" style="font-family: Coolvetica;">Thank you for registering!<br>There is one more step to finish your sign up.</h1>
        <p class="text-center">
            <br>
            We have sent a confirmation letter to your email!
            <br>
            <br>
            Please check your email inbox for a confirmation email to complete your sign up. 
            Once complete you will be able to log in to your account. If it is not there, please check your <strong>spam folder</strong>.
            <br>
            <br>
            <em>Still can't find it?</em>
            </p>
                <v-dialog v-model="dialog" max-width="600" style="font-family: Poppins;">
                    <template v-slot:activator="{ props: activatorProps }">
                        <div class="resend-container">
                            <btn v-bind="activatorProps" class="resend-button" @click="resendEmail">Resend Email</btn>
                        </div>
                    </template>
                    <!-- Confirmation dialog for resend email -->
                    <!--Pop up -->
                    <v-card title="Confirmation email resent!">
                        <v-card-text>
                            <v-row dense>
                                <v-col>
                                    <p>A confirmation email has been resent to your email. Please check your inbox.</p>
                                </v-col>
                            </v-row>
                        </v-card-text> 
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="grey" text="Close" variant="tonal" @click="dialog = false"></v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
    import axios from 'axios';

    export default {
        data() {
            return{
                dialog: false,
                email: '', // Populate with user email
            };
        },
        methods: {
            resendEmail() {
                axios.post('http://127.0.0.1:5000/resend_confirmation_email', { email: this.email })
                    .then(response => {
                        this.dialog=true;
                    })
                    .catch(error => {
                        console.error("Error resending email", error);
                    });
            },
        },
    };
</script>

<style scoped>
    .resend-container{
        display:flex;
        justify-content: space-between;
    }

    .resend-button {
        margin: auto;
        position: relative;
        font-family: coolvetica;
        background-color: #000000;
        color: #ffffff;
        padding: 5px 10px;
        font-size: 15px;
        border-radius: 5px;
        margin-top: -10px;
        cursor: pointer;
        transition: background-color 0.3s linear, color 0.3s linear;
        text-decoration: none;
    }

    .resend-button:hover {
        background-color: #ffffff;
        color: #000000;
    }
</style>
