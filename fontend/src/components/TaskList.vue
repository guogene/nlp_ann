<template>
    <div>
        <v-row>
            <v-col
                    cols="12"
            >
                <v-card>
                    <v-subheader>未完成 总共: {{ wait_list.length }}</v-subheader>

                    <v-list two-line>
                        <template v-for="n in wait_list">
                            <v-list-item

                                    :key="n"
                            >
                                <v-list-item-avatar color="grey darken-1">
                                </v-list-item-avatar>

                                <v-list-item-content>
                                    <v-list-item-title><a @click="get_file_data(n['title'])">{{ n['title'] }}</a>
                                    </v-list-item-title>

                                    <v-list-item-subtitle>
                                        最近标注时间：{{ n['update_time']}}
                                    </v-list-item-subtitle>
                                </v-list-item-content>
                            </v-list-item>

                            <v-divider
                                    v-if="n !== wait_list.length"
                                    :key="`divider-${n}`"
                                    inset
                            ></v-divider>
                        </template>
                    </v-list>
                </v-card>
            </v-col>

            <v-col
                    cols="12"
            >
                <v-card>
                    <v-subheader>已完成 总共: {{ done_list.length }}</v-subheader>

                    <v-list two-line>
                        <template v-for="n in done_list">
                            <v-list-item

                                    :key="n"
                            >
                                <v-list-item-avatar color="grey darken-1">
                                </v-list-item-avatar>

                                <v-list-item-content>
                                    <v-list-item-title><a @click="get_file_data(n['title'])">{{ n['title'] }}</a>
                                    </v-list-item-title>

                                    <v-list-item-subtitle>
                                        最近标注时间：{{ n['update_time']}}
                                    </v-list-item-subtitle>
                                </v-list-item-content>
                            </v-list-item>

                            <v-divider
                                    v-if="n !== done_list.length"
                                    :key="`divider-${n}`"
                                    inset
                            ></v-divider>
                        </template>
                    </v-list>
                </v-card>
            </v-col>

        </v-row>
        <v-row justify="center">
            <v-dialog
                    v-model="select_label"
                    persistent
                    max-width="1200px"
                    overlay-opacity="0.5"
                    overlay-color="#00BFFF"
            >
                <v-card>
                    <v-card-title>
                        <span class="headline">初始化标签模版</span>
                    </v-card-title>
                    <v-card-text>
                        <v-container>
                            <template v-for="(n, p_idx) in labels_data">
                                <v-list-item

                                        :key="p_idx"
                                >

                                    <v-list-item-content>
                                        <v-list-item-title>{{ n["title"] }}</v-list-item-title>
                                        <div>
                                            标签：
                                            <v-chip v-for="(l, idx) in n.labelCategories"
                                                    :key="idx"
                                                    class="ma-2"
                                                    :color="l.color"
                                                    text-color="white"
                                            >
                                                {{ l.text }}
                                            </v-chip>
                                            关联：
                                            <v-chip v-for="(cc, idx) in n.connectionCategories"
                                                    :key="idx"
                                                    class="ma-2"
                                            >
                                                {{ cc.text }}
                                            </v-chip>
                                        </div>
                                    </v-list-item-content>

                                    <v-list-item-action>
                                        <div>
                                            <v-btn @click="select_now_label(p_idx)">
                                                选中
                                            </v-btn>
                                        </div>

                                    </v-list-item-action>
                                </v-list-item>

                                <v-divider
                                        v-if="n !== 6"
                                        :key="`divider-${n}`"
                                        inset
                                ></v-divider>
                            </template>
                        </v-container>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                                color="blue darken-1"
                                text
                                @click="select_label = false"
                        >
                            返回
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
    </div>

</template>

<script lang="ts">
    import Vue from "vue";

    export default Vue.extend({
        data: () => ({
            wait_list: [],
            done_list: [],
            select_label: false,
            labels_data: [],
            temp_filedata: null
        }),
        methods: {
            get_file_data(filename) {
                let Base64 = require('js-base64').Base64;
                var self = this;
                this.$http.post('/task', {
                    "action": "get_file",
                    "file_name": Base64.encode(filename)
                }).then(({data}) => {
                    if (data.status === 200) {
                        if (!data.data.labelCategories.length || !data.data.connectionCategories.length) {
                            self.get_label_list();
                            self.temp_filedata = data.data;
                            self.select_label = true;
                        } else {
                            window.setTimeout(() => {
                                this.$eventbus.$emit("fileUploaded", data.data);
                                this.$forceUpdate();
                            }, 10);
                            this.$router.push("annotate").catch(_ => {
                            });
                        }

                    } else {
                        alert(data.msg);
                    }
                });

            },
            select_now_label(idx) {
                var data = this.temp_filedata;
                data["labelCategories"] = this.labels_data[idx]["labelCategories"];
                data["connectionCategories"] = this.labels_data[idx]["connectionCategories"];
                window.setTimeout(() => {
                    this.$eventbus.$emit("fileUploaded", data);
                    this.$forceUpdate();
                }, 10);
                this.$router.push("annotate").catch(_ => {
                });
            },
            get_task_list() {
                this.$http.get('/task').then(({data}) => {
                    if (data.status === 200) {
                        this.wait_list = data.data.wait;
                        this.done_list = data.data.done;
                    } else {
                        alert(data.msg);
                    }
                })
            },
            get_label_list() {
                this.$http.get('/label').then(({data}) => {
                    if (data.status === 200) {
                        this.labels_data = data.data;
                    } else {
                        alert(data.msg);
                    }
                });
            },
        },
        mounted(): void {
            this.get_task_list()
        }
    });
</script>

<style scoped>

</style>
