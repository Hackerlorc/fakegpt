/**
 * EduMind - Lightweight, High-Performance Application Core
 * Zero-lag, zero infinite loops, zero particles.
 * Includes ThemeManager (Dark / Light switcher).
 */

(function (window, document) {
  'use strict';

  const EduMind = window.EduMind || {};

  /* ==========================================================================
     1. THEME MANAGER (DARK / LIGHT READY)
     ========================================================================== */
  const ThemeManager = {
    init() {
      const savedTheme = localStorage.getItem('edumind_theme') || 'dark';
      this.apply(savedTheme, false);

      document.addEventListener('click', (e) => {
        const toggleBtn = e.target.closest('[data-action="toggle-theme"]');
        if (toggleBtn) {
          e.preventDefault();
          this.toggle();
        }
      });
    },

    apply(theme, showToast = false) {
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('edumind_theme', theme);
      this.updateIcons(theme);

      if (showToast && Toast) {
        Toast.info(theme === 'light' ? 'Đã bật chế độ Sáng' : 'Đã bật chế độ Tối');
      }
    },

    toggle() {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      this.apply(next, true);
    },

    updateIcons(theme) {
      document.querySelectorAll('[data-action="toggle-theme"]').forEach((btn) => {
        const isDark = theme === 'dark';
        btn.setAttribute('title', isDark ? 'Chuyển sang chế độ Sáng' : 'Chuyển sang chế độ Tối');
        btn.setAttribute('aria-label', isDark ? 'Chuyển sang chế độ Sáng' : 'Chuyển sang chế độ Tối');

        if (isDark) {
          // Show Sun Icon (click to switch to Light)
          btn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="4"/>
              <path d="M12 2v2"/><path d="M12 20v2"/>
              <path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/>
              <path d="M2 12h2"/><path d="M20 12h2"/>
              <path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>
            </svg>
          `;
        } else {
          // Show Moon Icon (click to switch to Dark)
          btn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
            </svg>
          `;
        }
      });
    }
  };

  /* ==========================================================================
     2. TOAST NOTIFICATION SYSTEM
     ========================================================================== */
  const Toast = {
    _container: null,

    _getContainer() {
      if (!this._container) {
        this._container = document.querySelector('.toast-container');
        if (!this._container) {
          this._container = document.createElement('div');
          this._container.className = 'toast-container';
          document.body.appendChild(this._container);
        }
      }
      return this._container;
    },

    show(message, type = 'info', duration = 2500) {
      const container = this._getContainer();
      const el = document.createElement('div');
      el.className = `toast toast-${type}`;
      
      let icon = '•';
      if (type === 'success') icon = '✓';
      if (type === 'error') icon = '✕';
      if (type === 'warning') icon = '!';

      el.innerHTML = `
        <span style="font-weight:700; color:${type === 'success' ? 'var(--success)' : type === 'error' ? 'var(--danger)' : 'var(--primary-light)'}">${icon}</span>
        <span>${message}</span>
      `;
      container.appendChild(el);

      setTimeout(() => {
        el.style.opacity = '0';
        el.style.transition = 'opacity 0.2s ease';
        setTimeout(() => el.remove(), 200);
      }, duration);
    },

    success(msg) { this.show(msg, 'success'); },
    error(msg) { this.show(msg, 'error'); },
    info(msg) { this.show(msg, 'info'); },
    warning(msg) { this.show(msg, 'warning'); }
  };

  /* ==========================================================================
     3. SIDEBAR NAVIGATION CONTROLLER
     ========================================================================== */
  const Sidebar = {
    init() {
      const sidebar = document.getElementById('sidebar');
      const toggleBtn = document.getElementById('sidebarMobileToggle') || document.querySelector('.sidebar-mobile-toggle');
      const closeBtn = document.getElementById('sidebarCloseBtn') || document.querySelector('.sidebar-close-btn');
      const backdrop = document.getElementById('sidebarBackdrop') || document.querySelector('.sidebar-backdrop');

      if (!sidebar) return;

      const open = () => {
        sidebar.classList.add('open');
        backdrop?.classList.add('active');
        document.body.style.overflow = 'hidden';
      };

      const close = () => {
        sidebar.classList.remove('open');
        backdrop?.classList.remove('active');
        document.body.style.overflow = '';
      };

      toggleBtn?.addEventListener('click', (e) => {
        e.stopPropagation();
        open();
      });

      closeBtn?.addEventListener('click', close);
      backdrop?.addEventListener('click', close);

      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && sidebar.classList.contains('open')) {
          close();
        }
      });
    }
  };

  /* ==========================================================================
     4. MODAL CONTROLLER
     ========================================================================== */
  const Modal = {
    init() {
      document.querySelectorAll('[data-modal-target]').forEach((trigger) => {
        trigger.addEventListener('click', (e) => {
          e.preventDefault();
          const targetId = trigger.getAttribute('data-modal-target');
          const modal = document.getElementById(targetId);
          if (modal) modal.classList.add('active', 'open');
        });
      });

      document.querySelectorAll('.modal-overlay, .review-modal-overlay, .results-modal-overlay').forEach((overlay) => {
        overlay.addEventListener('click', (e) => {
          if (e.target === overlay) {
            overlay.classList.remove('active', 'open');
          }
        });
      });

      document.querySelectorAll('.modal-close-btn, .modal-close-icon-btn, [data-action="close-modal"]').forEach((btn) => {
        btn.addEventListener('click', () => {
          const overlay = btn.closest('.modal-overlay, .review-modal-overlay, .results-modal-overlay');
          if (overlay) overlay.classList.remove('active', 'open');
        });
      });
    }
  };

  /* ==========================================================================
     5. AUTH STATE & LOGOUT
     ========================================================================== */
  const Auth = {
    init() {
      const user = this.getUser();
      this.syncUI(user);

      // Hook live Firebase Auth changes
      const hookFirebase = (fb) => {
        if (!fb || typeof fb.onAuthStateChanged !== 'function') return;
        fb.onAuthStateChanged((authData) => {
          if (authData && authData.user) {
            const u = authData.user;
            const p = authData.profile;
            const displayName = p?.name || p?.displayName || u.displayName || u.email?.split('@')[0] || 'Học viên';
            const initials = displayName.split(' ').filter(Boolean).map(x => x[0]).join('').substring(0, 2).toUpperCase() || 'HV';
            const userRole = (u.email === 'admin@edumind.ai' || p?.role === 'admin') ? 'admin' : (p?.role || 'student');
            this.syncUI({
              name: displayName,
              email: u.email,
              role: userRole,
              initials
            });
          }
        });
      };

      if (window.EduMindFirebase) {
        hookFirebase(window.EduMindFirebase);
      } else {
        window.addEventListener('edumind:firebase-ready', (e) => hookFirebase(e.detail));
      }

      document.addEventListener('click', async (e) => {
        const logoutBtn = e.target.closest('.user-profile-logout');
        if (logoutBtn) {
          e.preventDefault();
          if (window.EduMindFirebase) {
            await window.EduMindFirebase.logout();
          } else {
            localStorage.removeItem('edumind_user');
          }
          if (Toast) Toast.info('Đã đăng xuất tài khoản');
          setTimeout(() => {
            window.location.href = 'auth.html';
          }, 400);
        }
      });
    },

    getUser() {
      try {
        return JSON.parse(localStorage.getItem('edumind_user'));
      } catch {
        return null;
      }
    },

    syncUI(user) {
      // 1. RBAC: Only show Admin menu items for Admin role
      const isAdmin = user && (user.role === 'admin' || user.email === 'admin@edumind.ai');
      document.querySelectorAll('[data-role="admin"], a[href="admin.html"]').forEach(el => {
        const item = el.closest('.nav-item') || el;
        item.style.display = isAdmin ? '' : 'none';
      });

      if (!user) return;
      const name = user.name || (user.email ? user.email.split('@')[0] : 'Học viên');
      const initials = user.initials || name.split(' ').filter(Boolean).map(x => x[0]).join('').substring(0, 2).toUpperCase() || 'HV';

      document.querySelectorAll('.user-profile-name').forEach(el => el.textContent = name);
      document.querySelectorAll('.user-avatar-circle, .user-avatar, .avatar').forEach(el => {
        el.textContent = initials;
      });
      document.querySelectorAll('.user-profile-role').forEach(el => {
        if (isAdmin) el.textContent = 'Quản trị viên';
        else if (user.role === 'teacher') el.textContent = 'Giáo viên bộ môn';
        else el.textContent = user.plan ? `Học viên • ${user.plan}` : 'Học viên';
      });
      const greetingSub = document.querySelector('.greeting-title .user-name');
      if (greetingSub) {
        greetingSub.textContent = name.split(' ').pop() || name;
      } else {
        const fullGreeting = document.querySelector('.greeting-title');
        if (fullGreeting) fullGreeting.textContent = `Xin chào, ${name.split(' ').pop() || name}`;
      }
    }
  };

  /* ==========================================================================
     6. INIT ON LOAD
     ========================================================================== */
  function init() {
    ThemeManager.init();
    Sidebar.init();
    Modal.init();
    Auth.init();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Export
  EduMind.theme = ThemeManager;
  EduMind.toast = Toast;
  EduMind.sidebar = Sidebar;
  EduMind.modal = Modal;
  EduMind.auth = Auth;
  window.EduMind = EduMind;

})(window, document);
