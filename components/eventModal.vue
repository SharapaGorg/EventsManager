<template>
  <div class="topic-wrapper">
    <div class="add-topic-card">


      <div class="field">
        <span>Название</span>
        <input class="topic-field" placeholder="Турнир по ничегонеделанию" v-model="title"/>
      </div>

      <div class="w-[450px] mx-auto" v-if="showWarningTitle && title === ''">
        <div class="warning">Обязательно введите название события!</div>
      </div>

      <div class="field">
        <span>Ссылка</span>
        <input class="topic-field" placeholder="https://radolyn.com" v-model="link"/>
      </div>

      <div class="w-[450px] mx-auto" v-if="showWarningLink && link === ''">
        <div class="warning">Пожалуйста, введите ссылку на событие!</div>
      </div>

      <div class="field">
        <span>Описание</span>
        <input class="topic-field" placeholder="Что-нибудь" v-model="desc"/>
      </div>

      <div class="time-header">Время события</div>

      <div class="w-[450px] mx-auto mt-1 mb-3">
        <span>Начало</span>
        <input
          placeholder="12"
          class="time-field"
          type="number"
          v-model="startHoursTime"
        />
        <input
          placeholder="30"
          class="time-field"
          type="number"
          v-model="startMinutesTime"
        />
        <br/>
        <span>Конец</span>
        <input
          placeholder="12"
          class="time-field"
          type="number"
          v-model="finishHoursTime"
        />
        <input
          placeholder="30"
          class="time-field"
          type="number"
          v-model="finishMinutesTime"
        />
      </div>

      <Dropdown
        :workers="topics"
        :worker="topics[0]"
        class="mx-auto"
      />

      <div class="w-[450px] grid grid-cols-2 justify-items-end w-fit mx-auto">
        <div class="col-start-2 mt-2">
          <div class="add-button" @click="$emit('closeEventModal')">Закрыть</div>
          <div class="add-button" @click="addEvent">Добавить</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "topicModal",
  data() {
    return {
      title: '',
      link : '',
      showWarningTitle: false,
      showWarningLink : false,
      desc : '',
      startHoursTime : 1,
      startMinutesTime : 30,
      finishHoursTime : 1,
      finishMinutesTime : 30,
      topics : [{
        id : 0,
        title : "Не выбрано"
      }],
      months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    }
  },
  async mounted() {
    let topics = await this.$post('topics', {})

    for (let elem of topics) {
      this.topics.push(elem)
    }
  },
  methods: {
    async $post(link, options) {
      options['JWT_TOKEN'] = this.$cookies.get('JWT_TOKEN')

      return await this.$axios.$post(this.url + link, options)
    },
    async addEvent() {
      // validation fields
      if (!this.title) {
        this.showWarningTitle = true
      }
      if (!this.link) {
        this.showWarningLink = true
      }

      if (!this.title || !this.link || !this.startMinutesTime || !this.startHoursTime || !this.finishHoursTime || !this.finishMinutesTime) {
        return
      }

      let date = `${this.selectedDate.getDate()}/${this.selectedDate.getMonth() + 1}/${this.selectedDate.getFullYear()}`
      let start = new Date();
      let finish = new Date();

      start.setHours(this.startHoursTime)
      start.setMinutes(this.startMinutesTime)
      start.setSeconds(0)

      finish.setHours(this.finishHoursTime)
      finish.setMinutes(this.finishMinutesTime)
      finish.setSeconds(0)

      await this.$post('add_event', {
        title : this.title,
        link : this.link,
        description : this.desc,
        start : start.getTime() / 1000,
        finish : finish.getTime() / 1000,
        topic_id : this.selectedTopic,
        date : date
      })

      this.resetForm()
    },
    resetForm() {
      this.title = ''
      this.link = ''
      this.desc = ''
      this.startHoursTime = 1
      this.startMinutesTime = 30
      this.finishHoursTime = 2
      this.finishMinutesTime = 30
      this.$store.commit('setSelectedTopic', 0)
    }
  },
  computed: {
    url() {
      return this.$store.state.url
    },
    selectedTopic() {
      return this.$store.state.selectedTopic
    },
    selectedDate() {
      return this.$store.state.selectedDate
    }
  }
}
</script>

<style scoped>

.topic-wrapper {
  background : rgba(0, 0, 0, .5);
  @apply w-screen h-screen fixed z-[100]
}

.add-topic-card {
  @apply w-[600px] px-4 py-3 relative top-[70px] mx-auto;
  @apply bg-[#23272A] rounded-md border-2 border-[#7289DA];
}

.add-topic-card span {
  @apply w-[100px] text-[#e1dfdf] font-bold text-center;
  @apply inline-block pt-1;
}

.topic-field {
  @apply px-2 py-1 outline-none rounded-md w-[350px];
}

.add-button {
  @apply px-2 py-1 rounded-md bg-[#7289DA] text-white;
  @apply w-fit font-bold cursor-pointer inline;
}

.field {
  @apply w-fit mx-auto flex mb-1
}

.time-header {
  @apply w-full block mx-auto text-center;
  @apply text-[#e1dfdf]
}

.time-field {
  @apply w-[50px] rounded-sm px-1
}

</style>
