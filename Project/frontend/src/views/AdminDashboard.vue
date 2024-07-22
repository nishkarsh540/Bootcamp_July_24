<template>
  <h2>This is the admin page</h2>
  <button @click="exportcsv">Download Report</button>
  <div>
    <h2>Manager Managing</h2>
    <table v-if="pendingManagers.length > 0">
      <thead>
        <tr>
          <th>Id</th>
          <th>Name</th>
          <th>Email</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="manager in pendingManagers" :key="manager.id">
          <td>{{ manager.id }}</td>
          <td>{{ manager.name }}</td>
          <td>{{ manager.email }}</td>
          <td>
            <button @click="confirmApproval(manager)">Approve</button>
            <button @click="confirmRejection(manager)">Reject</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-if="showConfirmationModal">
    <h2>{{ confirmationTitle }}</h2>
    <p>{{ confirmationMessage }}</p>
    <div>
      <button @click="handleConfirmation(true)">Confirm</button>
      <button @click="handleConfirmation(false)">Cancel</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      pendingManagers: [],
      showConfirmationModal: false,
      confirmationTitle: '',
      confirmationMessage: '',
      pendingManagerToHandle: null
    };
  },
  created() {
    this.fetchPendingManagers();
  },
  methods: {
    async fetchPendingManagers() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/managers');
        this.pendingManagers = response.data;
        console.log(response.data);
        console.log(this.pendingManagers);
      } catch (error) {
        console.log(error);
      }
    },
    async handleManagerAction(managerId, status) {
      const data = {
        manager_id: managerId,
        status: status
      };
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/managers', data);
        console.log(response.data);
        this.fetchPendingManagers();
      } catch (error) {
        console.log(error);
      }
    },
    confirmApproval(manager) {
      this.pendingManagerToHandle = manager;
      this.confirmationTitle = 'Approve Manager';
      this.confirmationMessage = `Approve ${manager.name}'s manager request?`;
      this.showConfirmationModal = true;
    },
    confirmRejection(manager) {
      this.pendingManagerToHandle = manager;
      this.confirmationTitle = 'Reject Manager';
      this.confirmationMessage = `Reject ${manager.name}'s manager request?`;
      this.showConfirmationModal = true;
    },
    handleConfirmation(isConfirmed) {
      if (isConfirmed) {
        if (this.confirmationTitle === 'Approve Manager') {
          this.handleManagerAction(this.pendingManagerToHandle.id, 'approve');
        } else if (this.confirmationTitle === 'Reject Manager') {
          this.handleManagerAction(this.pendingManagerToHandle.id, 'reject');
        }
      }
      this.showConfirmationModal = false;
      this.confirmationTitle = '';
      this.confirmationMessage = '';
      this.pendingManagerToHandle = null;
    },
    exportcsv(){
      const accessToken = localStorage.getItem('token');
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios.post('http://127.0.0.1:5000/exportcsv/1',{},{headers,
        responseType:'blob'
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const downloadLink = document.createElement('a');
        downloadLink.href=url;
        downloadLink.setAttribute('download','category_report.csv');
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      }
      )
      .catch(error => {
        console.error(error);
      });
    }
  }
};
</script>
