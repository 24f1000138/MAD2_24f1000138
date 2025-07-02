<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <label for="name">Name:</label>
      <input type="text" v-model="name" placeholder="Name" required />
      <label for="email">Email:</label> 
      <input type="email" v-model="email" placeholder="Email" required />
      <label for="password">Password:</label>
      <input type="password" v-model="password" placeholder="Password" required />
      <label for="addr">Address:</label>
      <input type="text" v-model="addr" placeholder="Address" required />
      <label for="pin">PIN:</label>
      <input type="text" v-model="pin" placeholder="PIN" required />
      <button type="submit">Submit</button>
      <button @click="$router.push('/login')">Already have an Account?</button>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    return {
      name: '',
      email: '',
      password: '',
      addr: '',
      pin: '',
      msg: '',
      error: false
    }
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://localhost:5000/register', {
          name: this.name,
          email: this.email,
          password: this.password,
          addr: this.addr,
          pin: this.pin
        })
        this.msg = response.data.msg
        this.error = false
        setTimeout(() => {
          this.$router.push('/login')
        }, 1000)
      } catch (err) {
        this.msg = err.response?.data?.msg || 'Registration failed'
        this.error = true
      }
    }
  }
}
</script>

<style scoped>
.register-container {
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
