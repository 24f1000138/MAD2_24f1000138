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
      <h2>User Summary</h2>
      <div class="summary-graphs">
        <img :src="reservationGraph" alt="Reservation Summary">
      </div>
    </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'UserSummary',
  data() {
    return {
      reservationGraph: ''
    };
  },
  methods: {
    fetchUserSummary() {
      const token = localStorage.getItem('token')
      axios.get('http://localhost:5000/user_summary', {
          headers: {
            Authorization: `Bearer ${token}`
          },
          withCredentials: true
        })
        .then(response => {
          this.reservationGraph = 'http://localhost:5000'+ response.data.reservation_graph + '?t=' + new Date().getTime();
        })
        .catch(error => {
          console.error('Error fetching user summary:', error);
        });
    }
  },
  mounted() {
    this.fetchUserSummary();
  }
};
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
}
</style>