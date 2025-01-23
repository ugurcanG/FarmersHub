import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/DashboardPage.vue') },
      { path: 'fields', component: () => import('pages/FieldsPage.vue') },
      { path: 'employees', component: () => import('src/pages/EmployeesPage.vue') },
      { path: 'machines', component: () => import('src/pages/MachinesPage.vue') },
      { path: 'market', component: () => import('src/pages/MarketPage.vue') },
      { path: 'about', component: () => import('pages/AboutPage.vue') },
      { path: 'impressum', component: () => import('src/pages/ImpressumPage.vue') },
    ],
  },
  // 404-Seite
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
