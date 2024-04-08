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
                        <h3 class="admin-text">Admin Options</h3>

                        <v-container>
                            <v-row>
                                <v-col cols="4" class="d-flex justify-center align-center">
                                    <v-dialog v-model="notificationDialog" max-width="1000" style="font-family: Poppins;">
                                        <template v-slot:activator="{ props: activatorProps }">
                                            <v-btn v-bind="activatorProps" stacked variant="outlined" style="height:150px; width:350px;">
                                                <span class="material-symbols-outlined">
                                                    campaign
                                                </span>
                                                <br>
                                                Send a Site Wide Notification
                                            </v-btn>
                                        </template>
                                        <!--Pop up -->
                                        <v-card title="Send A Site Wide Notification">
                                            <v-card-text>
                                                <br>
                                                <v-row>
                                                    <v-col cols="4">
                                                        <v-menu
                                                            v-model="menu"
                                                            :close-on-content-click="false"
                                                            transition="scale-transition"
                                                            offset-y
                                                        >
                                                            <template v-slot:activator="{ on }">
                                                            <v-btn
                                                                color="primary"
                                                                dark
                                                                v-on="on"
                                                            >
                                                                Open Date Picker
                                                            </v-btn>
                                                            </template>
                                                            <v-date-picker
                                                            v-model="selectedDate"
                                                            @input="menu = false"
                                                            locale="en-us"
                                                            scrollable
                                                            ></v-date-picker>
                                                        </v-menu>
                                                    </v-col>
                                                </v-row>
                                            </v-card-text> 
                                            <v-card-actions>
                                                <v-spacer></v-spacer>
                                                <v-btn text="Close" variant="plain" @click="notificationDialog = false"></v-btn>
                                                <v-btn color="primary" text="Send" variant="tonal"></v-btn>
                                            </v-card-actions>
                                        </v-card>
                                    </v-dialog>

                                </v-col>
                                <v-col cols="4" class="d-flex justify-center align-center">
                                    <v-btn stacked variant="outlined" style="height:150px; width:350px;">
                                        <span class="material-symbols-outlined">
                                            stacked_email
                                        </span>
                                        <br>
                                        Send an Email to Users
                                    </v-btn>
                                </v-col>
                                <v-col cols="4" class="d-flex justify-center align-center">
                                    <v-btn stacked variant="outlined" style="height:150px; width:350px;">
                                        <span class="material-symbols-outlined">
                                            settings
                                        </span>
                                        <br>
                                        Other Admin Settings
                                    </v-btn>
                                </v-col>
                            </v-row>

                            <v-row>
                                <v-col cols="4"></v-col>
                                <v-col cols="4"></v-col>
                                <v-col cols="4" class="d-flex justify-end align-center" style="margin-left:-12px;">
                                    <v-btn variant="outlined">
                                        Log Out
                                    </v-btn>
                                </v-col>
                            </v-row>
                        </v-container>
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
                                        <v-dialog v-model="removeDialog[index]" max-width="500" style="font-family: Poppins;">
                                            <template v-slot:activator="{ props: activatorProps }">
                                                <v-btn v-bind="activatorProps" icon="$close" variant="plain">
                                                    <span class="material-symbols-outlined">
                                                    block
                                                    </span>
                                                </v-btn>
                                            </template>
                                            <!--Pop up -->
                                            <v-card title="Are you sure you want to remove instructor:">
                                                <v-card-text>
                                                    <br>
                                                    <p>{{pendingInstructors[index].name}} - {{pendingInstructors[index].email}}</p>
                                                </v-card-text> 
                                                <v-card-actions>
                                                    <v-spacer></v-spacer>
                                                    <v-btn text="No" variant="plain" @click="removeDialog[index] = false"></v-btn>
                                                    <v-btn color="primary" text="Yes" variant="tonal" @click="removePendingInstructor(index)"></v-btn>
                                                </v-card-actions>
                                            </v-card>
                                        </v-dialog>                                        

                                    </v-col>
                                    <v-col cols="1">
                                        <v-dialog v-model="approveDialog[index]" max-width="500" style="font-family: Poppins;">
                                            <template v-slot:activator="{ props: activatorProps }">
                                                <v-btn v-bind="activatorProps" icon="$close" variant="plain">
                                                    <span class="material-symbols-outlined">
                                                    check_circle
                                                    </span>
                                                </v-btn>
                                            </template>
                                            <!--Pop up -->
                                            <v-card title="Are you sure you want to approve instructor:">
                                                <v-card-text>
                                                    <br>
                                                    <p>{{pendingInstructors[index].name}} - {{pendingInstructors[index].email}}</p>
                                                </v-card-text> 
                                                <v-card-actions>
                                                    <v-spacer></v-spacer>
                                                    <v-btn text="No" variant="plain" @click="approveDialog[index] = false"></v-btn>
                                                    <v-btn color="primary" text="Yes" variant="tonal" @click="approvePendingInstructor(index)"></v-btn>
                                                </v-card-actions>
                                            </v-card>
                                        </v-dialog>   

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
                                        <v-dialog v-model="removeDialog[index]" max-width="500" style="font-family: Poppins;">
                                            <template v-slot:activator="{ props: activatorProps }">
                                                <v-btn v-bind="activatorProps" icon="$close" variant="plain">
                                                    <span class="material-symbols-outlined">
                                                    block
                                                    </span>
                                                </v-btn>
                                            </template>
                                            <!--Pop up -->
                                            <v-card title="Are you sure you want to remove instructor:">
                                                <v-card-text>
                                                    <br>
                                                    <p>{{approvedInstructors[index].name}} - {{approvedInstructors[index].email}}</p>
                                                </v-card-text> 
                                                <v-card-actions>
                                                    <v-spacer></v-spacer>
                                                    <v-btn text="No" variant="plain" @click="removeDialog[index] = false"></v-btn>
                                                    <v-btn color="primary" text="Yes" variant="tonal" @click="removeApprovedInstructor(index)"></v-btn>
                                                </v-card-actions>
                                            </v-card>
                                        </v-dialog> 

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
                
                notificationDialog: false,
                removeDialog: [],
                approveDialog: [],

                date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
                menu: false,
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
                this.removeDialog[index] = false;
            },

            removeApprovedInstructor(index) {
                this.approvedInstructors.splice(index, 1);
                this.removeDialog[index] = false;
            },

            approvePendingInstructor(index) {
                const instructor = this.pendingInstructors[index];
                this.approveDialog[index] = false;                
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

    .admin-text{
        margin-left: 10px;
    }
    
    .v-tab{
        font-family: Poppins;
    }

    .selected-tab{
        background-color: rgb(224, 224, 224);
    }

    .dashboard-page{
        border-left: 1px solid black;
        height: 100%;
    }

    .instructors-page{
        border-left: 1px solid black;
        height: 100%;
    }

    .analytics-page{
        border-left: 1px solid black;
        height: 100%;    }

    .v-expansion-panel{
        position: relative;
        background-color: rgba(187, 187, 187, 0.242);
        font-family: Poppins;
        border-radius: 0px;
    }

    .dashboard-container{
        position: relative;
        font-family: Poppins;
    }

    .instructor-divider{
        width: 90%;
    }
</style>
