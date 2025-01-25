<template>
  <q-btn
    :label="label"
    :color="color"
    :icon="icon"
    class="button-custom"
    :unelevated="unelevated"
    :flat="flat"
    :rounded="rounded"
    :dense="dense"
    v-bind="props"
    @click="onClick"
  >
    <slot />
  </q-btn>
</template>

<script setup lang="ts">
import type { QBtnProps } from 'quasar'
import type { PropType } from 'vue'

defineProps({
  label: {
    type: String as PropType<string>,
    default: '',
  },
  color: {
    type: String as PropType<string>,
    default: 'primary',
  },
  icon: {
    type: String as PropType<string>,
    default: '',
  },
  unelevated: {
    type: Boolean as PropType<boolean>,
    default: false,
  },
  flat: {
    type: Boolean as PropType<boolean>,
    default: false,
  },
  rounded: {
    type: Boolean as PropType<boolean>,
    default: true,
  },
  dense: {
    type: Boolean as PropType<boolean>,
    default: false,
  },
  onClick: {
    type: Function as PropType<QBtnProps['onClick']>,
    default: undefined,
  },
  props: {
    type: Object as PropType<Record<string, unknown>>,
    default: () => ({}),
  },
})
</script>

<style lang="scss">
.button-custom {
  font-weight: bold; /* Fett für den Text */
  font-size: 1.1rem; /* Textgröße anpassen */
  text-transform: uppercase; /* Text in Großbuchstaben */
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid;
}
</style>
