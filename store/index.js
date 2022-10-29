export const state = () => ({
  url : 'http://127.0.0.1:5000/',
  timeStep : 900 // 15 minutes
})

export const mutations = {
  setTimeStep(state, value) {
    state.timeStep = value
  }
}
