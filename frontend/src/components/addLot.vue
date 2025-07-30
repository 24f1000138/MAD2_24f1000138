<template>
  <div class="add-container">
    <h2>New Parking Lot</h2>
    <form @submit.prevent="addLot">
      <label for="name">Prime Location Name:</label>
      <input type="text" v-model="name" placeholder="Name" required />
      <label for="address">Address:</label>
      <input type="text" v-model="address" placeholder="Address" required />
      <label for="pinc">Pin Code:</label>
      <input type="text" v-model="pinc" placeholder="PIN" required />
      <label for="price">Price(per hour) :</label>
      <input type="number" v-model="price" placeholder="Price" required />
      <label for="num">Maximum spots:</label>
        <input type="number" v-model="num" placeholder="Max Spots" required />
      <button type="submit">Add</button>
      <button @click="$router.push('/admin_dashboard')">Cancel</button>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AddLot',
  data() {
    return {
      name: '',
      address: '',
      pinc: '',
      price: '',
      num: '',
      msg: '',
      error: false
    }
  },
  methods: {
    async addLot() {
      const token= localStorage.getItem('token')
      try {
        const response = await axios.post('http://localhost:5000/admin_addlot', {
          name: this.name,
          address: this.address,
          pinc: this.pinc,
          price: this.price,
          num: this.num
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }})
        this.msg = response.data.msg
        this.error = false
        setTimeout(() => {
          this.$router.push('/admin_dashboard')
        }, 1000)
      } catch (err) {
        this.msg = err.response?.data?.msg || 'Add failed'
        this.error = true
      }
    }
  }
}
</script>

<style scoped>
.add-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #0e1117, #1a1f2b);
  background-image: url('/admin_dash.png'); 
  background-size: cover;
  background-position: center;
  font-family: 'Segoe UI', sans-serif;
  color: #ffffff;
  padding: 2rem;
}
.add-container form {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

.add-container h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #00bfff;
}
label {
  display: block;
  margin-bottom: 6px;
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

button {
  width: 48%;
  margin-top: 10px;
  margin-right: 4%;
  padding: 10px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  color: white;
  background-color: #288c30;
  transition: 0.3s ease;
}

button:last-of-type {
  background-color: #4551a9;
  margin-right: 0;
}

button:hover {
  filter: brightness(1.1);
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
