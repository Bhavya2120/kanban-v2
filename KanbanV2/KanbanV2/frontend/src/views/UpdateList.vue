<template>

    <h1 text-align: center>Update List</h1>
    <form @submit.prevent="submit" style="margin-right: 150px;margin-top: 29px; margin-left: 150px" method="POST">
        <div class="form-group">
          <label for="title">Enter the list name:</label>
          <input type="name" class="form-control" v-model="data.list_name" name="Name" placeholder="New List Name"  required>
          <br/>
          </div>

        <button type="submit" class="btn btn-outline-dark"  style="border-radius: 15px;">submit</button>
      </form>
</template>

<script>
import { reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
export default {
  Name: 'UpdateCard',
  data () {
    return {
      list_id: this.$route.params.list_id,
      items: []
    }
  },
  mounted () {
    localStorage.setItem('list_id', this.list_id)
    axios.get('http://localhost:5000/lists/update/' + this.list_id)
      .then((resp) => {
        this.items = resp.data
      })
      .catch((err) => {
        console.log(err.resp)
      })
  },
  setup () {
    const router = useRouter()
    const data = reactive({
      list_name: ''
    })

    const submit = async () => {
      await fetch('http://localhost:5000/lists/update/' + localStorage.list_id, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        body: JSON.stringify(data)
      }).then(resp => resp.json())
        .then(data => {
          console.log(data)
          alert('List Name Updated!')
        })
        .catch(error => {
          alert('Error Occurred: ' + error)
        })
      await router.push('/lists/' + localStorage.id)
    }
    return {
      data,
      submit
    }
  }
}
</script>

<style>

</style>
