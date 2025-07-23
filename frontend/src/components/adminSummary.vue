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
    <div class="admin-summary-content">
    <h2>Summary</h2>
    <div class="summary-graphs">
        <img :src="revenueGraph" alt="Revenue Graph">
        <img :src="availabilityGraph" alt="Availability Graph">
    </div>
</div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'AdminSummary',
  data() {
    return {
      revenueGraph: '',
      availabilityGraph: ''
    };
  },
  methods: {
    fetchSummaryGraphs() {
      const token = localStorage.getItem('token')
      axios.get('http://localhost:5000/admin_summary', {
        headers: {
          Authorization: `Bearer ${token}`
        },
        withCredentials: true
      })
        .then(response => {
          this.revenueGraph = 'http://localhost:5000'+ response.data.revenue_graph + '?t=' + new Date().getTime();
          this.availabilityGraph = 'http://localhost:5000'+ response.data.availability_graph + '?t=' + new Date().getTime();
        })
        .catch(error => {
          console.error('Error fetching summary graphs:', error);
        });
    }
  },
  mounted() {
    this.fetchSummaryGraphs();
  }
};
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
.admin-summary-content {
  max-width: 1000px;
  margin: auto;
  padding: auto;
  align-content: center;

}
.nav-links {
  display: flex;
  gap: 15px;
}

.nav-links a{
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.nav-links a:hover{
  text-decoration: underline;
}

h2 {
  color: #333;
  margin-bottom: 15px;
}
.summary-graphs {
  display: flex;
  flex-direction: row; 
  justify-content: center;
  gap: 20px;
  flex-wrap: nowrap; 
}

.summary-graphs img {
  width: 45%; 
  height: auto;
  border: 1px solid #ccc;
  padding: 10px;
  background: white;
  border-radius: 6px;
}
</style>