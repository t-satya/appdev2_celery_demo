const Article = Vue.component("my-article",{
    props:["article"],
    template:`
        <div>
            <h2>{{article.title}}</h2>
            <p>{{article.content}}</p>
        </div>
    
    `
})


const Profile = Vue.component("profile",{
    data:function(){
        return{
            all_articles:null,
        }
    },
    components:{
        "my-article":Article,
    },
    template:`
    <div>
        <h1>You are in the Customer Profile Page</h1>
        <button @click="logout">Logout</button>
        <h2>All Articles</h2>
        <my-article v-for="article in all_articles" :key="article.article_id" v-bind:article="article"></my-article>
    </div>
    `,
    methods:{
        logout:function(){
            localStorage.clear();
            this.$router.push("/")
        }
    },
    mounted:async function(){
        await fetch("http://localhost:3000/api/articles",{
            method:"GET",
            headers:{
                "Authentication-Token": localStorage.getItem('token'),
                "Content-Type": "application/json",
                },
            
        })
        .then((response)=>
        {
            if(response.ok){
            return response.json()
        }else{
            throw new Error("Request Failed")
        }
        })
        .then((data)=>{
            console.log(data);
            this.all_articles=data;
        })
        .catch((error)=>console.error(error))
    },
    beforeRouteEnter(to, from, next) {
        if (!localStorage.getItem("token")) {
          next("/");
        } else {
          next();
        }
      }
});

export default Profile;