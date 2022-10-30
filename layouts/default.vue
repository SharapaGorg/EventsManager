<template>
  <div>
    <nav>
      <div
        class="account"
        @click="activateAccButton"
      >
        <div v-show="user">{{ user }}</div>
        <nuxt-link to="/auth" v-show="!user">
          <div>Войти</div>
        </nuxt-link>
      </div>

      <div class="account-menu" v-show="showMenu">
        <nuxt-link to="/account">
          <div class="menu-section">Профиль</div>
        </nuxt-link>

        <nuxt-link to="/schedule">
          <div class="menu-section">Расписание</div>
        </nuxt-link>

        <div class="menu-section" @click="logOut">Выйти</div>
      </div>

    </nav>
    <nuxt @click.native="showMenu = false"/>
  </div>
</template>

<script>
export default {
  name: "default",
  data() {
    return {
      user: {},
      showMenu: false
    }
  },
  async mounted() {
    let user = await this.$axios.$post(this.url + 'user', {
      'JWT_TOKEN': this.$cookies.get("JWT_TOKEN")
    })
    this.user = user.login
    this.$store.commit('setCurrentUser', this.user)
  },
  methods: {
    async logOut() {
      this.$cookies.remove('JWT_TOKEN')
      await this.$router.replace('/auth')

      this.user = ''
      this.showMenu = false
      this.$store.commit('setCurrentUser', '')
    },
    async activateAccButton() {
      if (this.user) {
        console.log(this.user)
        this.showMenu = !this.showMenu
      }
    }
  },
  watch: {
    '$store.state.currentUser'(value) {
      this.user = value
      console.log(this.user, value)
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

nav {
  @apply w-screen h-[40px] bg-[#23272A] border-b-2 border-[#e1dfdf];
  @apply text-[#e1dfdf] pb-1 fixed z-50;
}

.account {
  @apply fixed right-[10px] cursor-pointer px-3 py-2 font-bold;
}

.account-menu {
  @apply w-[150px] rounded-md bg-[#23272A] text-[#e1dfdf] z-50;
  @apply fixed right-[10px] top-[35px] border-2 border-[#e1dfdf]
}

.menu-section {
  @apply px-3 py-1 cursor-pointer;
}

.menu-section:hover {
  transition: all .25s ease;
  @apply bg-[#e1dfdf] text-[#23272A]
}

.account:hover {
  @apply underline
}


</style>
