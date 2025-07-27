<template>
  <div class="user-release">
  <div class="add-container">
    <h2>Release the Parking Spot</h2>
    <form @submit.prevent="releaseSpot">
      <label for="spot_id">Spot ID :</label>
      <input type="number" v-model="id.spot_id" placeholder="id.spot_id" readonly />
      <label for="veh_no">Vehicle Number: </label>
      <input type="text" v-model="id.veh_no" placeholder="id.veh_no" readonly />
      <label for="start_time">Start Time: </label>
      <input type="datetime" v-model="id.start_time" placeholder="id.start_time" readonly />
      <label for="end_time">End Time: </label>
      <input type="datetime" v-model="id.end_time" placeholder="id.end_time" readonly />
      <label for="cost">Cost: </label>
      <input type="number" v-model="id.cost" placeholder="id.cost" readonly />
      <div class="button-group">
      <button type="submit">Release</button>
      <button @click="$router.push('/user_dashboard')" type="button">Cancel</button>
      </div>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
    </form>
  </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserRelease',
  data() {
    return {
        id: {
            spot_id: '',
            veh_no: '',
            start_time: '',
            end_time: '',
            cost: ''    
        },
      msg: '',
      error: false
    }
  },
  methods: {
    async releaseSpot() {
      const rid = this.$route.params.r_id
      const token= localStorage.getItem('token')
      try {
        const response = await axios.post(`http://localhost:5000/user_release/${rid}`, {}, {
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
        this.msg = err.response?.data?.msg || 'Release failed'
        this.error = true
      }
    },
    async fetchReleasingInfo() {
  const r_id = this.$route.params.r_id
  const token = localStorage.getItem('token')
  try {
    const response = await axios.get(`http://localhost:5000/user_release/${r_id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      },
      withCredentials: true
    })
    this.id = response.data[0]
    this.id.start_time = new Date(this.id.start_time).toLocaleString()
    this.id.end_time = new Date(this.id.end_time).toLocaleString()
  } catch (err) {
    this.msg = err.response?.data?.msg || 'Failed to fetch releasing info'
    this.error = true
  }
}

  },
  mounted(){
    this.fetchReleasingInfo()
  }
}
</script>

<style scoped>
.user-release {
  background: url('C:/Users/Muthukumar Natesan/Downloads/mad2_24f1000138/frontend/src/assets/user_dash.png') no-repeat center center fixed;
  background-size: cover;
  min-height: 100vh;
  padding: 40px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.add-container {
  width: 100%;
  max-width: 450px;
  background: rgba(255, 255, 255, 0.2); 
  backdrop-filter: blur(12px);
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #babec1;
}

label {
  font-weight: 600;
  margin-bottom: 4px;
  color: #f0f2f5;
  display: block;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

input:focus {
  border-color: #007BFF;
  outline: none;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 10px;
}

button {
  flex: 1;
  padding: 10px;
  font-size: 1rem;
  font-weight: bold;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button[type="submit"] {
  background-color: #2ecc71;
}

button[type="submit"]:hover {
  background-color: #27ae60;
}

button[type="button"] {
  background-color: #e74c3c;
}

button[type="button"]:hover {
  background-color: #c0392b;
}

p {
  text-align: center;
  margin-top: 1rem;
  font-weight: bold;
}

.success {
  color: green;
}

.error {
  color: red;
}
</style>
