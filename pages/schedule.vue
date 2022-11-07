<template>
  <div ref="schedule" class="events-window">

    <topic-modal
      v-show="showTopicModal"
      @closeTopicModal="showTopicModal=false"
    />

    <event-modal
      v-show="showEventModal"
      @closeEventModal="showEventModal = false"
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

    <div class="day-line">
      <img
        src="../static/arrow-left.svg"
        @click="changeDay(-1)"
      />

      <span>{{ currentDay }} {{ currentMonth }} / {{ currentYear }}</span>

      <img
        src="../static/arrow-left.svg"
        style="transform : rotate(180deg)"
        @click="changeDay(1)"
      />
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
        :title="event.title"
        :topic_number="topicNumber(event.topic_id)"
      />
      <!--      </nuxt-link>-->
    </div>


    <div class="sidebar" v-show="true">
      <div class="add-topic" @click="showEventModal = true">
        <div class="plus">
          <span class="relative top-[-10px] noselect">+</span>
        </div>
      </div>

      <div
        v-for="event in freeEvents"
        :key="event.id"
        class="free-event"
        id="yes-drop"
      >
        <SimpleEvent
          :title="event.title"
          :id="event.id"
        />
      </div>

<!--      <SimpleEvent-->
<!--        v-for="event in freeEvents"-->
<!--        :key="event.id"-->
<!--        :title="event.title"-->
<!--        :id="event.id"-->
<!--        class="free-event"-->
<!--      />-->

      <div
        v-for="event in freeEvents"
        :key="event.id"
        class="w-[150px] h-[60px] rounded-md bg-blue-500 free-event"
        id='yes-drop'
      >
        SOMETHING
      </div>

    </div>

  </div>
</template>

<script>

import interact from 'interactjs'

export default {
  name: "schedule",
  layout: 'base',
  data() {
    return {
      timePoints: [],
      events: [],
      topics: [],
      showSideBar: false,
      selectedEvent: {},
      showTopicModal: false,
      showEventModal: false,
      freeEvents: [],
      currentDate: new Date(),
      currentDay: 1,
      currentMonth: 1,
      currentYear: 2022,
      months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    }
  },
  async mounted() {
    let localTimeStep = localStorage.getItem('timeStep')
    if (localTimeStep) {
      this.setTimeStep(parseInt(localTimeStep))
    }
    this.changeDay(0)
    this.renderTimeline();

    await this.getEvents()
    this.topics = await this.$post('topics', {})
    this.freeEvents = await this.getFreeEvents()

    // cancel selecting event
    this.$refs.events.addEventListener('click', (event) => {
      this.selectEvent(NaN)
    })
    this.$refs.topics.addEventListener('click', (event) => {
      this.selectEvent(NaN)
    })

    let localDate = localStorage.getItem('selectedDate')
    if (localDate) {
      this.selectDate(localDate)
    }

    let base = this

    // enable draggables to be dropped into this (move events into topic)
    interact('.topic').dropzone({
      // only accept elements matching this CSS selector
      accept: '#yes-drop',
      // Require a 75% element overlap for a drop to be possible
      overlap: .75,

      // listen for drop related events:

      ondropactivate: function (event) {
        // add active dropzone feedback
        console.log('dropped')
        // event.target.classList.add('drop-active')
      },
      ondragenter: function (event) {
        let draggableElement = event.relatedTarget
        let dropzoneElement = event.target

        // feedback the possibility of a drop
        dropzoneElement.classList.add('drop-target')
        draggableElement.classList.add('can-drop')
        draggableElement.textContent = 'Dragged in'
      },
      ondragleave: function (event) {
        // remove the drop feedback style
        event.target.classList.remove('drop-target')
        event.relatedTarget.classList.remove('can-drop')
        event.relatedTarget.textContent = 'Dragged out'
      },
      ondrop: function (event) {
        event.relatedTarget.textContent = 'Dropped'
      },
      ondropdeactivate: function (event) {
        // remove active dropzone feedback
        event.target.classList.remove('drop-active')
        event.target.classList.remove('drop-target')
      }
    })

    interact('.free-event')
      .draggable({
        inertia: true,
        modifiers: [
          interact.modifiers.restrictRect({
            restriction: 'window',
            endOnly: true
          })
        ],
        autoScroll: true,
        // dragMoveListener from the dragging demo above
        listeners: {move: base.dragMoveListener}
      })
  },
  methods: {
    async $post(link, options) {
      options['JWT_TOKEN'] = this.$cookies.get('JWT_TOKEN')

      return await this.$axios.$post(this.url + link, options)
    },
    selectDate(date) {
      this.$store.commit('setSelectedTime', date)
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
    dragMoveListener(event) {
      let target = event.target
      // keep the dragged position in the data-x/data-y attributes
      let x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx
      let y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy

      // translate the element
      target.style.transform = 'translate(' + x + 'px, ' + y + 'px)'

      // update the position attributes
      target.setAttribute('data-x', x)
      target.setAttribute('data-y', y)
    }
    ,
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
    }
    ,
    changeDay(sign) {
      let date = this.$store.state.selectedDate
      this.currentDate = date

      this.currentDate.setDate(this.currentDate.getDate() + sign)

      this.currentDay = this.currentDate.getDate()
      this.currentMonth = this.months[this.currentDate.getMonth()]
      this.currentYear = this.currentDate.getFullYear()

      this.selectDate(this.currentDate)

      // rerender events
    }
    ,
    editTimeStep(step) {
      if (this.timeStep + step <= 0 || this.timeStep + step > 60 * 60 * 2) {
        return
      }

      localStorage.setItem('timeStep', this.timeStep + step)
      this.setTimeStep(this.timeStep + step)
    }
    ,
    async getFreeEvents() {
      return await this.$post('events', {
        date: `${this.currentDay}/${this.months.indexOf(this.currentMonth) + 1}/${this.currentYear}`,
        topic_id: 0
      })
    }
    ,
    async getEvents() {
      this.events = await this.$post('events', {
        date: `${this.currentDay}/${this.months.indexOf(this.currentMonth) + 1}/${this.currentYear}`
      })
    }
  },
  computed: {
    topicNumber() {
      return (topic_id) => {
        return this.topics.indexOf(this.topics.find(x => x.id === topic_id))
      }
    }
    ,
    timeStep() {
      return this.$store.state.timeStep
    }
    ,
    url() {
      return this.$store.state.url
    }
    ,
  }
  ,
  watch: {
    '$store.state.timeStep'(newValue, oldValue) {
      this.renderTimeline()
    }
    ,
    async currentDay(value) {
      await this.getEvents()
    }
    ,
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

.day-line {
  @apply h-[30px] w-screen bg-[#23272A] relative top-[40px];
  @apply border-b-2 border-[#e1dfdf] text-center font-bold;
  @apply text-[#e1dfdf] flex;
}

.day-line img {
  @apply w-[22px] h-[22px] relative top-[3px] cursor-pointer;
}

.day-line span {
  @apply block mx-auto w-[90%] text-center;
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
  @apply fixed top-[100px] bg-[#23272A] z-20
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
