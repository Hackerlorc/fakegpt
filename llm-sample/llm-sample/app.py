import os
import json
import hashlib
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Page config
st.set_page_config(
    page_title="EduMind AI - Gia Sư & Luyện Thi Thông Minh",
    page_icon="📚",
    layout="wide"
)

# Load environment & Gemini
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ Chưa tìm thấy GOOGLE_API_KEY trong file .env!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3.8-flash")

# ==================== QUẢN LÝ TÀI KHOẢN (USERS.JSON) ====================
USER_DB_FILE = "users.json"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USER_DB_FILE):
        return {}
    try:
        with open(USER_DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users):
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Tên đăng nhập đã tồn tại!"
    users[username] = {
        "password": hash_password(password),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "history": []
    }
    save_users(users)
    return True, "Đăng ký thành công! Hãy đăng nhập."

def authenticate_user(username, password):
    users = load_users()
    if username not in users:
        return False, "Tài khoản không tồn tại!"
    if users[username]["password"] != hash_password(password):
        return False, "Sai mật khẩu!"
    return True, "Đăng nhập thành công!"

def add_quiz_history(username, topic, score, total):
    users = load_users()
    if username in users:
        entry = {
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "topic": topic,
            "score": score,
            "total": total,
            "percentage": round((score / total) * 100) if total > 0 else 0
        }
        users[username].setdefault("history", []).append(entry)
        save_users(users)

def get_user_history(username):
    users = load_users()
    return users.get(username, {}).get("history", [])

# ==================== KHỞI TẠO SESSION STATE ====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Xin chào! Tôi là Gia sư EduMind. Bạn có câu hỏi nào về bài học hay cần giải thích kiến thức gì không?"}
    ]

# ==================== GIAO DIỆN ĐĂNG NHẬP / ĐĂNG KÝ ====================
if not st.session_state.logged_in:
    st.title("📚 EduMind AI - Trợ Lý Học Tập & Luyện Thi")
    st.write("Đăng nhập để bắt đầu học tập, làm bài trắc nghiệm và theo dõi điểm số của bạn!")

    col1, col2, _ = st.columns([1, 1, 1])
    tab_login, tab_register = st.tabs(["🔑 Đăng Nhập", "📝 Đăng Ký Tài Khoản"])

    with tab_login:
        with st.form("login_form"):
            login_user = st.text_input("Tên đăng nhập", key="login_u")
            login_pass = st.text_input("Mật khẩu", type="password", key="login_p")
            btn_login = st.form_submit_button("Đăng nhập", use_container_width=True)
            if btn_login:
                if not login_user or not login_pass:
                    st.warning("Vui lòng điền đầy đủ tên đăng nhập và mật khẩu.")
                else:
                    success, msg = authenticate_user(login_user, login_pass)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = login_user
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    with tab_register:
        with st.form("register_form"):
            reg_user = st.text_input("Tên đăng nhập mới", key="reg_u")
            reg_pass = st.text_input("Mật khẩu", type="password", key="reg_p")
            reg_pass_confirm = st.text_input("Xác nhận mật khẩu", type="password", key="reg_pc")
            btn_register = st.form_submit_button("Tạo tài khoản", use_container_width=True)
            if btn_register:
                if not reg_user or not reg_pass:
                    st.warning("Vui lòng điền đầy đủ thông tin.")
                elif reg_pass != reg_pass_confirm:
                    st.error("Mật khẩu xác nhận không khớp!")
                else:
                    success, msg = register_user(reg_user, reg_pass)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
    st.stop()

# ==================== KHI ĐÃ ĐĂNG NHẬP ====================
# Sidebar
with st.sidebar:
    st.header(f"👋 Chào bạn, **{st.session_state.username}**!")
    if st.button("🚪 Đăng xuất", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.quiz_data = None
        st.session_state.quiz_submitted = False
        st.session_state.user_answers = {}
        st.rerun()

    st.markdown("---")
    st.subheader("🎯 Cấu hình Đề thi")
    topic_input = st.text_area(
        "Chủ đề hoặc Dán tài liệu học:",
        value=st.session_state.quiz_topic,
        placeholder="Ví dụ: Lịch sử Việt Nam thế kỷ 20, Ngữ pháp Thì hiện tại hoàn thành, Lập trình Python căn bản...",
        height=120
    )
    
    num_questions = st.selectbox("Số lượng câu hỏi:", [3, 5, 10], index=1)
    difficulty = st.select_slider("Độ khó:", options=["Dễ", "Trung bình", "Khó"], value="Trung bình")

    if st.button("🎲 Tạo Đề Trắc Nghiệm", type="primary", use_container_width=True):
        if not topic_input.strip():
            st.warning("Vui lòng nhập chủ đề hoặc tài liệu cần kiểm tra!")
        else:
            with st.spinner("🤖 AI đang phân tích và tạo bộ câu hỏi trắc nghiệm..."):
                prompt_quiz = f"""
Bạn là một chuyên gia giáo dục. Dựa vào nội dung/chủ đề sau:
"{topic_input}"

Hãy tạo ra đúng {num_questions} câu hỏi trắc nghiệm ở mức độ {difficulty}.
YÊU CẦU BẮT BUỘC:
Chỉ trả về JSON thuần túy (không kèm giải thích bên ngoài, không dùng markdown ```json).
Cấu trúc JSON đúng định dạng sau:
[
  {{
    "question": "Nội dung câu hỏi...",
    "options": ["A. Lựa chọn 1", "B. Lựa chọn 2", "C. Lựa chọn 3", "D. Lựa chọn 4"],
    "correct_answer": "A",
    "explanation": "Giải thích chi tiết vì sao đáp án này đúng..."
  }}
]
"""
                try:
                    response = model.generate_content(prompt_quiz)
                    raw_text = response.text.strip()
                    # Bỏ bọc ```json nếu có
                    if raw_text.startswith("```json"):
                        raw_text = raw_text[7:]
                    if raw_text.startswith("```"):
                        raw_text = raw_text[3:]
                    if raw_text.endswith("```"):
                        raw_text = raw_text[:-3]
                    
                    quiz_json = json.loads(raw_text.strip())
                    st.session_state.quiz_data = quiz_json
                    st.session_state.quiz_topic = topic_input
                    st.session_state.quiz_submitted = False
                    st.session_state.user_answers = {}
                    st.success("Tạo đề thi thành công! Hãy chuyển sang phần Làm bài.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi khi tạo đề: {e}. Vui lòng thử lại!")

# Main Tabs
tab_quiz, tab_chat, tab_history = st.tabs([
    "🎯 Luyện Thi Trắc Nghiệm",
    "💬 Gia Sư AI Hỏi Đáp",
    "📊 Lịch Sử Điểm Số"
])

# ----------------- TAB 1: LÀM TRẮC NGHIỆM -----------------
with tab_quiz:
    st.subheader("📝 Bài Kiểm Tra Trắc Nghiệm")
    if not st.session_state.quiz_data:
        st.info("👈 Hãy nhập chủ đề hoặc dán tài liệu vào **thanh bên trái (Sidebar)** và bấm **'Tạo Đề Trắc Nghiệm'** để bắt đầu!")
    else:
        st.caption(f"Chủ đề: **{st.session_state.quiz_topic[:100]}...**")
        
        # Render câu hỏi
        for idx, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"**Câu {idx + 1}: {q['question']}**")
            
            # Key cho radio button
            radio_key = f"q_{idx}"
            chosen = st.radio(
                f"Chọn đáp án cho câu {idx + 1}:",
                options=q["options"],
                index=None if radio_key not in st.session_state.user_answers else q["options"].index(st.session_state.user_answers[radio_key]),
                key=radio_key,
                disabled=st.session_state.quiz_submitted,
                label_visibility="collapsed"
            )
            if chosen:
                st.session_state.user_answers[radio_key] = chosen

            # Nếu đã nộp bài: hiển thị đáp án đúng/sai
            if st.session_state.quiz_submitted:
                user_ans = st.session_state.user_answers.get(radio_key, "")
                user_choice_letter = user_ans[0] if user_ans else ""
                correct_letter = q["correct_answer"].strip().upper()[0]

                if user_choice_letter == correct_letter:
                    st.success(f"✅ **Chính xác!** Đáp án: **{correct_letter}**")
                else:
                    st.error(f"❌ **Chưa đúng.** Bạn chọn: **{user_choice_letter or 'Chưa chọn'}** | Đáp án đúng: **{correct_letter}**")
                
                with st.expander("📖 Xem giải thích chi tiết"):
                    st.write(q["explanation"])
            
            st.markdown("---")

        # Nút nộp bài
        if not st.session_state.quiz_submitted:
            if st.button("📤 Nộp Bài Chấm Điểm", type="primary", use_container_width=True):
                # Tính điểm
                score = 0
                total = len(st.session_state.quiz_data)
                for idx, q in enumerate(st.session_state.quiz_data):
                    user_ans = st.session_state.user_answers.get(f"q_{idx}", "")
                    user_choice_letter = user_ans[0] if user_ans else ""
                    correct_letter = q["correct_answer"].strip().upper()[0]
                    if user_choice_letter == correct_letter:
                        score += 1
                
                st.session_state.quiz_submitted = True
                st.session_state.last_score = score
                st.session_state.last_total = total
                # Lưu vào lịch sử người dùng
                add_quiz_history(st.session_state.username, st.session_state.quiz_topic, score, total)
                st.rerun()
        else:
            # Kết quả sau khi nộp
            score = st.session_state.get("last_score", 0)
            total = st.session_state.get("last_total", 1)
            pct = round((score / total) * 100)
            
            if pct >= 80:
                st.balloons()
                st.success(f"🎉 Xuất sắc! Bạn đạt **{score}/{total}** câu đúng ({pct}%).")
            elif pct >= 50:
                st.info(f"👍 Khá tốt! Bạn đạt **{score}/{total}** câu đúng ({pct}%). Hãy xem lại các câu sai để ghi nhớ nhé.")
            else:
                st.warning(f"💪 Bạn đạt **{score}/{total}** câu đúng ({pct}%). Cố gắng ôn lại kiến thức và thử lại nào!")

            if st.button("🔄 Làm lại đề mới", use_container_width=True):
                st.session_state.quiz_data = None
                st.session_state.quiz_submitted = False
                st.session_state.user_answers = {}
                st.rerun()

# ----------------- TAB 2: GIA SƯ AI HỎI ĐÁP -----------------
with tab_chat:
    st.subheader("💬 Gia Sư AI - Giải Đáp & Tóm Tắt Bài Học")
    st.write("Bạn có thể đặt câu hỏi về bài học, yêu cầu tóm tắt ý chính hoặc nhờ giải thích lại bất kỳ câu nào trong đề thi.")

    # Hiển thị lịch sử chat
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Ô nhập prompt
    if user_prompt := st.chat_input("Hỏi gia sư bất kỳ điều gì (ví dụ: Tóm tắt bài học, giải thích câu 1...)..."):
        with st.chat_message("user"):
            st.write(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        # Ngữ cảnh nếu có đề thi
        context = ""
        if st.session_state.quiz_topic:
            context = f"\n[Ngữ cảnh chủ đề bài học của học sinh: {st.session_state.quiz_topic}]\n"

        prompt_for_ai = f"""
Bạn là EduMind - một gia sư AI thân thiện, nhiệt tình và sư phạm.
{context}
Lịch sử trao đổi gần nhất:
{st.session_state.chat_history[-5:]}

Câu hỏi của học sinh: {user_prompt}
Hãy trả lời rõ ràng, súc tích, có ví dụ minh họa và định dạng gạch đầu dòng dễ nhìn.
"""
        with st.chat_message("assistant"):
            with st.spinner("Gia sư đang suy nghĩ..."):
                resp = model.generate_content(prompt_for_ai)
                reply = resp.text
                st.write(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

# ----------------- TAB 3: LỊCH SỬ ĐIỂM SỐ -----------------
with tab_history:
    st.subheader(f"📊 Lịch Sử Luyện Thi Của {st.session_state.username}")
    history = get_user_history(st.session_state.username)

    if not history:
        st.info("Bạn chưa hoàn thành bài thi nào. Hãy tạo đề và làm bài ở tab **'Luyện Thi Trắc Nghiệm'** nhé!")
    else:
        # Thống kê nhanh
        total_quizzes = len(history)
        avg_score = round(sum([h["percentage"] for h in history]) / total_quizzes, 1)

        c1, c2 = st.columns(2)
        c1.metric("Tổng số bài đã luyện:", f"{total_quizzes} bài")
        c2.metric("Điểm trung bình:", f"{avg_score}%")

        st.markdown("### Chi tiết các lần làm bài:")
        for idx, h in enumerate(reversed(history)):
            with st.container(border=True):
                st.markdown(f"**Lần {total_quizzes - idx} - {h['date']}**")
                st.write(f"📌 **Chủ đề**: {h['topic'][:150]}...")
                st.write(f"🏆 **Kết quả**: `{h['score']}/{h['total']}` câu đúng (**{h['percentage']}%**)")
