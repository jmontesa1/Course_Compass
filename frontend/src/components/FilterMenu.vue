<!-- Created by: John Montesa -->
<!-- This component creates the filter menu that the user will interact with -->

<template>
  <!--<p>Applied Filters: {{ selected }}</p>-->
  <v-card class="menu">
    <v-list v-model:opened="open">
      <v-list-item v-for="(menuItem, index) in menuItems" :key="index">
        <v-list-group :value="menuItem.label">
          <template v-slot:activator="{ props }">
            <v-list-item class="label" v-bind="props" :title="menuItem.label"></v-list-item>
          </template>

          <v-list-item v-for="(childItem, childIndex) in menuItem.children" :key="childIndex">
            <v-checkbox class="child-checkbox" :checked="isChecked(childItem.label)"  :label="childItem.label" :value="childItem.label" @change="handleCheckboxChange(childItem.label)"></v-checkbox>
          </v-list-item>
        </v-list-group>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script setup>
  import { ref, defineEmits, defineProps } from 'vue';
  
  const { selectedFilters } = defineProps(['selectedFilters']);
  const emit = defineEmits();

  const open = ref(['Filters']);
  const selected = ref(selectedFilters);

  const isChecked = (label) => selected.value.includes(label);

  const handleCheckboxChange = (value) => {
      const updatedSelected = [...selected.value];

      if (updatedSelected.includes(value)) {
        updatedSelected.splice(updatedSelected.indexOf(value), 1);
      } else {
        updatedSelected.push(value);
      }

      selected.value = updatedSelected;

      emit('itemSelected', value);
      emit('update:selectedFilters', selected.value);
    };
</script>

<script>
    export default {
    data: () => ({
        open:['Filters'],
        //The different filters that the user can use to filter classes
          menuItems: [
              { label: 'Level', children: [{ label: '0-99' }, { label: '100-199' }, { label: '200-299' },
                                          { label: '300-399' }, { label: '400-499' }, { label: '500-599' }, { label: '600-699' },
                                          { label: '700-799' }] },
              { label: 'Start Time', children: [{ label: '8-9 AM' }, { label: '10-11 AM' }, { label: '12-1 PM' },
                                              { label: '1-2 PM' }, { label: '3-4 PM' }, { label: '5-6 PM' }, { label: '7-8 PM' }]},
              { label: 'Rating', children: [{ label: '0+ Stars' }, { label: '1+ Stars' },{ label: '2+ Stars' },{ label: '3+ Stars' },
                                          { label: '4+ Stars' }] },
              { label: 'Keywords', children: [{ label: 'Attendance' }, { label: 'Lecture Heavy' }, { label: 'Pop Quizzes' },
                                              { label: 'Exam Heavy' }, { label: 'Textbook Required' }, { label: 'Presentations' }, { label: 'Projects' }]},
              { label: 'Location', children: [{ label: 'SEM' }, { label: 'WPEB' }, { label: 'AB' }, { label: 'MS' }, { label: 'DMSC' }, { label: 'PSAC' }, { label: 'SLH' }] },
              { label: 'Format', children: [{ label: 'In-Person' }, { label: 'Online' }, { label: 'Hybrid' }] },
              { label: 'Requirement', children: [{ label: 'CO1' }, { label: 'CO2' },{ label: 'CO3' },
                                              { label: 'CO4' },{ label: 'CO5' },{ label: 'CO6' },{ label: 'CO7' },
                                              { label: 'CO8' },{ label: 'CO9' }] },
              { label: 'Term', children: [{ label: 'Fall' }, { label: 'Winter' }, { label: 'Spring' }, { label: 'Summer' }] },
              ],
          selected: [],
        }),

      methods: {
          filterPress(item) {
            this.$emit('itemSelected', item);
          },
      },
    };
</script>

<style scoped>
    .menu{
        width: auto;
        max-height: 800px;
        overflow-y: auto;
        box-shadow: none !important;
        left: 1px;
    }

    .label{
      font-family: 'Poppins';
      border-bottom: 1px solid black;
      font-size: 13px;
    }

    .child-checkbox{
      align-content: left;
      align-items: left;
      text-align: left;
      color: black;
      height: 45px;
    }
    

</style>
