<template>
  <q-page class="q-pa-md">
    <h3 class="text-h5 text-dark">Marktübersicht</h3>

    <!-- Ladeanimation während Datenabruf -->
    <q-inner-loading :showing="loading">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>

    <!-- Saatgut & Erntepreise -->
    <InfoCard title="Marktpreise für Saatgut & Ernte">
      <DataTable :rows="seedRows" :columns="seedColumns" />
    </InfoCard>

    <!-- Kostenübersicht -->
    <InfoCard title="Kostenanalyse">
      <DataTable :rows="costRows" :columns="costColumns" />
    </InfoCard>

    <!-- Gewinn-/Verlustübersicht -->
    <InfoCard title="Gewinn- & Verlustrechnung">
      <q-card class="q-pa-md">
        <div class="text-h6">Gesamteinnahmen: {{ formatCurrency(marketData.total_revenue) }}</div>
        <div class="text-h6">Gesamtkosten: {{ formatCurrency(totalExpenses) }}</div>
        <div class="text-h6" :class="profitLoss >= 0 ? 'text-green' : 'text-red'">
          {{ profitLoss >= 0 ? 'Gewinn' : 'Verlust' }}: {{ formatCurrency(profitLoss) }}
        </div>
      </q-card>
    </InfoCard>

    <!-- Diagramme -->
    <EntityCharts
      title="Kosten- & Gewinnentwicklung"
      :labels="['Felder', 'Mitarbeiter', 'Maschinen']"
      :formattedData="chartData"
      :chartOptions="[{ label: 'Kosten', value: 'costs' }, { label: 'Gewinn', value: 'profit' }]"
    />

    <!-- ChatDrawer für GPT Chat -->
    <ChatDrawer v-model:chatDrawerOpen="chatDrawerOpen" />
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'
import ChatDrawer from 'src/components/shared/ChatDrawer.vue'
import InfoCard from 'src/components/shared/InfoCard.vue'
import DataTable from 'src/components/shared/DataTable.vue'
import EntityCharts from 'src/components/shared/EntityCharts.vue'
import type { MarketData } from 'src/components/models'

const chatDrawerOpen = ref(false)
const loading = ref(true)
const marketData = ref<MarketData>({
  seed_prices: {},
  harvest_prices: {},
  expenses: {
    fields: 0,
    employees: 0,
    machines: 0,
  },
  total_revenue: 0,
  profit_loss: 0,
})


// **Marktdaten abrufen**
const fetchMarketData = async () => {
  try {
    const response = await api.get('/market/')
    marketData.value = response.data
  } catch (error) {
    console.error('Fehler beim Abrufen der Marktdaten:', error)
  } finally {
    loading.value = false
  }
}

// **Daten für Saatgut- & Erntepreise**
const seedRows = computed(() =>
  Object.keys(marketData.value.seed_prices || {}).map((name) => ({
    name,
    seed_price: marketData.value.seed_prices[name],
    harvest_price: marketData.value.harvest_prices[name],
  }))
)

const seedColumns = [
  { name: 'name', label: 'Saatgut', field: 'name', align: 'left' as const },
  { name: 'seed_price', label: 'Saatgutpreis (€/kg)', field: 'seed_price', align: 'right' as const },
  { name: 'harvest_price', label: 'Erntepreis (€/kg)', field: 'harvest_price', align: 'right' as const },
]

// **Kostenübersicht**
const costRows = computed(() => [
  { category: 'Felder', amount: marketData.value.expenses?.fields || 0 },
  { category: 'Mitarbeiter', amount: marketData.value.expenses?.employees || 0 },
  { category: 'Maschinenwartung', amount: marketData.value.expenses?.machines || 0 },
])

const costColumns = [
  { name: 'category', label: 'Kategorie', field: 'category', align: 'left' as const },
  { name: 'amount', label: 'Kosten (€)', field: 'amount', align: 'right' as const, format: (val: unknown) => formatCurrency(val as number) },
]

// **Berechnung der Gesamtkosten und des Gewinns**
const totalExpenses = computed(() => {
  const expenses = marketData.value.expenses || {}
  return expenses.fields + expenses.employees + expenses.machines
})

const profitLoss = computed(() => marketData.value.profit_loss || 0)

// **Daten für Diagramme**
const chartData = computed(() => [
  { costs: marketData.value.expenses?.fields || 0, profit: profitLoss.value },
  { costs: marketData.value.expenses?.employees || 0, profit: profitLoss.value },
  { costs: marketData.value.expenses?.machines || 0, profit: profitLoss.value },
])

// **Formatierung von Währungswerten**
const formatCurrency = (value: number) => `${value.toFixed(2)} €`

onMounted(fetchMarketData)
</script>
