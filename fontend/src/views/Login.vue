<template>
    <v-row justify="center">
        <v-dialog
                v-model="d_login"
                persistent
                max-width="600px"
                overlay-opacity="1"
                overlay-color="#00BFFF"
        >
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                        color="primary"
                        dark
                        v-bind="attrs"
                        v-on="on"
                >
                    ac
                </v-btn>
            </template>
            <v-card>
                <v-card-title>
                    <span class="headline">NLP标注平台</span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field
                                        label="账号"
                                        required
                                        v-model="username"
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                        label="密码"
                                        type="password"
                                        v-model="password"
                                        required
                                ></v-text-field>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                            color="blue darken-1"
                            text
                            @click="login_res"
                    >
                        登陆
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script lang="ts">
    import Vue from "vue";

    export default Vue.extend({
        components: {},
        data() {
            return {
                d_login: true,
                username: null,
                password: null
            }
        },
        methods: {
            login_res() {
                var self = this;
                this.$http.post('/login', {"username": this.username, "password": this.password}).then(({data}) => {
                    if (data.status === 200) {
                        var token = data.data;
                        localStorage.setItem("token", this.username + "_" + token);
                        this.$router.push("/").catch(_ => {
                        });
                        location.reload();


                    } else {
                        alert(data.msg);
                    }
                })
            }
        }
    });
</script>

<style scoped>
    @import "~prismjs/themes/prism-dark.css";

    .container {
        max-height: calc(100vh - 64px);
        overflow: hidden;
    }
</style>
