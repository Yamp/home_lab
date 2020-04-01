<template>
  <div class="users">
    <h1>Users</h1>
    <draggable
      v-model="users"
      tag="ul"

    >
      <div v-for="user in users">
        <transition-group type="transition" name="flip-list">
          <label :class="{contacted: user.contacted}">
            <input type="checkbox" v-model="user.contacted"/>
            <span>{{user.name}}: {{user.email}}</span>
            <button v-on:click="deleteUser(user)">x</button>
          </label>
        </transition-group>
      </div>
    </draggable>
    <form v-on:submit="addUser">
      <input type="text" placeholder="Введите имя" v-model="newUser.name"/>
      <input type="text" placeholder="Введите email" v-model="newUser.email"/>
      <input type="submit" value="Create user"></input>
    </form>
  </div>
</template>

<script>
  import draggable from 'vuedraggable'

  export default {
    name: "users",
    display: "Users",

    components: {
      draggable
    },

    data() {
      return {
        newUser: {
          name: "",
          email: ""
        },
        users: []
      }
    },

    methods: {
      addUser: function (e) {
        this.users.push({
          name: this.newUser.name,
          email: this.newUser.email,
          contacted: false,
        });
        e.preventDefault();
      },
      deleteUser: function (user) {
        this.users.splice(this.users.indexOf(user), 1)
      },
    },

    created: function () {
      console.log('Running created!!!!!!!!!');
      this.$http.get('https://jsonplaceholder.typicode.com/users')
        .then((response) => {
          this.users = response.data
          console.log(response.data())
        });
    },
  }
</script>

<style scoped>
  .users {
    background-color: #c8ebfb;
  }

  .contacted {
    text-decoration: line-through;
  }

  label {
    background-color: #B0FFB0;
  }
</style>
