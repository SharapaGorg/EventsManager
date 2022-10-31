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
      showWarningLink : false
    }
  },
  async mounted() {
  },
  methods: {
    addEvent() {
      // validation fields
      if (!this.title) {
        this.showWarningTitle = true
      }
      if (!this.link) {
        this.showWarningLink = true
      }

      if (!this.title || !this.link) {
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
  @apply px-2 py-1 outline-none rounded-md w-[350px] bg-[#e1dfdf];
}

.add-button {
  @apply px-2 py-1 rounded-md bg-[#7289DA] text-white;
  @apply w-fit font-bold cursor-pointer inline;
}

.field {
  @apply w-fit mx-auto flex mb-1
}

</style>
