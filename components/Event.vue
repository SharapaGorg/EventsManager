<template>
  <div
    ref="block"
    class="task-block"
    @click.stop="selectEvent"
  >
    <span>{{ title }}</span>
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
  props: ['start', 'finish', 'id', 'topic', 'title'],
  mounted() {
    this.renderEvent()
  },
  methods: {
    selectEvent() {
        this.$store.commit('setEvent', this.id)
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
    },
    '$store.state.selectedEvent'(value) {
      let block = this.$refs.block
      if (value === this.id) {
        block.style.borderColor = '#e1dfdf'
      }
      else {
        block.style.borderColor = ''
      }
    }
  },
  computed: {
    timeStep() {
      return this.$store.state.timeStep
    },
    selectedEvent() {
      return this.$store.state.selectedEvent
    }
  }
}
</script>

<style scoped>
.task-block {
  @apply h-[50px] bg-[#23272A] inline-block absolute;
  @apply w-[200px] cursor-pointer z-20 rounded-md;
  @apply border-2 border-transparent
}

.task-block span {
  @apply text-[#e1dfdf] font-bold block text-center;
  @apply h-[23px] relative top-[10px] overflow-hidden;
}

.task-block:hover {
  @apply border-[#e1dfdf]
}

</style>
