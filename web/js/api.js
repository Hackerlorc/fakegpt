/**
 * EduMind AI - Unified Database API Client
 * Connects frontend directly to SQLite REST API (`/api/*`) on the server.
 */

const API_BASE = (typeof window !== 'undefined' && window.location && window.location.protocol.startsWith('http')) ? '' : 'http://localhost:8080';

export const EduMindAPI = {
  // 1. Auth & Users
  async login(email, password) {
    try {
      const res = await fetch(`${API_BASE}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        localStorage.setItem('edumind_user', JSON.stringify(data.user));
        return { success: true, user: data.user };
      }
      return { success: false, error: data.error || 'Đăng nhập thất bại.' };
    } catch (e) {
      return { success: false, error: 'Không thể kết nối đến máy chủ cơ sở dữ liệu.' };
    }
  },

  async register(email, password, name) {
    try {
      const res = await fetch(`${API_BASE}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, name })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        localStorage.setItem('edumind_user', JSON.stringify(data.user));
        return { success: true, user: data.user };
      }
      return { success: false, error: data.error || 'Đăng ký thất bại.' };
    } catch (e) {
      return { success: false, error: 'Lỗi kết nối cơ sở dữ liệu.' };
    }
  },

  async getUsers() {
    try {
      const res = await fetch(`${API_BASE}/api/users`);
      const data = await res.json();
      return data.users || [];
    } catch (e) {
      console.warn('API getUsers error:', e);
      return [];
    }
  },

  async addUser(userData) {
    try {
      const res = await fetch(`${API_BASE}/api/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      return await res.json();
    } catch (e) {
      return { success: false, error: e.message };
    }
  },

  async updateUser(uid, updateData) {
    try {
      const res = await fetch(`${API_BASE}/api/users/${uid}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updateData)
      });
      return await res.json();
    } catch (e) {
      return { success: false, error: e.message };
    }
  },

  async deleteUser(uid) {
    try {
      const res = await fetch(`${API_BASE}/api/users/${uid}`, {
        method: 'DELETE'
      });
      return await res.json();
    } catch (e) {
      return { success: false, error: e.message };
    }
  },

  async toggleUserLock(uid, currentStatus) {
    const nextStatus = currentStatus === 'active' ? 'locked' : 'active';
    return this.updateUser(uid, { status: nextStatus });
  },

  // 2. Quizzes & Questions
  async getQuizzes() {
    try {
      const res = await fetch(`${API_BASE}/api/quizzes`);
      const data = await res.json();
      return data.quizzes || [];
    } catch (e) {
      console.warn('API getQuizzes error:', e);
      return [];
    }
  },

  async createQuiz(quizData) {
    try {
      const res = await fetch(`${API_BASE}/api/quizzes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(quizData)
      });
      return await res.json();
    } catch (e) {
      return { success: false, error: e.message };
    }
  },

  // 3. Quiz Attempts (History)
  async getQuizAttempts(userId) {
    try {
      const url = userId ? `${API_BASE}/api/attempts?userId=${encodeURIComponent(userId)}` : `${API_BASE}/api/attempts`;
      const res = await fetch(url);
      const data = await res.json();
      return data.attempts || [];
    } catch (e) {
      console.warn('API getQuizAttempts error:', e);
      return [];
    }
  },

  async getAttempts(userId) {
    return this.getQuizAttempts(userId);
  },

  async saveQuizAttempt(attemptData) {
    try {
      const res = await fetch(`${API_BASE}/api/attempts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(attemptData)
      });
      return await res.json();
    } catch (e) {
      return { success: false, error: e.message };
    }
  },

  // 4. Knowledge Gaps
  async getKnowledgeGaps(userId) {
    try {
      const url = userId ? `${API_BASE}/api/knowledge-gaps?userId=${encodeURIComponent(userId)}` : `${API_BASE}/api/knowledge-gaps`;
      const res = await fetch(url);
      const data = await res.json();
      return data.gaps || [];
    } catch (e) {
      console.warn('API getKnowledgeGaps error:', e);
      return [];
    }
  },

  // 5. Roadmaps
  async getRoadmap(userId) {
    try {
      const url = userId ? `${API_BASE}/api/roadmap?userId=${encodeURIComponent(userId)}` : `${API_BASE}/api/roadmap`;
      const res = await fetch(url);
      const data = await res.json();
      return data.roadmap || null;
    } catch (e) {
      console.warn('API getRoadmap error:', e);
      return null;
    }
  },

  // 6. Chat Messages
  async getChatMessages() {
    try {
      const res = await fetch(`${API_BASE}/api/chat`);
      const data = await res.json();
      return data.messages || [];
    } catch (e) {
      console.warn('API getChatMessages error:', e);
      return [];
    }
  },

  async saveChatMessage(msgData) {
    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(msgData)
      });
      return await res.json();
    } catch (e) {
      return { success: false, error: e.message };
    }
  },

  async clearChat() {
    try {
      const res = await fetch(`${API_BASE}/api/chat/clear`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      return await res.json();
    } catch (e) {
      return { success: false, error: e.message };
    }
  },

  async askAI(question, apiKey = null) {
    try {
      const res = await fetch(`${API_BASE}/api/ai/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, apiKey })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        return data;
      }
      return null;
    } catch (e) {
      return null;
    }
  },

  // 7. Notes & Survey
  async getNotes(userId = 'local_user') {
    try {
      const res = await fetch(`${API_BASE}/api/notes?userId=${userId}`);
      const data = await res.json();
      return data.notes || '';
    } catch (e) {
      return '';
    }
  },

  async saveNotes(notes, userId = 'local_user') {
    try {
      const res = await fetch(`${API_BASE}/api/notes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, notes })
      });
      return await res.json();
    } catch (e) {
      return { success: false, error: e.message };
    }
  },

  async saveSurvey(survey, userId = 'local_user') {
    try {
      const res = await fetch(`${API_BASE}/api/survey`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, survey })
      });
      return await res.json();
    } catch (e) {
      return { success: false, error: e.message };
    }
  },

  // 8. Stats
  async getStats() {
    try {
      const res = await fetch(`${API_BASE}/api/stats`);
      const data = await res.json();
      return data.stats || {};
    } catch (e) {
      return {};
    }
  },

  async getUserStats(userId) {
    try {
      const res = await fetch(`${API_BASE}/api/user-stats?userId=${encodeURIComponent(userId)}`);
      const data = await res.json();
      return data.stats || null;
    } catch (e) {
      return null;
    }
  }
};

window.EduMindAPI = EduMindAPI;
export default EduMindAPI;
