<template>
    <div>
        <v-row>
            <v-btn color="primary ma-1" @click="add_new_info"
            >
                新增模版
            </v-btn>
        </v-row>
        <v-row>
            <v-col
                    cols="12"
            >
                <v-list two-line>
                    <template v-for="(n, p_idx) in labels_data">
                        <v-list-item

                                :key="p_idx"
                        >

                            <v-list-item-content>
                                <v-list-item-title>{{ n["title"] }}</v-list-item-title>
                                <div>
                                    标签：
                                    <v-chip v-for="(l, idx) in n.label"
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
                                    <v-btn @click="edit_info(p_idx)">
                                        编辑
                                    </v-btn>
                                    <v-btn
                                            color="error"
                                            style="margin-left: 5px"
                                    >
                                        删除
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
                </v-list>
            </v-col>

        </v-row>

        <v-dialog
                v-model="dialog_edit"
                fullscreen
                hide-overlay
                transition="dialog-bottom-transition"
                scrollable
        >
            <v-card tile>
                <v-toolbar
                        flat
                        dark
                        color="primary"
                >
                    <v-btn
                            icon
                            dark
                            @click="dialog_edit = false"
                    >
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                    <v-toolbar-title>
                        <v-text-field v-model="temp_label_info.title" label="请输入模版名称"></v-text-field>
                    </v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-toolbar-items>
                        <v-btn
                                dark
                                text
                                @click="saveTemp"
                        >
                            保存
                        </v-btn>
                    </v-toolbar-items>
                </v-toolbar>
                <v-list
                        three-line
                        subheader
                >
                    <v-subheader>标签</v-subheader>
                    <v-list-item v-for="(l, idx) in temp_label_info.label" :key="idx">
                        <v-list-item-content>
                            <v-list-item-title>{{ l.text }}
                            </v-list-item-title>

                        </v-list-item-content>
                        <v-list-item-action>
                            <div>
                                颜色:
                                <colorPicker v-model="l.color" style="margin-right: 200px"/>
                                <v-btn
                                        color="error"
                                        style="margin-left: 5px"
                                        @click="delLabel(idx)"
                                >
                                    删除
                                </v-btn>
                            </div>
                        </v-list-item-action>
                    </v-list-item>
                    <v-list-item>
                        <v-list-item-content>
                            <v-text-field v-model="temp_label" label="请输入标签名称"></v-text-field>
                        </v-list-item-content>
                        <v-list-item-action>
                            <div>
                                颜色:
                                <colorPicker v-model="temp_color" style="margin-right: 200px"/>
                                <v-btn
                                        class="ma-2"
                                        color="secondary"
                                        @click="addLabel"
                                >
                                    添加
                                </v-btn>
                            </div>

                        </v-list-item-action>
                    </v-list-item>

                </v-list>
                <v-divider></v-divider>
                <v-list
                        three-line
                        subheader
                >
                    <v-subheader>关联</v-subheader>
                    <v-list-item v-for="(l, idx) in temp_label_info.connectionCategories" :key="idx">
                        <v-list-item-content>
                            <v-list-item-title>{{ l.text }}
                            </v-list-item-title>

                        </v-list-item-content>
                        <v-list-item-action>
                            <div>
                                <v-btn
                                        color="error"
                                        style="margin-left: 5px"
                                        @click="delCon(idx)"
                                >
                                    删除
                                </v-btn>
                            </div>
                        </v-list-item-action>
                    </v-list-item>
                    <v-list-item>
                        <v-list-item-content>
                            <v-text-field v-model="temp_connectionCategories" label="请输入关联名称"></v-text-field>
                        </v-list-item-content>
                        <v-list-item-action>
                            <div>
                                <v-btn
                                        class="ma-2"
                                        color="secondary"
                                        @click="addCon"
                                >
                                    添加
                                </v-btn>
                            </div>

                        </v-list-item-action>
                    </v-list-item>
                </v-list>

                <div style="flex: 1 1 auto;"></div>
            </v-card>

        </v-dialog>

    </div>

</template>

<script lang="ts">
    import Vue from "vue";

    export default Vue.extend({
        data: () => ({
            dialog_edit: false,
            temp_label_info: {
                "label": [],
                "connectionCategories": [],
                "title": "模版名称"
            },
            temp_label: "",
            temp_color: "",
            temp_connectionCategories: "",
            labels_data: [
                {
                    label: [
                        {
                            "id": 0,
                            "text": "名词",
                            "color": "#eac0a2",
                            "borderColor": "#a38671"
                        },
                        {
                            "id": 1,
                            "text": "动词",
                            "color": "#619dff",
                            "borderColor": "#436db2"
                        },
                        {
                            "id": 2,
                            "text": "形容词",
                            "color": "#9d61ff",
                            "borderColor": "#6d43b2"
                        },
                        {
                            "id": 3,
                            "text": "副词",
                            "color": "#ff9d61",
                            "borderColor": "#b26d43"
                        }
                    ],
                    connectionCategories: [
                        {
                            "id": 0,
                            "text": "修饰"
                        },
                        {
                            "id": 1,
                            "text": "限定"
                        },
                        {
                            "id": 2,
                            "text": "是...的动作"
                        }
                    ],
                    title: "测试模版"
                }
            ]
        }),
        methods: {
            addLabel() {
                var label = this.temp_label;
                var color = this.temp_color;
                if (!label || !color) {
                    alert("标签和颜色不能为空");
                    return
                }
                for (let i = 0; i < this.temp_label_info.label.length; i++) {
                    if (label == this.temp_label_info.label[i].text) {
                        alert("标签不能重复");
                        return;
                    }
                }
                this.temp_label_info.label.push({text: label, "color": color})
            },
            delLabel(idx) {
                this.temp_label_info.label.splice(idx, 1);
            },
            addCon() {
                var label = this.temp_connectionCategories;
                if (!label) {
                    alert("关联不能为空");
                    return
                }
                for (let i = 0; i < this.temp_label_info.connectionCategories.length; i++) {
                    if (label == this.temp_label_info.connectionCategories[i].text) {
                        alert("关联不能重复");
                        return;
                    }
                }
                this.temp_label_info.connectionCategories.push({text: label})
            },
            delCon(idx) {
                this.temp_label_info.connectionCategories.splice(idx, 1);
            },
            saveTemp() {
                var res = {};
                res["label"] = this.temp_label_info.label;
                res["connectionCategories"] = this.temp_label_info.connectionCategories;
                res["title"] = this.temp_label_info.title;
                if (!res['title']) {
                    alert("模版名称不能为空");
                    return
                }
                if (!res['label']) {
                    alert("标签不能为空");
                    return
                }
                console.log(res);
            },
            edit_info(idx) {
                this.temp_label_info = this.labels_data[idx];
                this.dialog_edit = true;
            },
            add_new_info() {
                this.temp_label_info = {
                    "label": [],
                    "connectionCategories": [],
                    "title": ""
                };
                this.dialog_edit = true;
            }
        }
    });
</script>

<style scoped>

</style>
