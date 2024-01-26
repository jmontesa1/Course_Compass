<!-- Created by: John Montesa -->
<!-- This component creates the filter menu that the user will interact with -->

<template>
  <div class="sidebar-menu">
    <!-- Display the menu items in a list -->
    <ul class="list-group">
      <li class="list-group-item" v-for="(menuItem, index) in menuItems" :key="index">
        <div v-if="menuItem.children && menuItem.children.length > 0" class="dropdown">
          <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownListItem" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            {{ menuItem.label }}
          </button>
          <!-- Each menu items are dropdowns with specific filters -->
          <div class="dropdown-menu" aria-labelledby="dropdownListItem">
            <!-- Children are the specific filters -->
            <a class="dropdown-item" v-for="(childItem, childIndex) in menuItem.children" :key="childIndex" @click="filterPress(childItem)">{{ childItem.label }}</a>
          </div>
        </div>
        <div v-else @click="filterPress(menuItem)">{{ menuItem.label }}</div>
      </li>
    </ul>
  </div>
</template>

<script>
    export default {
    data() {
        return {
        //The different filters that the user can use to filter classes
        menuItems: [
            { label: 'Level', children: [{ label: '0+' }, { label: '100+' }, { label: '200+' },
                                         { label: '300+' }, { label: '400+' }, { label: '500+' }, { label: '600+' },
                                         { label: '700+' }] },
            { label: 'Start Time', children: [{ label: '8-9 AM' }, { label: '10-11 AM' }, { label: '12-1 PM' },
                                             { label: '1-2 PM' }, { label: '3-4 PM' }, { label: '5-6 PM' }, { label: '7-8 PM' }]},
            { label: 'Rating', children: [{ label: '0+ Stars' }, { label: '1+ Stars' },{ label: '2+ Stars' },{ label: '3+ Stars' },
                                        { label: '4+ Stars' }] },
            { label: 'Keywords', children: [{ label: 'Attendance' }, { label: 'Lecture Heavy' }, { label: 'Pop Quizzes' },
                                             { label: 'Exam Heavy' }, { label: 'Textbook Required' }, { label: 'Presentations' }, { label: 'Projects' }]},
            { label: 'Location', children: [{ label: 'SEM' }, { label: 'WPEB' }] },
            { label: 'Format', children: [{ label: 'In-Person' }, { label: 'Online' }, { label: 'Hybrid' }] },
            { label: 'Requirement', children: [{ label: 'CO1' }, { label: 'CO2' },{ label: 'CO3' },
                                            { label: 'CO4' },{ label: 'CO5' },{ label: 'CO6' },{ label: 'CO7' },
                                            { label: 'CO8' },{ label: 'CO9' }] },
            { label: 'Term', children: [{ label: 'Fall' }, { label: 'Winter' }, { label: 'Spring' }, { label: 'Summer' }] },
            ],
        };
    },
    methods: {
        filterPress(item) {
        this.$emit('itemSelected', item);
        },
    },
    };
</script>

<style scoped>
    .sidebar-menu{
        width: 100%;
        background-color: #ffffff;
        overflow-y: auto;
        height: 100%;
        margin-bottom : 40px;
    }
    .list-group-item{
        font-family: 'Poppins';
        font-size: 25px;
        text-align: left;
        border: 1px solid #000000;
        box-sizing: border-box;
        border-radius: 0px;

    }
    .btn-secondary.dropdown-toggle {
        font-family: 'Poppins';
        background-color: #ffffff;
        color: #000000;
        border: 1px solid transparent;
        text-align: center;
        font-size: 15px;
    }

    .btn-secondary.dropdown-toggle:hover {
        color: #ffffff;
        background-color: #000000;
    }

    .dropdown-item {
        color: #000000;
        border: 1px solid #000000;
        text-align: left;
        font-size: 12px;
    }

    .dropdown-item:hover {
        color: #ffffff;
        background-color: #000000;
    }
</style>
