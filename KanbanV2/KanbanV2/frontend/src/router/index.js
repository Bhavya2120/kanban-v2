import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import ListView from '../views/ListView.vue'
import DeleteList from '../views/DeleteList.vue'
import CreateList from '../views/CreateList.vue'
import AddCards from '../views/AddCards.vue'
import DeleteCard from '../views/DeleteCard.vue'
import UpdateCard from '../views/UpdateCard.vue'
import UpdateList from '../views/UpdateList.vue'
import CardView from '../views/CardView.vue'
import ExportCard from '../views/ExportCard.vue'
import SummaryView from '../views/SummaryView.vue'

const routes = [{
  path: '/',
  name: 'home',
  component: HomeView
},
{
  path: '/about',
  name: 'about',
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  component: () =>
    import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
},
{
  path: '/register',
  name: 'register',
  component: RegisterView
},
{
  path: '/login',
  name: 'login',
  component: LoginView
},
{
  path: '/lists/:id',
  name: 'lists',
  component: ListView
},
{
  path: '/lists/delete/:id',
  name: 'listdelete',
  component: DeleteList
},
{
  path: '/createlist/:id',
  name: 'createlist',
  component: CreateList
},
{
  path: '/cards/:list_id',
  name: 'CardView',
  component: CardView
},
{
  path: '/addcard/:list_id',
  name: 'AddCards',
  component: AddCards

},
{
  path: '/cards/delete/:id',
  name: 'DeleteCards',
  component: DeleteCard
},
{
  path: '/cards/update/:card_id',
  name: 'UpdateCard',
  component: UpdateCard
},
{
  path: '/lists/update/:list_id',
  name: 'UpdateList',
  component: UpdateList
},
{
  path: '/exportcard/:list_id',
  name: 'ExportCards',
  component: ExportCard
},
{
  path: '/summary/:list_id',
  name: 'SummaryView',
  component: SummaryView
}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
