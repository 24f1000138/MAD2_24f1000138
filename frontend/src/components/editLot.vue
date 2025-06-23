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
        const response = await axios.get(`http://localhost:5000/admin_editlot/${lotid}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
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
        const response = await axios.post(`http://localhost:5000/admin_editlot/${lotid}`, {

          name: this.lot.name,
          address: this.lot.address,
          pinc: this.lot.pinc,
          price: this.lot.price,
          num: this.lot.num
        }, {headers: {
          Authorization: `Bearer ${token}`
        }
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
