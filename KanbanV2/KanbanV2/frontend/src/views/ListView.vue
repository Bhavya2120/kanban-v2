<template>
    <h1>Hello {{name}}!</h1><br/>
    <h2>These are your Lists</h2><br/><br>
    <h3 v-if="!items.length">No Lists yet</h3>
    <table v-else class="table table-striped">
  <thead>
    <th>Sno</th>
    <th>List ID</th>
    <th>List name</th>
    <th>Action 1</th>
    <th>Action 2</th>
    <th>Action 3</th>
    <th>Action 4</th>
    <th>Action 5</th>
  </thead>
  <tbody>
<tr v-for="item,index in items" :key="index">
                <td>{{index+1}}</td>
                <td>{{item.listid}}</td>
                <td><router-link :to="`/cards/${item.listid}`">{{item.listname}}</router-link></td>
                <td><router-link :to="`/addcard/${item.listid}`" style="text-decoration:strong; color: grey;"><button class="btn btn-outline-light">Add Cards to {{item.listname}}</button></router-link></td>
                <td><router-link :to="`/lists/update/${item.listid}`"><button class="btn btn-info">Update List</button></router-link></td>
                <td><router-link :to="`/lists/delete/${item.listid}`"><button class="btn btn-danger">Delete this List</button></router-link></td>
                <td><router-link :to="`/exportcard/${item.listid}`"><button class="btn btn-warning">Export Cards of this List</button></router-link></td>
                <td><router-link :to="`/summary/${item.listid}`"><button class="btn btn-success">Get a Summary</button></router-link></td>
              </tr>
  </tbody>
</table>
<br/><br/><br/><br/><br/>
<button class="btn btn-outline-dark add" @click="createlist">Click to add lists</button>
<button class="btn btn-outline-dark export">
  <a :href="url" class="nav-link">
            Export Lists
  </a>
</button>
<br/><br/>
    <h5>Caution: Deleting a List will also delete the Cards associated with it!</h5>
    <h5>If you do not want to lose the Cards, move them to another List</h5>
</template>

<script>
import { useRouter } from 'vue-router'
import axios from 'axios'
export default {
  Name: 'ListView',
  mounted () {
    const id = localStorage.id
    return {
      id
    }
  },
  data () {
    return {
      name: localStorage.name,
      items: [],
      id: localStorage.id,
      url: 'http://localhost:5000/export/' + localStorage.id

    }
  },
  methods: {
    getLists () {
      const router = useRouter()
      const path = 'http://localhost:5000/lists/' + localStorage.id
      axios.get(path)
        .then((res) => {
          this.items = res.data.list
        })

        .catch((err) => {
          if (err.response.status === 401) {
            router.push({ name: 'login' })
            alert('Token expired')
          }
        })

      console.log(this.items)
    }
  },
  setup () {
    const router = useRouter()
    const createlist = async () => {
      await router.push({ name: 'createlist', params: { id: localStorage.id } })
    }
    return {
      createlist
    }
  },
  created () {
    this.getLists()
  }
}
</script>
