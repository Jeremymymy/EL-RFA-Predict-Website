<template>
  <q-page class="q-pa-md">
    <div class="text-center">
      <h2 class="custom-header">Please choose the predictor:</h2>
    </div>
    <div class="row justify-center q-gutter-lg q-mt-lg">
      <q-btn
        class="col-5 custom-btn"
        color="primary"
        label="Risk Predictor for Early Recurrence of Liver Cancer Patients Undergoing Radiofrequency Ablation"
        @click="navigateTo('early_recurrence')"
      />
      <q-btn
        class="col-5 custom-btn"
        color="secondary"
        label="Risk Predictor for Overall Survival of Liver Cancer Patients Undergoing Radiofrequency Ablation"
        @click="navigateTo('overall_survival')"
      />
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'CataloguePage',
  setup() {
    const router = useRouter()

    const navigateTo = (path) => {
      router.push({ path })
    }

    return { navigateTo }
  },
})
</script>

<style>
.custom-header {
  font-size: 32px; /* 調整標題的字體大小 */
  font-weight: bold; /* 設置字體粗細 */
  color: #333; /* 設置字體顏色 */
  margin-bottom: 20px; /* 設置底部距離 */
}

.custom-btn {
  height: 100px; /* 設定按鈕的高度 */
  font-size: 24px; /* 設定按鈕文字的大小 */
  text-transform: none; /* 不改變文字大小寫 */
  transition: all 0.3s ease; /* 添加過渡效果 */
  padding: 0 40px;
}

.custom-btn:hover {
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2); /* 添加陰影效果 */
}

.q-gutter-lg > .q-btn {
  margin-top: 20px; /* 設置按鈕的頂部距離 */
  margin-left: 30px;
  margin-right: 30px;
  padding-top: 50px;
  padding-bottom: 50px;
}
</style>
