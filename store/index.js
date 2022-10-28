export const state = () => ({
  timeStep : 900 // 15 minutes
})

export const mutations = {
  setTimeStep(state, value) {
    state.timeStep = value
  }
}
