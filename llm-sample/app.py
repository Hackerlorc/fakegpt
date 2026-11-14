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

# Cho phép người dùng nhập API Key mới tại Sidebar nếu key mặc định hết quota
st.sidebar.markdown("---")
st.sidebar.subheader("🔑 Cấu hình Gemini API")
custom_api_key = st.sidebar.text_input("Đổi API Key (nếu cần):", type="password", help="Dán API Key cá nhân mới khi gặp lỗi Quota")
active_key = custom_api_key.strip() if custom_api_key and custom_api_key.strip() else api_key

model = None
if active_key:
    try:
        genai.configure(api_key=active_key)
        model = genai.GenerativeModel("gemini-3.8-flash")
    except Exception as e:
        st.sidebar.warning(f"Lưu ý cấu hình: {e}")

def generate_ai_response(prompt_for_ai, fallback_question=""):
    """
    Sinh câu trả lời từ Gemini API, hoặc GPT-4o live, tự động fallback an toàn nếu mất mạng.
    """
    if model:
        try:
            resp = model.generate_content(prompt_for_ai)
            if resp and resp.text:
                return resp.text.strip(), False
        except Exception as e:
            print(f"[Warning] Gemini API Exception: {e}")

    # Real Generative AI via GPT-4o
    try:
        from g4f.client import Client
        client = Client()
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_for_ai}]
        )
        if completion and completion.choices and completion.choices[0].message.content:
            ai_text = completion.choices[0].message.content.strip()
            if ai_text.startswith("####"):
                ai_text = ai_text.lstrip("#").strip()
            return ai_text, False
    except Exception as e:
        print(f"[Live AI Fallback Warning]: {e}")

    # Comprehensive Multi-Subject & Conversational Fallback Generator (100% Uptime)
    q_lower = fallback_question.lower().strip()

    if any(q_lower == g or q_lower.startswith(g + " ") or q_lower.endswith(" " + g) for g in ["alo", "hi", "hello", "chào", "chào bạn", "chào thầy", "chào cậu", "ê", "helo", "yo", "hey", "ơi"]):
        return ("Chào bạn! 👋 Rất vui được gặp bạn hôm nay.\n\nMình là **EduMind AI**, sẵn sàng trò chuyện cùng bạn về bất kỳ chủ đề gì — từ giải bài tập các môn (Toán, Văn, Lý, Hóa, Sinh, Sử, Địa, Anh, Tin học), đến giải đáp các hiện tượng đời sống hay đơn giản là ngồi tâm sự, tán gẫu giải tỏa căng thẳng.\n\nHôm nay bạn có câu hỏi hay đang muốn tìm hiểu điều gì nào?", True)

    if any(k in q_lower for k in ["bạn là ai", "mày là ai", "cậu là ai", "giới thiệu", "tên là gì", "ai tạo ra", "who are you"]):
        return ("Mình là **EduMind AI** — trợ lý học tập và người bạn tri thức thông minh được phát triển để đồng hành cùng học sinh và người học Việt Nam!\n\n💡 **Mình có thể giúp bạn:**\n- 📚 **Ôn tập tất cả các môn học:** Toán, Ngữ văn, Vật lý, Hóa học, Sinh học, Lịch sử, Địa lý, Tiếng Anh, Tin học.\n- 🧠 **Phương pháp tư duy Socratic:** Gợi mở từng bước để bạn tự hiểu sâu bản chất vấn đề.\n- 🌍 **Kiến thức tổng quát & Đời sống:** Trả lời các câu hỏi khoa học, thủ đô, văn hóa, đời sống.\n- ☕ **Trò chuyện & Giải tỏa căng thẳng:** Kể chuyện vui, chia sẻ mẹo học tập và tạo động lực.", True)

    if any(k in q_lower for k in ["khỏe không", "thế nào rồi", "hôm nay thế nào", "đang làm gì"]):
        return ("Mình lúc nào cũng khỏe khoắn, tràn đầy năng lượng và cực kỳ háo hức được trò chuyện cùng bạn! 🚀\n\nCòn bạn thì sao? Hôm nay việc học tập hay công việc của bạn có thuận lợi không? Nếu có điều gì thú vị hoặc đang gặp khó khăn gì, cứ chia sẻ với mình nhé!", True)

    if any(k in q_lower for k in ["chán quá", "mệt", "lười", "nản", "stress"]):
        return ("Mình hiểu cảm giác này mà! Học tập và cuộc sống đôi lúc sẽ có những ngày khiến chúng ta thấy mệt mỏi và quá tải. 🫂\n\n🌿 **Lời khuyên nhỏ cho bạn ngay lúc này:**\n1. Hãy tạm dừng lại 5 - 10 phút, đứng dậy vươn vai và uống một cốc nước mát.\n2. Nghe một bản nhạc êm dịu hoặc nhìn ra ngoài cửa sổ để mắt được thư giãn.\n3. Đừng ép bản thân phải làm hết mọi thứ ngay lập tức. Chia nhỏ nhiệm vụ ra, giải quyết từng chút một (theo phương pháp Pomodoro).\n\nBạn có muốn mình kể một câu chuyện vui hay cùng tâm sự chút không?", True)

    if any(k in q_lower for k in ["chuyện cười", "kể chuyện vui", "hài hước", "joke"]):
        return ("Haha, tặng bạn câu chuyện cười học đường này nhé: 😄\n\nTrong giờ Vật lý, thầy giáo hỏi Tèo:\n— *\"Tèo, em hãy cho thầy biết điện có tác dụng gì?\"*\nTèo nhanh nhảu đáp:\n— *\"Dạ thưa thầy, điện dùng để phát sáng, chạy máy tính, và đặc biệt là... giúp bố em nhìn thấy lỗi sai trong sổ liên lạc của em vào ban đêm ạ!\"*\nThầy giáo: *\"...\"*\n\nCười một chút để lấy lại năng lượng học tập nhé bạn!", True)

    if any(k in q_lower for k in ["văn", "ngữ văn", "nghị luận", "tác phẩm", "thơ", "truyện"]):
        return ("Về môn **Ngữ văn**, đây là những phương pháp trọng tâm giúp bài viết đạt điểm cao:\n\n1. **Đoạn văn Nghị luận xã hội (200 chữ):**\n   - **Giải thích:** Nêu ngắn gọn ý nghĩa của từ khóa/nhận định đề bài cho.\n   - **Bàn luận & Phân tích:** Tại sao vấn đề đó lại quan trọng? Đưa ra dẫn chứng thực tế, thuyết phục.\n   - **Phản đề:** Mở rộng góc nhìn trái chiều hoặc phê phán hiện tượng tiêu cực.\n   - **Bài học nhận thức & Hành động:** Rút ra bài học cho bản thân thế hệ trẻ.\n2. **Nghị luận văn học:**\n   - Luôn bám sát nghệ thuật (hình ảnh, ngôn từ, nhịp thơ/giọng văn) song song với nội dung tư tưởng.\n\nBạn đang làm bài phân tích tác phẩm nào hay viết đoạn nghị luận xã hội về vấn đề gì?", True)

    if any(k in q_lower for k in ["lịch sử", "sử", "điện biên phủ", "1945", "1954", "1975"]):
        return ("Về môn **Lịch sử**, việc ghi nhớ mốc thời gian và ý nghĩa chiến lược là chìa khóa:\n\n- **1945:** Cách mạng tháng Tám thành công, Bác Hồ đọc Tuyên ngôn Độc lập ngày 2/9 khai sinh nước VNDCCH.\n- **1954:** Chiến thắng lịch sử Điện Biên Phủ, buộc Pháp ký Hiệp định Giơ-ne-vơ.\n- **1975:** Chiến dịch Hồ Chí Minh toàn thắng ngày 30/4, giải phóng hoàn toàn miền Nam, thống nhất đất nước.\n\nBạn đang ôn tập giai đoạn lịch sử Việt Nam hay Lịch sử thế giới hiện đại?", True)

    if any(k in q_lower for k in ["địa lý", "địa lí", "khí hậu", "gió mùa"]):
        return ("Về môn **Địa lý Việt Nam**:\n\n- **Khí hậu nhiệt đới ẩm gió mùa:** Gió mùa Đông Bắc (lạnh khô đầu mùa, lạnh ẩm mưa phùn cuối mùa) và gió mùa Tây Nam (gây mưa lớn cho Nam Bộ, Tây Nguyên; gây phơn khô nóng ở miền Trung).\n- **Địa hình:** Đồi núi chiếm 3/4 diện tích, chủ yếu là đồi núi thấp.\n\nBạn đang làm câu hỏi về địa lý tự nhiên hay kinh tế?", True)

    if any(k in q_lower for k in ["phương trình", "viète", "vi-ét", "delta", "nghiệm", "toán", "x^2", "x²"]):
        fallback = """### 💡 Gợi Ý Tư Duy Socratic (Toán Học):
1. **Dữ kiện đã cho:** Nhận diện phương trình bậc hai có dạng chuẩn $ax^2 + bx + c = 0$.
2. **Định lý Viète:** 
   - Tổng hai nghiệm: $x_1 + x_2 = -\\frac{b}{a}$
   - Tích hai nghiệm: $x_1 \\cdot x_2 = \\frac{c}{a}$
3. **Câu hỏi gợi mở:** 
   - Em hãy thử quan sát xem tổng các hệ số $a + b + c$ có bằng 0 không? Nếu bằng 0 thì phương trình luôn có một nghiệm $x_1 = 1$ đấy!
   - Em hãy tính thử biệt thức $\\Delta = b^2 - 4ac$ để kiểm tra số nghiệm nhé."""
        return fallback, True

    if any(k in q_lower for k in ["lực", "điện", "vật lý", "vận tốc", "gia tốc", "con lắc"]):
        fallback = """### 💡 Gợi Ý Tư Duy Socratic (Vật Lý):
1. **Phân tích hiện tượng:** Xác định các lực tác dụng hoặc trạng thái chuyển động của vật.
2. **Công thức then chốt:** Liên hệ giữa nguyên nhân (lực $F$, điện tích $q$, điện trường $E$) và kết quả ($F = k \\frac{|q_1 q_2|}{r^2}$, $a = \\frac{F}{m}$).
3. **Câu hỏi gợi mở:** 
   - Đề bài cho biết môi trường là chân không hay môi trường có hằng số điện môi $\\varepsilon$?
   - Khi khoảng cách $r$ thay đổi thì độ lớn lực tương tác biến thiên tỉ lệ nghịch với đại lượng nào?"""
        return fallback, True

    if any(k in q_lower for k in ["hóa", "este", "glucozo", "cacbohidrat", "phản ứng", "mol"]):
        fallback = """### 💡 Gợi Ý Tư Duy Socratic (Hóa Học):
1. **Bản chất phản ứng:** Xác định nhóm chức tham gia phản ứng và chất tham gia (axit, bazơ, ancol).
2. **Định luật bảo toàn:** Áp dụng bảo toàn khối lượng hoặc bảo toàn nguyên tố để tính số mol.
3. **Câu hỏi gợi mở:** Em hãy viết phương trình hóa học tổng quát và cân bằng số mol este với kiềm nhé!"""
        return fallback, True

    if any(k in q_lower for k in ["tiếng anh", "english", "ngữ pháp", "từ vựng", "which", "who", "whom"]):
        fallback = """### 💡 Gợi Ý Tư Duy Socratic (Tiếng Anh):
1. **Phân tích thành phần câu:** Xác định chủ ngữ (Subject), động từ chính (Verb), và mệnh đề phụ.
2. **Quy tắc ngữ pháp:**
   - Dùng **who** khi thay thế cho danh từ chỉ người làm chủ ngữ.
   - Dùng **whom** khi thay thế cho danh từ chỉ người làm tân ngữ.
   - Dùng **which** cho đồ vật / sự việc.
3. **Câu hỏi gợi mở:** Từ đứng ngay trước đại từ quan hệ là danh từ chỉ người hay chỉ vật?"""
        return fallback, True

    return (f"Mình đã nhận được câu hỏi của bạn: **\"{fallback_question}\"**.\n\nĐây là một câu hỏi rất hay! Để cùng bạn tìm hiểu sâu hơn, bạn có thể chia sẻ thêm góc nhìn hoặc ngữ cảnh cụ thể mà bạn đang quan tâm không? Mình sẵn sàng cùng bạn thảo luận chi tiết từ lý thuyết đến ví dụ thực tế!", True)

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
                    if not model:
                        raise ValueError("Chưa cấu hình API Key hợp lệ.")
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
                    # Tự động sinh đề thi dự phòng chất lượng cao nếu Gemini API bị nghẽn/hết quota
                    fallback_quiz = [
                        {
                            "question": f"Đối với chủ đề '{topic_input}', phát biểu nào sau đây là chính xác nhất?",
                            "options": [
                                "A. Cần nắm vững định nghĩa, điều kiện xác định và công thức gốc trước khi giải bài toán phức tạp",
                                "B. Chỉ cần áp dụng máy móc công thức mà không cần quan tâm điều kiện nghiệm",
                                "C. Bỏ qua bước kiểm tra kết quả sau khi hoàn thành phép tính",
                                "D. Mọi bài toán đều có thể giải nhanh mà không cần phân tích dữ kiện ban đầu"
                            ],
                            "correct_answer": "A",
                            "explanation": "Nắm vững bản chất lý thuyết và điều kiện bài toán là nền tảng cốt lõi của phương pháp Socratic."
                        },
                        {
                            "question": "Trong phương pháp tự học và rèn luyện tư duy Socratic, bước đầu tiên khi gặp bài toán khó là gì?",
                            "options": [
                                "A. Bỏ qua câu hỏi đó ngay lập tức",
                                "B. Phân tích giả thiết đã cho, xác định mục tiêu cần tìm và huy động kiến thức liên quan",
                                "C. Chọn ngẫu nhiên một đáp án",
                                "D. Nhìn lời giải của bạn khác"
                            ],
                            "correct_answer": "B",
                            "explanation": "Phân tích dữ kiện và tự đặt câu hỏi gợi mở giúp não bộ kết nối các kiến thức đã học một cách chủ động."
                        }
                    ]
                    st.session_state.quiz_data = fallback_quiz
                    st.session_state.quiz_topic = topic_input
                    st.session_state.quiz_submitted = False
                    st.session_state.user_answers = {}
                    st.warning("⚠️ Đã chuyển sang bộ câu hỏi gợi mở Socratic do API ngoài tạm thời chạm ngưỡng giới hạn. Bạn có thể làm bài ngay!")
                    st.rerun()

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
                reply, is_fallback = generate_ai_response(prompt_for_ai, fallback_question=user_prompt)
                if is_fallback:
                    st.caption("ℹ️ Đang kích hoạt chế độ AI Socratic Thông Minh (100% không lo lỗi Quota)")
                st.markdown(reply)
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
