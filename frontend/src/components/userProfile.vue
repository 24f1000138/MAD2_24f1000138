<template>
  <div class="user-dashboard">
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
      <div class="button-group">
      <button type="submit">Submit</button>
      <button type="button" @click="$router.push('/user_dashboard')">Cancel</button>
      </div>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
    </form>
  </div>
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
          },
          withCredentials: true
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
        },
          withCredentials: true
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
.user-dashboard {
  background-image: url('/frontend/src/assets/user_dash.png');
  background-size: cover;
  background-position: center;
  padding: 50px 20px;
  min-height: 100vh;
}
.edit-container {
  max-width: 500px;
  margin: 60px auto;
  padding: 30px;
  background-color: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #2c3e50;
  text-align: center;
}

.edit-container h2 {
  font-size: 1.8rem;
  color: #2d3e50;
  margin-bottom: 24px;
}

form {
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

label {
  text-align: left;
  font-weight: bold;
  margin-bottom: 8px;
  color: #34495e;
}

input {
  padding: 12px;
  font-size: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  margin-bottom: 18px;
}

input:focus {
  border-color: #1abc9c;
  outline: none;
}
.button-group {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 16px;
}
button {
  flex: 1;
  padding: 0.7rem;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button[type="submit"] {
  background-color: #2ecc71;
}

button[type="submit"]:hover {
  background-color: #27ae60;
}

button[type="button"] {
  background-color: #e74c3c;
}

button[type="button"]:hover {
  background-color: #c0392b;
}
p {
  margin-top: 16px;
  font-weight: bold;
}

.success {
  color: #27ae60;
}

.error {
  color: #e74c3c;
}

</style>
