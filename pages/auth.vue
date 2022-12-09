<template>
  <auth-form/>
</template>

<script>
export default {
  name: "auth",
  async mounted() {
    if (this.$cookies.get('JWT')) {
        await this.$router.replace('/account')
    }
  }
}
</script>

<style scoped>

.auth-card {
  @apply w-1/3 rounded-md bg-[#23272A] mx-auto text-[#e1dfdf] px-2 py-3;
}

.field {
  @apply outline-none px-2 py-1 rounded-sm;
}

</style>
