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
  props: ['start', 'finish', 'id', 'topic'],
  mounted() {
    this.renderEvent()
  },
  methods: {
    selectTask() {
      this.$store.commit('setSelectedTaskId', this.id)
    },
    renderEvent() {
      let block = this.$refs.block
      let blockIndent = this.timeToPixels(this.start)
      let blockWidth = this.calculateWidth(this.start, this.finish)

      block.style.transform = `translateX(${blockIndent}px) translateY(${4 + (this.topic - 1) * 60}px)`
      block.style.width = blockWidth + 'px'
    },
    timeToPixels(time) {
      let t = new Date(time * 1000)
      let hours = t.getHours()
      let minutes = t.getMinutes() + hours * 60

      let startPoint = 5.68 * minutes / (this.timeStep / 900) + 15.5 + 200
      return startPoint
    },
    calculateWidth(startTime, finishTime) {
      let start_ = this.timeToPixels(startTime)
      let finish_ = this.timeToPixels(finishTime)

      if (finish_ < start_) {
        finish_ += 24 * 60 * 5.68 + 200
      }
      return finish_ - start_
    }
  },
  watch: {
    '$store.state.timeStep'(oldValue, newValue) {
        this.renderEvent()
    }
  },
  computed: {
    timeStep() {
      return this.$store.state.timeStep
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
