<template>
  <div class="test">

    <label>
      Название всего этого
      <input type="text" v-model="title"></input>
    </label>

    <label>
      Показывать имя
      <input type="checkbox" v-model="showFirstName"></input>
    </label>

    <br/>
    <h1>{{title}}</h1>
    <span v-html="title"></span>
    <p v-if="showFirstName">{{user.firstName}}</p>
    <p v-else>Имя скрыто</p>
    <p v-text="user.lastName"></p>
    <ul>
      <li v-for="item in items">{{item.title}}</li>
    </ul>
    <button v-on:click="greet('Hello world!')">Say hello</button>
    <label><input
      type="text"
      v-on:keypress="keyUp"
      v-on:keypress.enter="hitEnter">
    </input></label>

    <label><input type="text" v-model="user.firstName"></input></label>
    <label><input type="text" v-model="user.lastName"></input></label>

    <p>{{fullName}}</p>
    <h2>{{msg}}</h2>
  </div>
</template>

<script>
  export default {
    name: "test",

    props: {
      msg: {
        type: String,
        default: "Foobar"
      }
    },

    data() {
      return {
        title: " Hello, bla-bla",
        user: {
          firstName: "Dmitriy",
          lastName: "Yampolskiy"
        },
        showFirstName: false,
        items: [
          {title: "item1"},
          {title: "item2"},
          {title: "item3"},
        ]
      }
    },

    methods: {
      greet: s => alert(s),
      keyUp: e => console.log(e.target.value),
      hitEnter: () => console.log('Enter hit'),
    },

    computed: {
      fullName: function () {
        return this.user.firstName + ' ' + this.user.lastName
      }
    }
  }
</script>

<style scoped>
  .test {
    background-color: #7D9029;
  }
</style>
