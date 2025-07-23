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
        const response = await axios.post(`http://localhost:5000/user_book/${lotid}`, {
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
    const response = await axios.get(`http://localhost:5000/user_book/${lotid}`, {
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
