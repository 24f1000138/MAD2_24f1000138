<template>
  <div class="logout-page">
    <div class="logout-logo">
      <img src="C:\Users\Muthukumar Natesan\Downloads\mad2_24f1000138\backend\static\ParkPal Logo Design.png" alt="ParkPal Logo" />
    </div>
  <div class="logout-card">
    <h1>Logout</h1>
    <form>
      <h2>Do you want to logout?</h2>
      <button type="button" @click="logout" class="primary">Logout</button>
      <button type="button" @click="$router.back()" class="secondary">Back</button>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
    </form>
  </div>
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
      const token = localStorage.getItem('token')
      try {
        const response = await axios.post('http://localhost:5000/logout', {}, {
            headers: {
            Authorization: `Bearer ${token}`
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
<style scoped>
.logout-page {
  height: 100vh;
  background: linear-gradient(135deg, #0e1117, #1a1f2b);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-image: url('C:/Users/Muthukumar Natesan/Downloads/mad2_24f1000138/frontend/src/assets/Parking Icons Vector Pattern.png');
  background-size: cover;
  background-position: center;
  padding: 2rem;
}

.logout-logo img {
  width: 180px;
  margin-bottom: 20px;
  border-radius: 50% / 40%; 
  padding: 8px;
  background-color: rgba(255, 255, 255, 0.05); 
  box-shadow: 0 0 10px rgba(52, 199, 89, 0.3);
}

.logout-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
  color: #ffffff;
}

.logout-card h2 {
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
h1 {
  text-align: center;
  color: #00bfff;
  margin-bottom: 20px;
}
</style>