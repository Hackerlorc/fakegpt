"""
EduMind AI - Unified Application & Database Server
Combines High-Performance Static Web Serving with SQLite REST API.
Port: 8080
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys

import database

PORT = 8080
WEB_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_socratic_reply(question, user_api_key=None):
    # 1. If user explicitly provided a Gemini API Key, try Google Gemini
    if user_api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=user_api_key)
            model = genai.GenerativeModel("gemini-flash-latest")
            prompt = f"""
Bạn là EduMind AI - Trợ lý gia sư và người bạn đồng hành thông minh, thân thiện của học sinh Việt Nam.
Câu hỏi của học sinh: "{question}"
Hãy trả lời tự nhiên, thân thiện, giải thích bản chất dễ hiểu, dùng LaTeX cho công thức nếu có.
"""
            res = model.generate_content(prompt, request_options={"timeout": 6.0})
            if res and res.text:
                return {
                    "text": res.text.strip(),
                    "socraticHint": "Bạn có muốn mình giải thích chi tiết hơn hay làm bài tập liên quan không?",
                    "source": "gemini-live"
                }
        except Exception as e:
            print("[Gemini Custom Key Warning]:", e)

    # 2. Real Generative AI Engine (GPT-4o / GPT-4o-mini live generative responses)
    try:
        from g4f.client import Client
        client = Client()
        system_msg = (
            "Bạn là EduMind AI - Trợ lý gia sư và người bạn đồng hành thông minh, thân thiện của học sinh Việt Nam. "
            "Bạn có thể trò chuyện tự nhiên, giải đáp bài tập mọi môn học (Toán, Văn, Lý, Hóa, Sinh, Sử, Địa, Anh, Tin học), "
            "và trả lời mọi câu hỏi đời sống, khoa học một cách sinh động, dễ hiểu, chuẩn tiếng Việt."
        )
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": question}
            ]
        )
        if completion and completion.choices and completion.choices[0].message.content:
            ai_text = completion.choices[0].message.content.strip()
            if ai_text.startswith("####"):
                ai_text = ai_text.lstrip("#").strip()
            return {
                "text": ai_text,
                "socraticHint": "Bạn có muốn mình giải thích chi tiết hơn hay làm bài tập liên quan không?",
                "source": "generative-ai"
            }
    except Exception as e:
        print("[Live Generative AI Warning]:", e)

    # 3. Comprehensive High-Intelligence Offline Fallback (Active when no internet)
    q_lower = question.lower().strip()

    # 1. Greetings & Everyday Conversation
    if any(q_lower == g or q_lower.startswith(g + " ") or q_lower.endswith(" " + g) for g in ["alo", "hi", "hello", "chào", "chào bạn", "chào thầy", "chào cậu", "ê", "helo", "yo", "hey", "ơi"]):
        return {
            "text": "Chào bạn! 👋 Rất vui được gặp bạn hôm nay.\n\nMình là **EduMind AI**, sẵn sàng trò chuyện cùng bạn về bất kỳ chủ đề gì — từ giải bài tập các môn (Toán, Văn, Lý, Hóa, Sinh, Sử, Địa, Anh, Tin học), đến giải đáp các hiện tượng đời sống hay đơn giản là ngồi tâm sự, tán gẫu giải tỏa căng thẳng.\n\nHôm nay bạn có câu hỏi hay đang muốn tìm hiểu điều gì nào?",
            "socraticHint": "Gợi ý: Bạn có thể hỏi bất cứ điều gì, từ bài tập đến kiến thức đời sống!",
            "source": "edu-socratic"
        }

    # 2. Identity & Introduction
    if any(k in q_lower for k in ["bạn là ai", "mày là ai", "cậu là ai", "giới thiệu", "tên là gì", "ai tạo ra", "who are you"]):
        return {
            "text": "Mình là **EduMind AI** — trợ lý học tập và người bạn tri thức thông minh được phát triển để đồng hành cùng học sinh và người học Việt Nam!\n\n💡 **Mình có thể giúp bạn:**\n- 📚 **Ôn tập tất cả các môn học:** Toán, Ngữ văn, Vật lý, Hóa học, Sinh học, Lịch sử, Địa lý, Tiếng Anh, Tin học.\n- 🧠 **Phương pháp tư duy Socratic:** Gợi mở từng bước để bạn tự hiểu sâu bản chất vấn đề.\n- 🌍 **Kiến thức tổng quát & Đời sống:** Trả lời các câu hỏi khoa học, thủ đô, văn hóa, đời sống.\n- ☕ **Trò chuyện & Giải tỏa căng thẳng:** Kể chuyện vui, chia sẻ mẹo học tập và tạo động lực.",
            "socraticHint": "Hãy thử hỏi mình một câu đố hoặc một chủ đề bạn đang quan tâm nhé!",
            "source": "edu-socratic"
        }

    # 3. Chit-chat: How are you, Mood, Motivation, Jokes
    if any(k in q_lower for k in ["khỏe không", "thế nào rồi", "hôm nay thế nào", "đang làm gì", "how are you"]):
        return {
            "text": "Mình lúc nào cũng khỏe khoắn, tràn đầy năng lượng và cực kỳ háo hức được trò chuyện cùng bạn! 🚀\n\nCòn bạn thì sao? Hôm nay việc học tập hay công việc của bạn có thuận lợi không? Nếu có điều gì thú vị hoặc đang gặp khó khăn gì, cứ chia sẻ với mình nhé!",
            "socraticHint": "Hãy kể cho mình nghe về ngày hôm nay của bạn nhé!",
            "source": "edu-socratic"
        }

    if any(k in q_lower for k in ["chán quá", "mệt", "lười", "nản", "stress", "áp lực"]):
        return {
            "text": "Mình hiểu cảm giác này mà! Học tập và cuộc sống đôi lúc sẽ có những ngày khiến chúng ta thấy mệt mỏi và quá tải. 🫂\n\n🌿 **Lời khuyên nhỏ cho bạn ngay lúc này:**\n1. Hãy tạm dừng lại 5 - 10 phút, đứng dậy vươn vai và uống một cốc nước mát.\n2. Nghe một bản nhạc êm dịu hoặc nhìn ra ngoài cửa sổ để mắt được thư giãn.\n3. Đừng ép bản thân phải làm hết mọi thứ ngay lập tức. Chia nhỏ nhiệm vụ ra, giải quyết từng chút một (theo phương pháp Pomodoro).\n\nBạn có muốn mình kể một câu chuyện vui hay cùng tâm sự chút không?",
            "socraticHint": "Nghỉ ngơi một chút rồi chúng ta lại tiếp tục nhé!",
            "source": "edu-socratic"
        }

    if any(k in q_lower for k in ["chuyện cười", "kể chuyện vui", "hài hước", "kể chuyện hài", "joke"]):
        return {
            "text": "Haha, tặng bạn câu chuyện cười học đường này nhé: 😄\n\nTrong giờ Vật lý, thầy giáo hỏi Tèo:\n— *\"Tèo, em hãy cho thầy biết điện có tác dụng gì?\"*\nTèo nhanh nhảu đáp:\n— *\"Dạ thưa thầy, điện dùng để phát sáng, chạy máy tính, và đặc biệt là... giúp bố em nhìn thấy lỗi sai trong sổ liên lạc của em vào ban đêm ạ!\"*\nThầy giáo: *\"...\"*\n\nCười một chút để lấy lại năng lượng học tập nhé bạn!",
            "socraticHint": "Bạn có muốn nghe thêm câu chuyện nào nữa không?",
            "source": "edu-socratic"
        }

    if any(k in q_lower for k in ["cảm ơn", "thank", "tks", "cam on"]):
        return {
            "text": "Không có gì đâu bạn ơi! Giúp được bạn là niềm vui lớn nhất của mình rồi. 🥰\n\nBất cứ khi nào bạn cần giải đáp bài tập hay chỉ muốn tìm người trò chuyện, mình luôn ở đây sẵn sàng hỗ trợ nhé!",
            "socraticHint": "Chúc bạn một ngày học tập thật hứng khởi!",
            "source": "edu-socratic"
        }

    if any(k in q_lower for k in ["tạm biệt", "bye", "goodbye", "ngủ đây", "đi ngủ", "g9"]):
        return {
            "text": "Tạm biệt bạn nhé! Chúc bạn có một giấc ngủ thật ngon lành để nạp lại đầy pin cho ngày mai. Hẹn gặp lại bạn sớm nha! ✨",
            "socraticHint": "Chúc bạn ngủ ngon và có những giấc mơ đẹp!",
            "source": "edu-socratic"
        }

    # 4. Literature & Writing (Ngữ văn)
    if any(k in q_lower for k in ["văn", "ngữ văn", "nghị luận", "tác phẩm", "thơ", "truyện", "vợ chồng a phủ", "chiếc thuyền ngoài xa", "sóng", "tây tiến", "đất nước", "việt bắc", "truyện kiều"]):
        return {
            "text": "Về môn **Ngữ văn**, đây là những phương pháp trọng tâm giúp bài viết đạt điểm cao:\n\n1. **Đoạn văn Nghị luận xã hội (200 chữ):**\n   - **Giải thích:** Nêu ngắn gọn ý nghĩa của từ khóa/nhận định đề bài cho.\n   - **Bàn luận & Phân tích:** Tại sao vấn đề đó lại quan trọng? Đưa ra dẫn chứng thực tế, thuyết phục.\n   - **Phản đề:** Mở rộng góc nhìn trái chiều hoặc phê phán hiện tượng tiêu cực.\n   - **Bài học nhận thức & Hành động:** Rút ra bài học cho bản thân thế hệ trẻ.\n2. **Nghị luận văn học:**\n   - Luôn bám sát nghệ thuật (hình ảnh, ngôn từ, nhịp thơ/giọng văn) song song với nội dung tư tưởng.\n   - So sánh, liên hệ mở rộng với các tác phẩm cùng đề tài.\n\nBạn đang làm bài phân tích tác phẩm nào hay viết đoạn nghị luận xã hội về vấn đề gì?",
            "socraticHint": "Hãy chia sẻ đề văn cụ thể để mình hướng dẫn lập dàn ý chi tiết nhé!",
            "source": "edu-socratic"
        }

    # 5. History (Lịch sử)
    if any(k in q_lower for k in ["lịch sử", "sử", "điện biên phủ", "cách mạng tháng tám", "chiến dịch hồ chí minh", "thế chiến", "chiến tranh lạnh", "1945", "1954", "1975"]):
        return {
            "text": "Về môn **Lịch sử**, việc ghi nhớ mốc thời gian và ý nghĩa chiến lược là chìa khóa:\n\n- **1945:** Cách mạng tháng Tám thành công, Bác Hồ đọc Tuyên ngôn Độc lập ngày 2/9 khai sinh nước VNDCCH.\n- **1954:** Chiến thắng lịch sử Điện Biên Phủ (*\"Lừng lẫy năm châu, chấn động địa cầu\"*), buộc Pháp ký Hiệp định Giơ-ne-vơ.\n- **1975:** Chiến dịch Hồ Chí Minh toàn thắng ngày 30/4, giải phóng hoàn toàn miền Nam, thống nhất đất nước.\n- **Thế chiến II (1939 - 1945):** Phe Đồng minh đánh bại chủ nghĩa phát xít (Đức - Ý - Nhật).\n\nBạn đang ôn tập giai đoạn lịch sử Việt Nam hay Lịch sử thế giới hiện đại?",
            "socraticHint": "Hãy liên hệ giữa nguyên nhân, diễn biến và ý nghĩa lịch sử của sự kiện nhé!",
            "source": "edu-socratic"
        }

    # 6. Geography (Địa lý)
    if any(k in q_lower for k in ["địa lý", "địa lí", "khí hậu", "gió mùa", "địa hình", "sông ngòi", "vùng kinh tế", "đồng bằng", "tây nguyên"]):
        return {
            "text": "Về môn **Địa lý Việt Nam**:\n\n1. **Khí hậu nhiệt đới ẩm gió mùa:**\n   - **Gió mùa Đông Bắc (tháng 11 - 4):** Đầu mùa lạnh khô, nửa sau mùa lạnh ẩm gây mưa phùn ở Bắc Bộ.\n   - **Gió mùa Tây Nam (tháng 5 - 10):** Gây mưa lớn cho Nam Bộ, Tây Nguyên và gây hiệu ứng phơn khô nóng (gió Lào) ở duyên hải miền Trung.\n2. **Địa hình:** Đồi núi chiếm 3/4 diện tích, chủ yếu là đồi núi thấp (dưới 1000m chiếm 85%).\n3. **Kinh tế:** Vùng kinh tế trọng điểm phía Nam là vùng kinh tế năng động và đóng góp GDP lớn nhất cả nước.\n\nBạn đang làm câu hỏi về tự nhiên hay địa lý các ngành kinh tế?",
            "socraticHint": "Kết hợp Atlat Địa lý Việt Nam là bí quyết giải nhanh và chính xác nhất!",
            "source": "edu-socratic"
        }

    # 7. Biology (Sinh học)
    if any(k in q_lower for k in ["sinh học", "sinh", "adn", "arn", "men-đen", "di truyền", "đột biến", "quang hợp", "hệ sinh thái", "nhiễm sắc thể"]):
        return {
            "text": "Về môn **Sinh học**:\n\n1. **Cơ chế di truyền phân tử:**\n   - Phân tử ADN có cấu trúc xoắn kép theo nguyên tắc bổ sung ($A - T$ bằng 2 liên kết hiđro, $G - X$ bằng 3 liên kết hiđro).\n   - Quá trình nhân đôi ADN diễn ra theo nguyên tắc bán bảo toàn và nguyên tắc bổ sung.\n2. **Quy luật Men-đen:**\n   - Lai một cặp tính trạng: F2 phân ly tỉ lệ kiểu hình 3 trội : 1 lặn.\n   - Phân ly độc lập: Tỉ lệ F2 là 9:3:3:1.\n3. **Đột biến gen:** Gồm các dạng mất, thêm hoặc thay thế một cặp nuclêôtit.\n\nBài tập Sinh học của bạn đang thuộc phần di truyền hay phần sinh thái học?",
            "socraticHint": "Hãy nhớ đếm tổng số nuclêôtit $N = 2A + 2G$ và chiều dài $L = \\frac{N}{2} \\times 3.4$ Å.",
            "source": "edu-socratic"
        }

    # 8. Informatics & Programming (Tin học & Lập trình)
    if any(k in q_lower for k in ["tin học", "lập trình", "python", "code", "thuật toán", "javascript", "c++", "vòng lặp", "hàm"]):
        return {
            "text": "Về **Tin học & Lập trình**:\n\n- **Tư duy lập trình cốt lõi:**\n  1. **Tuần tự (Sequence):** Lệnh thực thi từ trên xuống dưới.\n  2. **Rẽ nhánh (Selection):** Cấu trúc điều kiện `if ... elif ... else`.\n  3. **Lặp (Iteration):** Vòng lặp `for` (khi biết trước số lần lặp) hoặc `while` (lặp theo điều kiện).\n- **Ví dụ hàm tính tổng trong Python:**\n  ```python\n  def tinh_tong(n):\n      return sum(range(1, n + 1))\n  ```\n\nBạn đang học ngôn ngữ lập trình nào (Python, Pascal, C++, JavaScript) hay đang muốn giải thuật toán nào?",
            "socraticHint": "Hãy chia nhỏ bài toán thành Input -> Xử lý thuật toán -> Output.",
            "source": "edu-socratic"
        }

    # 9. Natural Science & Everyday Trivia (Khoa học & Đời sống)
    if any(k in q_lower for k in ["bầu trời màu xanh", "sao trời màu xanh", "tại sao trời xanh", "màu xanh"]):
        return {
            "text": "Hiện tượng bầu trời có màu xanh ban ngày là do **tán xạ Rayleigh** của ánh sáng Mặt Trời trong bầu khí quyển Trái Đất:\n\n- Ánh sáng Mặt Trời là ánh sáng trắng, gồm vô số bước sóng từ đỏ đến tím.\n- Khi ánh sáng đi vào bầu khí quyển, nó va chạm với các phân tử khí (Nitơ, Oxy).\n- Ánh sáng có bước sóng ngắn (xanh lam, tím) bị tán xạ mạnh hơn rất nhiều so với ánh sáng bước sóng dài (đỏ, vàng).\n- Do mắt con người nhạy cảm với màu xanh lam hơn màu tím, nên chúng ta nhìn thấy bầu trời có màu xanh lam tuyệt đẹp! 🌌",
            "socraticHint": "Vào lúc hoàng hôn, ánh sáng phải đi qua tầng khí quyển dày hơn nên ta lại thấy trời màu đỏ cam đấy!",
            "source": "edu-socratic"
        }

    if any(k in q_lower for k in ["thủ đô", "capital"]):
        return {
            "text": "Dưới đây là thủ đô của một số quốc gia nổi tiếng trên thế giới:\n\n- 🇻🇳 **Việt Nam:** Hà Nội\n- 🇫🇷 **Pháp:** Paris\n- 🇯🇵 **Nhật Bản:** Tokyo\n- 🇺🇸 **Hoa Kỳ (Mỹ):** Washington, D.C.\n- 🇬🇧 **Vương quốc Anh:** London\n- 🇰🇷 **Hàn Quốc:** Seoul\n- 🇩🇪 **Đức:** Berlin\n- 🇨🇳 **Trung Quốc:** Bắc Kinh\n- 🇷🇺 **Nga:** Moskva (Moscow)\n- 🇦🇺 **Úc:** Canberra (rất nhiều người hay nhầm với Sydney!)\n\nBạn đang muốn hỏi thủ đô của đất nước nào nữa không?",
            "socraticHint": "Đố bạn: Thủ đô của Canada là thành phố nào? (Gợi ý: Không phải Toronto đâu nhé!)",
            "source": "edu-socratic"
        }

    # 2. Simple arithmetic & basic math
    if any(k in q_lower for k in ["1+1", "1 + 1", "2+2", "2 + 2"]):
        return {
            "text": "Trong số học thập phân thông thường, $1 + 1 = 2$.\n\nTuy nhiên trong hệ nhị phân (Binary) dùng cho máy tính điện tử, $1 + 1 = 10_2$ (số 2 trong hệ cơ số 2) đấy! Em có đang cần hỗ trợ bài toán hay chuyên đề cụ thể nào không?",
            "socraticHint": "Hãy chia sẻ bài tập toán mà em muốn cùng giải quyết nhé!",
            "source": "edu-socratic"
        }

    # 3. Quadratic equations & Viète theorem
    if any(k in q_lower for k in ["viète", "viete", "bậc hai", "bậc 2", "delta", "nghiệm", "phương trình", "x^2", "x²"]):
        return {
            "text": "Đối với phương trình bậc hai $ax^2 + bx + c = 0$ ($a \\neq 0$):\n\n1. **Biệt thức:** $\\Delta = b^2 - 4ac$ (hoặc $\\Delta' = b'^2 - ac$). Nếu $\\Delta > 0$, phương trình có 2 nghiệm phân biệt.\n2. **Định lý Viète:**\n   - Tổng hai nghiệm: $S = x_1 + x_2 = -\\frac{b}{a}$\n   - Tích hai nghiệm: $P = x_1 \\cdot x_2 = \\frac{c}{a}$\n3. **Mẹo nhẩm nghiệm nhanh:**\n   - Nếu $a + b + c = 0 \\implies x_1 = 1, x_2 = \\frac{c}{a}$\n   - Nếu $a - b + c = 0 \\implies x_1 = -1, x_2 = -\\frac{c}{a}$\n   - Nhẩm hai số có tổng bằng $S$ và tích bằng $P$.\n\nEm đang làm phương trình cụ thể nào, hãy gửi đề bài để thầy hướng dẫn từng bước nhé!",
            "socraticHint": "Hãy xác định 3 hệ số a, b, c của phương trình em đang xét.",
            "source": "edu-socratic"
        }

    # 4. Calculus & Functions (Lớp 12)
    if any(k in q_lower for k in ["hàm số", "đạo hàm", "cực trị", "đồng biến", "nghịch biến", "tiệm cận", "tích phân", "nguyên hàm"]):
        return {
            "text": "Khảo sát và xử lý bài toán hàm số luôn tuân theo các bước nền tảng:\n\n1. **Tập xác định:** Tìm điều kiện của $x$ để hàm số có nghĩa.\n2. **Tính đạo hàm $y'$:** Giải phương trình $y' = 0$ để tìm điểm dừng.\n3. **Xét dấu đạo hàm:**\n   - $y' > 0$ trên $(a; b) \\implies$ hàm số đồng biến.\n   - $y' < 0$ trên $(a; b) \\implies$ hàm số nghịch biến.\n   - $y'$ đổi dấu từ (+) sang (-) qua $x_0 \\implies x_0$ là điểm cực đại.\n\nBài toán của em thuộc dạng đa thức bậc ba, hàm phân thức bậc nhất hay chứa tham số $m$?",
            "socraticHint": "Lưu ý kiểm tra xem đạo hàm có đổi dấu qua nghiệm bội chẵn hay không!",
            "source": "edu-socratic"
        }

    # 5. Physics: Coulomb, Electricity, Mechanics
    if any(k in q_lower for k in ["lực", "điện", "cu-lông", "coulomb", "tĩnh điện", "dao động", "con lắc", "vận tốc", "gia tốc", "vật lý"]):
        return {
            "text": "Đối với bài toán Vật lý, em hãy nắm vững công thức gốc:\n\n- **Định luật Cu-lông:** $F = k \\frac{|q_1 q_2|}{\\varepsilon r^2}$ với $k = 9 \\cdot 10^9 \\text{ N}\\cdot\\text{m}^2/\\text{C}^2$.\n- **Quy luật:** Lực $F$ tỉ lệ nghịch với bình phương khoảng cách $r^2$. Khoảng cách tăng 2 lần thì lực giảm 4 lần.\n- **Nguyên lý chuyển động:** $F_{\\text{hl}} = m \\cdot a$.\n\nHai điện tích trong bài là cùng dấu hay trái dấu? Em đã đổi đơn vị sang mét (m) và Cu-lông (C) chưa?",
            "socraticHint": "Hãy tóm tắt các đại lượng đã cho kèm đơn vị chuẩn SI ra giấy nháp trước nhé!",
            "source": "edu-socratic"
        }

    # 6. Chemistry: Organic, Esters, Lipids, Reactions
    if any(k in q_lower for k in ["este", "lipit", "ancol", "axit", "xà phòng", "hóa", "glucozo", "cacbohidrat"]):
        return {
            "text": "Về chuyên đề Hóa học hữu cơ (Este & Lipit):\n\n1. **Phản ứng thủy phân trong môi trường kiềm (Xà phòng hóa):**\n   $$RCOOR' + NaOH \\xrightarrow{t^\\circ} RCOONa + R'OH$$\n2. **Bảo toàn khối lượng:**\n   $$m_{\\text{este}} + m_{NaOH} = m_{\\text{muối}} + m_{\\text{ancol}}$$\n3. **Este đơn chức no mạch hở:** Công thức phân tử chung là $C_n H_{2n} O_2$ ($n \\ge 2$).\n\nEm đang cần tìm công thức cấu tạo của este hay tính khối lượng muối thu được sau phản ứng?",
            "socraticHint": "So sánh tỉ lệ mol giữa este và kiềm để nhận biết este thông thường hay este của phenol.",
            "source": "edu-socratic"
        }

    # 7. English Grammar & Vocabulary
    if any(k in q_lower for k in ["english", "tiếng anh", "ngữ pháp", "mệnh đề", "từ vựng", "who", "whom", "which", "whose"]):
        return {
            "text": "Về đại từ quan hệ trong Tiếng Anh (Relative Pronouns):\n\n- **Who:** Thay thế cho danh từ chỉ người làm chủ ngữ ($S + \\text{who} + V$).\n- **Whom:** Thay thế cho danh từ chỉ người làm tân ngữ ($S + \\text{whom} + S + V$).\n- **Which:** Thay thế cho danh từ chỉ sự vật, hiện tượng.\n- **Whose:** Chỉ quan hệ sở hữu ($N + \\text{whose} + N$).\n- **That:** Có thể thay thế cho who/which trong mệnh đề xác định (không đứng sau dấu phẩy và giới từ).\n\nEm hãy gửi câu bài tập tiếng Anh cụ thể để thầy cùng phân tích thành phần câu nhé!",
            "socraticHint": "Nhìn vào từ đứng ngay trước chỗ trống là danh từ chỉ người hay vật.",
            "source": "edu-socratic"
        }

    # 8. Intelligent Open Conversation (Tự do, đa năng)
    return {
        "text": f"Mình đã nhận được câu hỏi của bạn: **\"{question}\"**.\n\nĐây là một chủ đề rất thú vị! Để cùng bạn tìm hiểu sâu hơn, bạn có thể chia sẻ thêm góc nhìn của mình hoặc ngữ cảnh cụ thể bạn đang quan tâm không? Mình sẵn sàng cùng bạn thảo luận chi tiết từ lý thuyết đến ví dụ thực tế!",
        "socraticHint": "Bạn có thể chia sẻ thêm chi tiết để mình cùng bạn phân tích sâu hơn nhé!",
        "source": "edu-socratic"
    }

class EduMindHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def _read_body_json(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length > 0:
                raw = self.rfile.read(length).decode("utf-8")
                return json.loads(raw)
        except Exception as e:
            print("Error parsing JSON body:", e)
        return {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # ----------------- REST API ROUTES -----------------
        if path.startswith("/api/"):
            if path == "/api/users":
                users = database.get_all_users()
                return self._send_json({"success": True, "users": users})

            elif path == "/api/quizzes":
                quizzes = database.get_all_quizzes()
                return self._send_json({"success": True, "quizzes": quizzes})

            elif path == "/api/attempts":
                query = urllib.parse.parse_qs(parsed.query)
                uid = query.get("userId", [None])[0]
                attempts = database.get_all_attempts(user_id=uid)
                return self._send_json({"success": True, "attempts": attempts})

            elif path == "/api/user-stats":
                query = urllib.parse.parse_qs(parsed.query)
                uid = query.get("userId", [""])[0]
                stats = database.get_user_stats(uid)
                return self._send_json({"success": True, "stats": stats})

            elif path == "/api/knowledge-gaps":
                query = urllib.parse.parse_qs(parsed.query)
                uid = query.get("userId", [None])[0]
                gaps = database.get_knowledge_gaps(user_id=uid)
                return self._send_json({"success": True, "gaps": gaps})

            elif path == "/api/roadmap":
                query = urllib.parse.parse_qs(parsed.query)
                uid = query.get("userId", [None])[0]
                roadmap = database.get_active_roadmap(user_id=uid)
                return self._send_json({"success": True, "roadmap": roadmap})

            elif path == "/api/chat":
                messages = database.get_chat_history()
                return self._send_json({"success": True, "messages": messages})

            elif path == "/api/stats":
                users = database.get_all_users()
                attempts = database.get_all_attempts()
                quizzes = database.get_all_quizzes()
                total_users = len(users)
                active_users = sum(1 for u in users if u.get("status") == "active")
                pro_users = sum(1 for u in users if u.get("plan") == "Pro")
                locked_users = sum(1 for u in users if u.get("status") == "locked")
                return self._send_json({
                    "success": True,
                    "stats": {
                        "totalUsers": total_users,
                        "activeUsers": active_users,
                        "proUsers": pro_users,
                        "lockedUsers": locked_users,
                        "totalQuizzes": len(quizzes),
                        "totalAttempts": len(attempts)
                    }
                })

            elif path == "/api/notes":
                query = urllib.parse.parse_qs(parsed.query)
                uid = query.get("userId", ["local_user"])[0]
                users = database.get_all_users()
                user = next((u for u in users if u["id"] == uid), None)
                return self._send_json({"success": True, "notes": user.get("notes", "") if user else ""})

            else:
                return self._send_json({"error": "Endpoint not found"}, status=404)

        # ----------------- STATIC FILE SERVING -----------------
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self._read_body_json()

        if path == "/api/auth/login":
            email = body.get("email", "").strip()
            password = body.get("password", "")
            user = database.authenticate_user(email, password)
            if user:
                return self._send_json({"success": True, "user": user})
            return self._send_json({"success": False, "error": "Email hoặc mật khẩu không chính xác."}, status=401)

        elif path == "/api/auth/register":
            name = body.get("name", "").strip()
            email = body.get("email", "").strip()
            password = body.get("password", "")
            if not email or not password:
                return self._send_json({"success": False, "error": "Vui lòng nhập đủ thông tin."}, status=400)
            created = database.create_user({"name": name, "email": email, "password": password})
            return self._send_json({"success": True, "user": created})

        elif path == "/api/users":
            created = database.create_user(body)
            return self._send_json({"success": True, "user": created}, status=201)

        elif path == "/api/quizzes":
            created = database.create_quiz(body)
            return self._send_json({"success": True, "quiz": created}, status=201)

        elif path == "/api/attempts":
            created = database.create_attempt(body)
            return self._send_json({"success": True, "attempt": created}, status=201)

        elif path == "/api/chat":
            msg = database.add_chat_message(body)
            return self._send_json({"success": True, "message": msg}, status=201)

        elif path == "/api/chat/clear":
            database.clear_chat_history()
            return self._send_json({"success": True})

        elif path == "/api/ai/chat":
            question = (body.get("question") or "").strip()
            raw_key = body.get("apiKey")
            user_key = raw_key.strip() if (isinstance(raw_key, str) and raw_key.strip()) else None
            reply_obj = generate_socratic_reply(question, user_api_key=user_key)
            return self._send_json({"success": True, **reply_obj})

        elif path == "/api/notes":
            uid = body.get("userId", "local_user")
            notes = body.get("notes", "")
            database.update_user(uid, {"notes": notes})
            return self._send_json({"success": True})

        elif path == "/api/survey":
            uid = body.get("userId", "local_user")
            survey_json = json.dumps(body.get("survey", {}), ensure_ascii=False)
            database.update_user(uid, {"survey": survey_json})
            return self._send_json({"success": True})

        elif path == "/api/db/seed":
            database.init_db()
            return self._send_json({"success": True, "message": "Database reset & seeded successfully."})

        return self._send_json({"error": "Endpoint not found"}, status=404)

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self._read_body_json()

        if path.startswith("/api/users/"):
            uid = path.replace("/api/users/", "").strip()
            database.update_user(uid, body)
            return self._send_json({"success": True, "id": uid})

        return self._send_json({"error": "Endpoint not found"}, status=404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/users/"):
            uid = path.replace("/api/users/", "").strip()
            database.delete_user(uid)
            return self._send_json({"success": True, "deleted": uid})

        return self._send_json({"error": "Endpoint not found"}, status=404)

def run():
    database.init_db()
    print("=" * 60)
    print(f" EduMind AI - Server with SQLite Database running on port {PORT}")
    print(f" Database: {database.DB_PATH}")
    print(f" Open browser: http://localhost:{PORT}")
    print("=" * 60)
    sys.stdout.flush()

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), EduMindHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    run()
