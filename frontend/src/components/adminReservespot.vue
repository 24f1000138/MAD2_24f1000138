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
          }
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
  max-width: 500px;
  margin: 40px auto;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

h2 {
  text-align: center;
  color: #333;
}

button {
  padding: 10px 20px;
  margin-right: 10px;
  border: none;
  border-radius: 5px;
  background-color: #2d4263;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #1e2e4c;
}

.click {
  color: #0074d9;
  font-weight: bold;
  cursor: pointer;
}

.click:hover {
  text-decoration: underline;
}

.error {
  color: red;
}
.success {
  color: green;
}
input {
  margin-bottom: 12px;
  padding: 8px;
  width: 100%;
  box-sizing: border-box;
}

label {
  font-weight: 500;
  display: block;
  margin-bottom: 4px;
  color: #555;
}
</style>
