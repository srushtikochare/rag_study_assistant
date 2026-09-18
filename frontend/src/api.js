import axios from "axios";

const API_BASE = "http://localhost:8000";

export const uploadPDF = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return axios.post(`${API_BASE}/upload`, formData);
};

export const getDocuments = () => axios.get(`${API_BASE}/documents`);

export const askQuestion = (question) =>
  axios.post(`${API_BASE}/ask`, { question });

export const evaluateAnswer = (question) =>
  axios.post(`${API_BASE}/evaluate`, { question });
