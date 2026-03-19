import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Applications API
export const applicationsAPI = {
  list: (params?: {
    type?: string;
    category?: string;
    search?: string;
    page?: number;
    page_size?: number;
    sort_by?: string;
  }) => api.get('/api/v1/applications/', { params }),

  get: (appId: string) => api.get(`/api/v1/applications/${appId}`),

  create: (data: {
    name: string;
    display_name: string;
    description: string;
    category: string;
    type: string;
  }) => api.post('/api/v1/applications/', data),
};

// Versions API
export const versionsAPI = {
  upload: (formData: FormData) => {
    return api.post('/api/v1/versions/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  getAudit: (versionId: string) =>
    api.get(`/api/v1/versions/${versionId}/audit`),
};

// Installations API
export const installationsAPI = {
  install: (appId: string) =>
    api.post('/api/v1/installations/install', { app_id: appId }),

  list: () => api.get('/api/v1/installations/my'),

  uninstall: (installationId: string) =>
    api.delete(`/api/v1/installations/${installationId}`),
};

export default api;
