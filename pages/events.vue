<template>
  <div ref="schedule">
    <div class="scale-menu">
      <div class="scale-button noselect" @click="editTimeStep(-900)">
        <span>+</span>
      </div>
      <div class="scale-button noselect" @click="editTimeStep(900)">
        <span>-</span>
      </div>
    </div>
      <div class="topics">
        <div
          v-for="topic in topics"
          :key="topic.id"
          class="topic"
        >
          {{ topic.title }}
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
        :topic="event.topic_id"
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
      topics : []
    }
  },
  async mounted() {
    let localTimeStep = localStorage.getItem('timeStep')
    if (localTimeStep) {
        this.setTimeStep(parseInt(localTimeStep))
    }

    this.renderTimeline();
    this.events = await this.$axios.$post(this.url + 'events', {})
    this.topics = await this.$axios.$post(this.url + 'topics', {})

    console.log(this.events)
  },
  methods: {
    setTimeStep(value) {
      this.$store.commit('setTimeStep', value)
    },
    renderTimeline() {
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

      localStorage.setItem('timeStep', this.timeStep + step)
      this.setTimeStep(this.timeStep + step)
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
      this.renderTimeline()
    }
  }
}
</script>

<style scoped>

.scale-menu {
  @apply fixed py-1 px-2 mx-auto w-fit py-3 bottom-0 right-0;
}

.scale-button {
  @apply px-2 py-1 rounded-lg w-fit cursor-pointer text-white;
  @apply font-bold border-2 border-white w-[50px] text-center mx-3;
  @apply text-2xl my-1
}

.scale-button:hover {
  transition: all .25s ease;
  @apply bg-white text-[#3C3F41];
}

.scale-button span {
  @apply relative top-[-3px]
}

.timeline {
  @apply flex pl-[215px] border-b-2 border-[#434D68] h-[30px];
  @apply bg-[#8F97AC] w-fit min-w-[100vw];
}

.time-point {
  @apply w-[85px] font-bold text-white h-[40px] text-[#434D68];
}

.topics {
  @apply w-[200px] min-h-[100vh];
  @apply fixed top-[30px] bg-[#8F97AC]
}

.topic {
  @apply px-2 py-4 h-[60px] border-b-2 border-[#434D68] w-screen;
  @apply text-[#3C3F41] font-bold;
}

</style>
