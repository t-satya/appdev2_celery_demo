import AddArticle from "./add_article.js";
import AllArticles from "./all_articles.js";


const AdminProfile= Vue.component("profile",{
    data:function(){
        return{
        x:null,
        y:null,
        }
    },
    
    components:{
        "all-articles":AllArticles,
        "add-article":AddArticle
    },
    template:`
    <div>
        <h1>You are in the Admin Profile Page</h1>
        <button @click="logout">Logout</button>
        <router-link to="/adminprof">All Articles</router-link>
        <router-link to="/adminprof/addarticle">Add Article</router-link>
        <router-view></router-view>


        <label for="fnum">Fnum:</label>
        <input type="number" id="fnum" v-model="x">
        <label for = "snum">Snum:</label>
        <input type="number" id="snum" v-model="y">

        <button @click="celery_add">TriggerCelery</button>
    </div>
    `,
    methods:{
        logout:function(){
            localStorage.clear();
            this.$router.push("/")
        },

        celery_add:function(){
            fetch(`http://localhost:3000/api/trigger_celery/${this.x}/${this.y}`)
            .then((res)=>res.json())
            .then((data)=>{
                console.log(data.result)
            })
            .catch((error)=>console.error(error))
        }
    },
    
    
});

export default AdminProfile;