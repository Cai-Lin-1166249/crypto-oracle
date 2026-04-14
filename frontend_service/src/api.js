import axios from "axios";

const API = axios.create({
  // baseURL: "http://127.0.0.1/api"
  baseURL: "https://realtime-crypto.xyz/"
});

export default API;