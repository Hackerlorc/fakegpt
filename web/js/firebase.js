/**
 * EduMind - Firebase Full Integration & Database Architecture Module
 * Connected to project: project-2940809306874456220
 * Integrates Firebase Auth, Cloud Firestore (Real Database), and Analytics.
 */

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-analytics.js";
import {
  getAuth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  signOut,
  onAuthStateChanged,
  updateProfile
} from "https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js";
import {
  getFirestore,
  doc,
  setDoc,
  getDoc,
  updateDoc,
  deleteDoc,
  collection,
  addDoc,
  getDocs,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

// User's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDkH5DVFSAeP3TByD4MzJu08HVQavpyTtU",
  authDomain: "project-2940809306874456220.firebaseapp.com",
  projectId: "project-2940809306874456220",
  storageBucket: "project-2940809306874456220.firebasestorage.app",
  messagingSenderId: "663871217998",
  appId: "1:663871217998:web:ee62d87c12f3dbacf6fe1f",
  measurementId: "G-P665JWJER4"
};

// Initialize Firebase Core
export const app = initializeApp(firebaseConfig);

let analytics = null;
try {
  analytics = getAnalytics(app);
} catch (e) {
  // Analytics may fail in sandboxes/non-browser
}

export const auth = getAuth(app);
export const db = getFirestore(app);
export const googleProvider = new GoogleAuthProvider();

/* ==========================================================================
   DEFAULT SEED DATASETS FOR CLOUD FIRESTORE COLLECTIONS
   ========================================================================== */

export const DEFAULT_SEED_USERS = [
  {
    id: "usr_001",
    name: "Phi Le Minh",
    email: "phi@example.com",
    role: "student",
    plan: "Pro",
    status: "active",
    lastActive: "Vừa xong",
    quizzes: 47,
    streak: 12
  },
  {
    id: "usr_002",
    name: "Nguyễn Hoàng Long",
    email: "long.nh@gmail.com",
    role: "student",
    plan: "Free",
    status: "active",
    lastActive: "2 giờ trước",
    quizzes: 18,
    streak: 5
  },
  {
    id: "usr_003",
    name: "ThS. Trần Thị Mai",
    email: "mai.tran@thpt-chuyen.edu.vn",
    role: "teacher",
    plan: "Pro",
    status: "active",
    lastActive: "Hôm qua",
    quizzes: 64,
    streak: 22
  },
  {
    id: "usr_004",
    name: "Lê Quốc Bảo",
    email: "bao.le@outlook.com",
    role: "student",
    plan: "Pro",
    status: "active",
    lastActive: "3 ngày trước",
    quizzes: 32,
    streak: 8
  },
  {
    id: "usr_005",
    name: "Phạm Thu Trang",
    email: "trang.pham@yahoo.com",
    role: "student",
    plan: "Free",
    status: "locked",
    lastActive: "12 ngày trước",
    quizzes: 4,
    streak: 0
  },
  {
    id: "usr_006",
    name: "Thầy Đỗ Quang Huy",
    email: "huy.do@supham.edu.vn",
    role: "teacher",
    plan: "Pro",
    status: "active",
    lastActive: "Hôm nay",
    quizzes: 95,
    streak: 30
  },
  {
    id: "usr_007",
    name: "Ngô Thanh Vân",
    email: "van.ngo@hotmail.com",
    role: "student",
    plan: "Free",
    status: "active",
    lastActive: "5 ngày trước",
    quizzes: 9,
    streak: 2
  },
  {
    id: "usr_008",
    name: "Vũ Đức Thành",
    email: "admin@edumind.ai",
    role: "admin",
    plan: "Pro",
    status: "active",
    lastActive: "Trực tuyến",
    quizzes: 120,
    streak: 45
  }
];

export const DEFAULT_QUIZZES = [
  {
    id: "quiz_toan_01",
    title: "Phương trình bậc hai & Định lý Viète",
    subject: "Toán học",
    grade: "10",
    difficulty: "Trung bình",
    durationMinutes: 30,
    questions: [
      {
        id: 1,
        text: "Phương trình x² - 5x + 6 = 0 có tập nghiệm S là:",
        options: ["S = {1; 6}", "S = {2; 3}", "S = {-2; -3}", "S = {3; -2}"],
        correctIndex: 1,
        explanation: "Theo định lý Viète: x₁ + x₂ = 5 và x₁ × x₂ = 6. Hai nghiệm là x = 2 và x = 3."
      },
      {
        id: 2,
        text: "Tìm m để phương trình x² - 2mx + m² - 1 = 0 luôn có 2 nghiệm phân biệt:",
        options: ["Mọi m ∈ ℝ", "m > 1", "m < 0", "Không có m nào"],
        correctIndex: 0,
        explanation: "Ta có Δ' = (-m)² - 1(m² - 1) = m² - m² + 1 = 1 > 0 với mọi m. Do đó phương trình luôn có 2 nghiệm phân biệt."
      },
      {
        id: 3,
        text: "Gọi x₁, x₂ là hai nghiệm của x² - 3x - 4 = 0. Giá trị biểu thức A = x₁² + x₂² là:",
        options: ["17", "25", "7", "9"],
        correctIndex: 0,
        explanation: "Theo Viète: x₁ + x₂ = 3, x₁ × x₂ = -4. Khi đó A = (x₁ + x₂)² - 2x₁x₂ = 3² - 2(-4) = 9 + 8 = 17."
      },
      {
        id: 4,
        text: "Phương trình 2x² + 5x + 2 = 0 có tích hai nghiệm bằng:",
        options: ["1", "2.5", "-1", "2"],
        correctIndex: 0,
        explanation: "Theo Viète, tích hai nghiệm P = c/a = 2/2 = 1."
      },
      {
        id: 5,
        text: "Cho phương trình x² - (m + 1)x + m = 0. Nghiệm của phương trình là:",
        options: ["x = 1 hoặc x = m", "x = -1 hoặc x = -m", "x = 1 hoặc x = -m", "x = 2 hoặc x = m"],
        correctIndex: 0,
        explanation: "Ta có a + b + c = 1 - (m + 1) + m = 0. Do đó luôn có nghiệm x₁ = 1 và x₂ = c/a = m."
      }
    ]
  },
  {
    id: "quiz_ly_01",
    title: "Lực tương tác tĩnh điện & Điện tích",
    subject: "Vật lý",
    grade: "11",
    difficulty: "Cơ bản",
    durationMinutes: 20,
    questions: [
      {
        id: 1,
        text: "Đơn vị của điện tích trong hệ đo lường quốc tế SI là:",
        options: ["Vôn (V)", "Ampe (A)", "Cu-lông (C)", "Oát (W)"],
        correctIndex: 2,
        explanation: "Đơn vị của điện tích trong hệ SI là Cu-lông, ký hiệu là C."
      },
      {
        id: 2,
        text: "Khi khoảng cách giữa hai điện tích điểm trong chân không tăng lên 2 lần thì độ lớn lực Cu-lông:",
        options: ["Tăng 2 lần", "Giảm 2 lần", "Tăng 4 lần", "Giảm 4 lần"],
        correctIndex: 3,
        explanation: "Lực tương tác tĩnh điện F tỉ lệ nghịch với bình phương khoảng cách r². Khi r tăng 2 thì F giảm 4."
      },
      {
        id: 3,
        text: "Hằng số điện môi của chân không có giá trị bằng:",
        options: ["1", "2", "8.85 × 10⁻¹²", "9 × 10⁹"],
        correctIndex: 0,
        explanation: "Trong chân không, hằng số điện môi ε = 1."
      }
    ]
  },
  {
    id: "quiz_hoa_01",
    title: "Phân loại Cacbohidrat & Glucozo",
    subject: "Hóa học",
    grade: "12",
    difficulty: "Trung bình",
    durationMinutes: 25,
    questions: [
      {
        id: 1,
        text: "Chất nào sau đây thuộc loại monosaccarit?",
        options: ["Saccarozo", "Tinh bột", "Xenlulozo", "Glucozo"],
        correctIndex: 3,
        explanation: "Monosaccarit là cacbohidrat đơn giản nhất không thể thủy phân được nữa, gồm Glucozo và Fructozo."
      },
      {
        id: 2,
        text: "Công thức phân tử của Glucozo là:",
        options: ["C₆H₁₂O₆", "C₁₂H₂₂O₁₁", "(C₆H₁₀O₅)n", "CH₂O"],
        correctIndex: 0,
        explanation: "Glucozo có công thức phân tử là C₆H₁₂O₆ (phân tử khối là 180)."
      }
    ]
  },
  {
    id: "quiz_anh_01",
    title: "Cấu trúc câu phức & Mệnh đề quan hệ",
    subject: "Tiếng Anh",
    grade: "12",
    difficulty: "Nâng cao",
    durationMinutes: 20,
    questions: [
      {
        id: 1,
        text: "The student _____ won the first prize studies in our class.",
        options: ["which", "who", "whom", "whose"],
        correctIndex: 1,
        explanation: "'The student' là người đóng vai trò chủ ngữ trong mệnh đề quan hệ, do đó ta dùng đại từ 'who'."
      }
    ]
  }
];

export const DEFAULT_KNOWLEDGE_GAPS = [
  {
    id: "gap_01",
    subject: "Vật lý",
    topic: "Điện từ học — Cảm ứng điện từ",
    accuracyPercent: 28,
    priority: "Cao",
    description: "Hay nhầm lẫn chiều dòng điện cảm ứng theo định luật Len-xơ."
  },
  {
    id: "gap_02",
    subject: "Toán học",
    topic: "Hình học không gian — Khoảng cách 2 đường thẳng",
    accuracyPercent: 35,
    priority: "Cao",
    description: "Chưa thành thạo dựng mặt phẳng song song chứa 1 đường thẳng."
  },
  {
    id: "gap_03",
    subject: "Toán học",
    topic: "Phương trình lượng giác chứa tham số",
    accuracyPercent: 42,
    priority: "Trung bình",
    description: "Cần rèn luyện thêm điều kiện nghiệm của phương trình bậc 2 theo sin/cos."
  },
  {
    id: "gap_04",
    subject: "Tiếng Anh",
    topic: "Cấu trúc câu phức & Mệnh đề quan hệ",
    accuracyPercent: 55,
    priority: "Trung bình",
    description: "Thường phân vân giữa which và that trong mệnh đề quan hệ không xác định."
  },
  {
    id: "gap_05",
    subject: "Hóa học",
    topic: "Kim loại kiềm thổ & Nước cứng",
    accuracyPercent: 62,
    priority: "Thấp",
    description: "Cần nhớ bảng phân biệt làm mềm nước cứng tạm thời và vĩnh cửu."
  }
];

export const DEFAULT_ROADMAP = {
  id: "roadmap_active",
  subject: "Toán học 10 • Đại số",
  currentLesson: "Phương trình bậc hai & Định lý Viète",
  progressPercent: 65,
  summary: "Bạn đã nắm vững cách tính biệt thức Δ, cần luyện thêm kỹ năng tìm tham số m.",
  nextMilestone: "Dấu của tam thức bậc hai & Bất phương trình",
  updatedAt: "Hôm nay"
};

export const DEFAULT_ATTEMPTS = [
  {
    id: "att_01",
    title: "Phương trình bậc hai & Viète",
    subject: "Toán học",
    score: 9.0,
    total: 10,
    timeSpent: "14:20",
    completedAt: "Hôm nay"
  },
  {
    id: "att_02",
    title: "Lực tương tác tĩnh điện & Điện tích",
    subject: "Vật lý",
    score: 7.5,
    total: 10,
    timeSpent: "22:10",
    completedAt: "23/10/2026"
  },
  {
    id: "att_03",
    title: "Phân loại Cacbohidrat & Glucozo",
    subject: "Hóa học",
    score: 8.5,
    total: 10,
    timeSpent: "18:45",
    completedAt: "21/10/2026"
  },
  {
    id: "att_04",
    title: "Đại cương về Dao động điều hòa",
    subject: "Vật lý",
    score: 5.0,
    total: 10,
    timeSpent: "28:10",
    completedAt: "18/10/2026"
  }
];

export const DEFAULT_CHAT_MESSAGES = [
  {
    id: "msg_01",
    sender: "Study Coach",
    isAi: true,
    text: "Chào em! Hôm nay chúng ta tiếp tục với phần Định lý Viète nhé. Em hãy nhớ lại xem: nếu phương trình bậc hai ax² + bx + c = 0 có hai nghiệm x₁ và x₂, thì tổng và tích của chúng được tính như thế nào?",
    socraticHint: "Hãy nhớ đến công thức liên hệ giữa các hệ số a, b, c với (x₁ + x₂) và (x₁ × x₂)."
  },
  {
    id: "msg_02",
    sender: "Bạn",
    isAi: false,
    text: "Dạ, x1 + x2 = -b/a và x1 * x2 = c/a ạ."
  },
  {
    id: "msg_03",
    sender: "Study Coach",
    isAi: true,
    text: "Rất chính xác! Bây giờ giả sử thầy có phương trình x² - 5x + 6 = 0. Không cần tính Δ, em có thể nhẩm ra hai số nào có tổng bằng 5 và tích bằng 6 không?",
    socraticHint: "Tìm hai số nguyên dương nhỏ mà tích bằng 6 (ví dụ: 1 và 6, hoặc 2 và 3)."
  }
];

/* ==========================================================================
   AUTHENTICATION & USER PROFILE CONTROLLER
   ========================================================================== */
export const EduMindFirebase = {
  app,
  auth,
  db,
  analytics,

  async login(email, password) {
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      
      let profile = null;
      try {
        const docSnap = await getDoc(doc(db, "users", user.uid));
        if (docSnap.exists()) {
          profile = docSnap.data();
        }
      } catch (err) {
        console.warn("Could not fetch user profile from Firestore:", err);
      }

      this._syncLocalUser(user, profile?.name || profile?.displayName);
      return { success: true, user, profile };
    } catch (error) {
      return { success: false, error: this._formatAuthError(error.code) };
    }
  },

  async register(email, password, displayName) {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;

      if (displayName) {
        await updateProfile(user, { displayName });
      }

      const initialProfile = {
        id: user.uid,
        uid: user.uid,
        email: user.email,
        name: displayName || user.email.split("@")[0],
        displayName: displayName || user.email.split("@")[0],
        role: "student",
        plan: "Pro",
        status: "active",
        quizzes: 0,
        streak: 1,
        lastActive: "Vừa xong",
        createdAt: serverTimestamp()
      };

      try {
        await setDoc(doc(db, "users", user.uid), initialProfile, { merge: true });
      } catch (err) {
        console.warn("Could not save initial profile to Firestore:", err);
      }

      this._syncLocalUser(user, displayName);
      return { success: true, user, profile: initialProfile };
    } catch (error) {
      return { success: false, error: this._formatAuthError(error.code) };
    }
  },

  async loginWithGoogle() {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      const user = result.user;

      const profileData = {
        id: user.uid,
        uid: user.uid,
        email: user.email,
        name: user.displayName || user.email.split("@")[0],
        displayName: user.displayName || user.email.split("@")[0],
        photoURL: user.photoURL || null,
        role: "student",
        plan: "Pro",
        status: "active",
        lastActive: "Vừa xong",
        lastLogin: serverTimestamp()
      };

      try {
        await setDoc(doc(db, "users", user.uid), profileData, { merge: true });
      } catch (err) {
        console.warn("Could not save Google user to Firestore:", err);
      }

      this._syncLocalUser(user, user.displayName);
      return { success: true, user, profile: profileData };
    } catch (error) {
      return { success: false, error: this._formatAuthError(error.code) };
    }
  },

  async logout() {
    try {
      await signOut(auth);
      localStorage.removeItem("edumind_user");
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  onAuthStateChanged(callback) {
    return onAuthStateChanged(auth, async (user) => {
      if (user) {
        let profile = null;
        try {
          const docSnap = await getDoc(doc(db, "users", user.uid));
          if (docSnap.exists()) {
            profile = docSnap.data();
          }
        } catch (err) {
          console.warn("Could not fetch user profile:", err);
        }
        this._syncLocalUser(user, profile?.name || profile?.displayName);
        callback({ user, profile });
      } else {
        callback(null);
      }
    });
  },

  getCurrentUser() {
    return auth.currentUser;
  },

  // Admin users queries
  async getUsers() {
    return EduMindDB.getUsers();
  },

  async addUser(userData) {
    return EduMindDB.addUser(userData);
  },

  async updateUser(userId, updatedFields) {
    return EduMindDB.updateUser(userId, updatedFields);
  },

  async toggleUserLock(userId, currentStatus) {
    return EduMindDB.toggleUserLock(userId, currentStatus);
  },

  async deleteUser(userId) {
    return EduMindDB.deleteUser(userId);
  },

  // Survey, Notes, Quizzes
  async saveSurvey(surveyData) {
    return EduMindDB.saveSurvey(surveyData);
  },

  async getSurvey(uid) {
    return EduMindDB.getSurvey(uid);
  },

  async saveNotes(notesText) {
    return EduMindDB.saveNotes(notesText);
  },

  async getNotes(uid) {
    return EduMindDB.getNotes(uid);
  },

  async saveQuizResult(quizResult) {
    return EduMindDB.saveQuizAttempt(quizResult);
  },

  async getUserQuizzes(uid) {
    return EduMindDB.getQuizAttempts(uid);
  },

  _syncLocalUser(user, customName) {
    const name = customName || user.displayName || user.email.split("@")[0] || "Học viên";
    const initials = name
      .split(" ")
      .filter(Boolean)
      .map(part => part[0])
      .join("")
      .substring(0, 2)
      .toUpperCase();

    const userData = {
      uid: user.uid,
      email: user.email,
      name,
      initials: initials || "HV"
    };

    localStorage.setItem("edumind_user", JSON.stringify(userData));

    document.querySelectorAll(".user-profile-name").forEach(el => el.textContent = name);
    document.querySelectorAll(".user-avatar-circle, .user-avatar, .avatar").forEach(el => {
      el.textContent = initials || "HV";
    });
    const greetingName = document.querySelector(".greeting-title .user-name");
    if (greetingName) greetingName.textContent = name.split(" ").pop() || name;
  },

  _formatAuthError(code) {
    switch (code) {
      case "auth/invalid-email":
        return "Địa chỉ email không đúng định dạng.";
      case "auth/user-disabled":
        return "Tài khoản này đã bị khóa.";
      case "auth/user-not-found":
        return "Không tìm thấy tài khoản với email này.";
      case "auth/wrong-password":
      case "auth/invalid-credential":
        return "Mật khẩu hoặc email không chính xác.";
      case "auth/email-already-in-use":
        return "Email này đã được sử dụng bởi một tài khoản khác.";
      case "auth/weak-password":
        return "Mật khẩu quá yếu (cần tối thiểu 6 ký tự).";
      case "auth/popup-closed-by-user":
        return "Cửa sổ đăng nhập Google đã bị đóng.";
      case "auth/operation-not-allowed":
        return "Phương thức đăng nhập này chưa được kích hoạt trong Firebase Console (Authentication -> Sign-in method).";
      case "auth/network-request-failed":
        return "Không thể kết nối tới máy chủ Firebase. Vui lòng kiểm tra mạng Internet.";
      default:
        return "Lỗi xác thực: " + code;
    }
  }
};

/* ==========================================================================
   CENTRALIZED CLOUD FIRESTORE DATABASE SERVICE (EduMindDB)
   ========================================================================== */
export const EduMindDB = {
  db,

  /**
   * Seed all 5 core collections in Cloud Firestore
   * - users
   * - quizzes
   * - knowledge_gaps
   * - roadmaps
   * - quiz_attempts
   */
  async seedAllCollections(force = false) {
    const results = {
      users: 0,
      quizzes: 0,
      knowledge_gaps: 0,
      roadmaps: 0,
      attempts: 0
    };

    try {
      // 1. Seed Users
      for (const u of DEFAULT_SEED_USERS) {
        await setDoc(doc(db, "users", u.id), u, { merge: !force });
        results.users++;
      }

      // 2. Seed Quizzes
      for (const q of DEFAULT_QUIZZES) {
        await setDoc(doc(db, "quizzes", q.id), q, { merge: !force });
        results.quizzes++;
      }

      // 3. Seed Knowledge Gaps
      for (const g of DEFAULT_KNOWLEDGE_GAPS) {
        await setDoc(doc(db, "knowledge_gaps", g.id), g, { merge: !force });
        results.knowledge_gaps++;
      }

      // 4. Seed Roadmaps
      await setDoc(doc(db, "roadmaps", DEFAULT_ROADMAP.id), DEFAULT_ROADMAP, { merge: !force });
      results.roadmaps++;

      // 5. Seed Attempts
      for (const a of DEFAULT_ATTEMPTS) {
        await setDoc(doc(db, "quiz_attempts", a.id), a, { merge: !force });
        results.attempts++;
      }

      localStorage.setItem("edumind_db_seeded", "true");
      return { success: true, results };
    } catch (e) {
      console.warn("Error seeding Firestore collections:", e);
      return { success: false, error: e.message, results };
    }
  },

  /* ------------------------------------------------------------------------
     1. USERS COLLECTION (Admin & Directory)
     ------------------------------------------------------------------------ */
  async getUsers() {
    try {
      const snapshot = await getDocs(collection(db, "users"));
      if (!snapshot.empty) {
        const firestoreUsers = [];
        snapshot.forEach(docSnap => {
          const data = docSnap.data();
          firestoreUsers.push({
            id: docSnap.id,
            name: data.name || data.displayName || "Người dùng",
            email: data.email || "",
            role: data.role || "student",
            plan: data.plan || "Free",
            status: data.status || "active",
            lastActive: data.lastActive || "Hôm nay",
            quizzes: data.quizzes !== undefined ? data.quizzes : 0,
            streak: data.streak !== undefined ? data.streak : 0
          });
        });
        localStorage.setItem("edumind_admin_users", JSON.stringify(firestoreUsers));
        return { success: true, users: firestoreUsers, source: "firestore" };
      }

      // If empty, auto-seed
      await this.seedAllCollections();
      localStorage.setItem("edumind_admin_users", JSON.stringify(DEFAULT_SEED_USERS));
      return { success: true, users: DEFAULT_SEED_USERS, source: "seeded" };
    } catch (error) {
      console.warn("Firestore getUsers fell back to cache:", error);
      let cached = DEFAULT_SEED_USERS;
      try {
        const stored = localStorage.getItem("edumind_admin_users");
        if (stored) cached = JSON.parse(stored);
      } catch {}
      return { success: false, users: cached, source: "cache", error: error.message };
    }
  },

  async addUser(userData) {
    const id = userData.id || ("usr_" + Date.now());
    const fullUser = {
      ...userData,
      id,
      createdAt: serverTimestamp()
    };
    try {
      await setDoc(doc(db, "users", id), fullUser);
      return { success: true, id, user: fullUser, source: "firestore" };
    } catch (error) {
      return { success: false, id, user: fullUser, error: error.message };
    }
  },

  async updateUser(userId, updatedFields) {
    try {
      await updateDoc(doc(db, "users", userId), {
        ...updatedFields,
        updatedAt: serverTimestamp()
      });
      return { success: true };
    } catch (error) {
      try {
        await setDoc(doc(db, "users", userId), updatedFields, { merge: true });
        return { success: true };
      } catch (e) {
        return { success: false, error: error.message };
      }
    }
  },

  async toggleUserLock(userId, currentStatus) {
    const nextStatus = currentStatus === "active" ? "locked" : "active";
    return this.updateUser(userId, { status: nextStatus });
  },

  async deleteUser(userId) {
    try {
      await deleteDoc(doc(db, "users", userId));
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  /* ------------------------------------------------------------------------
     2. QUIZZES COLLECTION (Quiz Bank & Questions)
     ------------------------------------------------------------------------ */
  async getQuizzes() {
    try {
      const snap = await getDocs(collection(db, "quizzes"));
      if (!snap.empty) {
        const list = [];
        snap.forEach(d => list.push({ id: d.id, ...d.data() }));
        localStorage.setItem("edumind_quizzes_cache", JSON.stringify(list));
        return list;
      }
      // If empty, seed
      for (const q of DEFAULT_QUIZZES) {
        await setDoc(doc(db, "quizzes", q.id), q);
      }
      return DEFAULT_QUIZZES;
    } catch (e) {
      console.warn("getQuizzes fallback:", e);
      try {
        return JSON.parse(localStorage.getItem("edumind_quizzes_cache")) || DEFAULT_QUIZZES;
      } catch {
        return DEFAULT_QUIZZES;
      }
    }
  },

  async getQuizById(id) {
    try {
      const snap = await getDoc(doc(db, "quizzes", id));
      if (snap.exists()) {
        return { id: snap.id, ...snap.data() };
      }
    } catch (e) {
      console.warn("getQuizById fallback:", e);
    }
    return DEFAULT_QUIZZES.find(q => q.id === id) || DEFAULT_QUIZZES[0];
  },

  async createQuiz(quizData) {
    const id = quizData.id || ("quiz_" + Date.now());
    const full = {
      ...quizData,
      id,
      createdAt: serverTimestamp()
    };
    try {
      await setDoc(doc(db, "quizzes", id), full);
      return { success: true, id, quiz: full };
    } catch (e) {
      console.warn("createQuiz fallback:", e);
      return { success: false, id, quiz: full, error: e.message };
    }
  },

  /* ------------------------------------------------------------------------
     3. QUIZ ATTEMPTS & HISTORY COLLECTION
     ------------------------------------------------------------------------ */
  async getQuizAttempts(userId) {
    try {
      const snap = await getDocs(collection(db, "quiz_attempts"));
      if (!snap.empty) {
        const list = [];
        snap.forEach(d => list.push({ id: d.id, ...d.data() }));
        list.sort((a, b) => (b.completedAt || "").localeCompare(a.completedAt || ""));
        localStorage.setItem("edumind_attempts_cache", JSON.stringify(list));
        return list;
      }
      // If empty, seed
      for (const a of DEFAULT_ATTEMPTS) {
        await setDoc(doc(db, "quiz_attempts", a.id), a);
      }
      return DEFAULT_ATTEMPTS;
    } catch (e) {
      console.warn("getQuizAttempts fallback:", e);
      try {
        return JSON.parse(localStorage.getItem("edumind_attempts_cache")) || DEFAULT_ATTEMPTS;
      } catch {
        return DEFAULT_ATTEMPTS;
      }
    }
  },

  async saveQuizAttempt(attemptData) {
    const id = attemptData.id || ("att_" + Date.now());
    const user = auth.currentUser;
    const full = {
      ...attemptData,
      id,
      userId: user ? user.uid : "local_user",
      userName: user ? (user.displayName || user.email) : "Phi Le Minh",
      completedAt: new Date().toLocaleDateString("vi-VN"),
      createdAt: serverTimestamp()
    };

    // Update local cache
    try {
      const cached = JSON.parse(localStorage.getItem("edumind_attempts_cache") || "[]");
      cached.unshift(full);
      localStorage.setItem("edumind_attempts_cache", JSON.stringify(cached));
    } catch {}

    // Save to Firestore
    try {
      await setDoc(doc(db, "quiz_attempts", id), full);
      if (user) {
        // Also save to user sub-collection
        await setDoc(doc(db, "users", user.uid, "quizzes", id), full);
      }
      return { success: true, id, attempt: full, firestore: true };
    } catch (e) {
      console.warn("saveQuizAttempt fallback:", e);
      return { success: true, id, attempt: full, firestore: false };
    }
  },

  /* ------------------------------------------------------------------------
     4. KNOWLEDGE GAPS COLLECTION (Analytics)
     ------------------------------------------------------------------------ */
  async getKnowledgeGaps() {
    try {
      const snap = await getDocs(collection(db, "knowledge_gaps"));
      if (!snap.empty) {
        const list = [];
        snap.forEach(d => list.push({ id: d.id, ...d.data() }));
        return list;
      }
      // If empty, seed
      for (const g of DEFAULT_KNOWLEDGE_GAPS) {
        await setDoc(doc(db, "knowledge_gaps", g.id), g);
      }
      return DEFAULT_KNOWLEDGE_GAPS;
    } catch (e) {
      console.warn("getKnowledgeGaps fallback:", e);
      return DEFAULT_KNOWLEDGE_GAPS;
    }
  },

  /* ------------------------------------------------------------------------
     5. LEARNING ROADMAP COLLECTION
     ------------------------------------------------------------------------ */
  async getRoadmap() {
    try {
      const snap = await getDoc(doc(db, "roadmaps", DEFAULT_ROADMAP.id));
      if (snap.exists()) {
        return { id: snap.id, ...snap.data() };
      }
      await setDoc(doc(db, "roadmaps", DEFAULT_ROADMAP.id), DEFAULT_ROADMAP);
      return DEFAULT_ROADMAP;
    } catch (e) {
      console.warn("getRoadmap fallback:", e);
      return DEFAULT_ROADMAP;
    }
  },

  async updateRoadmap(roadmapData) {
    try {
      await setDoc(doc(db, "roadmaps", DEFAULT_ROADMAP.id), roadmapData, { merge: true });
      return { success: true };
    } catch (e) {
      return { success: false, error: e.message };
    }
  },

  /* ------------------------------------------------------------------------
     6. CHAT MESSAGES COLLECTION (Study Coach)
     ------------------------------------------------------------------------ */
  async getChatMessages(userId) {
    try {
      const snap = await getDocs(collection(db, "chat_messages"));
      if (!snap.empty) {
        const list = [];
        snap.forEach(d => list.push({ id: d.id, ...d.data() }));
        return list;
      }
      // If empty, seed
      for (const m of DEFAULT_CHAT_MESSAGES) {
        await setDoc(doc(db, "chat_messages", m.id), m);
      }
      return DEFAULT_CHAT_MESSAGES;
    } catch (e) {
      console.warn("getChatMessages fallback:", e);
      return DEFAULT_CHAT_MESSAGES;
    }
  },

  async saveChatMessage(msg) {
    const id = msg.id || ("msg_" + Date.now());
    const full = {
      ...msg,
      id,
      createdAt: serverTimestamp()
    };
    try {
      await setDoc(doc(db, "chat_messages", id), full);
      return { success: true, id, message: full };
    } catch (e) {
      return { success: false, id, message: full, error: e.message };
    }
  },

  /* ------------------------------------------------------------------------
     7. USER SURVEY & STUDY NOTES
     ------------------------------------------------------------------------ */
  async saveSurvey(surveyData) {
    const user = auth.currentUser;
    const uid = user ? user.uid : "local_user";
    try {
      if (user) {
        await setDoc(doc(db, "users", uid), {
          survey: surveyData,
          surveyCompletedAt: serverTimestamp()
        }, { merge: true });
      }
      localStorage.setItem("edumind_survey", JSON.stringify(surveyData));
      return { success: true };
    } catch (e) {
      localStorage.setItem("edumind_survey", JSON.stringify(surveyData));
      return { success: false, error: e.message };
    }
  },

  async getSurvey(uid) {
    const targetUid = uid || (auth.currentUser ? auth.currentUser.uid : null);
    if (!targetUid) {
      try { return JSON.parse(localStorage.getItem("edumind_survey")); } catch { return null; }
    }
    try {
      const snap = await getDoc(doc(db, "users", targetUid));
      if (snap.exists() && snap.data().survey) {
        return snap.data().survey;
      }
    } catch (e) {}
    try { return JSON.parse(localStorage.getItem("edumind_survey")); } catch { return null; }
  },

  async saveNotes(notesText) {
    localStorage.setItem("edumind_notes", notesText);
    const user = auth.currentUser;
    if (!user) return false;
    try {
      await setDoc(doc(db, "users", user.uid), {
        notes: notesText,
        notesUpdatedAt: serverTimestamp()
      }, { merge: true });
      return true;
    } catch (e) {
      return false;
    }
  },

  async getNotes(uid) {
    const user = auth.currentUser;
    const targetUid = uid || (user ? user.uid : null);
    if (targetUid) {
      try {
        const snap = await getDoc(doc(db, "users", targetUid));
        if (snap.exists() && snap.data().notes !== undefined) {
          return snap.data().notes;
        }
      } catch (e) {}
    }
    return localStorage.getItem("edumind_notes") || "";
  }
};

// Expose globally and trigger custom event
window.EduMindFirebase = EduMindFirebase;
window.EduMindDB = EduMindDB;
window.dispatchEvent(new CustomEvent("edumind:firebase-ready", { detail: EduMindFirebase }));

// Auto-seed check in background
if (!localStorage.getItem("edumind_db_seeded")) {
  setTimeout(() => {
    EduMindDB.seedAllCollections(false).catch(() => {});
  }, 1000);
}

export default EduMindFirebase;
