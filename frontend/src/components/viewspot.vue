<template>
<div class="view-dashboard">
  <div class="view-container">
    <h2>View Parking Spot</h2>
       <p><strong>ID:</strong> {{ spot.spot_id }}</p>
      <p><strong>Status:</strong>
      <span v-if="spot.status === 'O'" class="click" @click="reserveSpot(spot.spot_id)">{{ spot.status }}</span>
      <span v-else>{{ spot.status }}</span>
      </p>
      <button @click="deletespot(spot.spot_id)">Delete</button>
      <button @click="$router.push('/admin_dashboard')">Cancel</button>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
  </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'viewSpot',
  data() {
    return {
      spot: {
        spot_id: '',
        status: ''
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
        const response = await axios.get(`http://localhost:5000/admin_viewspot/${spotid}`, {
          headers: {
            Authorization: `Bearer ${token}`
          },
          withCredentials: true
        })
        this.spot = response.data
      } catch (err) {
        this.msg = err.response?.data?.msg || 'Failed to fetch spot details'
        this.error = true
      }
    },
    async deletespot(spot_id) {
        const token = localStorage.getItem('token')
      try {
        await axios.delete(`http://localhost:5000/admin_viewspot/${spot_id}`, {
          headers: {
            Authorization: `Bearer ${token}`
          },
          withCredentials: true
        })
        this.$router.push('/admin_dashboard')
      } catch (error) {
        console.error('Error deleting spot:', error)
        this.msg = 'Failed to delete spot'
        this.error = true
      }
    },
    async reserveSpot(spot_id) {
      this.$router.push(`/admin_reservespot/${spot_id}`)
    }
 },
  mounted() {
    this.fetchSpot()
  }
}
</script>
<style scoped>
.view-dashboard {
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
.view-container{
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #f1c40f;
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

p {
  font-size: 1.1rem;
  margin: 0.8rem 0;
  color: #f9f9f9;
}

strong {
  color: #f1c40f;
}

button {
  padding: 10px 20px;
  margin: 12px 8px 0 0;
  border: none;
  border-radius: 8px;
  background-color: #3498db;
  color: white;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #2c80b4;
}

.click {
  color: #00e6e6;
  font-weight: bold;
  cursor: pointer;
  padding-left: 5px;
}

.click:hover {
  text-decoration: underline;
  color: #1abc9c;
}

.error {
  color: #ff6b6b;
  font-weight: bold;
  text-align: center;
  margin-top: 1rem;
}

.success {
  color: #2ecc71;
  font-weight: bold;
  text-align: center;
  margin-top: 1rem;
}

</style>
