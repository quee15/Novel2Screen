import axios from "axios";

const http = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 20000
});

export default http;
