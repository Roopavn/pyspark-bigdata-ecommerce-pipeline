const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.status === 204 ? null : response.json();
}

export const api = {
  products: () => request("/products/"),
  product: (id) => request(`/products/${id}/`),
  categories: () => request("/categories/"),
  dashboard: () => request("/dashboard/"),
};
