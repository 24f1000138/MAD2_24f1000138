<template>
  <div class="view-container">
    <h2>Occupied Parking Spot Details</h2>
    <form>
       <label for="spotid">Spot ID:</label>
      <input type="number" v-model="spot.spot_id" placeholder="spot.spot_id" readonly />
      <label for="uid">Customer ID:</label> 
      <input type="number" v-model="spot.u_id" placeholder="spot.u_id" readonly />
      <label for="name">Customer Name:</label>
      <input type="text" v-model="spot.user_name" placeholder="spot.user_name" readonly />
      <label for="vno">Vehicle Number:</label>
      <input type="text" v-model="spot.vehicle_no" placeholder="spot.vehicle_no" readonly />
      <label for="date">Date/Timeof Parking: </label>
      <input type="text" v-model="spot.start_time" placeholder="spot.start_time" readonly />
      <label for="cost">Est. Parking Cost: </label>
      <input type="number" v-model="spot.cost" placeholder="spot.cost" readonly />
      <button @click="$router.push('/admin_dashboard')">Cancel</button>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'viewreserveSpot',
  data() {
    return {
        spot: {
            spot_id: '',
            u_id: '',
            user_name: '',
            vehicle_no: '',
            start_time: '',
            cost: ''
        },
      msg: '',
      error: false
    }
  },
  methods: {
    async fetchSpot() {
      const spotid = this.$route.params.spot_id
      const token = localStorage.getItem('token')
      try {
        const response = await axios.get(`http://localhost:5000/admin_reservespot/${spotid}`, {
          headers: {
            Authorization: `Bearer ${token}`
          },
          withCredentials: true
        })
        this.spot = response.data
        this.spot.start_time = new Date(response.data.start_time).toLocaleString()
      } catch (err) {
        this.msg = err.response?.data?.msg || 'Failed to fetch reserved spot details'
        this.error = true
      }
    },
 },
  mounted() {
    this.fetchSpot()
  }
}
</script>
<style scoped>
.view-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #0e1117, #1a1f2b);
  background-image: url('/frontend/src/assets/admin_dash.png');
  background-size: cover;
  background-position: center;
  font-family: 'Segoe UI', sans-serif;
  color: #ffffff;
  padding: 2rem;
}

.view-container form {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 500px;
}
h2 {
  text-align: center;
  color: #00bfff;
  margin-bottom: 20px;
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
  width: 100%;
  padding: 12px;
  background-color: #267fa2;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s ease;
  margin-top: 10px;
}

button:hover {
  background-color: #27ae60;
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
