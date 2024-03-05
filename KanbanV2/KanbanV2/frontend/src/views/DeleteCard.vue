<template>
    <div class="app">
        <h1 align="center">
        Card Deleted Successfully! Click <a href="/lists/{{id}}">Here</a> to go back to your lists!
        </h1>
    </div>
  </template>

<script>
import { useRouter } from 'vue-router'
import axios from 'axios'
export default {
  Name: 'DeleteCard',
  data () {
    return {
      id: this.$route.params.id
    }
  },
  created () {
    const router = useRouter()
    const path = 'http://localhost:5000/cards/delete/' + this.id
    axios.get(path)
      .then((resp) => {
        console.log(resp.data)
        router.push({ name: 'Cards', params: { id: localStorage.id } })
        alert('Card Deleted!')
      })
      .catch((err) => console.log(err.response))
  }

}
</script>

  <style>

  </style>
