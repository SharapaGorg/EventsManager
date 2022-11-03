<template>
  <div class="simple-event">
    <span>{{ title }}</span>
  </div>
</template>

<script>
export default {
  name: "SimpleEvent",
  props: ['id', 'title']
}
</script>

<style scoped>

.simple-event {
  transition: all .25s ease;
  @apply w-[190px] mx-auto h-[60px] rounded-lg border-[#e1dfdf];
  @apply border-2 my-2 pt-[12px] cursor-pointer text-[#e1dfdf];
  @apply text-center font-bold;
}

.simple-event span {
  @apply h-[23px] overflow-hidden block;
}

</style>

