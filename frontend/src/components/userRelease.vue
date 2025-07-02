<template>
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
      
      <button type="submit">Release</button>
      <button @click="$router.push('/user_dashboard')">Cancel</button>
      <p v-if="msg" :class="{ error: error, success: !error }">{{ msg }}</p>
    </form>
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
          }})
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
      }
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
.add-container {
  max-width: 400px;
  margin: auto;
  padding: 1rem;
}
input {
  display: block;
  width: 100%;
  margin-bottom: 10px;
}
button {
  padding: 10px;
}
.error {
  color: red;
}
.success {
  color: green;
}
</style>
