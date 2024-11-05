import { ref, reactive, readonly  } from "vue"

// 早期復發 demo 資料(Case)為 RFA0071

export function useTestCase_ER(){
  const demo_case = reactive({
    'age': 79,
    'height': 169.4,
    'weight': 73.3,
    'tumor_number': 1,
    'tumor_size': 3.3,
    'afp': 93.32,
    'ast': 29,
    'alt': 28,
    'alb': 4.1,
    'alk_p': 87.0,
    'bili': 0.50,
    'cr': 1.05,
    'wbc': 5100,
    'plat': 138000,
    'ptinr': 0.98,
    'na': 138,
    'close_to_4_score': 0,
    'close_to_1': 1,
    'close_to_2378': 0,
    'bclc': 1
  })

  return { demo_case:readonly(demo_case) }
}

// 總體存活 demo 資料(Case)為 RFA0457

export function useTestCase_surv(){
  const demo_case = reactive({
    'age': 77,
    'height': 153.9,
    'weight': 76.7,
    'afp': 14.39,
    'ast': 77,
    'alt': 72,
    'alb': 3.4,
    'alk_p': 211.0,
    'bili': 0.71,
    'bun': 19,
    'cr': 0.75,
    'plat': 92000,
    'hb': 14.4,
    'neutrophil': 41.0,
    'lymphocyte': 51.8,
    'sex': 2,
    'bclc': 0,
    'child_class': 1,
    'close_to_4': 0
  })

  return { demo_case:readonly(demo_case) }
}
