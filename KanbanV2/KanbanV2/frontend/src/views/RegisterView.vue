<template>
    <h1 align="center"> Welcome to KanBanV2</h1><br/>
    <form class="form-signin" @submit.prevent="submit"  style="margin-left:150px;margin-right:250px;">
   <h2 align="center">Please Register</h2>
   <br/><br/>

   <input v-model="data.name" class="form-control" placeholder="Name" required>
<br/><br/>
   <input v-model="data.mail" type="email"  class="form-control" placeholder="Email address" required autofocus>
<br/><br/>
   <input v-model="data.password" type="password"  class="form-control" placeholder="Password" required><br/><br/>
   <button class="btn btn-lg btn-outline-dark" style="margin-left: 75px;" type="submit">Submit</button>
    </form>
    <br/><br/>
    Existing User? Click the below button!<br/><br/>

    <router-link to="login"><button class="btn btn-outline-dark" id="login">Login</button></router-link>
 </template>

<script>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

export default {
  Name: 'RegisterView',
  setup () {
    const data = reactive({
      name: '',
      mail: '',
      password: ''
    })
    const router = useRouter()
    const submit = async () => {
      await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      alert('Redirecting to Login')
      await router.push('/login')
    }

    return {
      data,
      submit

    }
  }
}
</script>
