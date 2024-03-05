<template>
  <a href="/lists/{{id}}">Go Back to your Lists</a>
    <h1>Hello {{name}}!</h1><br/>
    <h2>These are the cards of this list</h2><br/><br>
    <h3 v-if="!items.length">No Cards yet</h3>
    <table v-else class="table table-striped">
  <thead>
    <th>Sno</th>
    <th>Card Title name</th>
    <th>Card Content</th>
    <th>Card Completion Status</th>
    <th>Card Deadline</th>
    <th>Card Completion Date</th>
  </thead>
  <tbody>
<tr v-for="item,index in items" :key="index">
                <th>{{index+1}}</th>
                <th>{{item.card_title}}</th>
               <td>{{item.card_content}}</td>
               <td>{{item.card_complete}}</td>
               <td>{{item.card_deadline}}</td>
               <td>{{item.card_complete_date}}</td>
               <td><router-link :to="`/cards/update/${item.cardid}`"><button class="btn btn-info">Update this card</button></router-link>   </td>
                <td><router-link :to="`/cards/delete/${item.cardid}`"><button class="btn btn-danger">Delete this card</button></router-link></td>
            </tr>
  </tbody>
</table>
<br/><br/><br/><br/><br/>
<br/><br/>
</template>

<script>
import { useRouter } from 'vue-router'
import axios from 'axios'
export default {
  Name: 'CardView',
  data () {
    return {
      name: localStorage.name,
      items: [],
      id: this.$route.params.id
    }
  },
  methods: {
    getCards () {
      const router = useRouter()
      const path = 'http://localhost:5000/cards/' + this.$route.params.list_id
      axios.get(path)
        .then((res) => {
          this.items = res.data.cardsoflist
        })

        .catch((err) => {
          if (err.response.status === 401) {
            router.push({ name: 'login' })
            this.$router.push({ path: '/login' })
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
