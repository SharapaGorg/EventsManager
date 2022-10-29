<template>
  <div ref="schedule">
    <div class="scale-menu">
      <div class="scale-button" @click="editTimeStep(-900)">
        <span>+</span>
      </div>
      <div class="scale-button" @click="editTimeStep(900)">
        <span>-</span>
      </div>
    </div>

    <div class="timeline">
      <div
        v-for="point in timePoints"
        class="time-point"
        :key="point.id"
      >
        {{ point.hours }} : {{ point.minutes }}
      </div>
    </div>

    <Event
      v-for="event in events"
      :id="event.id"
      :key="event.id"
      :start="event.start"
      :finish="event.finish"
      :style="{'transform' : `translateY(${event.indent}px)`}"
    />

  </div>
</template>

<script>
export default {
  name: "events",
  data() {
    return {
      timePoints: [],
      events: [],
    }
  },
  async mounted() {
    this.renderTimeline();

    this.events = await this.$axios.$post(this.url, {})
  },
  methods: {
    renderTimeline(step) {
      let day = 60 * 60 * 24
      let timePoints = []

      let currentPoint = 0;
      while (currentPoint <= day) {
        let time = new Date((currentPoint - 60 * 60 * 3) * 1000)

        timePoints.push({
          id: currentPoint,
          hours: time.getHours(),
          minutes: time.getMinutes(),
        })
        currentPoint += this.timeStep
      }

      this.timePoints = timePoints
    },
    editTimeStep(step) {
      if (this.timeStep + step <= 0 || this.timeStep + step > 60 * 60 * 2) {
        return
      }

      this.$store.commit('setTimeStep', this.timeStep + step)
    }
  },
  computed: {
    timeStep() {
      return this.$store.state.timeStep
    },
    url() {
      return this.$store.state.url
    }
  },
  watch: {
    '$store.state.timeStep'(oldValue, newValue) {
      this.renderTimeline(oldValue - newValue)
    }
  }
}
</script>

<style scoped>

.scale-menu {
  @apply fixed py-1 px-2 mx-auto w-fit py-3 bottom-0 left-0;
}

.scale-button {
  @apply px-2 py-1 rounded-lg w-fit cursor-pointer text-white;
  @apply font-bold border-2 border-white w-[50px] text-center mx-3;
  @apply text-2xl
}

.scale-button:hover {
  transition: all .25s ease;
  @apply bg-white text-[#3C3F41];
}

.scale-button span {
  @apply relative top-[-3px]
}

.timeline {
  @apply flex pl-[15px] border-b-2 border-[#434D68] h-[30px];
  @apply bg-[#8F97AC] w-fit min-w-[100vw];
}

.time-point {
  @apply w-[85px] font-bold text-white h-[40px] text-[#434D68];
}

</style>
