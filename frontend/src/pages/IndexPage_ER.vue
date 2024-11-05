<template>
  <q-page class="q-pa-md">
    <div class="row justify-center">
      <q-card v-if="!showResults" class="q-pa-md column justify-center" flat bordered>

        <q-tabs v-model="mode" dense class="text-grey-7 custom-tabs" active-color="indigo-10" indicator-color="deep-orange-8" align="justify">
          <q-tab name="case" label="Early Recurrence (Case)" />
          <q-tab name="batch" label="Early Recurrence (Batch)" />
        </q-tabs>

        <q-tab-panels v-model="mode" animated>
          <q-tab-panel name="case">
            <CaseForm_ER @formSubmitted="(data) => handleFormSubmission('early recurrence', data)" />
          </q-tab-panel>
          <q-tab-panel name="batch">
            <BatchForm_ER />
          </q-tab-panel>
        </q-tab-panels>
      </q-card>

      <div v-if="showResults" class="flex-container full-width">
        <div class="col form-container" align="center">
          <q-tabs v-model="mode" dense class="text-grey-7 custom-tabs" active-color="indigo-10" indicator-color="deep-orange-8" align="justify">
            <q-tab name="case" label="Early Recurrence (Case)" />
            <q-tab name="batch" label="Early Recurrence (Batch)" />
          </q-tabs>

          <q-tab-panels v-model="mode" animated>
            <q-tab-panel name="case">
              <CaseForm_ER class="form-part" :initial-values="formValues" @formSubmitted="(data) => handleFormSubmission('early recurrence', data)" />
            </q-tab-panel>
            <q-tab-panel name="batch">
              <BatchForm_ER />
            </q-tab-panel>
          </q-tab-panels>
        </div>
        <CaseResultPage_ER class="result-part" />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import CaseForm_ER from "src/components/CaseForm_ER.vue"
import BatchForm_ER from 'src/components/BatchForm_ER.vue'
import CaseResultPage_ER from "src/pages/CaseResultPage_ER.vue"

export default defineComponent({
  name: 'IndexPage_ER',
  components: {
    CaseForm_ER,
    BatchForm_ER,
    CaseResultPage_ER
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
