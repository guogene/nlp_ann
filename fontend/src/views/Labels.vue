<template>
    <div>
            <LableList></LableList>
    </div>
</template>

<script lang="ts">
    import Vue from "vue";
    import LableList from "@/components/LableList.vue";

    export default Vue.extend({
        components: {LableList},
    });
</script>

<style scoped>
    @import "~prismjs/themes/prism-dark.css";

    .container {
        max-height: calc(100vh - 64px);
        overflow: hidden;
    }
</style>
