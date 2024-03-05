<template>
    <div id="app">
       <h1 class="header"> Welcome to KanBanV2</h1><br/><br/><br/>
       <body>
       <div id="form">
           <form class="form-signin" @submit.prevent="submit">
      <div class="container">
        <br>
      <h2>Please sign in</h2><br/>
      <input type="email" v-model="data.mail"  class="form-control" placeholder="Email address" required>

      <input type="password" v-model="data.password" class="form-control" placeholder="Password" required>
      </div>
      <br/><br/>
      <button class="btn btn-outline-dark" type="submit">Sign in</button><br/><br/>
    </form>
       </div>
       <br>
       <p class="or">If you are new, Register using the button below</p>
      <router-link to="register"><button class="btn btn-outline-dark" id="reg">Register</button></router-link>
       </body>
       </div>
    </template>

<script>
import { reactive } from 'vue'
import setAuthHeader from '@/utils/AuthHeader'
import { useRouter } from 'vue-router'

export default {
  Name: 'LoginView',

  setup () {
    const data = reactive({
      mail: '',
      password: ''
    })
    const router = useRouter()
    const submit = async () => {
      await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        body: JSON.stringify(data)
      }).then(resp => resp.json())
        .then(data => {
          console.log(data)
          localStorage.setItem('access_token', data.access_token)
          localStorage.setItem('id', data.id)
          localStorage.setItem('name', data.name)

          setAuthHeader(data.access_token)
          router.push('/lists/' + localStorage.id)
        })
        .catch(error => {
          if (error) {
            router.push({ name: 'Login' })
            alert('Wrong Password, Please try again')
          }
        })
    }
    return {
      data,
      submit
    }
  }
}

</script>

<style>
#form{
  animation: 10000ms ease-in-out infinite color-change;
}

@keyframes color-change {
  0% {
    background-color: teal;
  }
  20% {
    background-color: gold;
  }
  40% {
    background-color: indianred;
  }
  60% {
    background-color: violet;
  }
  80% {
    background-color: green;
  }
  100% {
    background-color: teal;
  }
}

</style>
