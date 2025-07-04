const API_BASE_URL = 'http://localhost:5000/api';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
};

export const api = {
  // Feedback endpoints
  async getFeedback() {
    const response = await fetch(`${API_BASE_URL}/feedback`, {
      headers: getAuthHeaders()
    });
    return response.json();
  },

  async submitFeedback(feedback: any) {
    const response = await fetch(`${API_BASE_URL}/feedback`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(feedback)
    });
    return response.json();
  },

  async updateFeedback(id: number, feedback: any) {
    const response = await fetch(`${API_BASE_URL}/feedback/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(feedback)
    });
    return response.json();
  },

  async acknowledgeFeedback(id: number) {
    const response = await fetch(`${API_BASE_URL}/feedback/${id}/acknowledge`, {
      method: 'POST',
      headers: getAuthHeaders()
    });
    return response.json();
  },

  // User endpoints
  async getTeamMembers() {
    const response = await fetch(`${API_BASE_URL}/users/team`, {
      headers: getAuthHeaders()
    });
    return response.json();
  },

  async getDashboardStats() {
    const response = await fetch(`${API_BASE_URL}/dashboard/stats`, {
      headers: getAuthHeaders()
    });
    return response.json();
  }
};