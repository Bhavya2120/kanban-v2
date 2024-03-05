<template>

    <h1 text-align: center>Update Card</h1>
    <form @submit.prevent="submit" style="margin-right: 150px;margin-top: 29px; margin-left: 150px" method="POST">
        <div class="form-group">
          <label for="title">Enter the card title:</label>
          <input type="name" class="form-control" v-model="data.card_title" name="Title" placeholder="Title"  required>
          <br/>
          <label for="content">Enter the card content:</label>
            <textarea class="form-control" v-model="data.card_content" id="content" name="content" placeholder="Content"></textarea>
           <br/>
            <label for="complete">Card Completion Status(Drag slider to the left for Complete, right for Not Complete):</label>
            <input v-model="data.card_complete" type="range" name="Complete" id="Complete" min="0" max="1">
            <br/><br/>
            <label for="card_list">Enter new list of this Card: </label>
            <input v-model="data.card_list" id="cardlist" name="cardlist" type="number" required>
            <label for="card_complete_date">Enter card complete date: </label>
            <input v-model="data.card_complete_date" type="date" name="completedate" id="completedate">
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
  Name: 'UpdateCard',
  data () {
    return {
      card_user: this.$route.params.card_user,
      card_id: this.$route.params.card_id,
      items: []
    }
  },
  mounted () {
    localStorage.setItem('card_user', this.card_user)
    localStorage.setItem('card_id', this.card_id)
    axios.get('http://localhost:5000/cards/update/' + this.card_id)
      .then((res) => {
        this.items = res.data
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
      card_deadline: '',
      card_list: ''
    })

    const submit = async () => {
      await fetch('http://localhost:5000/cards/update/' + localStorage.card_id, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        body: JSON.stringify(data)
      }).then(resp => resp.json())
        .then(data => {
          console.log(data)
          alert('This card has been updated successfully!')
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
