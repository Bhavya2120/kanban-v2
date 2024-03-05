<template>
    <div class="app">
      <a href="/lists/{{id}}"><h4 align="left">Back to Your Lists</h4></a>
    </div>
  </template>

<script>
import { useRouter } from 'vue-router'
import axios from 'axios'
export default {
  Name: 'DeleteList',
  data () {
    return {
      id: this.$route.params.id
    }
  },
  created () {
    const router = useRouter()
    const path = 'http://localhost:5000/lists/delete/' + this.id
    axios.get(path)
      .then((resp) => {
        console.log(resp.data)
        router.push({ name: 'Lists', params: { id: localStorage.id } })
        alert('List Deleted!')
      })
      .catch((err) => console.log(err.response))
  }

}
</script>

  <style>

  </style>
