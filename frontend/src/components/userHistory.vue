<template>
  <div class="user-dashboard">
    <nav class="user-nav">
        <span class="welcome">Welcome {{ userName }}</span>
        <div class="nav-links">
            <router-link to="/user_dashboard">Home</router-link>
            <router-link to="/user_history">History</router-link>
            <router-link to="/user_summary">Summary</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
        <span class="edit-profile"><router-link to="/user_profile">Edit Profile</router-link></span>
    </nav>
    <div class="users-content">
    <h2>Full User History</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Location</th>
          <th>Vehicle Number</th>
          <th>Start Time</th>
          <th>End Time</th>
          <th>Cost</th>
          <th>Payment Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="spot in rspots" :key="spot.r_id">
          <td>{{ spot.r_id }}</td>
          <td>{{ spot.loc }}</td>
          <td>{{ spot.veh_no }}</td>
          <td>{{ spot.start_time }}</td>
          <td>{{ spot.end_time }}</td>
          <td>{{ spot.cost }}</td>
          <td>
            <span v-if="spot.payment === 'Paid'" style="color: green;">Paid</span>
            <span v-else style="color: red;" @click="showQRCode(spot.r_id)">Pay Now</span>
          </td>
        </tr>
      </tbody>
    </table>
    <button @click="triggerCSV">Trigger and Download (CSV)</button>

    </div>
    

    <div v-if="showQRCodeModal" class="qr-code-modal">
      <div class="qr-code-content">
        <h3>Scan QR Code to Pay</h3>
        <img :src="qrCodeUrl" alt="QR Code" />
        <button @click="closeQRCode">Close</button>
      </div>
    </div>
  </div>
</template> 

<script>
import axios from 'axios'

export default {
  name: 'UserHistory',
  data() {
    return {
      rspots: [],
      showQRCodeModal: false,
      qrCodeUrl: ''
    }
  },
  methods: {   
    async fetchHistory() {
      const token = localStorage.getItem('token')
      const response = await axios.get('http://localhost:5000/user_history', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        withCredentials: true
      })
      this.rspots = response.data
      this.rspots.forEach(spot => {
        spot.start_time = new Date(spot.start_time).toLocaleString()
        spot.end_time = new Date(spot.end_time).toLocaleString()
      })
    },
    async triggerCSV() {
      const userId = this.rspots[0].u_id
  try {
    const res = await fetch(`http://localhost:5000/trigger_csv/${userId}`, {
      method: 'POST',
      headers: {
        Authorization: 'Bearer ' + localStorage.getItem('token'),
      },
    });
    const data = await res.json();
    alert(data.message);

    let attempts = 0;
    const maxAttempts = 10;
    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
    let fileReady = false;

    while (attempts < maxAttempts && !fileReady) {
      await delay(3000); 
      const check = await fetch(`http://localhost:5000/check_csv/${userId}`, {
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('token'),
        },
      });
      const status = await check.json();
      if (status.ready) {
        fileReady = true;
        break;
      }
      attempts++;
    }
    if (fileReady) {
      window.open(`http://localhost:5000/download_csv/${userId}`, '_blank');
    } else {
      alert("CSV not ready. Please try again later.");
    }
  } catch (err) {
    console.error('Error:', err);
  }
    },
    showQRCode(r_id) {
    this.qrCodeUrl = `http://localhost:5000/generate_qr/${r_id}`
    this.showQRCodeModal = true
  },

  closeQRCode() {
    this.showQRCodeModal = false
    this.qrCodeUrl = ''
  }
  },
  mounted() {
    this.fetchHistory()
  },
  computed: {
    userName() {
      return this.rspots.length > 0 ? this.rspots[0].name : 'User';
    }
  }
}
</script>

<style scoped>
.user-dashboard {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-image: url('/user_dash.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 20px;
  min-height: 100vh;
  color: #2c3e50;
}

.user-nav {
  background-color: rgba(45, 62, 80, 0.9);
  padding: 12px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 10px;
  margin-bottom: 30px;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.user-nav .welcome {
  font-size: 1.2rem;
  font-weight: bold;
  color: #f6b93b;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a,
.edit-profile a {
  color: #f0f8ff;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.2s;
}

.nav-links a:hover,
.edit-profile a:hover {
  color: #ffd700;
}

.edit-profile a {
  margin-left: 20px;
}

.users-content {
  background-color: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  max-width: 1200px;
  margin: auto;
}

h2 {
  color: #2d3e50;
  text-align: center;
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  background-color: #ffffffc2;
}

th {
  background-color: #34495e;
  color: white;
  padding: 12px;
  text-align: left;
}

td {
  padding: 12px;
  border-bottom: 1px solid #ccc;
  color: #2c3e50;
  background-color: #fcfcfc;
}

tbody tr:nth-child(even) td {
  background-color: #f3f3f3;
}

td span {
  font-weight: bold;
  cursor: pointer;
}

td span[style*="green"] {
  background-color: #eafaf1;
  padding: 6px 10px;
  border-radius: 6px;
  color: #2e7d32;
}

td span[style*="red"] {
  background-color: #fdecea;
  padding: 6px 10px;
  border-radius: 6px;
  color: #c0392b;
}

button {
  padding: 10px 18px;
  border-radius: 6px;
  border: none;
  background-color: #2ecc71;
  color: white;
  font-weight: bold;
  cursor: pointer;
  margin-top: 20px;
  display: block;
  margin-left: auto;
  margin-right: auto;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #27ae60;
}
.qr-code-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.qr-code-content {
  background-color: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  padding: 30px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
  color: #2c3e50;
}

.qr-code-content img {
  width: 200px;
  height: 200px;
  margin: 20px 0;
  border: 4px solid #2c3e50;
  border-radius: 8px;
}
</style>
