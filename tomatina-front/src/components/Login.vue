<template>
  <div>
    <md-layout md-gutter md-align="center">
      <md-layout md-flex-xsmall="100" md-flex-small="50" md-flex="33">
        <md-input-container>
          <label>Login</label>
          <md-input type="text" v-model="user.username" />
        </md-input-container>
      </md-layout>
    </md-layout md-gutter>
    <md-layout md-gutter md-align="center">
      <md-layout md-flex-xsmall="100" md-flex-small="50" md-flex="33">
        <md-input-container>
          <label>Passowrd</label>
          <md-input type="password" v-model="password"/>
        </md-input-container>
        <div>
          <md-button class="md-raised md-primary " v-on:click.native="doLogin"> login </md-button>
        </div>
      </md-layout>
    </md-layout md-gutter>
  </div>
</template>

<script>
  import UserService from '../services/user.service';
  import UserStatsService from '../services/user-stats.service';

  export default {
    name: 'login',
    methods:{
      doLogin: function() {
        var that = this;
        UserService.getUser(this.user.username)
          .then((user)=>{
            this.user.id = user.id;
            this.user.logged = true;
            this.user.teams = user.teams;
            this.$router.push('/dashboard');
          });
      }
    },
    props: ['user'],
    created(){

    },
    data() {
      return {
        password: ''
      };
    },
  };

</script>

<style scoped>

</style>
