<template>
  <div class="admin-dashboard">
    <nav class="admin-nav">
        <span class="welcome">Welcome Admin</span>
        <div class="nav-links">
            <router-link to="/admin_dashboard">Home</router-link>
            <router-link to="/admin_users">Users</router-link>
            <router-link to="/admin_search">Search</router-link>
            <router-link to="/admin_summary">Summary</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
    </nav>
    <div class="admin-dashboard-content">
    <h2>Parking Lots</h2>
    <div class="lot-container">
    <div v-for="lot in lots" :key="lot.lot_id" class="lot-card">
      <h3>{{ lot.name }}</h3>
      <span><button @click="editLot(lot.lot_id)">Edit</button>
      <button @click="deleteLot(lot.lot_id)">Delete</button></span>
      <p>Occupied: {{ lot.occupied }} / {{ lot.num }}</p>
      <p>--------------------------------------------</p>
      <div class="spots">
        <div v-for="spot in lot.spots" :key="spot.spot_id" class="spot-square" :class="{ occupied: spot.status === 'O'}" @click="viewspot(spot.spot_id)">
          <span>{{ spot.status }}</span>
        </div>
      </div>
    </div>
    </div>
    <button @click="addLot">Add Lot</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      lots: []
    }
  },
  methods: {
    
    async fetchLots() {
      const token = localStorage.getItem('token')
      const response = await axios.get('http://localhost:5000/admin_dashboard', {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json' 
        },
        withCredentials: true
      })
      this.lots = response.data
    },
    editLot(lot_id) {
      this.$router.push(`/admin_editlot/${lot_id}`)
    },
    deleteLot(lot_id) {
      const token = localStorage.getItem('token')
     axios.delete(`http://localhost:5000/admin_dashboard/${lot_id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(() => {
        this.fetchLots() 
      })
      .catch(error => {
        console.error('Error deleting lot:', error)
        alert('Failed to delete lot')
      })
    },
    addLot() {
      this.$router.push('/admin_addlot')
    },
    viewspot(spot_id) {
      this.$router.push(`/admin_viewspot/${spot_id}`)
    },
  },
  mounted() {
    this.fetchLots()
  }
}
</script>
<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #0e1117, #1a1f2b);
  background-image: url('C:/Users/Muthukumar Natesan/Downloads/mad2_24f1000138/frontend/src/assets/admin_dash.png'); 
  background-size: cover;
  background-position: center;
  padding: 20px;
  font-family: 'Segoe UI', sans-serif;
  color: #f0f0f0;
}
.admin-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: rgba(0, 120, 212, 0.95);
  padding: 12px 24px;
  color: white;
  border-radius: 12px;
  margin-bottom: 24px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 600;
  transition: 0.3s ease;
}

.nav-links a:hover {
  text-decoration: underline;
  color: #a6e2ff;
}

.welcome {
  font-size: 18px;
  font-weight: bold;
}
.admin-dashboard-content {
  text-align: center;
  padding: 20px;
}

h2 {
  color: #ffffff;
  font-size: 28px;
  margin-bottom: 20px;
}

.lot-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.lot-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
  width: 300px;
  text-align: left;
}

.lot-card h3 {
  color: #00bfff;
  margin-bottom: 10px;
}

.lot-card p {
  color: #cfd3dc;
  margin: 6px 0;
  font-size: 14px;
}

.lot-card button {
  margin-right: 10px;
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  background-color: #0078d4;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: 0.2s ease;
}

.lot-card button:hover {
  background-color: #005fa3;
}

.spots {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  margin-top: 10px;
}
.spot-square {
  width: 32px;
  height: 32px;
  background-color: #2ecc71;
  border: 1px solid #2c3e50;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: black;
  border-radius: 4px;
  transition: transform 0.2s ease;
}

.spot-square:hover {
  transform: scale(1.1);
}

.spot-square.occupied {
  background-color: #e74c3c;
  color: white;
}

button {
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  background-color: #2ecc71;
  color: white;
  font-weight: bold;
  cursor: pointer;
  margin-top: 20px;
  transition: 0.3s ease;
}
button:hover {
  background-color: #27ae60;
}
</style>