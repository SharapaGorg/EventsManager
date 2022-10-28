<template>
  <div ref="schedule">
    <div class="scale-menu">
      <div class="scale-button">
        <span>+</span>
      </div>
      <div class="scale-button">
        <span>-</span>
      </div>
    </div>

    <div class="timeline"></div>
  </div>
</template>

<script>
export default {
  name: "events",
  data() {
    return {
        timePoints: []
    }
  },
  mounted() {
      this.renderTimeline();
      console.log(this.timePoints)
  },
  methods: {
    renderTimeline() {
      let day = 60 * 60 * 24
      let timePoints = []

      let currentPoint = 0;
      while (currentPoint <= day) {
          let time = new Date(currentPoint * 1000)
          console.log(time)

          timePoints.push(currentPoint)
          currentPoint += this.timeStep
      }

      this.timePoints = timePoints
    },
    editTimeStep(step) {
        if (this.timeStep + step <= 0) {
          alert('Неа')
          return
        }

        this.$store.commit('setTimeStep', this.timeStep + step)
    }
  },
  computed: {
    timeStep() {
      return this.$store.state.timeStep
    }
  },
  watch: {
    '$store.state.timeStep': (oldValue, newValue) => {
      console.log(newValue)
    }
  }
}
</script>

<style scoped>

.scale-menu {
  @apply flex py-1 px-2 mx-auto w-fit py-3;
}

.scale-button {
  @apply px-2 py-1 rounded-lg w-fit cursor-pointer text-white;
  @apply font-bold border-2 border-white w-[50px] text-center mx-3;
  @apply text-2xl
}

.scale-button:hover {
  transition : all .25s ease;
  @apply bg-white text-[#3C3F41];
}

.scale-button span {
  @apply relative top-[-3px]
}

</style>
