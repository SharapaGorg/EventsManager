<template>
  <div class="form">
    <div class="form-content">

      <div v-show="isLoginPage">
        <div
          class="field-content"
          v-show="logInStep === 0"
        >
          <div class="field-header">Username</div>
          <div
            class="field-container"
          >
            <input
              class="field"
              placeholder="somebody.cool"
              spellcheck="false"
              type="text"
              v-model="loginLogin"
            />
          </div>
        </div>

        <div
          class="field-content"
          v-show="logInStep === 1"
        >
          <div class="field-header">Password</div>
          <div
            class="field-container"
          >
            <input
              class="field"
              placeholder="qwerty1234"
              spellcheck="false"
              type="password"
              v-model="loginPassword"
            />
          </div>
        </div>
      </div>

      <div v-show="!isLoginPage">
        <div
          class="field-content"
          v-show="signUpStep === 0"
        >
          <div class="field-header">Username</div>
          <div
            class="field-container"
          >
            <input
              class="field"
              placeholder="somebody.cool"
              spellcheck="false"
              type="text"
              v-model="signupLogin"
            />
          </div>
        </div>

        <div
          class="field-content"
          v-show="signUpStep === 1"
        >
          <div class="field-header">Password</div>
          <div
            class="field-container"
          >
            <input
              class="field"
              placeholder="qwerty1234"
              spellcheck="false"
              type="password"
              v-model="signupPassword"
            />
          </div>
        </div>

        <div
          class="field-content"
          v-show="signUpStep === 2"
        >
          <div class="field-header">Password again</div>
          <div
            class="field-container"
          >
            <input
              class="field"
              placeholder="qwerty1234"
              spellcheck="false"
              type="password"
              v-model="signupPassword"
            />
          </div>
        </div>
      </div>

      <div class="actions">
        <div
          class="back-button"
          @click="nextStep(true)"
          :style="{'background' : disableBackButton ? '#afa4a4' : '',
                    'color' : disableBackButton ? 'gray' : ''}"
        >
          Back
        </div>
        <div class="action-button" @click="nextStep(false)">Next</div>
      </div>
    </div>

    <div class="switchers">
      <div
        class="switcher"
        @click="isLoginPage = true"
        :style="{ 'border-color' : isLoginPage ? 'white' : 'transparent'}"
      >
        Login
      </div>

      <div class="text-white font-bold px-3 inline-block">|</div>

      <div
        class="switcher"
        @click="isLoginPage = false"
        :style="{ 'border-color' : !isLoginPage ? 'white' : 'transparent'}"
      >
        SignUp
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "authForm",
  data() {
    return {
      isLoginPage: true,
      logInStep: 0,
      signUpStep: 0,
      loginLogin: '',
      loginPassword: '',
      signupLogin: '',
      signupPassword: '',
      signupPasswordAgain: '',
      loginFields: [
        {
          id: 0,
          header: "Username",
          placeholder: "somebody.cool",
          type: "text"
        },
        {
          id: 1,
          header: "Password",
          placeholder: "qwerty1234",
          type: "password"
        }],
      signUpFields: [
        {
          id: 0,
          header: "Username",
          placeholder: "somebody.cool",
          type: "text"
        },
        {
          id: 2,
          header: "Password",
          placeholder: "qwerty1234",
          type: "password"
        },
        {
          id: 3,
          header: "Password again",
          placeholder: "qwerty1234",
          type: "password"
        }]
    }
  },
  computed: {
    disableBackButton() {
      if (this.isLoginPage) {
        return this.logInStep === 0
      } else {
        return this.signUpStep === 0
      }
    },
    url() {
      return this.$store.state.url
    }
  },
  methods: {
    async nextStep(reverse) {
      if (this.isLoginPage) {
        if (this.logInStep === this.loginFields.length - 1 && !reverse) {

          if (!(this.loginLogin && this.loginPassword)) {
            return
          }

          let loginAttempt = await this.loginUser()

          if (loginAttempt.status === 'SUCCESS') {
            this.$cookies.set("JWT", loginAttempt.token)
            this.setUser(this.loginLogin)
            await this.$router.replace('schedule')
          }
          else {
            alert(loginAttempt.message)
          }
          return
        }

        if (reverse && this.logInStep === 0) {
          return
        }

        this.logInStep += (reverse ? -1 : 1)
      } else {
        if (this.signUpStep === this.signUpFields.length - 1 && !reverse) {
          let signUpAttempt = await this.signUp()

          if (signUpAttempt.status === 'SUCCESS') {
            this.$cookies.set("JWT", signUpAttempt.token)
            await this.$router.replace('schedule')
          }
          else {
            alert(signUpAttempt.message)
          }
          return
        }

        if (this.signUpStep === 0 && reverse) {
          return
        }

        this.signUpStep += (reverse ? -1 : 1)
      }
    },
    async loginUser() {
      return await this.$axios.$post(this.url + 'login', {
        login: this.loginLogin,
        password: this.loginPassword
      })
    },
    async signUp() {
      return await this.$axios.$post(this.url + 'register', {
        login: this.signupLogin,
        password: this.signupPassword
      })
    },
    setUser(login) {
      this.$store.commit("setCurrentUser", login)
    }
  }
}
</script>

<style scoped>
.form {
  font-family: 'Ubuntu', sans-serif;
  background: url("https://i.gifer.com/hyE.gif") center;
  @apply h-[550px] w-[350px] rounded-md mx-auto bg-black;
  @apply pt-3 relative top-[100px];
}

.form-content {
  @apply w-4/5 mx-auto h-[490px];
}

.field-container {
  @apply w-full rounded-md px-2 py-1 bg-white ;
}

.field-header {
  /*color : #afa4a4;*/
  @apply text-white font-bold
}

.field {
  @apply w-full outline-none
}

.switchers {
  @apply w-fit mx-auto text-white font-bold;
}

.switcher {
  @apply inline-block cursor-pointer px-2 py-1 border-2 border-transparent;
  @apply rounded-md;
}

.switcher:hover {
  @apply underline
}

.actions {
  @apply w-fit float-right;
}

.back-button {
  @apply px-3 py-1 rounded-md font-bold text-white;
  @apply cursor-pointer w-fit mt-2 bg-blue-300 inline-block;
}

.action-button {
  @apply px-3 py-1 rounded-md bg-blue-600 font-bold text-white;
  @apply cursor-pointer w-fit mt-2 inline-block;
}
</style>
