<template>
    <div>
        <v-row>
            <v-btn @click="set_save" color="primary ma-1"
                   :loading="save_loading"
                   :disabled="save_loading"
                   v-if="this.$router.currentRoute.fullPath.includes('annotate')">
                保存
                <template v-slot:loader>
                    <span>保存...</span>
                </template>
            </v-btn>
            <v-btn @click="reset" color="primary ma-1"
                   v-if="this.$router.currentRoute.fullPath.includes('annotate')">
                重置
            </v-btn>
            <v-btn
                    class="ma-1"
                    :loading="complete_loading"
                    :disabled="complete_loading"
                    color="success"
                    @click="set_complete"
            >
                标记为已完成
                <template v-slot:loader>
                    <span>标记中...</span>
                </template>
            </v-btn>
        </v-row>
        <v-row no-gutters>
            <v-col>
                <div class="container" ref="container"></div>
            </v-col>
            <v-col class="pa-2" v-if="this.annotator !== null">
                <v-card>
                    <v-subheader>标签</v-subheader>

                    <v-chip v-for="label in this.jsonData.labelCategories"
                            :key="label"
                            class="ma-2"
                            :color="label.color"
                            text-color="white"
                    >
                        {{ label.text }}
                    </v-chip>
                </v-card>

                <v-divider style="margin-top: 10px; margin-bottom: 10px"></v-divider>
                <v-card>
                    <v-subheader>关联</v-subheader>

                    <v-chip v-for="cc in this.jsonData.connectionCategories"
                            :key="cc"
                            class="ma-2"
                    >
                        {{ cc.text }}
                    </v-chip>
                </v-card>
            </v-col>
            <v-dialog max-width="290" persistent v-model="showLabelCategoriesDialog">
                <v-card>
                    <v-card-title>
                        <span class="headline">请选择分类</span>
                    </v-card-title>
                    <v-card-text>
                        <v-radio-group v-model="selectedLabelCategory">
                            <v-radio :key="category.id"
                                     :label="category.text"
                                     :value="category.id"
                                     v-for="category in this.labelCategories"></v-radio>
                        </v-radio-group>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn @click="showLabelCategoriesDialog = false" color="primary">
                            取消
                        </v-btn>
                        <v-btn @click="addLabel" color="primary">
                            确定
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
            <v-dialog max-width="290" persistent v-model="showConnectionCategoriesDialog">
                <v-card>
                    <v-card-title>
                        <span class="headline">请选择分类</span>
                    </v-card-title>
                    <v-card-text>
                        <v-radio-group v-model="selectedConnectionCategory">
                            <v-radio :key="category.id"
                                     :label="category.text"
                                     :value="category.id"
                                     v-for="category in this.connectionCategories"></v-radio>
                        </v-radio-group>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn @click="showConnectionCategoriesDialog = false" color="primary">
                            取消
                        </v-btn>
                        <v-btn @click="addConnection" color="primary">
                            确定
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
    </div>
</template>

<script lang="ts">
    import Vue from "vue";
    import Prism from "prismjs";
    import {Action, Annotator} from "poplar-annotation";
    import {LabelCategory} from "poplar-annotation/dist/Store/LabelCategory";
    import {ConnectionCategory} from "poplar-annotation/dist/Store/ConnectionCategory";

    enum CategorySelectMode {
        Create,
        Update
    }

    export default Vue.extend({
        components: {},
        data() {
            return {
                jsonData: null,
                annotator: null as Annotator | null,
                selectedLabelCategory: null as LabelCategory.Entity | null,
                selectedConnectionCategory: null as ConnectionCategory.Entity | null,
                showLabelCategoriesDialog: false as boolean,
                showConnectionCategoriesDialog: false as boolean,
                json: "",
                startIndex: -1,
                endIndex: -1,
                first: -1,
                second: -1,
                categorySelectMode: CategorySelectMode.Create,
                selectedId: -1,
                complete_loading: false,
                save_loading: false
            };
        },
        methods: {
            updateJSON(): void {
                this.json = this.highlight(JSON.stringify(this.annotator.store.json, null, 4));
            },
            addLabel(): void {
                if (this.categorySelectMode === CategorySelectMode.Update) {
                    this.annotator.applyAction(Action.Label.Update(this.selectedId, this.selectedLabelCategory));
                } else {
                    this.annotator.applyAction(Action.Label.Create(this.selectedLabelCategory, this.startIndex, this.endIndex));
                }
                this.showLabelCategoriesDialog = false;
                this.updateJSON();
            },
            addConnection(): void {
                if (this.categorySelectMode === CategorySelectMode.Update) {
                    this.annotator.applyAction(Action.Connection.Update(this.selectedId, this.selectedConnectionCategory));
                } else {
                    this.annotator.applyAction(Action.Connection.Create(this.selectedConnectionCategory, this.from, this.to));
                }
                this.showConnectionCategoriesDialog = false;
                this.updateJSON();
            },
            createAnnotator(): Annotator {
                const annotator = new Annotator(this.jsonData, this.$refs.container);
                annotator.on("textSelected", (startIndex, endIndex) => {
                    this.startIndex = startIndex;
                    this.endIndex = endIndex;
                    this.categorySelectMode = CategorySelectMode.Create;
                    this.showLabelCategoriesDialog = true;
                });
                annotator.on("twoLabelsClicked", (fromLabelId, toLabelId) => {
                    this.from = fromLabelId;
                    this.to = toLabelId;
                    this.categorySelectMode = CategorySelectMode.Create;
                    this.showConnectionCategoriesDialog = true;
                });
                annotator.on("labelRightClicked", (labelId, event: MouseEvent) => {
                    if (event.ctrlKey) {
                        this.categorySelectMode = CategorySelectMode.Update;
                        this.selectedId = labelId;
                        this.showLabelCategoriesDialog = true;
                    } else {
                        annotator.applyAction(Action.Label.Delete(labelId));
                    }
                    this.updateJSON();
                });
                annotator.on("connectionRightClicked", (connectionId, event: MouseEvent) => {
                    if (event.ctrlKey) {
                        this.categorySelectMode = CategorySelectMode.Update;
                        this.selectedId = connectionId;
                        this.showConnectionCategoriesDialog = true;
                    } else {
                        annotator.applyAction(Action.Connection.Delete(connectionId));
                    }
                    this.updateJSON();
                });
                annotator.on("contentInput", (position, value) => {
                    annotator.applyAction(Action.Content.Splice(position, 0, value));
                    this.updateJSON();
                });
                annotator.on("contentDelete", (position, length) => {
                    annotator.applyAction(Action.Content.Splice(position, length, ""));
                    this.updateJSON();
                });
                return annotator;
            },
            highlight(code: string): string {
                return Prism.highlight(code, Prism.languages.javascript, "javascript");
            },
            download: function () {
                const eleLink = document.createElement("a");
                eleLink.download = "data.json";
                eleLink.style.display = "none";
                const blob = new Blob([JSON.stringify(this.annotator.store.json, null, 4)]);
                eleLink.href = URL.createObjectURL(blob);
                document.body.appendChild(eleLink);
                eleLink.click();
                document.body.removeChild(eleLink);
            },
            reset: function () {
                this.jsonData.labels = [];
                this.annotator.remove();
                this.annotator = this.createAnnotator();
                this.updateJSON();
            },
            set_complete: function () {
                this.complete_loading = true;
                var res_data = this.jsonData;
                res_data["labels"] = this.annotator.store.json.labels;
                res_data["connections"] = this.annotator.store.json.connections;
                res_data["done_state"] = true;
                this.$http.post('/task', res_data).then(({data}) => {
                    if (data.status === 200) {
                        this.complete_loading = false;
                    } else {
                        alert(data.msg);
                        this.complete_loading = false;
                    }
                });
            },
            set_save: function () {
                this.save_loading = true;
                var res_data = this.jsonData;
                res_data["labels"] = this.annotator.store.json.labels;
                res_data["connections"] = this.annotator.store.json.connections;
                this.$http.post('/task', res_data).then(({data}) => {
                    if (data.status === 200) {
                        this.save_loading = false;
                    } else {
                        alert(data.msg);
                        this.save_loading = false;
                    }
                });
            },
        },
        computed: {
            labelCategories(): LabelCategory.Entity[] {
                if (this.annotator === null) {
                    return [];
                }
                const result = [];
                for (const [_, category] of this.annotator.store.labelCategoryRepo) {
                    result.push(category);
                }
                return result;
            },
            connectionCategories(): ConnectionCategory.Entity[] {
                if (this.annotator === null) {
                    return [];
                }
                const result = [];
                for (const [_, category] of this.annotator.store.connectionCategoryRepo) {
                    result.push(category);
                }
                return result;
            }
        },
        created(): void {
            this.$eventbus.$on("fileUploaded", (jsonData: JSON) => {
                this.jsonData = jsonData;
                if (this.annotator !== null) {
                    this.annotator.remove();
                }
                if (this.jsonData !== null && this.jsonData.content) {
                    this.annotator = this.createAnnotator();
                    this.updateJSON();
                }
            });
            this.$eventbus.$on("downloadRequest", () => {
                this.download();
            });
            this.$eventbus.$on("downloadSVGRequest", () => {
                this.downloadSVG();
            });
        },
        mounted(): void {
            if (this.jsonData !== null && this.jsonData.content) {
                this.annotator = this.createAnnotator();
                this.updateJSON();
            }
        }
    });
</script>
<style scoped>
    .code-container-wrapper,
    .container-wrapper {
        min-height: calc(100vh - 64px);
        max-height: calc(100vh - 64px);
        overflow: hidden;
        padding: 0 !important;
    }

    .container-wrapper {
        border-right: solid 2px black;
    }

    .code-container-wrapper {
        border-left: solid 2px black;
    }

    .container,
    .code-container {
        padding-top: 10px;
        overflow: scroll;
        height: calc(100vh - 64px);
    }

    code {
        max-width: calc(45vw - 16px);
        background: rgb(32, 32, 32) !important;
        box-shadow: none !important;
        padding: 8px !important;
        padding-right: 40px !important;
        margin-bottom: 20px;
    }
</style>
<style>
    .container > svg {
        width: 45vw;
    }

    .poplar-annotation-label {
        font-size: 14px;
    }

    .poplar-annotation-connection {
        font-family: "PingFang SC", serif;
        font-size: 12px;
    }
</style>
