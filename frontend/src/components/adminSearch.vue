<template>
  <div class="admin-search">
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
    <div class="content">
        <label>Search By</label>
        <select v-model="searchBy" @change="fetchResults">
            <option value="location">Location</option>
            <option value="user">User ID</option>
            <option value="spot">Spot ID</option>
        </select>
        <input v-model="searchQuery" placeholder="Search string" />
      <button @click="fetchResults">Search</button>
    </div>
    <button @click="refreshResults" class="refresh-button">Refresh</button>
    <div v-if="results.length > 0  && searchBy === 'location'" class="results">
        <h3>Example search parking lots @{{ submittedQuery }} location</h3>
        <div v-for="res in results" :key="res.lot_id" class="result-item">
            <h4>{{ res.name }}</h4>
      <span><button @click="editLot(res.lot_id)">Edit</button>
      <button disabled>Delete</button></span>
      <p>Occupied: {{ res.occupied }} / {{ res.num }}</p>
      <p>--------------------------------------------</p>
      <div class="spots">
        <div v-for="spot in res.spots" :key="spot.spot_id" class="spot-square" :class="{ occupied: spot.status === 'O'}" @click="viewspot(spot.spot_id)">
          <span>{{ spot.status }}</span>
        </div>
      </div>
        </div>
    </div>
    <div v-if="results.length > 0 && searchBy === 'user'" class="results">
        <h3>Example search user @{{ submittedQuery }}</h3>
        <div v-for="res in results" :key="res.user_id" class="result-item">
            <h4>User ID: {{ res.u_id }}</h4>
            <p>Name: {{ res.name }}</p>
            <p>Email: {{ res.email }}</p>
            <p>Address: {{ res.addr }}</p>
            <p>Pin Code: {{ res.pin }}</p>
        </div>
    </div>
    <div v-if="results.length > 0 && searchBy === 'spot'" class="results">
        <h3>Example search spot @{{ submittedQuery }}</h3>
        <div v-for="res in results" :key="res.spot_id" class="result-item">
            <h4>Spot ID: {{ res.spot_id }}</h4>
            <p>Location ID: {{ res.lot_id }}</p>
            <p>Location Name: {{ res.lot_name }}</p>
            <p>Status: {{ res.status }}</p>
            <p>Reserved Count: {{ res.r_count }}</p>
        </div>
    </div>
    <div v-if="results.length === 0" class="no-results">
        <p>Refresh</p>
    </div>
  </div>
  
</template>

<script>
export default {
  name: 'AdminSearch',
  data() {
    return {
      searchBy: 'location',
      searchByOptions: ['location', 'user', 'spot'],
      searchQuery: '',
      submittedQuery: '',
      results: []
    };
  },
  methods: {
    fetchResults() {
      if (!this.searchQuery.trim()) {
        this.results = []
        this.submittedQuery = ''
        return
      }

      this.submittedQuery = this.searchQuery.trim()
      const token = localStorage.getItem('token');
      const searchBy = this.searchBy || 'location';
      const url = `http://localhost:5000/admin_search?searchBy=${searchBy}&query=${this.searchQuery}`;

      fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        credentials: 'include'
      })
      .then(response => response.json())
      .then(data => {
        this.results = data;
      })
      .catch(error => {
        console.error('Error fetching results:', error);
      });
    },
    editLot(lotId) {
      this.$router.push(`/admin_editlot/${lotId}`);
    },
    viewspot(spotId) {
      this.$router.push(`/admin_viewspot/${spotId}`);
    },
    refreshResults() {
      this.searchQuery = '';
      this.results = [];
  }
  },
  mounted() {
    this.fetchResults();
  }
};
</script>

<style scoped>
.admin-search {
  font-family: 'Segoe UI', sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #0e1117, #1a1f2b);
  background-image: url('/admin_dash.png'); 
  background-size: cover;
  background-position: center;
  color: #ffffff;
  padding: 20px;
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

.welcome {
  font-weight: bold;
  font-size: 18px;
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

.content {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin-bottom: 20px;
}

.content label {
  color: #cfcfcf;
}

.content input,
.content select {
  padding: 10px;
  border-radius: 6px;
  border: none;
  background-color: #1e2430;
  color: white;
  min-width: 200px;
}

.content input:focus,
.content select:focus {
  outline: 2px solid #34C759;
}

.content button {
  padding: 10px 16px;
  border-radius: 6px;
  border: none;
  background-color: #2ecc71;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s ease;
}

.content button:hover {
  background-color: #27ae60;
}

.results {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
  border-radius: 12px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
}

.result-item {
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px dashed #aaa;
}

.result-item h4 {
  color: #00bfff;
}

.result-item p {
  color: #ddd;
  font-size: 14px;
}

.spots {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.spot-square {
  width: 35px;
  height: 35px;
  border-radius: 5px;
  background-color: #2ecc71;
  border: 1px solid #2c3e50;
  text-align: center;
  line-height: 35px;
  font-weight: bold;
  color: black;
  transition: transform 0.2s ease;
  cursor: pointer;
}

.spot-square:hover {
  transform: scale(1.1);
}

.spot-square.occupied {
  background-color: #e74c3c;
  color: white;
}
.result-item span button {
  margin-right: 10px;
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  background-color: #0078d4;
  color: white;
  cursor: pointer;
  font-weight: bold;
}

.result-item span button:last-child {
  background-color: #cccccc;
  cursor: not-allowed;
}

.result-item span button:hover {
  filter: brightness(1.1);
}
.no-results {
  margin-top: 30px;
  text-align: center;
  font-weight: bold;
  color: #888;
}

.refresh-button {
  margin-top: 20px;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  background-color: #007bff;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s ease;
}

.refresh-button:hover {
  background-color: #0056b3;
}
</style>
