<!--Admin Dashboard Page-->
<!-- Created by: John Montesa -->

<template>
    <v-row no-gutters>
            <v-col cols="2">
                <h2 class="welcome-text">
                    Welcome, {{user.firstname}}
                </h2>
                <v-divider></v-divider>
                <v-tabs v-model="tab" direction="vertical" color="primary" selected-class="selected-tab" slider-color="black">
                    <v-tab value="dashboard" @click="chooseDashboard()">
                        <v-icon start>
                            <span class="material-icons" style="color:black">dashboard</span>
                        </v-icon>
                        Admin Dashboard
                    </v-tab>
                    <v-tab value="instructors" @click="chooseInstructors">
                        <v-icon start>
                            <span class="material-icons" style="color:black">verified</span>
                        </v-icon>
                        Approve Instructors
                    </v-tab>
                    <v-tab value="analytics" @click="chooseAnalytics()">
                        <v-icon start>
                            <span class="material-icons" style="color:black">analytics</span>
                        </v-icon>
                        Site Analytics
                    </v-tab>
                </v-tabs>
            </v-col>


            <v-col>
                <div class="dashboard-page" v-if="this.dashboard === true">
                    <div class="dashboard-container">
                        <p>Admin Options</p>
                        <p>Send a site-wide announcement:</p>
                        <p>Send an email to all users:</p>
                        <p>Log out</p>
                    </div>
                </div>

                <div class="instructors-page" v-if="this.instructors === true">
                    <v-expansion-panels>
                        <v-expansion-panel>
                            <v-expansion-panel-title>
                                    <v-row no-gutters>
                                        <v-col class="d-flex justify-start" cols="4">
                                        Pending Instructors ({{pendingInstructors.length}})
                                        </v-col>
                                    </v-row>
                            </v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <v-row class="instructor-rows" no-gutters v-for="(instructor, index) in pendingInstructors" :key="index">
                                    <v-col cols="10">
                                        <p>{{pendingInstructors[index].name}} - {{pendingInstructors[index].email}}</p>
                                    </v-col>
                                    <v-col cols="1">
                                        <v-btn icon="$close" variant="plain" @click="removePendingInstructor(index)">
                                            <span class="material-symbols-outlined">
                                            block
                                            </span>
                                        </v-btn>
                                    </v-col>
                                    <v-col cols="1">
                                        <v-btn icon="$close" variant="plain" @click="approvePendingInstructor(index)">
                                            <span class="material-symbols-outlined">
                                            check_circle
                                            </span>
                                        </v-btn>
                                    </v-col>
                                    <v-divider class="instructor-divider"></v-divider>
                                </v-row>
                            </v-expansion-panel-text>
                        </v-expansion-panel>
                        
                        <v-expansion-panel>
                            <v-expansion-panel-title>
                                    <v-row no-gutters>
                                        <v-col class="d-flex justify-start" cols="4">
                                        Approved Instructors ({{approvedInstructors.length}})
                                        </v-col>
                                        <v-col class="text-grey" cols="8">
                                        </v-col>
                                    </v-row>
                            </v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <v-row class="instructor-rows" no-gutters v-for="(instructor, index) in approvedInstructors" :key="index">
                                    <v-col cols="11">
                                        <p>{{approvedInstructors[index].name}} - {{approvedInstructors[index].email}}</p>
                                    </v-col>
                                    <v-col cols="1">
                                        <v-btn icon="$close" variant="plain" @click="removeApprovedInstructor(index)">
                                            <span class="material-symbols-outlined">
                                            block
                                            </span>
                                        </v-btn>
                                    </v-col>
                                    <v-divider class="instructor-divider"></v-divider>
                                </v-row>
                            </v-expansion-panel-text>
                        </v-expansion-panel>
                    </v-expansion-panels>
                </div>




                <div class="analytics-page" v-if="this.analytics === true">

                </div>

            </v-col>
    </v-row>
    
    
    
</template>

<script>
    export default {
        data() {
            return {
                confirmationDialog: false,
                tab: 'dashboard',
                dashboard: true,
                instructors: false,
                analytics: false,
                user: {
                    firstname: 'John',
                    lastname: '',
                    email: '',
                    major: '',
                },

                approvedInstructors: [],
                pendingInstructors: [
                    {name: 'Jeremy Potts', email: 'jeremypotts@nevada.unr.edu'},
                    {name: 'Jimmy Fraschia', email: 'jimmy.fraschia@gmail'},
                ],
            };
        },

        methods:{
            handleToast(toastData) {

            console.log(toastData.message);
            },

            chooseInstructors(){
                this.tab = 'instructors';
                this.dashboard = false;
                this.analytics = false;
                this.instructors = true;
            },

            chooseDashboard(){
                this.tab = 'dashboard';
                this.instructors = false;
                this.analytics = false;
                this.dashboard = true;
            },

            chooseAnalytics(){
                this.tab = 'analytics';
                this.dashboard = false;
                this.instructors = false;
                this.analytics = true;
            },

            removePendingInstructor(index) {
                this.pendingInstructors.splice(index, 1);
            },

            removeApprovedInstructor(index) {
                this.approvedInstructors.splice(index, 1);
            },

            approvePendingInstructor(index) {
                const instructor = this.pendingInstructors[index];
                this.approvedInstructors.push(instructor);
                this.removePendingInstructor(index);
            },
            
        },
    

        computed: {
            
            },
    };
</script>

<style scoped>
    .welcome-text{
        font-family: Poppins;
        margin-left: 14px;
        margin-top: 13px;

    }
    .v-tab{
        font-family: Poppins;
    }

    .selected-tab{
        background-color: rgb(224, 224, 224);
    }

    .dashboard-page{
        border-left: 1px solid black;
        min-height: 250px;
    }

    .instructors-page{
        border-left: 1px solid black;
        min-height: 250px;
    }

    .analytics-page{
        border-left: 1px solid black;
        min-height: 250px;
    }

    .v-expansion-panel{
        position: relative;
        background-color: rgba(187, 187, 187, 0.242);
        font-family: Poppins;
        border-radius: 0px;
    }

    .dashboard-container{
        background-color: rgba(187, 187, 187, 0.242);
        position: relative;
        top: 15px;
        margin-left: 15px;
        margin-right: 15px;
        border-radius: 7px;
        font-family: Poppins;
    }
    .instructor-divider{
        width: 90%;
    }
</style>
