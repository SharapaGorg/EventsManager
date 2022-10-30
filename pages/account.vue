<template>
  <div class="profile">{{ login }}</div>
</template>

<script>
export default {
  name: "account",
  data() {
    return {
      login: ''
    }
  },
  mounted() {
    this.login = this.$store.state.currentUser

    setTimeout(async () => {
      if (!this.login) {
        await this.$router.replace('/auth')
      }
    }, 1000)
  },
  watch: {
    '$store.state.currentUser'(value) {
      this.login = value
    }
  }
}
</script>

<style scoped>

.profile {
  @apply relative top-[50px] w-fit mx-auto text-xl font-bold;
  @apply text-[#e1dfdf] px-3 py-2 border-2 border-[#e1dfdf];
  @apply rounded-lg
}

</style>
