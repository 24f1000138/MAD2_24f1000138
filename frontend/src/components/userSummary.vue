<template>
  <div class="user-dashboard">
    <nav class="user-nav">
        <span class="welcome">Welcome {{ name }}</span>
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
      msg: '',
      reservationGraph: '',
      name: ''
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
          this.name = response.data.name;
        })
        .catch(error => {
          console.error('Error fetching user summary:', error);
        });
    }
  },
  mounted() {
    this.fetchUserSummary();
  },
};
</script>

<style scoped>
.user-dashboard {
  background: url('/user_dash.png') no-repeat center center fixed;
  background-size: cover;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  padding: 20px;
}

.user-nav {
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(6px);
  padding: 12px 24px;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.user-nav .welcome {
  color: #f1c40f;
  font-weight: bold;
  font-size: 1.1rem;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.nav-links a:hover {
  text-decoration: underline;
}

.edit-profile a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.edit-profile a:hover {
  text-decoration: underline;
}

.users-content {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

h2 {
  color: #c7c4c4;
  text-align: center;
  margin-bottom: 20px;
}

.summary-graphs {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.summary-graphs img {
  max-width: 400px;
  width: 100%;
  height: auto;
  border-radius: 12px;
  border: 2px solid rgba(0, 0, 0, 0.2);
  background-color: white;
  padding: 10px;
}
</style>