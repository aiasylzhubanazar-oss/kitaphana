/**
 * API утилиталары — backend-пен байланыс
 * Developer 2 жасайды
 */

const API_BASE = "http://localhost:8000/api";

/**
 * Жалпы fetch функциясы — барлық API сұраныстары осы арқылы өтеді
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;

  const config = {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Сервер қатесі" }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    if (response.status === 204) return null; // No content
    return await response.json();
  } catch (err) {
    console.error(`API қатесі [${endpoint}]:`, err.message);
    throw err;
  }
}

// ─── КІТАПТАР ────────────────────────────────────────────────

export const BooksAPI = {
  /** Барлық кітаптарды алу */
  getAll: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return apiRequest(`/books${query ? "?" + query : ""}`);
  },

  /** ID бойынша кітап */
  getById: (id) => apiRequest(`/books/${id}`),

  /** Кітап іздеу */
  search: (q) => apiRequest(`/books/search?q=${encodeURIComponent(q)}`),

  /** Жанрлар тізімі */
  getGenres: () => apiRequest("/genres"),

  /** Жаңа кітап қосу */
  create: (bookData) => apiRequest("/books", { method: "POST", body: JSON.stringify(bookData) }),
};

// ─── ПАЙДАЛАНУШЫЛАР ──────────────────────────────────────────

export const UsersAPI = {
  /** Тіркелу */
  register: (userData) =>
    apiRequest("/users/register", { method: "POST", body: JSON.stringify(userData) }),

  /** Кіру */
  login: (credentials) =>
    apiRequest("/users/login", { method: "POST", body: JSON.stringify(credentials) }),

  /** Профиль алу */
  getProfile: (userId) => apiRequest(`/users/${userId}`),
};

// ─── ОҚУ БАРЫСЫ ──────────────────────────────────────────────

export const ProgressAPI = {
  /** Пайдаланушының барысын алу */
  getUserProgress: (userId) => apiRequest(`/progress/${userId}`),

  /** Барысты жаңарту */
  update: (userId, bookId, data) =>
    apiRequest(`/progress/${userId}/${bookId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  /** Барысты жою */
  remove: (userId, bookId) =>
    apiRequest(`/progress/${userId}/${bookId}`, { method: "DELETE" }),
};

// ─── SESSION (жергілікті сақтау) ────────────────────────────

export const Session = {
  save: (userData) => localStorage.setItem("kitaphana_user", JSON.stringify(userData)),
  get: () => {
    try {
      return JSON.parse(localStorage.getItem("kitaphana_user"));
    } catch {
      return null;
    }
  },
  clear: () => localStorage.removeItem("kitaphana_user"),
  isLoggedIn: () => !!Session.get(),
};
