<template>
  <div
    ref="dropdown"
    class="dropdown"
    @click="showDropdown=!showDropdown"
  >
    <span class="z-10">{{ worker.title }}</span>

    <div
      class="workers"
      v-show="showDropdown"
    >
      <div
        class="worker-choice"
        v-for="worker in workers"
        :key="worker.id"
        @click="chooseWorker(worker.id)"
      >
        {{ worker.title }}
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "Dropdown",
  props: ['worker', 'workers'],
  methods: {
    chooseWorker(id) {
      this.worker = this.workers.find(elem => elem.id === id)
    }
  },
  data() {
    return {
      showDropdown: false,
    }
  }
}
</script>

<style scoped>
.dropdown {
  @apply py-1 text-white border-[2px] border-blue-500 rounded-md;
  @apply w-[200px] h-[35px] overflow-hidden cursor-pointer;
}

.dropdown span {
  word-break: break-all;
  white-space: nowrap;
  text-overflow: ellipsis;
  @apply text-center w-full block;
  @apply mx-auto relative top-[-1px];
}

.workers {
  transform: translateX(-2px);
  @apply w-[200px] absolute bg-white text-black;
  @apply rounded-sm z-20;
}

.worker-choice {
  @apply font-bold px-1 z-20;
}

.worker-choice:hover {
  transition: all .25s ease;
  @apply bg-blue-500 text-white px-3;
}
</style>
