<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <label for="email">Email:</label> 
      <input type="email" v-model="email" placeholder="Email" required />
      <label for="password">Password:</label>
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit">Submit</button>
      <button @click="$router.push('/register')">Register</button>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      msg: '',
      error: false
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:5000/login', {
          email: this.email,
          password: this.password
        })
        this.msg = response.data.msg
        this.error = false
        localStorage.setItem('token', response.data.access_token)

        setTimeout(() => {
          if (response.data.admin) {
            this.$router.push('/admin_dashboard')
          } else {
            this.$router.push('/user_dashboard')
          }
        }, 1000)
      } catch (err) {
        this.msg = err.response?.data?.msg || 'Login failed'
        this.error = true
      }
    }
  }
}
</script>
<style scoped>
.login-container {
  max-width: 400px;
  margin: auto;
  padding: 1rem;
}
input {
  display: block;
  width: 100%;
  margin-bottom: 10px;
}
button {
  padding: 10px;
}
.error {
  color: red;
}
.success {
  color: green;
}
</style>

