export const state = () => ({
  url : 'http://127.0.0.1:5000/',
  timeStep : 900, // 15 minutes
  selectedEvent : NaN,
  currentUser : '',
  selectedDate : new Date() // day/month/year
})

export const mutations = {
  setTimeStep(state, value) {
    state.timeStep = value
  },
  setEvent(state, value) {
    state.selectedEvent = value
  },
  setCurrentUser(state, value) {
    state.currentUser = value
  },
  setSelectedTime(state, value) {
    state.selectedDate = value
  }
}
