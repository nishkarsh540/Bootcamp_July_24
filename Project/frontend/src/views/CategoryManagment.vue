<template>
    <div class="category-managment">
        <h2>category-managment</h2>

        <form @submit.prevent="addCategory">
            <input type="text" v-model="newCategoryName" placeholder="Enter category name" required>
            <button type="submit">Add Category</button>
        </form>


        <table v-if="categories.length>0">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="category in categories" :key='category.id'>
                    <td>{{ category.id }}</td>
                    <td>
                        <input type="text" v-model="category.name" :disabled="category.id !== editingCategoryId">
                    </td>
                    <td>
                        <button v-if="category.id !== editingCategoryId" @click="startEditing(category)">Edit</button>

                        <button v-else @click="saveCategory(category)">Save</button>

                        <button @click="deleteCategory(category)">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <div v-else>
            <p>no categories found</p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default{
    data(){
    return {
        categories:[],
        newCategoryName:'',
        editingCategoryId:null,
    };
},
mounted(){
    this.loadCategories();
},
methods:{
    async loadCategories(){
        try{
            const access_token = localStorage.getItem('token')
            const response = await axios.get('http://127.0.0.1:5000/api/category',{
                headers:
                {
                    Authorization: `Bearer ${access_token}`,
                }
            });
            this.categories = response.data;
        } catch(error){
            console.error(error);
        }
    },
    async addCategory(){
        try{
            const response = await axios.post('http://127.0.0.1:5000/api/category',{
                name:this.newCategoryName
            });
            console.log(response.data);
            this.newCategoryName='';
            this.loadCategories();
        } catch(error){
            console.log(error)
        }
    },
    async deleteCategory(category){
        try{
            const response = await axios.delete('http://127.0.0.1:5000/api/category',{
                data:{id:category.id}
            });
            console.log(response.data);
            this.loadCategories();
        } catch(error){
            console.log(error);
        }
    },
    async saveCategory(category){
        try{
            const response = await axios.put('http://127.0.0.1:5000/api/category',{
                id:category.id,
                name:category.name
            });
            console.log(response.data);
            this.editingCategoryId = null;
            this.loadCategories;
        } catch(error){
            console.log(error);
        }
    },
    startEditing(category){
        this.editingCategoryId = category.id;
    }
}
}

</script>