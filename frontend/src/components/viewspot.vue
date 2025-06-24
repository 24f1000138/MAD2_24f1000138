<template>
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
          }
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
          }
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

p {
  font-size: 16px;
  margin-bottom: 12px;
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
</style>
