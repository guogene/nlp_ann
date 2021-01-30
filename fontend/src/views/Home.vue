<template>
    <div>
            <TaskList></TaskList>
    </div>
</template>

<script lang="ts">
    import Vue from "vue";
    import TaskList from "@/components/TaskList.vue";

    export default Vue.extend({
        components: {TaskList},
    });
</script>

<style scoped>
    @import "~prismjs/themes/prism-dark.css";

    .container {
        max-height: calc(100vh - 64px);
        overflow: hidden;
    }
</style>
