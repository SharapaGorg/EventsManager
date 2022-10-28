<template>
  <div
    ref="block"
    class="task-block"
    @click="selectTask"
  >
  </div>
</template>

<script>
// examples
// start  - 0 : 05
// finish - 1 : 20
// 1 minute = 2.8px
// точка отсчета - 0 : 00 - 15px
export default {
  name: "Event",
  props: ['start', 'finish', 'id'],
  mounted() {
    let block = this.$refs.block
    let blockIndent = this.timeToPixels(this.start)
    let blockWidth = this.calculateWidth(this.start, this.finish)
    block.style.transform = `translateX(${blockIndent}px) translateY(3px)`
    block.style.width = blockWidth + 'px'
  },
  methods: {
    selectTask() {
      this.$store.commit('setSelectedTaskId', this.id)
    },
    timeToPixels(time) {
      let s = time.split(':')
      let hours = s[0]
      let minutes = parseInt(s[1]) + hours * 60
      let startPoint = 2.84 * minutes + 15.5
      return startPoint
    },
    calculateWidth(startTime, finishTime) {
      let start_ = this.timeToPixels(startTime)
      let finish_ = this.timeToPixels(finishTime)
      if (finish_ < start_) {
        finish_ += 24 * 60 * 2.84
      }
      return finish_ - start_
    }
  }
}
</script>

<style scoped>
.task-block {
  @apply h-[50px] bg-[#434D68] inline-block absolute;
  @apply w-[200px] cursor-pointer;
}
</style>
