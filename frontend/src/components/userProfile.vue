<template>
  <div class="edit-container">
    <h2>Edit Profile</h2>
    <form @submit.prevent="updateProfile">
      <label for="name">Name:</label>
      <input type="text" v-model="user.name" placeholder="user.name" required />
      <label for="email">Email:</label> 
      <input type="email" v-model="user.email" placeholder="user.email" required />
      <label for="addr">Address:</label>
      <input type="text" v-model="user.addr" placeholder="user.addr" required />
      <label for="pin">PIN:</label>
      <input type="text" v-model="user.pin" placeholder="user.pin" required />
      <button type="submit">Submit</button>
      <button type="button" @click="$router.push('/user_dashboard')">Cancel</button>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'editProfile',
  data() {
    return {
      user: {
        name: '',
        email: '',
        addr: '',
        pin: ''
      },
      msg: '',
      error: false
    }
  },
  methods: {
    async fetchUser() {
      const token = localStorage.getItem('token')
      try {
        const response = await axios.get('http://localhost:5000/user_profile', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        this.user = response.data
      } catch (err) {
        this.msg = err.response?.data?.msg || 'Failed to fetch user details'
        this.error = true
      }
    },
    async updateProfile() {
      const token = localStorage.getItem('token')
      try {
        const response = await axios.post('http://localhost:5000/user_profile', {

          name: this.user.name,
          email: this.user.email,
          addr: this.user.addr,
          pin: this.user.pin
        }, {headers: {
          Authorization: `Bearer ${token}`
        }
      })
        this.msg = response.data.msg
        this.error = false
        setTimeout(() => {
          this.$router.push('/login')
        }, 1000)
      } catch (err) {
        this.msg = err.response?.data?.msg || 'Update failed'
        this.error = true
      }
    }
  },
  mounted() {
    this.fetchUser()
  }
}
</script>
<style scoped>
.edit-container {
  max-width: 400px;
  margin: 50px auto;
  background: #f9f9f9;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.edit-container h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 0.25rem;
  font-weight: 600;
  color: #444;
}

input {
  margin-bottom: 1rem;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}

input:focus {
  border-color: #007BFF;
  outline: none;
}

button {
  padding: 0.7rem;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

p {
  text-align: center;
  margin-top: 1rem;
  font-weight: bold;
}

.success {
  color: green;
}

.error {
  color: red;
}
</style>
