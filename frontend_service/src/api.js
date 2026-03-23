import axios from "axios";

const API = axios.create({
  baseURL: "http://34.234.12.88:8010/api"
});

export default API;