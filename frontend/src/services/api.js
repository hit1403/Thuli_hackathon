import axios from 'axios';
import { getBaseURL, API_CONFIG } from './config';

// Create axios instance with dynamic base URL
const createApiInstance = (baseURL) => {
  return axios.create({
    baseURL: baseURL,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  });
};

// Default API instance
let api = createApiInstance(getBaseURL());

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.message);
    if (error.response) {
      console.error('Error Status:', error.response.status);
      console.error('Error Data:', error.response.data);
    } else if (error.request) {
      console.error('Network Error - No response received');
      console.error('Request config:', error.config);
    }
    return Promise.reject(error);
  }
);

// Function to update API instance with working URL
export const updateApiBaseURL = (workingURL) => {
  console.log(`Updating API base URL to: ${workingURL}`);
  api = createApiInstance(workingURL);
  
  // Re-add interceptors
  api.interceptors.request.use(
    (config) => {
      console.log(`API Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
      return config;
    },
    (error) => {
      console.error('API Request Error:', error);
      return Promise.reject(error);
    }
  );

  api.interceptors.response.use(
    (response) => {
      console.log(`API Response: ${response.status} ${response.config.url}`);
      return response;
    },
    (error) => {
      console.error('API Response Error:', error.response?.status, error.message);
      return Promise.reject(error);
    }
  );
};

// API service methods
export const apiService = {
  // Get quiz items
  getQuizItems: async (count = 20) => {
    try {
      const response = await api.get(`/quiz/items?count=${count}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching quiz items:', error);
      throw error;
    }
  },

  // Submit quiz feedback
  submitQuizFeedback: async (feedback) => {
    try {
      const response = await api.post('/quiz/feedback', feedback);
      return response.data;
    } catch (error) {
      console.error('Error submitting quiz feedback:', error);
      throw error;
    }
  },

  // Get recommendations with serendipity
  getRecommendations: async (likedIds, serendipity = 0.5, limit = 20) => {
    try {
      const response = await api.post('/recommendations', {
        liked_ids: likedIds,
        serendipity: serendipity,
        limit: limit
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      throw error;
    }
  },

  // Get capsule wardrobe (with extended timeout)
  getCapsule: async (likedIds, budget = 8) => {
    try {
      const response = await api.post('/capsule', {
        liked_ids: likedIds,
        budget: budget
      }, {
        timeout: 30000 // 30 seconds for capsule optimization
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching capsule:', error);
      throw error;
    }
  },

  // Get item details
  getItemDetails: async (itemId) => {
    try {
      const response = await api.get(`/item/${itemId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching item details:', error);
      throw error;
    }
  }
};

export default apiService;
