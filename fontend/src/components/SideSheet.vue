<template>
    <div>
        <v-sheet
                color="grey lighten-4"
                class="pa-4"
        >
            <v-avatar
                    class="mb-4"
                    color="grey darken-1"
                    size="64"
            ></v-avatar>

            <div>管理员</div>
        </v-sheet>

        <v-divider></v-divider>

        <v-list>
            <v-list-item
                    v-for="[icon, text, link] in links"
                    :key="icon"
                    :href="link"
                    link
            >
                <v-list-item-icon>
                    <v-icon>{{ icon }}</v-icon>
                </v-list-item-icon>

                <v-list-item-content>
                    <v-list-item-title>{{ text }}</v-list-item-title>
                </v-list-item-content>
            </v-list-item>
        </v-list>
    </div>

</template>

<script lang="ts">
    import Vue from "vue";

    export default Vue.extend({
        data: () => ({
            links: [
                ['mdi-inbox-arrow-down', '任务大厅', "/poplar"],
                ['mdi-send', '标签管理', "/poplar/labels"],
                ['mdi-alert-octagon', "权限管理", "/poplar"],
                ['mdi-alert', "任务分配", "/poplar"],
                ['mdi-delete', '个人信息', "/poplar"],
            ],
        }),
        methods: {}
    });
</script>

<style scoped>

</style>
