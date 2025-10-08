import axios from "axios";

const API_BASE = "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
});

// Login
export const login = async (username, password) => {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const res = await api.post("/auth/login", formData, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return res.data;
};


// Register
export const register = async (username, password, email) => {
  const payload = { username, password };
  if (email) payload.email = email;

  const res = await api.post("/auth/register", payload);
  return res.data; // { id, username, email, created_at }
};

// ---- DATASETS ----
export const getUserCollections = async (token) => {
  const res = await api.get("/datasets/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};

export const searchDatasets = async (query) => {
  const res = await api.get("/search", { params: { query } });
  return res.data;
};

export const importDataset = async (ref, token) => {
  const res = await api.post(
    `/datasets/import?dataset_ref=${ref}`,
    {},
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return res.data;
};

export const addToPostgres = async (ref, token) => {
  const res = await api.post(
    `/datasets`,
    { dataset_ref: ref },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return res.data;
};
