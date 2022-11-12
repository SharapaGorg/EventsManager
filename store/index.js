export const state = () => ({
  url: 'http://127.0.0.1:5000/',
  // url : 'https://185.231.153.104:4002/',
  timeStep: 900, // 15 minutes
  selectedEvent: NaN,
  currentUser: '',
  selectedDate: new Date(), // day/month/year,
  selectedTopic : 0,
  topics : [],
  events: []
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
  },
  setSelectedTopic(state, value) {
    state.selectedTopic = value
  },
  setTopics(state, value) {
    state.topics = value
  },
  setEvents(state, value) {
    state.events = value
  }
}

export const getters = {
  getDate: (state) => {
    return state.selectedDate
  }
}
