
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/CataloguePage.vue') },
      { path: 'early_recurrence', component: () => import('pages/IndexPage_ER.vue') },
      { path: 'overall_survival', component: () => import('pages/IndexPage_Surv.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
