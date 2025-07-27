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
  font-family: 'Segoe UI', sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #0e1117, #1a1f2b);
  background-image: url('/frontend/public/admin_dash.png');
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

.admin-summary-content {
  max-width: 1000px;
  margin: auto;
  padding: 20px;
  text-align: center;
}

h2 {
  font-size: 28px;
  margin-bottom: 24px;
  color: #00bfff;
}
.summary-graphs {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}
.summary-graphs img {
  width: 45%;
  height: auto;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(6px);
  padding: 12px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}
.summary-graphs img:hover {
  transform: scale(1.02);
  transition: transform 0.3s ease;
}
</style>