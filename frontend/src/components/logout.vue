<template>
  <div class="logout-container">
    <h2>Logout</h2>
    <form @submit.prevent="register">
      <p>Do you want to logout?</p>
      <button @click="logout">Logout</button>
      <button @click="$router.back()">Back</button>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Logout',
  data() {
    return {
      msg: '',
      error: false
    }
  },
  methods: {
    async logout() {
      try {
        const response = await axios.post('http://localhost:5000/logout', {
            headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.msg = response.data.msg
        this.error = false
        localStorage.removeItem('token')
        setTimeout(() => {
          this.$router.push('/login')
        }, 1000)
      } catch (err) {
        this.msg = err.response?.data?.msg || 'Logout failed'
        this.error = true
      }
    }
  }
}
</script>