<template>
  <div class="admin-dashboard">
    <nav class="admin-nav">
        <span class="welcome">Welcome Admin</span>
        <div class="nav-links">
            <router-link to="/">Home</router-link>
            <router-link to="/admin_users">Users</router-link>
            <router-link to="/admin_search">Search</router-link>
            <router-link to="/admin_summary">Summary</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
        <span><router-link to="/admin_profile" class="edit-profile">Edit Profile</router-link></span>
    </nav>
    <div class="admin-dashboard-content">
    <h2>Parking Lots</h2>
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
        }
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
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
}

.admin-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #0074d9;
  padding: 10px 20px;
  color: white;
  border-radius: 8px;
  margin-bottom: 20px;
}
.admin-dashboard-content {
  max-width: 400px;
  margin: auto;
  padding: auto;
  align-content: center;

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

.lot-card {
  background-color: white;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  width:100%;
  max-width: 300px;
}

.lot-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #0074d9;
}

.lot-card button {
  margin-right: 10px;
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
  background-color: #0074d9;
  color: white;
  cursor: pointer;
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
  width: 30px;
  height: 30px;
  background-color: lightgreen;
  border: 1px solid #333;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-weight: bold;
  font-size: 16px;
}
.spot-square:hover {
  transform: scale(1.1);
}
.spot-square.occupied {
  background-color: tomato;
  color: white;
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
</style>
