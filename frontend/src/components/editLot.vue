<template>
  <div class="edit-container">
    <h2>Edit Parking Lot</h2>
    <form @submit.prevent="editLot">
    
      <label for="name">Prime Location Name:</label>
      <input type="text" v-model="lot.name" placeholder="lot.name" required />
      <label for="address">Address:</label>
      <input type="text" v-model="lot.address" placeholder="lot.address" required />
      <label for="pinc">Pin Code:</label>
      <input type="text" v-model="lot.pinc" placeholder="lot.pinc" required />
      <label for="price">Price(per hour) :</label>
      <input type="number" v-model="lot.price" placeholder="lot.price" required />
      <label for="num">Maximum spots:</label>
        <input type="number" v-model="lot.num" placeholder="lot.num" required />
      <button type="submit">Update</button>
      <button @click="$router.push('/admin_dashboard')">Cancel</button>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'EditLot',
  data() {
    return {
      lot: {
      name: '',
      address: '',
      pinc: '',
      price: '',
      num: ''
    },
      msg: '',
      error: false
    }
  },
  methods: {
    async fetchLot() {
      const lotid = this.$route.params.lot_id
      const token = localStorage.getItem('token')
      try {
        const response = await axios.get(`https://mad2-24f1000138.onrender.com/admin_editlot/${lotid}`, {
          headers: {
            Authorization: `Bearer ${token}`
          },
          withCredentials: true
        })
        this.lot = response.data
      } catch (err) {
        this.msg = err.response?.data?.msg || 'Failed to fetch lot details'
        this.error = true
      }
    },
    async editLot() {
      const lotid = this.$route.params.lot_id
      const token = localStorage.getItem('token')
      try {
        const response = await axios.post(`https://mad2-24f1000138.onrender.com/admin_editlot/${lotid}`, {

          name: this.lot.name,
          address: this.lot.address,
          pinc: this.lot.pinc,
          price: this.lot.price,
          num: this.lot.num
        }, {headers: {
          Authorization: `Bearer ${token}`
        },
          withCredentials: true
      })
        this.msg = response.data.msg
        this.error = false
        setTimeout(() => {
          this.$router.push('/admin_dashboard')
        }, 1000)
      } catch (err) {
        this.msg = err.response?.data?.msg || 'Update failed'
        this.error = true
      }
    }
  },
  mounted() {
    this.fetchLot()
  }
}
</script>

<style scoped>
.edit-container {
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

.edit-container form {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

.edit-container h2 {
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
  background-color: #34C759;
  transition: 0.3s ease;
}

button:last-of-type {
  background-color: #0078D4;
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
