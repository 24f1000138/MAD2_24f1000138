<template>
  <div class="login-page">
    <div class="login-logo">
      <img src="/frontend/public/ParkPal Logo Design.png" alt="ParkPal Logo" />
    </div>
    <div class="login-card">
      <h2>Sign in</h2>
      <form @submit.prevent="login">
        <label>Email address</label>
        <input type="email" v-model="email" placeholder="Email" required /> 
        <label>Password</label>
        <input type="password" v-model="password" placeholder="Password" required /> 
        <button type="submit" class="primary">Sign in</button>   
        <button type="button" class="secondary" @click="$router.push('/register')">
          Create an Account?
        </button>
        <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
      </form>
    </div>
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
.login-page {
  height: 100vh;
  background: linear-gradient(135deg, #0e1117, #1a1f2b);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-image: url('/frontend/public/Parking Icons Vector Pattern.png');
  background-size: cover;
  background-position: center;
  padding: 2rem;
}

.login-logo img {
  width: 180px;
  margin-bottom: 20px;
  border-radius: 50% / 40%; 
  padding: 8px;
  background-color: rgba(255, 255, 255, 0.05); 
  box-shadow: 0 0 10px rgba(52, 199, 89, 0.3);
}

.login-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
  color: #ffffff;
}

.login-card h2 {
  margin-bottom: 1.5rem;
  text-align: center;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #cfcfcf;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 10px 12px;
  margin-bottom: 1rem;
  border-radius: 6px;
  border: none;
  background-color: #1e2430;
  color: white;
}

input:focus {
  outline: 2px solid #34C759;
}

button.primary {
  width: 100%;
  padding: 12px;
  background-color: #0078D4;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
}

button.secondary {
  width: 100%;
  padding: 10px;
  background-color: transparent;
  border: 1px solid #34C759;
  color: #34C759;
  border-radius: 8px;
  cursor: pointer;
}

.error {
  color: #ff4d4f;
  text-align: center;
  margin-top: 10px;
}

.success {
  color: #34C759;
  text-align: center;
  margin-top: 10px;
}
</style>