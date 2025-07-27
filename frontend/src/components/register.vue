<template>
  <div class="register-page">
    <div class="register-logo">
      <img src="/frontend/src/assets/ParkPal Logo Design.png" alt="ParkPal Logo" />
    </div>
  <div class="register-card">
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
      <button type="submit" class="primary">Submit</button>
      <button @click="$router.push('/login')" class="secondary">Already have an Account?</button>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
    </form>
  </div>
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
.register-page {
  height: 100vh;
  background: linear-gradient(135deg, #0e1117, #1a1f2b);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-image: url('/frontend/src/assets/Parking Icons Vector Pattern.png');
  background-size: cover;
  background-position: center;
  padding: 2rem;
}

.register-logo img {
  width: 180px;
  margin-bottom: 20px;
  border-radius: 50% / 40%; 
  padding: 8px;
  background-color: rgba(255, 255, 255, 0.05); 
  box-shadow: 0 0 10px rgba(52, 199, 89, 0.3);
}

.register-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
  color: #ffffff;
}

.register-card h2 {
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
input:-webkit-autofill,
input:-webkit-autofill:focus,
input:-webkit-autofill:hover,
input:-webkit-autofill:active {
  -webkit-box-shadow: 0 0 0px 1000px #1e2430 inset !important;
  -webkit-text-fill-color: white !important;
  transition: background-color 5000s ease-in-out 0s;
}
</style>