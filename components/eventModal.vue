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
      startHoursTime : 1,
      startMinutesTime : 30,
      finishHoursTime : 1,
      finishMinutesTime : 30,
      topics : [{
        id : 0,
        title : "Не выбрано"
      }]
    }
  },
  async mounted() {
    let topics = await this.$post('topics', {})

    for (let elem of topics) {
      this.topics.push(elem)
    }

    console.log(this.topics)
  },
  methods: {
    async $post(link, options) {
      options['JWT_TOKEN'] = this.$cookies.get('JWT_TOKEN')

      return await this.$axios.$post(this.url + link, options)
    },
    addEvent() {
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
    }
  },
  computed: {
    url() {
      return this.$store.state.url
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
