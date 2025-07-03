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
    <div class="users-content"></div>
    <h2>Full User History</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Location</th>
          <th>Vehicle Number</th>
          <th>Start Time</th>
          <th>End Time</th>
          <th>Cost</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="spot in rspots" :key="spot.r_id">
          <td>{{ spot.r_id }}</td>
          <td>{{ spot.loc }}</td>
          <td>{{ spot.veh_no }}</td>
          <td>{{ spot.start_time }}</td>
          <td>{{ spot.end_time }}</td>
          <td>{{ spot.cost }}</td>
        </tr>
      </tbody>
    </table>
    </div>
</template> 

<script>
import axios from 'axios'

export default {
  name: 'UserHistory',
  data() {
    return {
      rspots: []
    }
  },
  methods: {   
    async fetchHistory() {
      const token = localStorage.getItem('token')
      const response = await axios.get('http://localhost:5000/user_history', {
        headers: {
          Authorization: `Bearer ${token}`,
        }
      })
      this.rspots = response.data
      this.rspots.forEach(spot => {
        spot.start_time = new Date(spot.start_time).toLocaleString()
        spot.end_time = new Date(spot.end_time).toLocaleString()
      })
    },
  },
  mounted() {
    this.fetchHistory()
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
.users-content {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}
.nav-links {
  display: flex;
  gap: 15px;
}

.nav-links a,
.edit-profile {
  color: white;
  text-decoration: none;
  font-weight: bold;
}
.nav-links a:hover,
.edit-profile:hover {
  text-decoration: underline;
}
h2 {
  color: #333;
  margin-bottom: 15px;
}
button {
  padding: 8px 16px;
  border-radius: 5px;
  border: none;
  background-color: #2ecc71;
  color: white;
  font-weight: bold;
  cursor: pointer;
  margin-top: 15px;
}
button:hover {
  background-color: #27ae60;
}
table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

th, td {
  padding: 12px;
  border: 1px solid #ccc;
}

thead {
  background-color: #eaf4ff;
}

tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}
</style>
