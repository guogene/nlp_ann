<template>
    <div>
        <v-row>
          <v-col
            v-for="card in cards"
            :key="card"
            cols="12"
          >
            <v-card>
              <v-subheader>{{ card }} 总共: 6</v-subheader>

              <v-list two-line>
                <template v-for="n in 6">
                  <v-list-item

                    :key="n"
                  >
                    <v-list-item-avatar color="grey darken-1">
                    </v-list-item-avatar>

                    <v-list-item-content>
                      <v-list-item-title><a @click="useDefault">患者 {{ n }}病理文本</a></v-list-item-title>

                      <v-list-item-subtitle>
                        最近标注时间：2020-01-28 14:32:10
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>

                  <v-divider
                    v-if="n !== 6"
                    :key="`divider-${n}`"
                    inset
                  ></v-divider>
                </template>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
    </div>

</template>

<script lang="ts">
    import Vue from "vue";
    import defaultData from "@/assets/default.json";

    export default Vue.extend({
        data: () => ({
             cards: ['未完成', '已完成'],
        }),
        methods: {
            useDefault() {
                window.setTimeout(() => {
                    this.$eventbus.$emit("fileUploaded", defaultData);
                    this.$forceUpdate();
                }, 10);
                this.$router.push("annotate").catch(_ => {
                });
            }
        }
    });
</script>

<style scoped>

</style>
