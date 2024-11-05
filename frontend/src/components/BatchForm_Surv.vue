<template>
  <q-form @submit.prevent="submitForm" class="q-gutter-md custom-bg">
    <div class="row justify-between q-gutter-sm">
      <div class="col-auto row justify-start self-center">
        <q-file
          color="indigo-9"
          v-model="file"
          accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
          hint="Accepted files: .csv, .xls, .xlsx"
          label="Upload file"
          @remove="file = null"
          class="limited-width-q-file"
        >
          <template v-slot:prepend>
            <q-icon name="attach_file" />
          </template>
          <template v-slot:append v-if="file">
            <q-btn flat round dense icon="close" color="negative" @click="file = null" />
          </template>
        </q-file>
      </div>
      <div class="col-auto row justify-end self-center q-gutter-sm">
        <div class="col-auto">
          <q-btn type="submit" label="upload" color="teal-6" :loading="submitting" unelevated>
            <template v-slot:loading>
              <q-spinner-cube color="white" />
            </template>
          </q-btn>
        </div>
        <div class="col-auto">
          <DownloadExampleButton folderName="OS_Batch" />
        </div>
      </div>
    </div>
  </q-form>
  <div class="description-text">
    Based on the feature combinations used in the example files, you can batch upload the corresponding clinical features or multimodal features of the patients. The prediction results (Excel file) will be downloaded directly to your computer. The prediction results will provide the risk score, high/low-risk group, and survival rate for each patient.
  </div>
</template>

<script>
import { defineComponent, reactive, ref } from 'vue';
import { useQuasar, Notify } from 'quasar'
import { api } from 'boot/axios';
import { downloadBlob } from '../helpers/useUtils'
import DownloadExampleButton from './DownloadExampleButton.vue';

export default defineComponent({
  name: 'BatchForm_Surv',
  components: {
    DownloadExampleButton
  },
  setup () {
    const file = ref(null)
    const submitting = ref(false)
    const $q = useQuasar()

    const getFormData = () =>{
      if (file.value) {
        const formData = new FormData()
        formData.append("file", file.value)
        return formData
      }
      else {
        return null
      }
    }

    const submitForm = async () =>{
      let formData = getFormData()
      if (formData == null) {
        $q.notify({
          message: 'Please select the file.',
          color: 'red-8'
        })
      }
      else {
        submitting.value = true
        try {
          const response = await api.post("overall_survival/submit/batch", formData, { responseType: 'blob' })
          if (response.headers['content-type'] === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
            downloadBlob(response.data, 'overall_survival_results.xlsx');
            $q.notify({
              message: 'Results has been downloaded.',
              color: 'green-6'
            });
          } else {
            const errorMessage = 'Data format error. Please ensure the data is correctly formatted and try again.'
            Notify.create({
              color: 'negative',
              position: 'top',
              message: errorMessage,
              icon: 'report_problem'
            })
          }
        } catch (error) {
          console.error("Submission error:", error.message)
          const errorMessage = 'Data format error. Please ensure the data is correctly formatted and try again.'
          Notify.create({
            color: 'negative',
            position: 'top',
            message: errorMessage,
            icon: 'report_problem'
          })
        } finally {
          submitting.value = false
        }
      }
    }

    return {file, submitting, submitForm}
  }
})
</script>

<style>
.custom-bg {
  background-color: rgba(255, 255, 255, 0.7); /* White background with 70% opacity */
}

.limited-width-q-file {
  max-width: 450px; /* Set the maximum width you want */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.description-text {
  margin-top: 20px; /* Set the margin you want */
  font-size: 16px; /* Set the font size you want */
  color: grey; /* Set the text color to grey */
  text-align: justify; /* Make text justified */
  line-height: 1.5; /* Set the line height for better readability */
  max-width: 800px; /* Set the maximum width */
  margin-left: auto; /* Center the text */
  margin-right: auto; /* Center the text */
}
</style>
