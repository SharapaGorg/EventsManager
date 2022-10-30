<template>
  <div ref="root" class='relative top-[70px]'>
    Index page

    <dropdown
      :worker="topics[0]"
      :workers="topics"
    />
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  data() {
    return {
      topics : [
        {
          id : 1,
          title: "Что-нибудь"
        }
      ]
    }
  },
  async mounted() {
    this.topics = await this.$axios.$post(this.url + 'topics', {
      'JWT_TOKEN' : this.$cookies.get('JWT_TOKEN')
    })

    console.log(this.topics)
  },
  computed: {
    url() {
      return this.$store.state.url
    }
  }
}
</script>

<style>



</style>
