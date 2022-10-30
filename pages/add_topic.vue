<template>
  <div class="add-topic-card">

    <div class="existed-topics">
      <div
        class="existed-topic"
        v-for="topic in topics"
        :key="topic.id"
      >
        {{ topic.title }}
      </div>
    </div>

    <div class="w-fit mx-auto flex mb-1">
      <span>Название</span>
      <input class="topic-field" placeholder="Игры" v-model="topicTitle"/>
    </div>

    <div class="w-[450px] mx-auto" v-if="showWarning && topicTitle === ''">
      <div class="warning">Обязательно введите название раздела!</div>
    </div>

    <div class="w-[450px] grid grid-cols-2 justify-items-end w-fit mx-auto" @click="addTopic">
      <div class="add-button col-start-2">Добавить</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "add_topic",
  data() {
    return {
      topicTitle: '',
      showWarning: false,
      topics: []
    }
  },
  async mounted() {
    this.topics = await this.getTopics()

      console.log(this.topics)
  },
  methods: {
    async getTopics() {
      return await this.$axios.$post(this.url + 'topics', {
        'JWT_TOKEN' : this.$cookies.get('JWT_TOKEN')
      })
    },
    async addTopic() {
      if (!this.topicTitle) {
        this.showWarning = true
        return
      }
      await this.$axios.$post(this.url + 'add_topic', {
        'JWT_TOKEN' : this.$cookies.get('JWT_TOKEN'),
        'title' : this.topicTitle
      })
      this.topicTitle = ''
      this.topics = await this.getTopics()
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

.add-topic-card {
  @apply w-[600px] px-4 py-3 relative top-[70px] mx-auto;
  @apply bg-[#23272A] rounded-md
}

.add-topic-card span {
  @apply w-[100px] text-[#e1dfdf] font-bold text-center;
  @apply inline-block pt-1;
}

.topic-field {
  @apply px-2 py-1 outline-none rounded-md w-[350px] bg-[#e1dfdf];
}

.add-button {
  @apply px-2 py-1 rounded-md bg-[#7289DA] text-white;
  @apply w-fit font-bold mt-1 cursor-pointer;
}

.existed-topics {
  @apply w-[450px] max-h-[400px] overflow-y-auto text-[#e1dfdf];
  @apply mb-2 mx-auto;
}

.existed-topic {
  @apply px-2 py-2 font-bold border-2 border-[e1dfdf] rounded-md;
  @apply text-center overflow-hidden;
}

</style>
