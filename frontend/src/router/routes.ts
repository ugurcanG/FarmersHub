import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/DashboardPage.vue') },
      { path: 'simulation', component: () => import('src/pages/SimulationPanelPage.vue') },
      { path: 'fields', component: () => import('src/pages/FieldsPage.vue') },
      {
        path: '/fields/:id',
        component: () => import('src/pages/FieldDetailsPage.vue'),
        props: true,
      },
      { path: 'employees', component: () => import('src/pages/EmployeesPage.vue') },
      { path: 'machines', component: () => import('src/pages/MachinesPage.vue') },
      {
        path: '/machines/:id',
        component: () => import('src/pages/MachineDetailsPage.vue'),
        props: true,
      },
      { path: 'seeds', component: () => import('src/pages/SeedsPage.vue') },
      { path: 'market', component: () => import('src/pages/MarketPage.vue') },
      { path: 'about', component: () => import('src/pages/AboutPage.vue') },
      { path: 'impressum', component: () => import('src/pages/ImpressumPage.vue') },
    ],
  },
  // 404-Seite
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes
