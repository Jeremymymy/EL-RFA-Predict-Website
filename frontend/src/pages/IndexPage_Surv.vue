<template>
  <q-page class="q-pa-md">
    <div class="row justify-center">
      <q-card v-if="!showResults" class="q-pa-md column justify-center" flat bordered>

        <q-tabs v-model="mode" dense class="text-grey-7 custom-tabs" active-color="indigo-10" indicator-color="deep-orange-8" align="justify">
          <q-tab name="case" label="Overall Survival (Case)" />
          <q-tab name="batch" label="Overall Survival (Batch)" />
        </q-tabs>

        <q-tab-panels v-model="mode" animated>
          <q-tab-panel name="case">
            <CaseForm_Surv @formSubmitted="(data) => handleFormSubmission('overall survival', data)" />
          </q-tab-panel>
          <q-tab-panel name="batch">
            <BatchForm_Surv />
          </q-tab-panel>
        </q-tab-panels>
      </q-card>

      <div v-if="showResults" class="flex-container full-width">
        <div class="col form-container" align="center">
          <q-tabs v-model="mode" dense class="text-grey-7 custom-tabs" active-color="indigo-10" indicator-color="deep-orange-8" align="justify">
            <q-tab name="case" label="Overall Survival (Case)" />
            <q-tab name="batch" label="Overall Survival (Batch)" />
          </q-tabs>

          <q-tab-panels v-model="mode" animated>
            <q-tab-panel name="case">
              <CaseForm_Surv class="form-part" :initial-values="formValues" @formSubmitted="(data) => handleFormSubmission('overall survival', data)" />
            </q-tab-panel>
            <q-tab-panel name="batch">
              <BatchForm_Surv />
            </q-tab-panel>
          </q-tab-panels>
        </div>
        <CaseResultPage_Surv class="result-part" />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import CaseForm_Surv from 'src/components/CaseForm_Surv.vue'
import BatchForm_Surv from "src/components/BatchForm_Surv.vue"
import CaseResultPage_Surv from 'src/pages/CaseResultPage_Surv.vue'

export default defineComponent({
  name: 'IndexPage_Surv',
  components: {
    CaseForm_Surv,
    BatchForm_Surv,
    CaseResultPage_Surv
  },
  setup() {
    const mode = ref('case')
    const showResults = ref(false)
    const formValues = ref(null)

    const handleFormSubmission = (formMode, data) => {
      if (!data || !data.formValues) {
        console.error('Invalid data received:', data);
        return;
      }

      formValues.value = data.formValues;
      showResults.value = true;
    }

    return { mode, showResults, formValues, handleFormSubmission }
  },
})
</script>
<style>
.custom-tabs .q-tab__label {
  text-transform: none; /* 保持原始大小寫格式 */
  font-size: 18px; /* 設定字體大小 */
  font-weight: bold; /* 設定字體粗細 */
}

.flex-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: stretch;
  width: 100%;
}

.form-container {
  width: 38%; /* 调整表格部分的宽度 */
}

.form-part {
  max-width: 100%;
  width: 100%;
  margin-right: -250px; /* 负 margin 使得右侧没有留白 */
  margin-left: -40px; /* 负 margin 使得左侧没有留白 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}

.result-part {
  width: 62%;
  margin-right: -140px;
  margin-left: -40px;
  flex-direction: column;
  justify-content: center;
  align-items: flex-end;
  transition: width 0.3s;
}

.hide-result {
  width: 0;
  overflow: hidden;
  transition: width 0.3s;
}

.full-width {
  width: 100%;
}

.q-mt-md {
  margin-top: 1rem;
}
</style>
