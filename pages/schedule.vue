<template>
  <div ref="schedule" class="events-window">

    <topic-modal
      v-show="showTopicModal"
      @closeTopicModal="showTopicModal=false"
    />

    <event-modal
      v-show="showEventModal"
      @closeEventModal = "showEventModal = false"
    />


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

      <div class="add-topic" @click="showTopicModal = true">
        <div class="plus">
          <span class="relative top-[-10px] noselect">+</span>
        </div>
      </div>
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
<!--      <nuxt-link-->
<!--        v-for="event in events"-->
<!--        :key="event.id"-->
<!--        :to='"events/" + event.id'>-->
          <Event
            v-show="event.topic_id !== 0"
            v-for="event in events"
            :key="event.id"
            :id="event.id"
            :start="event.start"
            :finish="event.finish"
            :topic="event.topic_id"
            :title="event.title"/>
<!--      </nuxt-link>-->
    </div>


    <div class="sidebar" v-show="true">
      <div class="add-topic" @click="showEventModal = true">
        <div class="plus">
          <span class="relative top-[-10px] noselect">+</span>
        </div>
      </div>

      <SimpleEvent
        v-for="event in freeEvents"
        :key="event.id"
        :title = "event.title"
        :id="event.id"
      />

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
      topics: [],
      showSideBar: false,
      selectedEvent: {},
      showTopicModal: false,
      showEventModal : false,
      freeEvents: []
    }
  },
  async mounted() {
    let localTimeStep = localStorage.getItem('timeStep')
    if (localTimeStep) {
      this.setTimeStep(parseInt(localTimeStep))
    }

    this.renderTimeline();

    this.events = await this.$post('events', {})
    this.topics = await this.$post('topics', {})
    this.freeEvents = await this.getFreeEvents()

    // cancel selecting event
    this.$refs.events.addEventListener('click', (event) => {
      this.selectEvent(NaN)
    })
    this.$refs.topics.addEventListener('click', (event) => {
      this.selectEvent(NaN)
    })
  },
  methods: {
    async $post(link, options) {
      options['JWT_TOKEN'] = this.$cookies.get('JWT_TOKEN')

      return await this.$axios.$post(this.url + link, options)
    },
    selectEvent(id) {
      this.$store.commit('setEvent', id)
    },
    setTimeStep(value) {
      this.$store.commit('setTimeStep', value)
    },
    async getEvent(id) {
      return await this.$axios.$post(this.url + 'event', {
        id: id
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
    },
    async getFreeEvents() {
      // return await this.$axios.$post(this.url + 'events', {
      //   'JWT_TOKEN' : this.$cookies.get('JWT_TOKEN'),
      //   'topic_id' : 0
      // })

      return await this.$post('events', {
        'topic_id' : 0
      })
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
    async '$store.state.selectedEvent'(newValue, oldValue) {
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
  @apply flex pl-[215px] border-b-2 border-[#e1dfdf] h-[30px];
  @apply bg-[#23272A] w-fit min-w-[100vw] relative top-[40px];
}

.events {
  height: calc(100vh - 200px);
  @apply w-fit min-w-[100vw] relative top-[40px]
}

.time-point {
  @apply w-[85px] font-bold text-[#e1dfdf] h-[40px];
}

.topics {
  @apply w-[200px] h-screen;
  @apply fixed top-[70px] bg-[#23272A] z-20
}

.topic {
  @apply px-2 py-4 h-[60px] border-b-2 border-[#e1dfdf] w-screen;
  @apply text-[#e1dfdf] font-bold;
}

.topic:hover {
  background: rgba(114, 137, 218, 0.5);
}

.add-topic {
  transition: all .25s ease;
  @apply w-[190px] mx-auto h-[60px] rounded-lg border-[#e1dfdf];
  @apply border-2 my-2 border-dotted pt-[5px] cursor-pointer text-[#e1dfdf];
}

.add-topic .plus {
  border-radius: 100%;
  @apply h-[45px] w-[45px] border-[#e1dfdf] border-2 mx-auto;
  @apply border-dotted text-center text-5xl font-bold;
}

.add-topic:hover {
  @apply bg-[#e1dfdf] text-[#23272A] border-[#23272A]
}

.sidebar {
  @apply fixed bg-[#23272A] h-[270px] bottom-0 z-30 w-screen;
  @apply border-t-2 border-[#e1dfdf] pt-1 text-[#e1dfdf];
  @apply grid grid-cols-7 justify-items-center;
}

.sidebar .side-title {
  @apply text-xl text-center;
  @apply block w-[95%] mx-auto;
}

.side-title:hover {
  @apply underline;
}

.sidebar .side-description {
  @apply h-[130px] w-[95%] mx-auto;
  @apply overflow-y-auto text-justify;
}

.side-description::-webkit-scrollbar {
  width: 0 !important;
}

</style>
