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
                                                <v-row dense>
                                                    <v-col cols = "12" md="6">  
                                                        <br>
                                                        <v-textarea v-model="notificationDescription" label="Notification Description" single-line rows="8"></v-textarea>
                                                        <br>
                                                        <v-checkbox v-model="notificationOverride" label="Override all notifications?" hint="This notification is urgent and will be shown over other notifications until after selected date."></v-checkbox>
                                                    </v-col>
                                                    <v-col cols="12" md="6">
                                                        <v-date-picker v-model="notificationDate" width="100%"></v-date-picker>
                                                    </v-col>
                                                </v-row>
                                            </v-card-text> 
                                            <v-card-actions>
                                                <v-spacer></v-spacer>
                                                <v-btn text="Close" variant="plain" @click="notificationDialog = false"></v-btn>
                                                <v-btn color="primary" text="Send" variant="tonal" @click="sendNotification()"></v-btn>
                                            </v-card-actions>
                                        </v-card>
                                    </v-dialog>

                                </v-col>
                                <v-col cols="4" class="d-flex justify-center align-center">
                                    <v-dialog v-model="emailDialog" max-width="1000" style="font-family: Poppins;">
                                        <template v-slot:activator="{ props: activatorProps }">
                                            <v-btn v-bind="activatorProps" stacked variant="outlined" style="height:150px; width:350px;">
                                                <span class="material-symbols-outlined">
                                                    stacked_email
                                                </span>
                                                <br>
                                                Send an Email to Users
                                            </v-btn>
                                        </template>
                                        <!--Pop up -->
                                        <v-card title="Send An Email to Users">
                                            <v-card-text>
                                                <v-row dense>
                                                    <v-col cols = "12">  
                                                        <v-text-field v-model="emailSubject" label="Email Subject" required></v-text-field>
                                                        <v-select v-model="emailTo" :items="this.to" label="Send Email To:" required></v-select>
                                                        <v-textarea v-model="emailContent" label="Email Description" single-line rows="8"></v-textarea>

                                                    </v-col>
                                                </v-row>
                                            </v-card-text> 
                                            <v-card-actions>
                                                <v-spacer></v-spacer>
                                                <v-btn text="Close" variant="plain" @click="emailDialog = false"></v-btn>
                                                <v-btn color="primary" text="Send" variant="tonal" @click="sendEmail()"></v-btn>
                                            </v-card-actions>
                                        </v-card>
                                    </v-dialog>
                                </v-col>

                                <v-col cols="4" class="d-flex justify-center align-center">
                                    <v-dialog v-model="settingsDialog" max-width="1000" style="font-family: Poppins;">
                                        <template v-slot:activator="{ props: activatorProps }">
                                            <v-btn v-bind="activatorProps" stacked variant="outlined" style="height:150px; width:350px;">
                                                <span class="material-symbols-outlined">
                                                    settings
                                                </span>
                                                <br>
                                                Admin Settings
                                            </v-btn>
                                        </template>
                                        <!--Pop up -->
                                        <v-card title="Admin Settings">
                                            <v-card-text>
                                                <v-row dense>
                                                    <v-expansion-panels>
                                                        <v-expansion-panel>
                                                            <v-expansion-panel-title>
                                                                    <v-row no-gutters>
                                                                        <v-col class="d-flex justify-start" cols="4">
                                                                            Active Admin Notifications ({{adminNotifications.length}})
                                                                        </v-col>
                                                                    </v-row>
                                                            </v-expansion-panel-title>
                                                            <v-expansion-panel-text>
                                                                <v-row  no-gutters v-for="(notification, index) in adminNotifications" :key="index">
                                                                    <v-col cols="11">
                                                                        <p class="row-text"><strong>{{adminNotifications[index].date}}</strong> {{adminNotifications[index].source}} - {{adminNotifications[index].description}}</p>
                                                                    </v-col>
                                                                    <v-col cols="1">
                                                                        <v-dialog v-model="removeNotificationDialog[index]" max-width="800" style="font-family: Poppins;">
                                                                            <template v-slot:activator="{ props: activatorProps }">
                                                                                <v-btn v-bind="activatorProps" icon="$close" variant="plain">
                                                                                    <span class="material-symbols-outlined">
                                                                                    block
                                                                                    </span>
                                                                                </v-btn>
                                                                            </template>
                                                                            <!--Pop up -->
                                                                            <v-card title="Are you sure you want to remove notification:">
                                                                                <v-card-text>
                                                                                    <br>
                                                                                    <p><strong>{{adminNotifications[index].date}}</strong> {{adminNotifications[index].source}} - {{adminNotifications[index].description}}</p>
                                                                                </v-card-text> 
                                                                                <v-card-actions>
                                                                                    <v-spacer></v-spacer>
                                                                                    <v-btn text="No" variant="plain" @click="removeNotificationDialog[index] = false"></v-btn>
                                                                                    <v-btn color="primary" text="Yes" variant="tonal" @click="removeNotification(index)"></v-btn>
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
                                                                            Outbound Emails ({{emailSent.length}})
                                                                        </v-col>
                                                                    </v-row>
                                                            </v-expansion-panel-title>
                                                            <v-expansion-panel-text>
                                                                <v-row  no-gutters v-for="(email, index) in emailSent" :key="index">
                                                                    <v-col cols="11">
                                                                        <p class="row-text"><strong>{{emailSent[index].date}}</strong> {{emailSent[index].subject}}</p>
                                                                    </v-col>
                                                                    <v-col cols="1">
                                                                        <v-dialog v-model="removeEmailDialog[index]" max-width="800" style="font-family: Poppins;">
                                                                            <template v-slot:activator="{ props: activatorProps }">
                                                                                <v-btn v-bind="activatorProps" icon="$close" variant="plain">
                                                                                    <span class="material-symbols-outlined">
                                                                                        expand_content
                                                                                    </span>
                                                                                </v-btn>
                                                                            </template>
                                                                            <!--Pop up -->
                                                                            <v-card title="Email Details">
                                                                                <v-card-text>
                                                                                    <br>
                                                                                    <p>Sent to  - {{emailSent[index].to}}</p>
                                                                                    <p>Email Content - {{emailSent[index].content}}</p>
                                                                                </v-card-text> 
                                                                                <v-card-actions>
                                                                                    <v-spacer></v-spacer>
                                                                                    <v-btn text="Close" variant="plain" @click="removeEmailDialog[index] = false"></v-btn>
                                                                                </v-card-actions>
                                                                            </v-card>
                                                                        </v-dialog> 
                                                                    </v-col>
                                                                    <v-divider class="instructor-divider"></v-divider>
                                                                </v-row>
                                                            </v-expansion-panel-text>
                                                        </v-expansion-panel>
                                                    </v-expansion-panels>
                                                </v-row>
                                            </v-card-text> 
                                            <v-card-actions>
                                                <v-spacer></v-spacer>
                                                <v-btn text="Close" variant="plain" @click="settingsDialog = false"></v-btn>
                                            </v-card-actions>
                                        </v-card>
                                    </v-dialog>
                                </v-col>
                            </v-row>

                            <v-row>
                                <v-col cols="4"></v-col>
                                <v-col cols="4"></v-col>
                                <v-col cols="4" class="d-flex justify-end align-center" style="margin-left:-12px;">
                                    <v-btn variant="outlined" @click.prevent="handleLogout">
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
                                <v-row no-gutters v-for="(instructor, index) in pendingInstructors" :key="index">
                                    <v-col cols="10">
                                        <p class="row-text">{{pendingInstructors[index].name}} - {{pendingInstructors[index].email}}</p>
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
                                <v-row no-gutters v-for="(instructor, index) in approvedInstructors" :key="index">
                                    <v-col cols="11">
                                        <p class="row-text">{{approvedInstructors[index].name}} - {{approvedInstructors[index].email}}</p>
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
    import axios from 'axios';

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
                settingsDialog: false,
                emailDialog: false,
                removeDialog: [],
                removeNotificationDialog: [],
                removeEmailDialog: [],
                approveDialog: [],
                

                source: 'Admin',
                notificationDescription: '',
                notificationOverride: false,
                notificationDate: new Date(),
                adminNotifications:[],

                to:['All Users', 'Admins', 'Instructors', 'Students'],
                emailSubject: '',
                emailTo: '',
                emailContent: '',
                emailSent: [],
            };
        },

        methods:{
            handleLogout() {
                axios.post('http://127.0.0.1:5000/logout', {}, { withCredentials: true })
                    .then(response => {
                        console.log(response.data.message);
                        if (response.status === 200) {
                        setTimeout(() => {
                            this.$emit('logout');
                            this.$router.push('/');
                        }, 1000);
                        } else {
                            console.error("Unexpected response during logout: ", response);
                        }
                    })
                    .catch(error => {
                        console.error("Logout error: ", error);
                    });
            },
        
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

            removeNotification(index){
                this.adminNotifications.splice(index, 1);
                this.removeNotificationDialog[index] = false;
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

            sendNotification(){
                const reformatDate = new Date(this.notificationDate).toLocaleDateString('en-US', {
                    month: 'long',
                    day: 'numeric',
                    year: 'numeric',
                });

                const notification = {
                    date: reformatDate,
                    source: this.source,
                    description: this.notificationDescription,
                };

                this.adminNotifications.push(notification);

                this.notificationDate = new Date();
                this.notificationDescription ='';
                this.notificationOverride = false;
                this.notificationDialog = false;
            },

            sendEmail(){
                const reformatDate = new Date(this.notificationDate).toLocaleDateString('en-US', {
                    month: 'long',
                    day: 'numeric',
                    year: 'numeric',
                });

                const email = {
                    date: reformatDate,
                    subject: this.emailSubject,
                    to: this.emailTo,
                    content: this.emailContent,
                };

                this.emailSent.push(email);
                this.emailSubject = '';
                this.emailTo = '';
                this.emailContent = '';
                this.emailDialog = false;
            },
        },
    

        computed: {
            
            },
    };
</script>

<style scoped>
    .welcome-text{
        font-family: Poppins;
        font-size: 28px;
        margin-left: 14px;
        margin-top: 13px;
    }

    .admin-text{
        position: relative;
        top: 12px;
        margin-left: 10px;
        font-size: 24px;
    }
    
    .row-text{
        margin-top: 15px;
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

    .v-date-picker{
        margin-top: -29px;
        margin-bottom: -38px;
    }
</style>
