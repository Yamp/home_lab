<template>
  <div id="app">
    <img src="./assets/logo.png" alt="vue_img">
    <users></users>
    <test msg="Param msg"></test>
<!--    <draggable/>-->
  </div>
</template>

<script>
import Test from "./components/Test";
import HelloWorld from './components/HelloWorld'
import Users from './components/Users'
import draggable from 'vuedraggable'

export default {
  name: 'App',
  components: {
    Users,
    HelloWorld,
    Test,
    draggable,
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
