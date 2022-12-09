<template>
  <div
    ref="block"
    class="task-block"
    @click.stop="selectEvent"
  >
    <span :href="'/events/' + id">{{ title }}</span>
  </div>
</template>

<script>
// examples
// start  - 0 : 05
// finish - 1 : 20
// 1 minute = 2.8px
// точка отсчета - 0 : 00 - 15px

import interact from 'interactjs'

export default {
  name: "Event",
  props: ['start', 'finish', 'id', 'topic', 'title'],
  data() {
    return {
      initIndent: 0,
      step: 85.2,
      leftTranslate: 0,
      blockWidth: 0,
      topic_number : 0,
      topics: []
    }
  },
  mounted() {
    this.topics = this.$store.state.topics
    this.topic_number = this.topics.indexOf(this.topics.find(x => x.id === this.topic))

    this.renderEvent()

    let element = this.$refs.block
    let x = 0
    let y = 0

    let base = this
    interact(element)
      .draggable({
        modifiers: [
          interact.modifiers.snap({
            targets: [
              interact.snappers.grid({x: base.step, y: 85.2})
            ],
            range: Infinity,
            relativePoints: [{x: 0, y: 0}]
          }),
          interact.modifiers.restrict({
            // restriction: this.$refs.timeline,
            // elementRect: {top: 0, left: 0, bottom: 0, right: 1},
            // endOnly: true
          })
        ],
        inertia: false
      })
      .on('dragmove', function (event) {
        if (Math.abs(event.dx) < base.step) {
          return
        }

        x += event.dx
        y += event.dy

        event.target.style.transform = `translateX(${x}px)`
        base.leftTranslate = x

        base.applyTime()
      })
  },
  methods: {
    async $post(link, options) {
      options['JWT'] = this.$cookies.get('JWT')

      return await this.$axios.$post(this.url + link, options)
    },
    selectEvent() {
      this.$store.commit('setEvent', this.id)
    },
    renderEvent() {
      let block = this.$refs.block
      let blockIndent = this.timeToPixels(this.start)
      let blockWidth = this.calculateWidth(this.start, this.finish)

      this.blockWidth = blockWidth
      this.initIndent = blockIndent

      block.style.left = blockIndent + "px"
      block.style.top = 4 + (this.topic_number) * 60 + 'px'

      block.style.width = blockWidth + 'px'
    },
    timeToPixels(time) {
      let t = new Date(time * 1000)
      let hours = t.getHours()
      let minutes = t.getMinutes() + hours * 60

      return 5.68 * minutes / (this.timeStep / 900) + 15.5 + 200
    },
    pixelsToTime(pixels) {
      let withoutIndent = pixels - 215.5
      let minutes = withoutIndent / 5.68 * (this.timeStep / 900)
      let date = new Date(minutes * 60 * 1000 - 3 * 3600 * 1000)

      return date
    },
    calculateWidth(startTime, finishTime) {
      let start_ = this.timeToPixels(startTime)
      let finish_ = this.timeToPixels(finishTime)

      if (finish_ < start_) {
        finish_ += 24 * 60 * 5.68 + 200
      }
      return finish_ - start_
    },
    async applyTime() {
      let start_time = this.pixelsToTime(this.initIndent + this.leftTranslate)
      let finish_time = this.pixelsToTime(this.initIndent + this.leftTranslate + this.blockWidth)

      let date = this.$store.state.selectedDate

      let s = new Date(
        date.getFullYear(),
        date.getMonth(),
        date.getDate(),
        start_time.getHours(),
        start_time.getMinutes(),
        start_time.getSeconds()
      )

      let f = new Date(
        date.getFullYear(),
        date.getMonth(),
        date.getDate(),
        finish_time.getHours(),
        finish_time.getMinutes(),
        finish_time.getSeconds()
      )

      await this.$post('update_event', {
        event_id: this.id,
        start: s.getTime(),
        finish: f.getTime()
      })
    }
  },
  watch: {
    '$store.state.topics' (value) {
      let topic = value.find(x => x.id === this.topic)
      this.topic_number = value.indexOf(topic)

      this.renderEvent()
    },
    '$store.state.events'(value) {
      this.renderEvent()
    },
    '$store.state.timeStep'(oldValue, newValue) {
      this.renderEvent()
    },
    '$store.state.selectedEvent'(value) {
      let block = this.$refs.block
      if (value === this.id) {
        block.style.borderColor = '#e1dfdf'
      } else {
        block.style.borderColor = ''
      }
    }
  },
  computed: {
    url() {
      return this.$store.state.url
    },
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

.task-block a, span {
  @apply text-[#e1dfdf] font-bold block text-center;
  @apply h-[23px] relative top-[10px] overflow-hidden;
}

.task-block:hover {
  @apply border-[#e1dfdf]
}

.task-block a:hover {
  @apply underline;
}

</style>
