<template>
  <div class="add-container">
    <h2>Book the Parking Spot</h2>
    <form @submit.prevent="bookspot">
      <label for="lot_id">Lot ID: </label>
      <input type="number" v-model="id.lot_id" placeholder="id.lot_id" readonly />
      <label for="spot_id">Spot ID :</label>
      <input type="number" v-model="id.spot_id" placeholder="id.spot_id" readonly />
      <label for="u_id">User ID: </label>
      <input type="number" v-model="id.u_id" placeholder="id.u_id" readonly />
      <label for="v_no">Vehicle Number :</label>
      <input type="text" v-model="vehicle_no" placeholder="Enter vehicle number" required />
      
      <button type="submit">Book</button>
      <button @click="$router.push('/user_dashboard')">Cancel</button>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserBook',
  data() {
    return {
        id: {
            lot_id: '',
            spot_id: '',
            u_id: ''
        },
        vehicle_no: '',
      msg: '',
      error: false
    }
  },
  methods: {
    async bookspot() {
      const lotid = this.$route.params.lot_id
      const token= localStorage.getItem('token')
      try {
        const response = await axios.post(`https://mad2-24f1000138.onrender.com/user_book/${lotid}`, {
          lot_id: this.id.lot_id,
          spot_id: this.id.spot_id,
          u_id: this.id.u_id,
          vehicle_no: this.vehicle_no
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          },
          withCredentials: true})
        this.msg = response.data.msg
        this.error = false
        setTimeout(() => {
          this.$router.push('/user_dashboard')
        }, 1000)
      } catch (err) {
        this.msg = err.response?.data?.msg || 'Book failed'
        this.error = true
      }
    },
    async fetchBookingInfo() {
  const lotid = this.$route.params.lot_id
  const token = localStorage.getItem('token')
  try {
    const response = await axios.get(`https://mad2-24f1000138.onrender.com/user_book/${lotid}`, {
      headers: {
        Authorization: `Bearer ${token}`
      },
      withCredentials: true
    })
    this.id = response.data[0]
  } catch (err) {
    this.msg = err.response?.data?.msg || 'Failed to fetch booking info'
    this.error = true
  }
}

  },
  mounted(){
    this.fetchBookingInfo()
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
  background-image: url('/user_dash.png');
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
  margin-bottom: 20px;
  color: #ebeef1;
}

label {
  display: block;
  text-align: left;
  margin-top: 15px;
  font-weight: bold;
}

input {
  display: block;
  width: 100%;
  padding: 10px;
  margin-top: 6px;
  margin-bottom: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

button {
  padding: 10px 18px;
  margin: 10px 8px 0 8px;
  border: none;
  border-radius: 6px;
  background-color: #2ecc71;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #27ae60;
}
.error {
  color: #c0392b;
  margin-top: 16px;
  font-weight: bold;
}
.success {
  color: #2ecc71;
  margin-top: 16px;
  font-weight: bold;
}
</style>
