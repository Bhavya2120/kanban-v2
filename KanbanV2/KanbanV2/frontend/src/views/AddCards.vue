<template>
<a href="/lists/{{id}}"><h4 align="left">Back to Your Lists</h4></a>
    <h1 text-align: center>Add Cards to the List</h1>
    <form @submit.prevent="submit" style="margin-right: 150px;margin-top: 29px; margin-left: 150px" method="POST">
        <div class="form-group">
          <label for="title">Enter the card title:</label>
          <input type="name" class="form-control" v-model="data.card_title" name="Title" placeholder="Title" required>
          <br/>
          <label for="content">Enter the card content:</label>
            <textarea class="form-control" v-model="data.card_content" id="content" name="content" placeholder="Content"></textarea>
           <br/>
            <label for="complete">Card Completion Status(Drag slider to the left for Complete, right for Not Complete):</label>
            <input v-model="data.card_complete" type="range" name="Complete" id="Complete" min="0" max="1">
            <br/><br/>
            <label for="complete_date">Date of Completion of Card: </label>
            <input v-model="data.card_complete_date" id="complete_date" name="complete_date" type="date">
            <label for="deadline">Card Deadline: </label>
            <input v-model="data.card_deadline" id="deadline" name="deadline" type="date" required>
            <br/><br/>
          </div>

        <button type="submit" class="btn btn-outline-dark"  style="border-radius: 15px;">submit</button>
      </form>
</template>

<script>
import { reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
export default {
  Name: 'AddCards',
  data () {
    return {
      list_user: this.$route.params.list_user,
      list_id: this.$route.params.list_id,
      items: []
    }
  },
  mounted () {
    localStorage.setItem('list_user', this.list_user)
    localStorage.setItem('list_id', this.list_id)
    axios.get('http://localhost:5000/addcard/' + this.list_id)
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
      title: '',
      content: '',
      card_complete: '',
      card_complete_date: '',
      card_deadline: ''
    })

    const submit = async () => {
      await fetch('http://localhost:5000/addcard/' + localStorage.list_id, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        body: JSON.stringify(data)
      }).then(resp => resp.json())
        .then(data => {
          console.log(data)
          alert('This card has been added to your list successfully!')
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
