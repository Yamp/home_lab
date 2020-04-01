// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import vueResource from 'vue-resource'
import VueRouter from 'vue-router'
import Vuex from 'vuex'

import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.css";
import Users from "./components/Users";
import Test from "./components/Test";
import HelloWorld from "./components/HelloWorld";

// import routes from "./route";
// import rawDisplayer from "./components/infra/raw-displayer.vue";
// import ElementUI from "element-ui";
// import store from "./store";
// import App from './App'

Vue.config.productionTip = false

Vue.use(vueResource)
Vue.use(VueRouter)
Vue.use(Vuex)


// VUEX
const store = new Vuex.Store({
  state: {
    message: 'Hello from vuex!',
    count: 0,
  },
  mutations: {},
  actions: {},
  getters: {}
})

// Роутер
const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes: [
    {path: '/', component: Users},
    {path: '/test', component: Test},
    {path: '/hello_world', component: HelloWorld},
  ]
});

// Основной компонент VUE
new Vue({
  router,
  template: `
    <div id="app">
      <ul>
        <li><router-link to="/">Users</router-link></li>
        <li><router-link to="/test">Test</router-link></li>
        <li><router-link to="/hello_world">Hello World</router-link></li>
      </ul>
      <router-view></router-view>
    </div>
  `,
}).$mount('#app')
