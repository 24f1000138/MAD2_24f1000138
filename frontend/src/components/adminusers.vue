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
  },
  mounted() {
    this.fetchUsers()
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  max-width: 100%;
  max-height: 100%;
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
.nav-links {
  display: flex;
  gap: 15px;
}

.nav-links a {
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
.admin-users-content {
  max-width: 1200px;
  margin: 40px auto;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
}
table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

th, td {
  padding: 12px;
  border: 1px solid #ccc;
}

thead {
  background-color: #eaf4ff;
}

tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}
</style>
