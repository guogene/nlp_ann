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
                    link
                    @click="go_page(link)"
            >
                <v-list-item-icon>
                    <v-icon>{{ icon }}</v-icon>
                </v-list-item-icon>

                <v-list-item-content>
                    <v-list-item-title>{{ text }}</v-list-item-title>
                </v-list-item-content>
            </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list>
            <v-list-item
                    @click="log_out"
            >
                <v-list-item-icon>
                    <v-icon>mdi-delete</v-icon>
                </v-list-item-icon>

                <v-list-item-content>
                    <v-list-item-title>退出登陆</v-list-item-title>
                </v-list-item-content>
            </v-list-item>
        </v-list>

    </div>

</template>

<script lang="ts">
    import Vue from "vue";

    export default Vue.extend({
        data: () => ({
            admin_links: [
                ['mdi-inbox-arrow-down', '任务大厅', "/"],
                ['mdi-send', '标签管理', "labels"],
                ['mdi-delete', '个人信息', "null"],
                ['mdi-alert-octagon', "权限管理", "null"],
                ['mdi-alert', "任务分配", "null"],
            ],
            member_links: [
                ['mdi-inbox-arrow-down', '任务大厅', "/"],
                ['mdi-send', '标签管理', "labels"],
                ['mdi-delete', '个人信息', "null"],
            ],
            links: [],
            role: ""
        }),
        methods: {
            get_user_role() {
                this.$http.get('/task?action=user_info').then(({data}) => {
                    if (data.status === 200) {
                        var user_info = data.data;
                        this.role = user_info.role === 'admin' ? "管理员" : "标注员";
                        this.links = user_info.role === 'admin' ? this.admin_links : this.member_links

                    } else {
                        alert(data.msg);
                    }
                })
            },
            log_out() {
                localStorage.setItem("token", "");
                this.$router.push("login").catch(_ => {
                });
            },
            go_page(name){
                if (name == "null"){
                    alert("未开放功能");
                    return
                }
                this.$router.push(name).catch(_ => {
                });
            }
        },
        mounted(): void {
            this.get_user_role()
        }
    });
</script>

<style scoped>

</style>
