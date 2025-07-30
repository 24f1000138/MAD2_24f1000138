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
    <div class="admin-users-content">
    <h2>Registered Users</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>Full Name</th>
          <th>Address</th>
          <th>Pin Code</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.u_id">
          <td>{{ user.u_id }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.addr }}</td>
          <td>{{ user.pin }}</td>
        </tr>
      </tbody>
    </table>
    <button @click="triggerCSV">Trigger (CSV)</button>
    </div>
  </div>
</template> 

<script>
import axios from 'axios'

export default {
  name: 'AdminUsers',
  data() {
    return {
      users: []
    }
  },
  methods: {   
    async fetchUsers() {
      const token = localStorage.getItem('token')
      const response = await axios.get('http://localhost:5000/admin_users', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        withCredentials: true
      })
      this.users = response.data
    },
    async triggerCSV() {
      const token = localStorage.getItem('token')
  try {
    const response = await fetch('http://localhost:5000/trigger_csv', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const data = await response.json();
    alert(data.message);
  } catch (err) {
    console.error('Error:', err);
  }
    }
  },
  mounted() {
    this.fetchUsers()
  }
}
</script>

<style scoped>
.admin-dashboard {
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

.admin-users-content {
  max-width: 1200px;
  margin: 40px auto;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.3);
}

h2 {
  font-size: 28px;
  margin-bottom: 24px;
  color: #00bfff;
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  text-align: left;
  color: #f5f5f5;
}

th, td {
  padding: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

thead {
  background-color: rgba(255, 255, 255, 0.1);
}

tbody tr:nth-child(even) {
  background-color: rgba(255, 255, 255, 0.05);
}

tbody tr:hover {
  background-color: rgba(0, 120, 212, 0.15);
}

button {
  padding: 12px 18px;
  background-color: #2ecc71;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s ease;
}

button:hover {
  background-color: #27ae60;
}

</style>
