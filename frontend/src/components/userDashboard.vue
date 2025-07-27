<template>
  <div class="user-dashboard">
    <nav class="user-nav">
        <span class="welcome">Welcome {{ userName }}</span>
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
  },
  computed: {
    userName() {
      return this.rspots.length > 0 ? this.rspots[0].name : 'User';
    }
  }
}
</script>
<style scoped>
.user-dashboard {
  font-family: 'Segoe UI', sans-serif;
  background-image: url('/frontend/src/assets/user_dash.png');
  background-size: cover;
  background-position: center;
  color: #ffffff;
  padding: 20px;
  min-height: 100vh;
}

.user-nav {
  background-color: rgba(45, 62, 80, 0.9);
  padding: 12px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 10px;
  margin-bottom: 30px;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.user-nav .welcome {
  font-size: 1.2rem;
  font-weight: bold;
  color: #f6b93b;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a,
.edit-profile a {
  color: #f0f8ff;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.2s;
}

.nav-links a:hover,
.edit-profile a:hover {
  color: #ffd700;
}

.edit-profile a {
  margin-left: 20px;
}

.users-content {
  background-color: rgba(255, 255, 255, 0.4); 
  backdrop-filter: blur(16px);                
  -webkit-backdrop-filter: blur(16px);
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  max-width: 1200px;
  margin: auto;
  color: #2c3e50;
}

h2, h3 {
  margin-top: 0;
  text-align: center;
  color: #2c3e50;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  color: #2c3e50;
}

th {
  background-color: #2c3e50;
  color: white;
  padding: 12px;
  text-align: left;
}

td {
  padding: 12px;
  background-color: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid #ccc;
  color: #2c3e50;
}

td button {
  padding: 6px 14px;
  border: none;
  border-radius: 6px;
  background-color: #3498db;
  color: white;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

td button:hover {
  background-color: #2c80b4;
}

td span {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 4px;
  background-color: #ffe5e5;
  color: #c0392b;
  font-weight: bold;
}

.user_search {
  margin-top: 50px;
  background-color: rgba(255, 255, 255, 0.4); 
  backdrop-filter: blur(16px);              
  -webkit-backdrop-filter: blur(16px);
  padding: 25px;
  border-radius: 10px;
  color: #2c3e50;
}

input[type="text"] {
  padding: 10px;
  width: 300px;
  margin-right: 15px;
  border-radius: 6px;
  border: 1px solid #bbb;
}

button[type="submit"] {
  background-color: #1abc9c;
  color: white;
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

button[type="submit"]:hover {
  background-color: #159d86;
}

.success {
  color: #2ecc71;
  margin-top: 12px;
  font-weight: bold;
  text-align: center;
}
</style>
