<template>
  <div ref="schedule" class="events-window">
    <div class="scale-menu">
      <div class="scale-button noselect" @click="editTimeStep(-900)">
        <span>+</span>
      </div>
      <div class="scale-button noselect" @click="editTimeStep(900)">
        <span>-</span>
      </div>
    </div>
      <div class="topics" ref="topics">
          <div
            v-for="topic in topics"
            :key="topic.id"
            class="topic"
          >
            {{ topic.title }}
          </div>
      </div>

      <div class="sidebar" v-show="showSideBar">
        <div class="side-title">{{ selectedEvent.title }}</div>
        <div class="side-description">{{ selectedEvent.description}}</div>
      </div>

      <div ref='timeline' class="timeline">
        <div
          v-for="point in timePoints"
          class="time-point"
          :key="point.id"
        >
          {{ point.hours }} : {{ point.minutes }}
        </div>
      </div>

      <div class="events" ref="events">
        <Event
          v-for="event in events"
          :id="event.id"
          :key="event.id"
          :start="event.start"
          :finish="event.finish"
          :topic="event.topic_id"
          :title="event.title"/>
<!--          @click="selectEvent(event.id)"-->
      </div>
  </div>
</template>

<script>
export default {
  name: "events",
  data() {
    return {
      timePoints: [],
      events: [],
      topics : [],
      showSideBar : false,
      selectedEvent : {}
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

    // cancel selecting event
    this.$refs.events.addEventListener('click', (event) => {
      this.selectEvent(NaN)
    })
    this.$refs.topics.addEventListener('click', (event) => {
      this.selectEvent(NaN)
    })
  },
  methods: {
    selectEvent(id) {
      this.$store.commit('setEvent', id)
    },
    setTimeStep(value) {
      this.$store.commit('setTimeStep', value)
    },
    async getEvent(id) {
        return await this.$axios.$post(this.url + 'event', {
          id : id
        })
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
    '$store.state.timeStep'(newValue, oldValue) {
      this.renderTimeline()
    },
    async '$store.state.selectedEvent' (newValue, oldValue) {
      if (isNaN(newValue)) {
        this.showSideBar = false
        return
      }

      this.selectedEvent = await this.getEvent(newValue)
      this.showSideBar = true
    }
  }
}
</script>

<style scoped>

.scale-menu {
  @apply fixed py-1 px-2 mx-auto w-fit py-3 bottom-0 right-0;
  @apply z-40;
}

.scale-button {
  @apply px-2 py-1 rounded-lg w-fit cursor-pointer text-[#e1dfdf];
  @apply font-bold border-2 border-[#e1dfdf] w-[50px] text-center mx-3;
  @apply text-2xl my-1
}

.scale-button:hover {
  transition: all .25s ease;
  @apply bg-[#e1dfdf] text-[#3C3F41];
}

.scale-button span {
  @apply relative top-[-3px]
}

.timeline {
  @apply flex pl-[215px] border-b-2 border-[#434D68] h-[30px];
  @apply bg-[#23272A] w-fit min-w-[100vw];
}

.events {
  height : calc(100vh - 200px);
  @apply w-fit min-w-[100vw]
}

.time-point {
  @apply w-[85px] font-bold text-[#e1dfdf] h-[40px];
}

.topics {
  @apply w-[200px] h-screen;
  @apply fixed top-[30px] bg-[#23272A] z-20
}

.topic {
  @apply px-2 py-4 h-[60px] border-b-2 border-[#434D68] w-screen;
  @apply text-[#e1dfdf] font-bold;
}

.topic:hover {
  @apply bg-[#434D68];
}

.sidebar {
  @apply fixed bg-[#23272A] h-[170px] bottom-0 z-30 w-screen;
  @apply border-t-2 border-[#434D68] pt-1 text-[#e1dfdf]
}

.sidebar .side-title {
  @apply text-xl text-center underline;
  @apply block;
}

.sidebar .side-description {
  @apply h-[130px] max-w-[370px] mx-auto;
  @apply overflow-y-auto text-justify;
}

.side-description::-webkit-scrollbar {
  width : 0 !important;
}

</style>
