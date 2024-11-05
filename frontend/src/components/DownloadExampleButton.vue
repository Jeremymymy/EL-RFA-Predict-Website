<template>
  <q-btn
    label="Download example files"
    color="teal-6"
    unelevated
    @click="downloadFiles"
  />
</template>

<script>
export default {
  name: 'DownloadExampleButton',
  props: {
    folderName: {
      type: String,
      required: true
    },
    files: {
      type: Array,
      default: () => [
        { url: 'ER_Case/Image_features_example_for Early Recurrence prediction_case mode.xlsx', name: 'Image_features_example_for Early Recurrence prediction_case mode.xlsx' },
        { url: 'ER_Batch/Multimodal_features_examples_for Early Recurrence prediction_batch mode.xlsx', name: 'Multimodal_features_examples_for Early Recurrence prediction_batch mode.xlsx' },
        { url: 'ER_Batch/Clinical_features_examples_for Early Recurrence prediction_batch mode.xlsx', name: 'Clinical_features_examples_for Early Recurrence prediction_batch mode.xlsx' },
        { url: 'OS_Case/Image_features_example_for Overall Survival prediction_case mode.xlsx', name: 'Image_features_example_for Overall Survival prediction_case mode.xlsx' },
        { url: 'OS_Batch/Multimodal_features_examples_for Overall Survival prediction_batch mode.xlsx', name: 'Multimodal_features_examples_for Overall Survival prediction_batch mode.xlsx' },
        { url: 'OS_Batch/Clinical_features_examples_for Overall Survival prediction_batch mode.xlsx', name: 'Clinical_features_examples_for Overall Survival prediction_batch mode.xlsx' }
      ]
    }
  },
  setup(props) {
    const downloadFiles = () => {
      const folderName = props.folderName;
      const filesToDownload = props.files.filter(file => file.url.startsWith(folderName));

      filesToDownload.forEach(file => {
        const link = document.createElement('a');
        link.href = file.url;
        link.setAttribute('download', file.name);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      });
    };
    return { downloadFiles };
  }
}
</script>
