<template>
  <div class="event-card">
    <div class="title">{{ event.title }}</div>
    <div class="division-line"></div>
    <div class="description">{{ event.description }}</div>
    <div class="division-line"></div>

    <div class="link">Ссылка:</div>
    <a :href="event.link">{{ event.link }}</a>
    <div>{{ start }}</div>
    <div>{{ finish }}</div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      event: {},
      start : '',
      finish : '',
      defaultDesc : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    }
  },
  async mounted() {
    let params = this.$route.params

    this.event = await this.$axios.$post(this.url + 'event', {
      id: params.id
    })
    this.start = new Date(this.event.start * 1000)
    this.finish = new Date(this.event.finish * 1000)
  },
  computed: {
    url() {
      return this.$store.state.url
    }
  }
}

</script>

<style scoped>

.event-card {
  @apply rounded-md bg-[#23272A] w-1/3 mx-auto text-[#e1dfdf];
  @apply px-5 py-5 relative top-[70px]
}

.event-card .title {
  @apply font-bold text-xl text-center
}

.division-line {
  @apply border-b-2 border-[#e1dfdf] w-[90%] mx-auto my-1;
}

.event-card .description {
  @apply py-1 text-justify mx-4 max-h-[400px];
  @apply overflow-y-auto;
}

.event-card .link {
  @apply font-bold ml-10 inline;
}

.event-card a {
  @apply text-blue-500
}

</style>
