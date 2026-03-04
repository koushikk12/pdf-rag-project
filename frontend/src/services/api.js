import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export const uploadPDF = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return API.post("/upload", formData);
};

export const processPDF = (filename) =>
  API.post(`/process/${filename}`);

export const askQuestion = (query) =>
  API.post("/ask", { query });