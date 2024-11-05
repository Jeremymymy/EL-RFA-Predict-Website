<template>
  <q-form @submit.prevent="submitForm" class="q-gutter-md custom-bg">
      <div class="row q-gutter-sm">
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" v-model="form.age" label="Age (years)"
          :rules="[ (val) => Number.isInteger(Number(val)) || 'Value must be an integer', ]" />
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" step="0.1" v-model="form.height" label="Height (cm)" />
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" step="0.1" v-model="form.weight" label="Weight (kg)" />
      </div>
      <div class="row q-gutter-sm">
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" step="0.01" v-model="form.afp" label="AFP (ng/ml)" />
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" v-model="form.ast" label="AST (U/L)"
          :rules="[ (val) => Number.isInteger(Number(val)) || 'Value must be an integer', ]" />
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" v-model="form.alt" label="ALT (U/L)"
          :rules="[ (val) => Number.isInteger(Number(val)) || 'Value must be an integer', ]" />
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" step="0.1" v-model="form.alb" label="Albumin (g/dL)"
          :rules="[ (val) => (val >= 0 && val <= 10) || 'Value must be between 0 and 10', ]" />
      </div>
      <div class="row q-gutter-sm">
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" step="0.1" v-model="form.alk_p" label="ALK-P (U/L)" />
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" step="0.01" v-model="form.bili" label="Bilirubin (mg/dL)"
          :rules="[ (val) => (val >= 0 && val <= 10) || 'Value must be between 0 and 10', ]" />
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" v-model="form.bun" label="BUN (mg/dL)"
          :rules="[ (val) => Number.isInteger(Number(val)) || 'Value must be an integer', ]" />
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" step="0.01" v-model="form.cr" label="Creatinine (mg/dL)" />
      </div>
      <div class="row q-gutter-sm">
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" v-model="form.plat" label="Platelet count (/uL)"
          :rules="validationEnabled ? [
            val => val >= 1000 || 'Value must be larger than 1000',
            val => Number.isInteger(Number(val)) || 'Value must be an integer' ] : []"
        />
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" step="0.1" v-model="form.hb" label="Hemoglobin (g/dL)" />
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" step="0.1" v-model="form.neutrophil" label="Neutrophil (%)" />
        <q-input class="custom-label-spacing" outlined color="indigo-9" type="number" step="0.1" v-model="form.lymphocyte" label="Lymphocyte (%)" />
      </div>
      <div class="row q-gutter-sm">
        <div class="q-pa-sm rounded-borders" :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'">
          Sex
          <q-option-group
            :options="[
              { label: 'Male', value: 1, color: 'blue' },
              { label: 'Female', value: 2, color: 'red' }
            ]"
            type="radio"
            inline
            v-model="form.sex"
          />
        </div>
        <div class="q-pa-sm rounded-borders" :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'">
          BCLC stage
          <q-option-group
            :options="[
              { label: '0', value: 0, color: 'green' },
              { label: 'A', value: 1, color: 'orange' },
              { label: 'B', value: 2, color: 'red' },
            ]"
            type="radio"
            inline
            v-model="form.bclc"
          />
        </div>
        <div class="q-pa-sm rounded-borders" :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'">
          Child-Pugh class
          <q-option-group
            :options="[
              { label: 'A', value: 1, color: 'green' },
              { label: 'B', value: 2, color: 'orange' },
              { label: 'C', value: 3, color: 'red' },
            ]"
            type="radio"
            inline
            v-model="form.child_class"
          />
        </div>
        <div class="q-pa-sm rounded-borders" :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'">
          Tumor close to blood vessel
          <q-option-group
            :options="[
              { label: 'No', value: 0, color: 'green' },
              { label: 'Yes', value: 1, color: 'red' }
            ]"
            type="radio"
            inline
            v-model="form.close_to_4"
          />
        </div>
      </div>

      <!-- 文件上傳部分 -->
      <div class="row q-gutter-sm">
        <q-file
          v-model="file"
          filled
          label="Upload image features"
          accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
          hint="Accepted files: .csv, .xls, .xlsx"
          color="indigo-9"
          @remove="file = null"
        >
          <template v-slot:prepend>
            <q-icon name="attach_file" />
          </template>
          <template v-slot:append v-if="file">
            <q-btn flat round dense icon="close" color="negative" @click="file = null" />
          </template>
        </q-file>
      </div>

      <!-- Confirmation Dialog for Clearing the Form -->
      <q-dialog v-model="isClearConfirmOpen">
        <q-card>
          <q-card-section>
            Are you sure you want to clear all data from the form?
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="Cancel" color="primary" v-close-popup></q-btn>
            <q-btn flat label="Clear" color="negative" @click="clearForm" v-close-popup></q-btn>
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- 提交按钮 -->
      <div class="row q-gutter-md justify-between">
      <div class="col-auto">
        <DownloadExampleButton folderName="OS_Case" />
      </div>
      <div class="col-auto row q-gutter-sm">
        <q-btn unelevated color="red" label="Clear" @click="promptClearForm" />
        <q-btn unelevated color="teal-6" type="button" label="Demo" @click="demo" />
        <q-btn unelevated color="teal-6" type="submit" label="Submit" :loading="submitting">
          <template v-slot:loading>
            <q-spinner-cube color="white" />
          </template>
        </q-btn>
      </div>
    </div>
  </q-form>

  <q-dialog v-model="isDialogOpen">
    <q-card>
      <q-card-section>
        All fields are required. Please ensure no fields are left blank before submitting.
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="Close" color="primary" v-close-popup></q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { defineComponent, reactive, ref, computed, toRefs, watch } from 'vue'
import { api } from "boot/axios"
import { useJobStore_Surv } from 'stores/job'
import { useTestCase_surv } from '../helpers/useDemo'
import DownloadExampleButton from './DownloadExampleButton.vue';

export default defineComponent({
  name: 'CaseForm_Surv',
  components: {
    DownloadExampleButton
  },
  emits: ['formSubmitted'],
  props: {
    initialValues: {
      type: Object,
      default: () => ({})
    }
  },
  setup (props, { emit }) {
    const job_store = useJobStore_Surv()
    const { initialValues } = toRefs(props)
    let { demo_case } = useTestCase_surv()
    // console.log(demo_case)

    const form = reactive({
      sex: null,
      age: null,
      height: null,
      weight: null,
      afp: null,
      ast: null,
      alt: null,
      alb: null,
      alk_p: null,
      bili: null,
      child_class: null,
      plat: null,
      hb: null,
      neutrophil: null,
      lymphocyte: null,
      bun: null,
      cr: null,
      bclc: null,
      close_to_4: null
    })

    const initForm = () => {
      for (const key in initialValues.value) {
        if (form.hasOwnProperty(key)) {
          form[key] = initialValues.value[key];
        }
      }
    };

    watch( initialValues, () => {
        initForm();
      }, { immediate: true, deep: true }
    );

    initForm();

    const file = ref(null)
    const submitting = ref(false)
    const isDialogOpen = ref(false)
    const isClearConfirmOpen = ref(false)
    const validationEnabled = ref(true)

    const isFormEmpty = computed(() => {
      return Object.values(form).every(x => x === null || x === '') && file.value === null
    })

    const isFormIncomplete = computed(() => {
      return Object.values(form).some(x => x === null || x === '')  // Checks if any value is null or empty string
    })

    const demo = () => {
      Object.assign(form, demo_case)
    }

    const submitForm = async () => {
      if (isFormIncomplete.value) {
        isDialogOpen.value = true  // Open the dialog if form is incomplete
        return
      }

      submitting.value = true
      const formData = new FormData()
      Object.keys(form).forEach(key => {
        formData.append(key, form[key])
      })
      if (file.value) {
        formData.append("file", file.value)
      }

      try {
        const response = await api.post("/overall_survival/submit/case", formData, {
          headers: {
            'Accept': 'application/json'
          }
        })
        job_store.updateJobResult(response.data[0])
        job_store.updateFormValues(form)
        console.log(job_store.risk_score)
        emit("formSubmitted", {
          formValues: { ...form },
          predictionResult: response.data[0],
        })
      } catch (error) {
        console.error("Submission error:", error.message)
      } finally {
        submitting.value = false;
      }
    }

    const promptClearForm = () => {
      if (!isFormEmpty.value) {
        isClearConfirmOpen.value = true
      }
    }

    const clearForm = () => {
      validationEnabled.value = false
      Object.keys(form).forEach(key => {
        form[key] = null
      })
      file.value = null
      setTimeout(() => {
        validationEnabled.value = true
      }, 0)
    }

    return {form, file, submitting, isFormIncomplete, isDialogOpen, isClearConfirmOpen, validationEnabled, submitForm, promptClearForm, clearForm, demo}
  }
})
</script>
<style>
.custom-bg {
  background-color: rgba(255, 255, 255, 0.7); /* 白色背景，50% 透明度 */
}
.custom-label-spacing .q-field__label {
  padding-left: 8px; /* 或任何你需要的間距 */
}
.q-gutter-sm > .q-input {
  margin-top: 2px; /* 設定你想要的間距大小 */
  margin-bottom: 2px; /* 設定你想要的間距大小 */
  margin-left: 8px !important; /* 設定你想要的間距大小 */
  margin-right: 10px !important; /* 設定你想要的間距大小 */
  padding-left: 4px !important; /* 或任何你需要的間距 */
  padding-right: 2px !important; /* 或任何你需要的間距 */
  padding-top: 1px; /* 或任何你需要的間距 */
  padding-bottom: 1px; /* 或任何你需要的間距 */
}
.q-file {
  margin-top: 2px; /* 設定你想要的間距大小 */
  margin-bottom: 2px; /* 設定你想要的間距大小 */
  margin-left: 2px; /* 設定你想要的間距大小 */
  padding-left: 10px; /* 或任何你需要的間距 */
  padding-right: 14px; /* 或任何你需要的間距 */
  padding-top: 1px; /* 或任何你需要的間距 */
  padding-bottom: 1px; /* 或任何你需要的間距 */
}
.q-pa-sm {
  margin-top: 2px; /* 設定你想要的間距大小 */
  margin-bottom: 2px; /* 設定你想要的間距大小 */
  margin-left: 12px; /* 或任何你需要的間距 */
  margin-right: 8px; /* 或任何你需要的間距 */
  padding-top: 1px; /* 或任何你需要的間距 */
  padding-bottom: 1px; /* 或任何你需要的間距 */
}
</style>
