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
                        Manage Instructors
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
                                                        Source:
                                                        <v-select :items="sources" v-model="selectedSource"></v-select>
                                                        Description:
                                                        <v-textarea v-model="notificationDescription" label="Notification Description" single-line rows="8"></v-textarea>
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
                                                        Subject:
                                                        <v-text-field v-model="emailSubject" label="Email Subject" required></v-text-field>
                                                        Recipients:
                                                        <v-select v-model="emailTo" :items="this.to" label="Send Email To:" required></v-select>
                                                        Body:
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
                                                                        <p class="row-text"><strong>{{adminNotifications[index].date}}</strong> {{adminNotifications[index].source}} - {{adminNotifications[index].description}}<br>Override Status: {{adminNotifications[index].override}}</p>
                                                                    </v-col>
                                                                    <v-col cols="1">
                                                                        <v-dialog v-model="removeNotificationDialog[index]" max-width="800" style="font-family: Poppins;">
                                                                            <template v-slot:activator="{ props: activatorProps }">
                                                                                <v-btn v-bind="activatorProps" icon="$close" variant="plain">
                                                                                    <span class="material-symbols-outlined">
                                                                                    delete
                                                                                    </span>
                                                                                </v-btn>
                                                                            </template>
                                                                            <!--Pop up -->
                                                                            <v-card title="Are you sure you want to remove:">
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
                    <h3 class="admin-text">Manage Instructors</h3>
                    <div class="instructors-container">
                        <v-container class="panel-container">
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
                                                <v-card title="Are you sure you want to deny:">
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
                                                <v-card title="Are you sure you want to approve:">
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
                                            <p class="row-text" :style="approvedInstructors[index].onHold ? { color: 'grey' } : {}">{{approvedInstructors[index].name}} - {{approvedInstructors[index].email}}
                                                <span v-if="approvedInstructors[index].onHold === true"><em><br> On Administrative Hold</em> - {{approvedInstructors[index].holdReason}}</span></p>
                                        </v-col>
                                        <v-col cols="1">
                                            <v-dialog v-model="instructorDialog[index]" max-width="700" style="font-family: Poppins;">
                                                <template v-slot:activator="{ props: activatorProps }">
                                                    <v-btn v-bind="activatorProps" variant="plain">
                                                        <span class="material-symbols-outlined">
                                                            more_horiz
                                                        </span>
                                                    </v-btn>
                                                </template>
                                                <!--Pop up -->
                                                <v-card>
                                                    <v-card-title>
                                                        <strong>{{approvedInstructors[index].name}}</strong>
                                                    </v-card-title>
                                                    <v-card-text>
                                                        <p>Instructor Information:</p>
                                                        <p>Name: {{approvedInstructors[index].name}}
                                                        <br>Email: {{approvedInstructors[index].email}}
                                                        <br>
                                                        <br>
                                                        <v-row>
                                                            <v-col cols="auto">
                                                                <v-switch
                                                                    v-model="approvedInstructors[index].onHold"
                                                                    color="primary"
                                                                    label="On Hold"
                                                                ></v-switch>
                                                            </v-col>
                                                            <v-col>
                                                                <v-text-field 
                                                                    v-model="approvedInstructors[index].holdReason"
                                                                    v-if="approvedInstructors[index].onHold === true"
                                                                    label="Reason for hold"
                                                                    dense
                                                                ></v-text-field>
                                                            </v-col>
                                                        </v-row>
                                                        <br>Courses Taught:
                                                        <br>
                                                        
                                                        </p>
                                                    </v-card-text> 
                                                    <v-card-actions>
                                                        <v-dialog v-model="archiveDialog[index]" max-width="500" style="font-family: Poppins;">
                                                            <template v-slot:activator="{ props: activatorProps }">
                                                                <v-btn v-bind="activatorProps" text="Archive Instructor" variant="tonal" color="red"></v-btn>
                                                            </template>
                                                            <!--Pop up -->
                                                            <v-card title="Are you sure you want to archive:">
                                                                <v-card-text>
                                                                    <br>
                                                                    <p>{{approvedInstructors[index].name}} - {{approvedInstructors[index].email}}</p>
                                                                </v-card-text> 
                                                                <v-card-actions>
                                                                    <v-spacer></v-spacer>
                                                                    <v-btn text="No" variant="plain" @click="archiveDialog[index] = false"></v-btn>
                                                                    <v-btn color="primary" text="Yes" variant="tonal" @click="archiveApprovedInstructor(index)"></v-btn>
                                                                </v-card-actions>
                                                            </v-card>
                                                        </v-dialog> 
                                                        <v-spacer></v-spacer>
                                                        <v-btn text="Close" variant="plain" @click="instructorDialog[index] = false"></v-btn>
                                                    </v-card-actions>
                                                </v-card>
                                            </v-dialog> 

                                        </v-col>
                                        <v-divider class="instructor-divider"></v-divider>
                                    </v-row>
                                </v-expansion-panel-text>
                            </v-expansion-panel>

                            <!--archived-->
                            <v-expansion-panel>
                                <v-expansion-panel-title>
                                        <v-row no-gutters>
                                            <v-col class="d-flex justify-start" cols="4">
                                            Archived Instructors ({{archivedInstructors.length}})
                                            </v-col>
                                        </v-row>
                                </v-expansion-panel-title>
                                <v-expansion-panel-text>
                                    <v-row no-gutters v-for="(instructor, index) in archivedInstructors" :key="index">
                                        <v-col cols="10">
                                            <p class="row-text">{{archivedInstructors[index].name}} - {{archivedInstructors[index].email}}</p>
                                        </v-col>
                                        <v-col cols="1">
                                            <v-dialog v-model="removeDialog[index]" max-width="500" style="font-family: Poppins;">
                                                <template v-slot:activator="{ props: activatorProps }">
                                                    <v-btn v-bind="activatorProps" variant="plain">
                                                        <span class="material-symbols-outlined">
                                                            block
                                                        </span>
                                                    </v-btn>
                                                </template>
                                                <!--Pop up -->
                                                <v-card title="Are you sure you want to remove:">
                                                    <v-card-text>
                                                        <br>
                                                        <p>{{archivedInstructors[index].name}} - {{archivedInstructors[index].email}}</p>
                                                    </v-card-text> 
                                                    <v-card-actions>
                                                        <v-spacer></v-spacer>
                                                        <v-btn text="No" variant="plain" @click="removeDialog[index] = false"></v-btn>
                                                        <v-btn color="primary" text="Yes" variant="tonal" @click="removeArchivedInstructor(index)"></v-btn>
                                                    </v-card-actions>
                                                </v-card>
                                            </v-dialog> 
                                        </v-col>
                                        <v-col cols="1">
                                            <v-dialog v-model="unarchiveDialog[index]" max-width="500" style="font-family: Poppins;">
                                                <template v-slot:activator="{ props: activatorProps }">
                                                    <v-btn v-bind="activatorProps" variant="plain">
                                                        <span class="material-symbols-outlined">
                                                            published_with_changes
                                                        </span>
                                                    </v-btn>
                                                </template>
                                                <!--Pop up -->
                                                <v-card title="Are you sure you want to unarchive:">
                                                    <v-card-text>
                                                        <br>
                                                        <p>{{archivedInstructors[index].name}} - {{approvedInstructors[index].email}}</p>
                                                    </v-card-text> 
                                                    <v-card-actions>
                                                        <v-spacer></v-spacer>
                                                        <v-btn text="No" variant="plain" @click="unarchiveDialog[index] = false"></v-btn>
                                                        <v-btn color="primary" text="Yes" variant="tonal" @click="unarchiveInstructor(index)"></v-btn>
                                                    </v-card-actions>
                                                </v-card>
                                            </v-dialog> 
                                        </v-col>
                                        <v-divider class="instructor-divider"></v-divider>
                                    </v-row>
                                </v-expansion-panel-text>
                            </v-expansion-panel>
                        </v-expansion-panels>
                        </v-container>
                    </div>
                </div>




                <div class="analytics-page" v-if="this.analytics === true">
                    <h3 class="admin-text">Site Analytics</h3>
                    <v-container>
                        <v-row>
                        <v-col cols="6">
                            <v-card style="border: 1px solid black; height: 420px;">
                            <v-card-title style="font-family:Poppins;">Registered Users</v-card-title>
                            <br>
                            <v-card-text>
                                <v-sparkline
                                    :auto-line-width="false"
                                    :gradient="['navy']"
                                    :line-width="'15'"
                                    :smooth="2"
                                    :model-value="[userAnalytics[0].count, userAnalytics[1].count, userAnalytics[2].count]"
                                    :padding="'0'"
                                    :type="'bar'"
                                    auto-draw
                                    style="font-family: Poppins;"
                                >
                                <template v-slot:label="item">
                                    {{ item.value }}
                                </template>
                                </v-sparkline>
                                <v-divider></v-divider>
                                <v-row>
                                    <v-col cols="4">
                                        <p class="analytics-label" style="margin-left: 17px;">{{userAnalytics[0].label}}</p>
                                    </v-col>
                                    <v-col cols="4">
                                        <p class="analytics-label">{{userAnalytics[1].label}}</p>
                                    </v-col>
                                    <v-col cols="4">
                                        <p class="analytics-label" style="margin-right: 17px;">{{userAnalytics[2].label}}</p>
                                    </v-col>
                                </v-row>
                                <v-row>
                                    <p class="analytics-label" style="margin-left: 17px;"> Total users: {{ userAnalytics[0].count + userAnalytics[1].count + userAnalytics[2].count }}</p>
                                </v-row>
                            </v-card-text>
                            </v-card>
                        </v-col>

                        <v-col cols="6">
                            <v-card style="border: 1px solid black; height: 420px;">
                                <v-card-title style="font-family:Poppins;">User Analytics</v-card-title>
                                <v-card-text>
                                    <v-row>
                                        <p style="font-family:Poppins; margin-left:19px;">Average Users Per Day</p>
                                        <v-col cols="12">
                                            <v-sparkline
                                                :auto-line-width="false"
                                                :gradient="['pink']"
                                                :line-width="'2'"
                                                :smooth="0"
                                                :model-value="[2, 5, 9, 5, 10, 3, 5]"
                                                :padding="'5'"
                                                :type="'trend'"
                                                auto-draw
                                                style="font-family: Poppins;"
                                            >
                                            <template v-slot:label="item">
                                                {{ item.value }}
                                            </template>
                                            </v-sparkline>
                                        </v-col>
                                    </v-row>
                                    <v-divider></v-divider>
                                    <v-row>
                                        <v-col cols="1.5">
                                            <p style="font-family: Poppins; margin-left: 5px;">Sun</p>
                                        </v-col>
                                        <v-col cols="1.5">
                                            <p style="font-family: Poppins; margin-left: 6px;">Mon</p>
                                        </v-col>
                                        <v-col cols="1.5">
                                            <p style="font-family: Poppins;margin-left: 10px;">Tue</p>
                                        </v-col>
                                        <v-col cols="1.5">
                                            <p style="font-family: Poppins;margin-left: 15px;">Wed</p>
                                        </v-col>
                                        <v-col cols="1.5">
                                            <p style="font-family: Poppins;margin-left: 16px;">Thurs</p>
                                        </v-col>
                                        <v-col cols="1.5">
                                            <p style="font-family: Poppins;margin-left: 35px;">Fri</p>
                                        </v-col>
                                        <v-col cols="1.5">
                                            <p style="font-family: Poppins;margin-left: 33px;">Sat</p>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col cols="12">
                                            <p style="font-family: Poppins;">Currently Active Users: 0</p>
                                        </v-col>
                                    </v-row>

                                </v-card-text>
                                </v-card>                            
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="12">
                            <v-card style="border: 1px solid black;">
                                <v-card-title style="font-family:Poppins;">Stored Data</v-card-title>
                                <v-card-text>
                                    <v-row>
                                        <v-col cols="12">
                                            <v-sparkline
                                                :auto-line-width="false"
                                                :gradient="['black']"
                                                :line-width="'10'"
                                                :smooth="2"
                                                :model-value="[78, 3, 9, 5, 10, 0, 0]"
                                                :padding="'5'"
                                                :type="'bar'"
                                                auto-draw
                                                style="font-family: Poppins;"
                                            >
                                            <template v-slot:label="item">
                                                {{ item.value }}
                                            </template>
                                            </v-sparkline>
                                        </v-col>
                                    </v-row>
                                    <v-divider></v-divider>
                                    <v-row>
                                        <v-col cols="1.5">
                                            <p style="font-family: Poppins; margin-left: 60px;">Courses</p>
                                        </v-col>
                                        <v-col cols="1.5">
                                            <p style="font-family: Poppins; margin-left: 50px;">Majors</p>
                                        </v-col>
                                        <v-col cols="1.5">
                                            <p style="font-family: Poppins;margin-left: 0px;">Student Reviews</p>
                                        </v-col>
                                        <v-col cols="1.5">
                                            <p style="font-family: Poppins;margin-left: -8px;">User Schedules</p>
                                        </v-col>
                                        <v-col cols="1.5">
                                            <p style="font-family: Poppins;margin-left: -33px;">Announcements</p>
                                        </v-col>
                                        <v-col cols="1.5">
                                            <p style="font-family: Poppins;margin-left: 0px;">TBA</p>
                                        </v-col>
                                        <v-col cols="1">
                                            <p style="font-family: Poppins;margin-left: -16px;">TBA</p>
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                                </v-card>                            
                            </v-col>
                        </v-row>
                    </v-container>
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

                approvedInstructors: [
                    {name: 'Tony Yars', email: 'tyars@nevada.unr.edu', onHold: false, holdReason: ''},
                    {name: 'Hank Stark', email: 'hstark@nevada.unr.edu', onHold: true, holdReason: 'University Adminsitrative Leave'},
                ],

                archivedInstructors: [
                    {name: 'Tom Ross', email: 't.ross@nevada.unr.edu', onHold: false},
                ],

                pendingInstructors: [
                    {name: 'Jeremy Potts', email: 'jeremypotts@nevada.unr.edu', onHold: false, holdReason: ''},
                    {name: 'Jimmy Fraschia', email: 'jimmy.fraschia@gmail', onHold: false, holdReason: ''},
                ],
                
                notificationDialog: false,
                settingsDialog: false,
                emailDialog: false,
                removeDialog: [],
                removeNotificationDialog: [],
                removeEmailDialog: [],
                approveDialog: [],
                instructorDialog: [],
                archiveDialog: [],
                unarchiveDialog: [],
                

                sources: ['Admin', 'UNR'],
                selectedSource: '',
                notificationDescription: '',
                notificationOverride: false,
                notificationDate: new Date(),
                adminNotifications:[],

                to:['All Users', 'Admins', 'Instructors', 'Students'],
                emailSubject: '',
                emailTo: '',
                emailContent: '',
                emailSent: [],

                userAnalytics:[
                    {label: 'Students', count: 25}, 
                    {label: 'Instructors', count: 10}, 
                    {label: 'Admins', count: 3}, 
                ],
            };
        },

        methods:{
            handleLogout() {
                axios.post('http://127.0.0.1:5000/logout', {}, { withCredentials: true })
                    .then(response => {
                        console.log(response.data.message);
                        if (response.status === 200) {
                        setTimeout(() => {
                            this.$emit('login-status-changed', false);                        
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

            removeArchivedInstructor(index) {
                this.archivedInstructors.splice(index, 1);
                this.removeDialog[index] = false;
            },

            archiveApprovedInstructor(index) {
                const toArchive = this.approvedInstructors[index];
                this.approvedInstructors.splice(index, 1);
                this.archivedInstructors.push(toArchive);
                this.archiveDialog[index] = false;
                this.instructorDialog[index] = false;
            },

            unarchiveInstructor(index) {
                const toUnarchive = this.archivedInstructors[index];
                this.archivedInstructors.splice(index, 1);
                this.approvedInstructors.push(toUnarchive);
                this.unarchiveDialog[index] = false;
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
                    source: this.selectedSource,
                    description: this.notificationDescription,
                    override: this.notificationOverride,
                };

                this.adminNotifications.push(notification);

                this.selectedSource = '';
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
        font-family: Poppins;
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
        background-color: rgba(187, 187, 187, 0.082);
        font-family: Poppins;
        border-radius: 0px;
    }

    .dashboard-container{
        position: relative;
        font-family: Poppins;
    }

    .instructors-container{
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 96%;
        margin: 0 auto;
    }

    .panel-container{
        min-height: 500px;
        margin-top: 16px;
        width: 97%;
        margin-bottom: 10px;
        border-radius: 4px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
        border: 1px solid black;
    }
    .instructor-divider{
        width: 90%;
    }

    .v-date-picker{
        margin-top: -29px;
        margin-bottom: -38px;
    }

    .analytics-label{
        display: flex;
        justify-content: center;
        font-family: Poppins;
    }
</style>
