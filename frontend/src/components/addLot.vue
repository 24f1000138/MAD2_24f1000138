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
