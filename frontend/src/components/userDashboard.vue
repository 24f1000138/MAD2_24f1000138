<template>
  <div class="user-dashboard">
    <nav class="user-nav">
        <span class="welcome">Welcome User</span>
        <div class="nav-links">
            <router-link to="/user_dashboard">Home</router-link>
            <router-link to="/user_history">History</router-link>
            <router-link to="/user_summary">Summary</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
        <span class="edit-profile"><router-link to="/user_profile">Edit Profile</router-link></span>
    </nav>
    <div class="users-content">
    <h2>Recent Parking History</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Location</th>
          <th>Vehicle Number</th>
          <th>Timestamp</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="spot in rspots" :key="spot.r_id">
          <td>{{ spot.r_id }}</td>
          <td>{{ spot.loc }}</td>
          <td>{{ spot.veh_no }}</td>
          <td>{{ spot.stamp }}</td>
          <td>
            <span v-if="spot.end_time">Parked Out</span>
            <button v-else @click="release(spot.r_id)">Release</button>
            </td>
        </tr>
      </tbody>
    </table>
    <div class="user_search">
        <h2>Search Parking Spots</h2>
        <form @submit.prevent="search">
            <input type="text" v-model="searchQuery" placeholder="Enter location or vehicle number" />
            <button type="submit" :disabled="!searchQuery">Search</button>
        </form>

    <h3 v-if="searchQuery"> Parking Spots @ <span>{{ searchQuery }}</span></h3>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Address</th>
          <th>Availability</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="spot in spots" :key="spot.lot_id">
          <td>{{ spot.lot_id }}</td>
          <td>{{ spot.addr }}</td>
          <td>{{ spot.available }}</td>
          <td>
            <button @click="book(spot.lot_id)">Book</button>
            </td>
        </tr>
      </tbody>
    </table>
    <p v-if="msg" class="success">{{ msg }}</p>
    </div>
    </div>
  </div>
</template> 

<script>
import axios from 'axios'

export default {
  name: 'UserDashboard',
  data() {
    return {
      rspots: [],
      searchQuery: '',
      spots: [],
      msg:''
    }
  },
  methods: {   
    async fetchSpots() {
      const token = localStorage.getItem('token')
      const response = await axios.get('http://localhost:5000/user_dashboard', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        withCredentials: true
      })
      this.rspots = response.data
      this.rspots.forEach(spot => {
        spot.stamp = new Date(spot.stamp).toLocaleString()
        if (spot.end_time) {
          spot.end_time = new Date(spot.end_time).toLocaleString()
        }
      })
    },
  async search() {
      const token = localStorage.getItem('token')
      const response = await axios.get(`http://localhost:5000/user_search?query=${this.searchQuery}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        withCredentials: true
      })
      this.spots = response.data
    },
    async book(lotId) {
      this.$router.push(`/user_book/${lotId}`)
    },
    async release(rId) {
      this.$router.push(`/user_release/${rId}`)
    }
  },
  mounted() {
    this.fetchSpots()
  }
}
</script>
<style scoped>
.user-dashboard {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f4f7f9;
  padding: 20px;
  min-height: 100vh;
}

.user-nav {
  background-color: #d8f0e2;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 8px;
  margin-bottom: 20px;
}

.user-nav .welcome {
  font-weight: bold;
  color: #e53935;
}

.nav-links a {
  margin-left: 15px;
  text-decoration: none;
  color: #2c3e50;
  font-weight: bold;
}
.edit-profile{
  color: white;
  text-decoration: none;
  font-weight: bold;
}
.edit-profile:hover{
  text-decoration: underline;
}
.nav-links a:hover {
  text-decoration: underline;
}

.users-content {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

h2, h3 {
  margin-top: 0;
  color: #34495e;
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th {
  background-color: #2d4263;
  color: white;
  padding: 10px;
  text-align: left;
}

td {
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

td button {
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
  background-color: #4CAF50;
  color: white;
  cursor: pointer;
}

td button:hover {
  background-color: #388e3c;
}

td span {
  padding: 6px 12px;
  border-radius: 4px;
  background-color: #ffebee;
  color: #c62828;
  font-weight: bold;
}

.user_search {
  margin-top: 40px;
  background-color: #eef6f9;
  padding: 20px;
  border-radius: 8px;
}

input[type="text"] {
  padding: 8px;
  margin-right: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button[type="submit"] {
  background-color: #1976d2;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #0d47a1;
}

.success {
  color: green;
  margin-top: 10px;
  font-weight: bold;
}

</style>
