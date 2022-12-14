export default {
  target : 'static',
  ssr : false,
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'EventManager',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {rel : 'stylesheet', href : 'https://fonts.googleapis.com/css?family=Libre+Franklin:400,700&subset=latin'}
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '@/assets/css/main.css',
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/axios',
    'cookie-universal-nuxt'
  ],
  axios: {
    // proxy: true
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  },
  router: {
    base: '/EventsManager/'
  }
}
