import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000", // адрес main_server
});

export default api;
