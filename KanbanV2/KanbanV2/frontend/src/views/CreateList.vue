<template>
    <a href="/lists/{{id}}"><h4 align="left">Back to Your Lists</h4></a>

    <h1 style="text-align: center;">Create a New List</h1>
    <body>
    <form @submit.prevent="submit" style="margin-right: 522px;margin-top: 29px; margin-left: 519px" method="POST" action='/list/{{name}}/create'>
        <div class="form-group">
            <br/><br/>
          <label for="listName"><h5>List Name:</h5></label><br/><br/>
          <input type="name" v-model="data.listname" class="form-control" placeholder="Enter list name" required>
        </div>
        <br/><br/><br/>
            <button type="submit" class="btn btn-outline-dark">Create List</button>
      </form>
      </body>
</template>

<script>
import { useRouter } from 'vue-router'
import { reactive } from 'vue'
export default {
  Name: 'CreateList',

  setup () {
    const data = reactive({
      listname: ''
    })
    const router = useRouter()
    const submit = async () => {
      await fetch('http://localhost:5000/createlist/' + localStorage.id, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        body: JSON.stringify(data)
      }).then(resp => resp.json())
        .then(data => {
          console.log(data)
        })
        .catch(error => { console.log(error) })
      alert('List Created Successfully!')
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
    body {
    background: linear-gradient(315deg, #23a6d5 23%, #b1b0cf 76%);
    background-size: 100% 100%;
    animation: gradient 15s ease infinite;
    height: 100vh;
  }

  @keyframes gradient {
    0% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
    100% {
      background-position: 0% 50%;
    }
  }
</style>
