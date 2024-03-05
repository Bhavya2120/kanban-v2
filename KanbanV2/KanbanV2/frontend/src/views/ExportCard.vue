<template>
    <p>Click the button below to download your cards!</p>
    <button class="btn btn-primary">
    <a :href="url" class="nav-link">
            Export Cards
  </a>
  </button>
<br/><br/>
  <a href="/lists/{{id}}">Go back to your Lists</a>
</template>
<script>
export default {
  name: 'ExportCard',
  data () {
    return {
      id: this.$route.params.id,
      url: 'http://localhost:5000/exportcard/' + this.$route.params.list_id
    }
  }
}
</script>
