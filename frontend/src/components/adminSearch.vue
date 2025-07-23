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
            <h4>User ID: {{ res.user_id }}</h4>
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
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        withCredentials: true
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
  background-color: #f9fafa;
  padding: 20px;
  min-height: 100vh;
}

.admin-nav {
  background-color: #d8f0e2;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 8px;
  margin-bottom: 20px;
}

.admin-nav .welcome {
  font-weight: bold;
  color: #e53935;
}

.nav-links a {
  margin-left: 15px;
  text-decoration: none;
  color: #2c3e50;
  font-weight: bold;
}

.nav-links a:hover {
  text-decoration: underline;
}

.content {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 20px;
}

.content input,
.content select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.content button {
  padding: 8px 14px;
  border: none;
  border-radius: 4px;
  background-color: #4caf50;
  color: white;
  cursor: pointer;
  font-weight: bold;
}

.content button:hover {
  background-color: #45a049;
}

.results {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.1);
}

.result-item {
  margin-bottom: 30px;
  border-bottom: 1px dashed #ccc;
  padding-bottom: 15px;
}

.result-item h4 {
  color: #2c3e50;
}

.result-item span button {
  margin-right: 10px;
  padding: 5px 12px;
  border: none;
  border-radius: 5px;
  background-color: #2196f3;
  color: white;
  cursor: pointer;
}

.result-item span button:last-child {
  background-color: #f44336;
}

.result-item span button:hover {
  opacity: 0.85;
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
  text-align: center;
  line-height: 35px;
  font-weight: bold;
  background-color: lightgreen;
  cursor: pointer;
  border: 1px solid #999;
}

.spot-square.occupied {
  background-color: lightcoral;
  color: white;
}

.no-results {
  margin-top: 30px;
  text-align: center;
  font-weight: bold;
  color: #777;
}
.refresh-button {
  margin-top: 20px;
  padding: 10px;
  background-color: #007BFF;
  color: white;
  font-weight: bold;
  cursor: pointer;
  display: block;
}
.refresh-button:hover {
  background-color: #0056b3;
}
</style>
