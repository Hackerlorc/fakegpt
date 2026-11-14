"""
EduMind AI - Real SQLite Database Engine
Creates tables, defines schemas, and manages CRUD operations.
Database file: edumind.db
"""

import sqlite3
import json
import os
import time

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "edumind.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # 1. Users Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL DEFAULT '12345678',
        role TEXT NOT NULL DEFAULT 'student',
        plan TEXT NOT NULL DEFAULT 'Free',
        status TEXT NOT NULL DEFAULT 'active',
        streak INTEGER DEFAULT 1,
        quizzes INTEGER DEFAULT 0,
        notes TEXT DEFAULT '',
        survey TEXT DEFAULT '{}',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_active TEXT DEFAULT 'Vừa xong'
    )
    """)

    # 2. Quizzes Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        subject TEXT NOT NULL,
        grade TEXT DEFAULT '12',
        difficulty TEXT DEFAULT 'Trung bình',
        duration_minutes INTEGER DEFAULT 30,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 3. Questions Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id TEXT PRIMARY KEY,
        quiz_id TEXT NOT NULL,
        text TEXT NOT NULL,
        options_json TEXT NOT NULL,
        correct_index INTEGER NOT NULL,
        explanation TEXT DEFAULT '',
        sort_order INTEGER DEFAULT 1,
        FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
    )
    """)

    # 4. Quiz Attempts (History) Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id TEXT PRIMARY KEY,
        user_id TEXT DEFAULT 'local_user',
        quiz_id TEXT,
        title TEXT NOT NULL,
        subject TEXT NOT NULL,
        score REAL NOT NULL,
        total INTEGER DEFAULT 10,
        correct_count INTEGER DEFAULT 0,
        time_spent TEXT DEFAULT '15:00',
        answers_json TEXT DEFAULT '{}',
        completed_at TEXT DEFAULT 'Hôm nay',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 5. Knowledge Gaps Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_gaps (
        id TEXT PRIMARY KEY,
        user_id TEXT DEFAULT 'local_user',
        subject TEXT NOT NULL,
        topic TEXT NOT NULL,
        accuracy_percent REAL NOT NULL,
        priority TEXT DEFAULT 'Trung bình',
        description TEXT DEFAULT ''
    )
    """)

    # 6. Roadmaps Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS roadmaps (
        id TEXT PRIMARY KEY,
        user_id TEXT DEFAULT 'local_user',
        subject TEXT NOT NULL,
        current_lesson TEXT NOT NULL,
        progress_percent INTEGER DEFAULT 60,
        summary TEXT DEFAULT '',
        next_milestone TEXT DEFAULT '',
        updated_at TEXT DEFAULT 'Hôm nay'
    )
    """)

    # 7. Chat Messages Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages (
        id TEXT PRIMARY KEY,
        user_id TEXT DEFAULT 'local_user',
        sender TEXT NOT NULL,
        is_ai BOOLEAN DEFAULT 0,
        text TEXT NOT NULL,
        socratic_hint TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    # Seed initial data if empty
    seed_if_empty(cur, conn)
    conn.close()

def seed_if_empty(cur, conn):
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        seed_users = [
            ("usr_001", "Phi Le Minh", "phi@example.com", "12345678", "student", "Pro", "active", 12, 47, "Ôn tập định lý Viète và tam thức bậc 2", "{}", "Vừa xong"),
            ("usr_002", "Nguyễn Hoàng Long", "long.nh@gmail.com", "12345678", "student", "Free", "active", 5, 18, "", "{}", "2 giờ trước"),
            ("usr_003", "ThS. Trần Thị Mai", "mai.tran@thpt-chuyen.edu.vn", "12345678", "teacher", "Pro", "active", 22, 64, "", "{}", "Hôm qua"),
            ("usr_004", "Lê Quốc Bảo", "bao.le@outlook.com", "12345678", "student", "Pro", "active", 8, 32, "", "{}", "3 ngày trước"),
            ("usr_005", "Phạm Thu Trang", "trang.pham@yahoo.com", "12345678", "student", "Free", "locked", 0, 4, "", "{}", "12 ngày trước"),
            ("usr_006", "Thầy Đỗ Quang Huy", "huy.do@supham.edu.vn", "12345678", "teacher", "Pro", "active", 30, 95, "", "{}", "Hôm nay"),
            ("usr_007", "Ngô Thanh Vân", "van.ngo@hotmail.com", "12345678", "student", "Free", "active", 2, 9, "", "{}", "5 ngày trước"),
            ("usr_008", "Vũ Đức Thành", "admin@edumind.ai", "admin123", "admin", "Pro", "active", 45, 120, "", "{}", "Trực tuyến"),
            ("usr_009", "Học viên Demo", "student@edumind.vn", "12345678", "student", "Pro", "active", 7, 25, "", "{}", "Vừa xong")
        ]
        cur.executemany("INSERT INTO users (id, name, email, password, role, plan, status, streak, quizzes, notes, survey, last_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", seed_users)

    cur.execute("SELECT COUNT(*) FROM quizzes")
    if cur.fetchone()[0] == 0:
        seed_quizzes = [
            ("quiz_toan_01", "Phương trình bậc hai & Định lý Viète", "Toán học", "10", "Trung bình", 30),
            ("quiz_ly_01", "Lực tương tác tĩnh điện & Điện tích", "Vật lý", "11", "Cơ bản", 20),
            ("quiz_hoa_01", "Phân loại Cacbohidrat & Glucozo", "Hóa học", "12", "Trung bình", 25),
            ("quiz_anh_01", "Cấu trúc câu phức & Mệnh đề quan hệ", "Tiếng Anh", "12", "Nâng cao", 20)
        ]
        cur.executemany("INSERT INTO quizzes (id, title, subject, grade, difficulty, duration_minutes) VALUES (?, ?, ?, ?, ?, ?)", seed_quizzes)

        seed_questions = [
            ("q1", "quiz_toan_01", "Phương trình x² - 5x + 6 = 0 có tập nghiệm S là:", json.dumps(["S = {1; 6}", "S = {2; 3}", "S = {-2; -3}", "S = {3; -2}"], ensure_ascii=False), 1, "Theo định lý Viète: x₁ + x₂ = 5 và x₁ × x₂ = 6. Hai nghiệm là x = 2 và x = 3.", 1),
            ("q2", "quiz_toan_01", "Tìm m để phương trình x² - 2mx + m² - 1 = 0 luôn có 2 nghiệm phân biệt:", json.dumps(["Mọi m ∈ ℝ", "m > 1", "m < 0", "Không có m nào"], ensure_ascii=False), 0, "Ta có Δ' = (-m)² - 1(m² - 1) = 1 > 0 với mọi m. Do đó luôn có 2 nghiệm phân biệt.", 2),
            ("q3", "quiz_toan_01", "Gọi x₁, x₂ là hai nghiệm của x² - 3x - 4 = 0. Giá trị biểu thức A = x₁² + x₂² là:", json.dumps(["17", "25", "7", "9"], ensure_ascii=False), 0, "A = (x₁ + x₂)² - 2x₁x₂ = 3² - 2(-4) = 9 + 8 = 17.", 3),
            ("q4", "quiz_toan_01", "Phương trình 2x² + 5x + 2 = 0 có tích hai nghiệm bằng:", json.dumps(["1", "2.5", "-1", "2"], ensure_ascii=False), 0, "Theo Viète, P = c/a = 2/2 = 1.", 4),
            ("q5", "quiz_toan_01", "Cho phương trình x² - (m + 1)x + m = 0. Nghiệm của phương trình là:", json.dumps(["x = 1 hoặc x = m", "x = -1 hoặc x = -m", "x = 1 hoặc x = -m", "x = 2 hoặc x = m"], ensure_ascii=False), 0, "Do a + b + c = 0 nên có nghiệm x₁ = 1 và x₂ = c/a = m.", 5),
            ("q6", "quiz_ly_01", "Đơn vị của điện tích trong hệ đo lường quốc tế SI là:", json.dumps(["Vôn (V)", "Ampe (A)", "Cu-lông (C)", "Oát (W)"], ensure_ascii=False), 2, "Đơn vị của điện tích trong hệ SI là Cu-lông, ký hiệu C.", 1),
            ("q7", "quiz_ly_01", "Khi khoảng cách giữa 2 điện tích điểm trong chân không tăng lên 2 lần thì độ lớn lực Cu-lông:", json.dumps(["Tăng 2 lần", "Giảm 2 lần", "Tăng 4 lần", "Giảm 4 lần"], ensure_ascii=False), 3, "Lực Cu-lông tỉ lệ nghịch với bình phương khoảng cách r². r tăng 2 lần thì F giảm 4 lần.", 2),
            ("q8", "quiz_hoa_01", "Chất nào sau đây thuộc loại monosaccarit?", json.dumps(["Saccarozo", "Tinh bột", "Xenlulozo", "Glucozo"], ensure_ascii=False), 3, "Monosaccarit gồm Glucozo và Fructozo.", 1),
            ("q9", "quiz_anh_01", "The student _____ won the first prize studies in our class.", json.dumps(["which", "who", "whom", "whose"], ensure_ascii=False), 1, "Chủ ngữ chỉ người trong mệnh đề quan hệ dùng 'who'.", 1)
        ]
        cur.executemany("INSERT INTO questions (id, quiz_id, text, options_json, correct_index, explanation, sort_order) VALUES (?, ?, ?, ?, ?, ?, ?)", seed_questions)

    cur.execute("SELECT COUNT(*) FROM quiz_attempts")
    if cur.fetchone()[0] == 0:
        seed_attempts = [
            ("att_01", "usr_001", "quiz_toan_01", "Phương trình bậc hai & Viète", "Toán học", 9.0, 10, 9, "14:20", "{}", "Hôm nay"),
            ("att_02", "usr_001", "quiz_ly_01", "Lực tương tác tĩnh điện & Điện tích", "Vật lý", 7.5, 10, 7, "22:10", "{}", "23/10/2026"),
            ("att_03", "usr_001", "quiz_hoa_01", "Phân loại Cacbohidrat & Glucozo", "Hóa học", 8.5, 10, 8, "18:45", "{}", "21/10/2026"),
            ("att_04", "usr_001", "quiz_ly_01", "Đại cương về Dao động điều hòa", "Vật lý", 5.0, 10, 5, "28:10", "{}", "18/10/2026")
        ]
        cur.executemany("INSERT INTO quiz_attempts (id, user_id, quiz_id, title, subject, score, total, correct_count, time_spent, answers_json, completed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", seed_attempts)

    cur.execute("SELECT COUNT(*) FROM knowledge_gaps")
    if cur.fetchone()[0] == 0:
        seed_gaps = [
            ("gap_01", "usr_001", "Vật lý", "Điện từ học — Cảm ứng điện từ", 28.0, "Cao", "Hay nhầm lẫn chiều dòng điện cảm ứng theo định luật Len-xơ."),
            ("gap_02", "usr_001", "Toán học", "Hình học không gian — Khoảng cách 2 đường thẳng", 35.0, "Cao", "Chưa thành thạo dựng mặt phẳng song song chứa 1 đường thẳng."),
            ("gap_03", "usr_001", "Toán học", "Phương trình lượng giác chứa tham số", 42.0, "Trung bình", "Cần rèn luyện thêm điều kiện nghiệm của phương trình bậc 2 theo sin/cos."),
            ("gap_04", "usr_001", "Tiếng Anh", "Cấu trúc câu phức & Mệnh đề quan hệ", 55.0, "Trung bình", "Thường phân vân giữa which và that trong mệnh đề không xác định."),
            ("gap_05", "usr_001", "Hóa học", "Kim loại kiềm thổ & Nước cứng", 62.0, "Thấp", "Cần nhớ bảng phân biệt làm mềm nước cứng tạm thời và vĩnh cửu.")
        ]
        cur.executemany("INSERT INTO knowledge_gaps (id, user_id, subject, topic, accuracy_percent, priority, description) VALUES (?, ?, ?, ?, ?, ?, ?)", seed_gaps)

    cur.execute("SELECT COUNT(*) FROM roadmaps")
    if cur.fetchone()[0] == 0:
        cur.execute("""
        INSERT INTO roadmaps (id, user_id, subject, current_lesson, progress_percent, summary, next_milestone, updated_at)
        VALUES ('roadmap_active', 'usr_001', 'Toán học 10 • Đại số', 'Phương trình bậc hai & Định lý Viète', 65, 'Bạn đã nắm vững cách tính biệt thức Δ, cần luyện thêm kỹ năng tìm tham số m.', 'Dấu của tam thức bậc hai & Bất phương trình', 'Hôm nay')
        """)

    cur.execute("SELECT COUNT(*) FROM chat_messages")
    if cur.fetchone()[0] == 0:
        seed_chat = [
            ("msg_01", "usr_001", "Study Coach", 1, "Chào em! Hôm nay chúng ta tiếp tục với phần Định lý Viète nhé. Em hãy nhớ lại xem: nếu phương trình bậc hai ax² + bx + c = 0 có hai nghiệm x₁ và x₂, thì tổng và tích của chúng được tính như thế nào?", "Hãy nhớ đến công thức liên hệ giữa các hệ số a, b, c với (x₁ + x₂) và (x₁ × x₂)."),
            ("msg_02", "usr_001", "Bạn", 0, "Dạ, x1 + x2 = -b/a và x1 * x2 = c/a ạ.", ""),
            ("msg_03", "usr_001", "Study Coach", 1, "Rất chính xác! Bây giờ giả sử thầy có phương trình x² - 5x + 6 = 0. Không cần tính Δ, em có thể nhẩm ra hai số nào có tổng bằng 5 và tích bằng 6 không?", "Tìm hai số nguyên dương nhỏ mà tích bằng 6 (ví dụ: 1 và 6, hoặc 2 và 3).")
        ]
        cur.executemany("INSERT INTO chat_messages (id, user_id, sender, is_ai, text, socratic_hint) VALUES (?, ?, ?, ?, ?, ?)", seed_chat)

    conn.commit()

# ==============================================================================
# CRUD FUNCTIONS FOR API
# ==============================================================================

def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, role, plan, status, streak, quizzes, notes, survey, last_active, created_at FROM users ORDER BY created_at DESC")
    users = [dict(row) for row in cur.fetchall()]
    conn.close()
    return users

def create_user(user_data):
    conn = get_connection()
    cur = conn.cursor()
    uid = user_data.get("id") or f"usr_{int(time.time() * 1000)}"
    cur.execute("""
    INSERT INTO users (id, name, email, password, role, plan, status, streak, quizzes, last_active)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        uid,
        user_data.get("name", "Người dùng"),
        user_data.get("email", ""),
        user_data.get("password", "12345678"),
        user_data.get("role", "student"),
        user_data.get("plan", "Free"),
        user_data.get("status", "active"),
        user_data.get("streak", 1),
        user_data.get("quizzes", 0),
        "Vừa tạo"
    ))
    conn.commit()
    conn.close()
    return {"id": uid, **user_data}

def update_user(uid, update_data):
    conn = get_connection()
    cur = conn.cursor()
    fields = []
    values = []
    for k in ["name", "role", "plan", "status", "streak", "quizzes", "notes", "survey", "last_active"]:
        if k in update_data:
            fields.append(f"{k} = ?")
            values.append(update_data[k])
    if fields:
        values.append(uid)
        cur.execute(f"UPDATE users SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
    conn.close()
    return True

def delete_user(uid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (uid,))
    conn.commit()
    conn.close()
    return True

def authenticate_user(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, role, plan, status, streak, quizzes, notes, survey FROM users WHERE email = ? AND password = ?", (email, password))
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_all_quizzes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, subject, grade, difficulty, duration_minutes FROM quizzes ORDER BY created_at DESC")
    quizzes = [dict(row) for row in cur.fetchall()]
    
    # Attach questions
    for q in quizzes:
        cur.execute("SELECT id, text, options_json, correct_index, explanation FROM questions WHERE quiz_id = ? ORDER BY sort_order ASC", (q["id"],))
        q_rows = cur.fetchall()
        questions = []
        for r in q_rows:
            questions.append({
                "id": r["id"],
                "text": r["text"],
                "options": json.loads(r["options_json"]),
                "correctIndex": r["correct_index"],
                "explanation": r["explanation"]
            })
        q["questions"] = questions
    conn.close()
    return quizzes

def create_quiz(quiz_data):
    conn = get_connection()
    cur = conn.cursor()
    qid = quiz_data.get("id") or f"quiz_{int(time.time() * 1000)}"
    cur.execute("""
    INSERT INTO quizzes (id, title, subject, grade, difficulty, duration_minutes)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        qid,
        quiz_data.get("title", "Bài kiểm tra mới"),
        quiz_data.get("subject", "Toán học"),
        quiz_data.get("grade", "12"),
        quiz_data.get("difficulty", "Trung bình"),
        quiz_data.get("durationMinutes", 30)
    ))

    questions = quiz_data.get("questions", [])
    for idx, q in enumerate(questions):
        q_id = q.get("id") or f"q_{qid}_{idx + 1}"
        cur.execute("""
        INSERT INTO questions (id, quiz_id, text, options_json, correct_index, explanation, sort_order)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(q_id),
            qid,
            q.get("text", ""),
            json.dumps(q.get("options", []), ensure_ascii=False),
            q.get("correctIndex", 0),
            q.get("explanation", ""),
            idx + 1
        ))

    conn.commit()
    conn.close()
    return {"id": qid, **quiz_data}

def get_all_attempts(user_id=None):
    conn = get_connection()
    cur = conn.cursor()
    if user_id:
        cur.execute("SELECT id, user_id, quiz_id, title, subject, score, total, correct_count, time_spent, completed_at FROM quiz_attempts WHERE user_id = ? OR user_id = 'local_user' ORDER BY created_at DESC", (user_id,))
    else:
        cur.execute("SELECT id, user_id, quiz_id, title, subject, score, total, correct_count, time_spent, completed_at FROM quiz_attempts ORDER BY created_at DESC")
    attempts = [dict(row) for row in cur.fetchall()]
    conn.close()
    return attempts

def create_attempt(data):
    conn = get_connection()
    cur = conn.cursor()
    att_id = data.get("id") or f"att_{int(time.time() * 1000)}"
    user_id = data.get("userId", "local_user")
    cur.execute("""
    INSERT INTO quiz_attempts (id, user_id, quiz_id, title, subject, score, total, correct_count, time_spent, answers_json, completed_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        att_id,
        user_id,
        data.get("quizId", ""),
        data.get("title", "Bài kiểm tra"),
        data.get("subject", "Toán học"),
        float(data.get("score", 0.0)),
        int(data.get("total", 10)),
        int(data.get("correctCount", 0)),
        data.get("timeSpent", "15:00"),
        json.dumps(data.get("userAnswers", {}), ensure_ascii=False),
        data.get("completedAt", "Hôm nay")
    ))
    # Automatically increment user's quiz count in users table
    cur.execute("UPDATE users SET quizzes = quizzes + 1, last_active = 'Vừa xong' WHERE id = ? OR email = ?", (user_id, user_id))
    conn.commit()
    conn.close()
    return {"id": att_id, **data}

def get_user_stats(uid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, role, streak, quizzes, notes FROM users WHERE id = ? OR email = ?", (uid, uid))
    user_row = cur.fetchone()
    
    cur.execute("SELECT score, time_spent FROM quiz_attempts WHERE user_id = ?", (uid,))
    attempts = [dict(r) for r in cur.fetchall()]
    conn.close()

    if user_row:
        user = dict(user_row)
        streak = int(user.get("streak") or 1)
        db_quizzes = int(user.get("quizzes") or 0)
        quizzes = max(db_quizzes, len(attempts))
    else:
        streak = 1
        quizzes = len(attempts)

    if attempts:
        scores = [float(a["score"]) for a in attempts]
        avg_score = round(sum(scores) / len(scores), 1)
    elif quizzes > 0:
        avg_score = 8.2 if streak >= 10 else 7.8
    else:
        avg_score = 0.0

    # Calculate dynamic study time
    if quizzes >= 40:
        study_time = "1h 25m"
        time_sub = "Đạt 141% chỉ tiêu"
    elif quizzes >= 20:
        study_time = "45m"
        time_sub = "Đạt 90% chỉ tiêu"
    elif quizzes >= 5:
        study_time = "25m"
        time_sub = "Đạt 50% chỉ tiêu"
    elif quizzes > 0:
        study_time = "15m"
        time_sub = "Bắt đầu ngày học mới"
    else:
        study_time = "0m"
        time_sub = "Chưa học hôm nay"

    target_streak = max(streak + 2, 7)
    weekly_quizzes = min(quizzes, max(3, streak // 2 + 1))

    return {
        "streak": streak,
        "streakText": f"{streak} ngày",
        "streakSub": f"Mục tiêu: {target_streak} ngày",
        "quizzes": quizzes,
        "quizzesText": f"{quizzes} bài",
        "quizzesSub": f"+{weekly_quizzes} bài trong tuần này" if quizzes > 0 else "Chưa có bài kiểm tra",
        "avgScore": avg_score,
        "avgScoreText": f"{avg_score} / 10" if avg_score > 0 else "Chưa có điểm",
        "avgScoreSub": "+0.4 so với tuần trước" if avg_score > 0 else "Làm bài để tính điểm",
        "studyTime": study_time,
        "studyTimeSub": time_sub
    }

def get_knowledge_gaps(user_id=None):
    conn = get_connection()
    cur = conn.cursor()
    
    if user_id:
        # 1. Check if user has specific gaps in DB
        cur.execute("SELECT id, subject, topic, accuracy_percent, priority, description FROM knowledge_gaps WHERE user_id = ? ORDER BY accuracy_percent ASC", (user_id,))
        rows = cur.fetchall()
        if rows:
            gaps = []
            for r in rows:
                gaps.append({
                    "id": r["id"],
                    "subject": r["subject"],
                    "topic": r["topic"],
                    "accuracyPercent": r["accuracy_percent"],
                    "priority": r["priority"],
                    "description": r["description"]
                })
            conn.close()
            return gaps
            
        # 2. Check user info & quiz attempts
        cur.execute("SELECT id, name, email, quizzes, streak FROM users WHERE id = ? OR email = ?", (user_id, user_id))
        user_rec = cur.fetchone()
        
        # New user or user with 0 quizzes: no knowledge gaps yet!
        if user_rec and (user_rec["quizzes"] == 0 or user_rec["quizzes"] is None):
            conn.close()
            return []
            
        # Dedicated personalized gaps for student@edumind.vn
        if user_id in ["usr_009", "student@edumind.vn"]:
            conn.close()
            return [
                {
                    "id": "gap_stu_01",
                    "subject": "Vật lý",
                    "topic": "Dao động điều hòa — Con lắc lò xo",
                    "accuracyPercent": 45.0,
                    "priority": "Cao",
                    "description": "Hay nhầm lẫn giữa chu kỳ con lắc đơn và con lắc lò xo khi khối lượng thay đổi."
                },
                {
                    "id": "gap_stu_02",
                    "subject": "Hóa học",
                    "topic": "Este & Lipit — Phản ứng xà phòng hóa",
                    "accuracyPercent": 55.0,
                    "priority": "Trung bình",
                    "description": "Cần củng cố bài toán tính khối lượng muối khi este đơn chức tác dụng kiềm."
                }
            ]

    # Default/sample gaps for phi@example.com or general preview
    cur.execute("SELECT id, subject, topic, accuracy_percent, priority, description FROM knowledge_gaps ORDER BY accuracy_percent ASC LIMIT 5")
    gaps = []
    for r in cur.fetchall():
        gaps.append({
            "id": r["id"],
            "subject": r["subject"],
            "topic": r["topic"],
            "accuracyPercent": r["accuracy_percent"],
            "priority": r["priority"],
            "description": r["description"]
        })
    conn.close()
    return gaps

def get_active_roadmap(user_id=None):
    conn = get_connection()
    cur = conn.cursor()
    
    # 1. Check if user has specific roadmap in DB
    if user_id:
        cur.execute("SELECT id, user_id, subject, current_lesson, progress_percent, summary, next_milestone, updated_at FROM roadmaps WHERE user_id = ? LIMIT 1", (user_id,))
        row = cur.fetchone()
        if row:
            conn.close()
            return {
                "id": row["id"],
                "subject": row["subject"],
                "currentLesson": row["current_lesson"],
                "progressPercent": row["progress_percent"],
                "summary": row["summary"],
                "nextMilestone": row["next_milestone"],
                "updatedAt": row["updated_at"]
            }
            
        # 2. Check user's survey & profile in users table
        cur.execute("SELECT name, email, streak, quizzes, survey FROM users WHERE id = ? OR email = ?", (user_id, user_id))
        u = cur.fetchone()
        if u:
            survey_data = {}
            try:
                survey_data = json.loads(u["survey"] or "{}")
            except:
                pass
            
            grade = survey_data.get("grade", "12")
            subjects = survey_data.get("subjects", ["Toán học"])
            subject_name = subjects[0] if subjects else "Toán học"
            quizzes_count = u["quizzes"] or 0
            
            if "12" in str(grade) or user_id in ["usr_009", "student@edumind.vn"]:
                res = {
                    "id": f"roadmap_{user_id}",
                    "subject": f"{subject_name} 12 • Luyện thi tốt nghiệp",
                    "currentLesson": "Khảo sát hàm số & Các bài toán cực trị vận dụng cao",
                    "progressPercent": 40 if quizzes_count > 0 else 10,
                    "summary": "Tập trung rèn phương pháp loại trừ đáp án và đồ thị hàm ẩn theo chương trình lớp 12.",
                    "nextMilestone": "Chuyên đề Mũ & Logarit",
                    "updatedAt": "Hôm nay"
                }
            elif "11" in str(grade):
                res = {
                    "id": f"roadmap_{user_id}",
                    "subject": f"{subject_name} 11 • Cơ bản & Nâng cao",
                    "currentLesson": "Cấp số cộng, Cấp số nhân & Giới hạn dãy số",
                    "progressPercent": 35 if quizzes_count > 0 else 15,
                    "summary": "Nắm vững công thức số hạng tổng quát và điều kiện hội tụ.",
                    "nextMilestone": "Đạo hàm và tiếp tuyến đồ thị",
                    "updatedAt": "Hôm nay"
                }
            else:
                res = {
                    "id": f"roadmap_{user_id}",
                    "subject": f"{subject_name} 10 • Nền tảng THPT",
                    "currentLesson": "Phương trình bậc hai & Định lý Viète",
                    "progressPercent": 65 if quizzes_count > 10 else 20,
                    "summary": "Rèn luyện kỹ năng tìm điều kiện tham số m để phương trình có 2 nghiệm thỏa mãn hệ thức.",
                    "nextMilestone": "Dấu của tam thức bậc hai",
                    "updatedAt": "Hôm nay"
                }
            conn.close()
            return res

    # Default fallback
    cur.execute("SELECT id, subject, current_lesson, progress_percent, summary, next_milestone, updated_at FROM roadmaps LIMIT 1")
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "id": row["id"],
            "subject": row["subject"],
            "currentLesson": row["current_lesson"],
            "progressPercent": row["progress_percent"],
            "summary": row["summary"],
            "nextMilestone": row["next_milestone"],
            "updatedAt": row["updated_at"]
        }
    return None

def get_chat_history():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, sender, is_ai, text, socratic_hint, created_at FROM chat_messages ORDER BY created_at ASC")
    messages = []
    for r in cur.fetchall():
        messages.append({
            "id": r["id"],
            "sender": r["sender"],
            "isAi": bool(r["is_ai"]),
            "text": r["text"],
            "socraticHint": r["socratic_hint"]
        })
    conn.close()
    return messages

def add_chat_message(data):
    conn = get_connection()
    cur = conn.cursor()
    msg_id = data.get("id") or f"msg_{int(time.time() * 1000)}"
    cur.execute("""
    INSERT INTO chat_messages (id, user_id, sender, is_ai, text, socratic_hint)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        msg_id,
        data.get("userId", "local_user"),
        data.get("sender", "Bạn"),
        1 if data.get("isAi") else 0,
        data.get("text", ""),
        data.get("socraticHint", "")
    ))
    conn.commit()
    conn.close()
    return {"id": msg_id, **data}

def clear_chat_history():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM chat_messages")
    cur.execute("""
    INSERT INTO chat_messages (id, user_id, sender, is_ai, text, socratic_hint)
    VALUES ('msg_init', 'usr_001', 'Study Coach', 1, 'Chào em! Thầy là AI Study Coach. Hôm nay em muốn ôn tập chủ đề nào (Toán học, Vật lý, Hóa học hay Tiếng Anh)? Hãy gửi câu hỏi hoặc bài tập em đang cần gỡ rối nhé!', 'Gợi ý: Em có thể gõ câu hỏi hoặc dán đề bài vào đây.')
    """)
    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
    print("Total users:", len(get_all_users()))
    print("Total quizzes:", len(get_all_quizzes()))
