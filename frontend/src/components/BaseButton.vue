<template>
  <q-btn
    :label="label"
    :color="color"
    :icon="icon"
    :flat="flat"
    :round="round"
    :dense="dense"
    v-bind="props"
    @click="onClick"
  >
    <slot />
  </q-btn>
</template>

<script setup lang="ts">
import type { QBtnProps } from "quasar";
import type { PropType } from 'vue';

defineProps({
  label: {
    type: String as PropType<string>,
    default: ""
  },
  color: {
    type: String as PropType<string>,
    default: "primary"
  },
  icon: {
    type: String as PropType<string>,
    default: ""
  },
  flat: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  round: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  dense: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  onClick: {
    type: Function as PropType<QBtnProps["onClick"]>,
    default: undefined
  },
  props: {
    type: Object as PropType<Record<string, unknown>>,
    default: () => ({})
  }
});
</script>
