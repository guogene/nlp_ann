<template>
    <v-app>
        <v-navigation-drawer
                app
        >
            <side-sheet></side-sheet>

        </v-navigation-drawer>
        <v-main>
      <v-container
        class="py-8 px-6"
        fluid
      >
        <router-view></router-view>
      </v-container>
    </v-main>
    </v-app>
</template>

<script lang="ts">
    import Vue from "vue";
    import SideSheet from "@/components/SideSheet.vue";
    import AppBar from "@/components/AppBar.vue";

    export default Vue.extend({
        components: {
            SideSheet,
            AppBar
        }
    });
</script>
