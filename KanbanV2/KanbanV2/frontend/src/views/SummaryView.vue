<template>
    <a href="/lists/{{id}}">Go Back to your Lists</a>
      <h1>Hello {{name}}!</h1><br/>
      <h2>This is the summary of your list!</h2><br/><br>
      <table width="75%" align="center">
  <tr v-for="item,index in items" :key="index">
                  <th>Total Cards: </th>
                  <td>{{ item.total_cards }}</td>
                  <th>Cards Completed: </th>
                  <td> {{ item.complete_cards }}</td>
                 <th>Cards Completed Past Deadline: </th>
                 <td>{{item.tasks_completed_past_deadline}}</td>
                 <th>Incomplete Cards Past Deadline: </th>
                 <td>{{item.tasks_past_deadline}}</td>
                 </tr>
  </table>
  <br/>
<img src="../assets/logo.png">
  <br/><br/>
  </template>

<script>
// import { useRouter } from 'vue-router'
import axios from 'axios'
// import { VFrappeChart } from 'vue-frappe-chart'
export default {
  // components: { VFrappeChart },
  Name: 'SummaryView',
  data () {
    return {
      name: localStorage.name,
      items: [],
      id: this.$route.params.id
    }
  },
  methods: {
    getCards () {
      const path = 'http://localhost:5000/summary/' + this.$route.params.list_id
      axios.get(path)
        .then((res) => {
          this.items = res.data.summaryoflist
        })

        .catch((err) => {
          if (err.response.status === 401) {
            // router.push({ name: 'login' })
            alert('Token expired')
          }
        })

      console.log(this.items)
    }
  },
  mounted () {
    this.getCards()
  }
}
</script>
<style>
table {
  border: 1px solid black;
}
</style>
