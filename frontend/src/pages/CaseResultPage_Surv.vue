<template>
  <q-page padding>
    <div class="row justify-center q-gutter-md">
      <q-card class="col-md-6 custom-bg" flat bordered>
        <q-card-section>
          <q-markup-table :separator="'vertical'" flat bordered>
            <thead>
              <tr>
                <th class="text-left">Years</th>
                <th class="text-center">1</th>
                <th class="text-center">2</th>
                <th class="text-center">3</th>
                <th class="text-center">4</th>
                <th class="text-center">5</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="text-left">Survival rate</td>
                <td class="text-center">{{ formatPercentage(job_store.survival_rates[0]) }}</td>
                <td class="text-center">{{ formatPercentage(job_store.survival_rates[1]) }}</td>
                <td class="text-center">{{ formatPercentage(job_store.survival_rates[2]) }}</td>
                <td class="text-center">{{ formatPercentage(job_store.survival_rates[3]) }}</td>
                <td class="text-center">{{ formatPercentage(job_store.survival_rates[4]) }}</td>
              </tr>
            </tbody>
          </q-markup-table>
        </q-card-section>

        <q-card-section class="row justify-center">
          <Bar
            id="survival-chart"
            :options="chart_options"
            :data="survival_data"
          />
        </q-card-section>
      </q-card>
    </div>

  </q-page>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, LineElement, CategoryScale, LinearScale, PointElement, LineController, BarController } from 'chart.js'
import { useJobStore_Surv } from 'stores/job'
import { computed } from 'vue'

ChartJS.register(Title, Tooltip, Legend, BarElement, LineElement, CategoryScale, LinearScale, PointElement, LineController, BarController)

export default {
  name: 'CaseResultPage_Surv',
  components: { Bar },
  setup() {
    const job_store = useJobStore_Surv()

    const survival_data = computed(() => ({
      labels: ["1 year", "2 year", "3 year", "4 year", "5 year"],
      datasets: [
        {
          type: "bar",
          label: "Survival rate",
          data: job_store.survival_rates.map((rate) => rate * 100),
          backgroundColor: '#1976d2',
          order: 2,
        },
        {
          type: "line",
          label: "Survival rate",
          data: job_store.survival_rates.map((rate) => rate * 100),
          borderColor: "#f87979",
          borderWidth: 3,
          fill: false,
          tension: 0.5,  // 調整曲線的彎曲程度
          pointBackgroundColor: "#f87979",
          pointBorderColor: "#fff",
          pointBorderWidth: 2,
          pointRadius: 5,
          order: 1,
        },
      ],
    }));

    const chart_options = {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          labels: {
            filter: function (item, chart) {
              // 不顯示'line'的圖例
              return item.datasetIndex !== 1;
            },
          },
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              let label = context.dataset.label || '';
              if (label) {
                label += ': ';
              }
              label += context.raw + '%';
              return label;
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          suggestedMax: 100,
          title: {
            display: true,
            text: "Overall survival (%)", // 這裡設定你想顯示的標籤文字
            color: "#666", // 可以設定標籤文字顏色
            font: {
              size: 14, // 設定文字大小
              family: "Arial", // 設定字體
            },
          },
        },
      },
    };

    function formatPercentage(value) {
      return `${(value * 100).toFixed(0)}%`; // 轉換為整數百分比
    }

    return {job_store, survival_data, chart_options, formatPercentage}
  },
}
</script>

<style>
.status-indicators {
  display: flex;
}
.status-circle {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  margin-right: 4px;
}
.custom-bg {
  background-color: rgba(255, 255, 255, 0.7); /* 白色背景，50% 透明度 */
}
</style>
