BEGIN TRANSACTION;
CREATE TABLE chat_messages (
        id TEXT PRIMARY KEY,
        user_id TEXT DEFAULT 'local_user',
        sender TEXT NOT NULL,
        is_ai BOOLEAN DEFAULT 0,
        text TEXT NOT NULL,
        socratic_hint TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
INSERT INTO "chat_messages" VALUES('msg_01','usr_001','Study Coach',1,'Chào em! Hôm nay chúng ta tiếp tục với phần Định lý Viète nhé. Em hãy nhớ lại xem: nếu phương trình bậc hai ax² + bx + c = 0 có hai nghiệm x₁ và x₂, thì tổng và tích của chúng được tính như thế nào?','Hãy nhớ đến công thức liên hệ giữa các hệ số a, b, c với (x₁ + x₂) và (x₁ × x₂).','2026-10-31 13:38:13');
INSERT INTO "chat_messages" VALUES('msg_02','usr_001','Bạn',0,'Dạ, x1 + x2 = -b/a và x1 * x2 = c/a ạ.','','2026-10-31 13:38:13');
INSERT INTO "chat_messages" VALUES('msg_03','usr_001','Study Coach',1,'Rất chính xác! Bây giờ giả sử thầy có phương trình x² - 5x + 6 = 0. Không cần tính Δ, em có thể nhẩm ra hai số nào có tổng bằng 5 và tích bằng 6 không?','Tìm hai số nguyên dương nhỏ mà tích bằng 6 (ví dụ: 1 và 6, hoặc 2 và 3).','2026-10-31 13:38:13');
CREATE TABLE knowledge_gaps (
        id TEXT PRIMARY KEY,
        user_id TEXT DEFAULT 'local_user',
        subject TEXT NOT NULL,
        topic TEXT NOT NULL,
        accuracy_percent REAL NOT NULL,
        priority TEXT DEFAULT 'Trung bình',
        description TEXT DEFAULT ''
    );
INSERT INTO "knowledge_gaps" VALUES('gap_01','usr_001','Vật lý','Điện từ học — Cảm ứng điện từ',28.0,'Cao','Hay nhầm lẫn chiều dòng điện cảm ứng theo định luật Len-xơ.');
INSERT INTO "knowledge_gaps" VALUES('gap_02','usr_001','Toán học','Hình học không gian — Khoảng cách 2 đường thẳng',35.0,'Cao','Chưa thành thạo dựng mặt phẳng song song chứa 1 đường thẳng.');
INSERT INTO "knowledge_gaps" VALUES('gap_03','usr_001','Toán học','Phương trình lượng giác chứa tham số',42.0,'Trung bình','Cần rèn luyện thêm điều kiện nghiệm của phương trình bậc 2 theo sin/cos.');
INSERT INTO "knowledge_gaps" VALUES('gap_04','usr_001','Tiếng Anh','Cấu trúc câu phức & Mệnh đề quan hệ',55.0,'Trung bình','Thường phân vân giữa which và that trong mệnh đề không xác định.');
INSERT INTO "knowledge_gaps" VALUES('gap_05','usr_001','Hóa học','Kim loại kiềm thổ & Nước cứng',62.0,'Thấp','Cần nhớ bảng phân biệt làm mềm nước cứng tạm thời và vĩnh cửu.');
CREATE TABLE questions (
        id TEXT PRIMARY KEY,
        quiz_id TEXT NOT NULL,
        text TEXT NOT NULL,
        options_json TEXT NOT NULL,
        correct_index INTEGER NOT NULL,
        explanation TEXT DEFAULT '',
        sort_order INTEGER DEFAULT 1,
        FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
    );
INSERT INTO "questions" VALUES('q1','quiz_toan_01','Phương trình x² - 5x + 6 = 0 có tập nghiệm S là:','["S = {1; 6}", "S = {2; 3}", "S = {-2; -3}", "S = {3; -2}"]',1,'Theo định lý Viète: x₁ + x₂ = 5 và x₁ × x₂ = 6. Hai nghiệm là x = 2 và x = 3.',1);
INSERT INTO "questions" VALUES('q2','quiz_toan_01','Tìm m để phương trình x² - 2mx + m² - 1 = 0 luôn có 2 nghiệm phân biệt:','["Mọi m ∈ ℝ", "m > 1", "m < 0", "Không có m nào"]',0,'Ta có Δ'' = (-m)² - 1(m² - 1) = 1 > 0 với mọi m. Do đó luôn có 2 nghiệm phân biệt.',2);
INSERT INTO "questions" VALUES('q3','quiz_toan_01','Gọi x₁, x₂ là hai nghiệm của x² - 3x - 4 = 0. Giá trị biểu thức A = x₁² + x₂² là:','["17", "25", "7", "9"]',0,'A = (x₁ + x₂)² - 2x₁x₂ = 3² - 2(-4) = 9 + 8 = 17.',3);
INSERT INTO "questions" VALUES('q4','quiz_toan_01','Phương trình 2x² + 5x + 2 = 0 có tích hai nghiệm bằng:','["1", "2.5", "-1", "2"]',0,'Theo Viète, P = c/a = 2/2 = 1.',4);
INSERT INTO "questions" VALUES('q5','quiz_toan_01','Cho phương trình x² - (m + 1)x + m = 0. Nghiệm của phương trình là:','["x = 1 hoặc x = m", "x = -1 hoặc x = -m", "x = 1 hoặc x = -m", "x = 2 hoặc x = m"]',0,'Do a + b + c = 0 nên có nghiệm x₁ = 1 và x₂ = c/a = m.',5);
INSERT INTO "questions" VALUES('q6','quiz_ly_01','Đơn vị của điện tích trong hệ đo lường quốc tế SI là:','["Vôn (V)", "Ampe (A)", "Cu-lông (C)", "Oát (W)"]',2,'Đơn vị của điện tích trong hệ SI là Cu-lông, ký hiệu C.',1);
INSERT INTO "questions" VALUES('q7','quiz_ly_01','Khi khoảng cách giữa 2 điện tích điểm trong chân không tăng lên 2 lần thì độ lớn lực Cu-lông:','["Tăng 2 lần", "Giảm 2 lần", "Tăng 4 lần", "Giảm 4 lần"]',3,'Lực Cu-lông tỉ lệ nghịch với bình phương khoảng cách r². r tăng 2 lần thì F giảm 4 lần.',2);
INSERT INTO "questions" VALUES('q8','quiz_hoa_01','Chất nào sau đây thuộc loại monosaccarit?','["Saccarozo", "Tinh bột", "Xenlulozo", "Glucozo"]',3,'Monosaccarit gồm Glucozo và Fructozo.',1);
INSERT INTO "questions" VALUES('q9','quiz_anh_01','The student _____ won the first prize studies in our class.','["which", "who", "whom", "whose"]',1,'Chủ ngữ chỉ người trong mệnh đề quan hệ dùng ''who''.',1);
CREATE TABLE quiz_attempts (
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
    );
INSERT INTO "quiz_attempts" VALUES('att_01','usr_001','quiz_toan_01','Phương trình bậc hai & Viète','Toán học',9.0,10,9,'14:20','{}','Hôm nay','2026-10-31 13:38:13');
INSERT INTO "quiz_attempts" VALUES('att_02','usr_001','quiz_ly_01','Lực tương tác tĩnh điện & Điện tích','Vật lý',7.5,10,7,'22:10','{}','23/10/2026','2026-10-31 13:38:13');
INSERT INTO "quiz_attempts" VALUES('att_03','usr_001','quiz_hoa_01','Phân loại Cacbohidrat & Glucozo','Hóa học',8.5,10,8,'18:45','{}','21/10/2026','2026-10-31 13:38:13');
INSERT INTO "quiz_attempts" VALUES('att_04','usr_001','quiz_ly_01','Đại cương về Dao động điều hòa','Vật lý',5.0,10,5,'28:10','{}','18/10/2026','2026-10-31 13:38:13');
CREATE TABLE quizzes (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        subject TEXT NOT NULL,
        grade TEXT DEFAULT '12',
        difficulty TEXT DEFAULT 'Trung bình',
        duration_minutes INTEGER DEFAULT 30,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
INSERT INTO "quizzes" VALUES('quiz_toan_01','Phương trình bậc hai & Định lý Viète','Toán học','10','Trung bình',30,'2026-10-31 13:38:13');
INSERT INTO "quizzes" VALUES('quiz_ly_01','Lực tương tác tĩnh điện & Điện tích','Vật lý','11','Cơ bản',20,'2026-10-31 13:38:13');
INSERT INTO "quizzes" VALUES('quiz_hoa_01','Phân loại Cacbohidrat & Glucozo','Hóa học','12','Trung bình',25,'2026-10-31 13:38:13');
INSERT INTO "quizzes" VALUES('quiz_anh_01','Cấu trúc câu phức & Mệnh đề quan hệ','Tiếng Anh','12','Nâng cao',20,'2026-10-31 13:38:13');
CREATE TABLE roadmaps (
        id TEXT PRIMARY KEY,
        user_id TEXT DEFAULT 'local_user',
        subject TEXT NOT NULL,
        current_lesson TEXT NOT NULL,
        progress_percent INTEGER DEFAULT 60,
        summary TEXT DEFAULT '',
        next_milestone TEXT DEFAULT '',
        updated_at TEXT DEFAULT 'Hôm nay'
    );
INSERT INTO "roadmaps" VALUES('roadmap_active','usr_001','Toán học 10 • Đại số','Phương trình bậc hai & Định lý Viète',65,'Bạn đã nắm vững cách tính biệt thức Δ, cần luyện thêm kỹ năng tìm tham số m.','Dấu của tam thức bậc hai & Bất phương trình','Hôm nay');
CREATE TABLE users (
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
    );
INSERT INTO "users" VALUES('usr_001','Phi Le Minh','phi@example.com','12345678','student','Pro','active',12,47,'Ôn tập định lý Viète và tam thức bậc 2','{}','2026-10-31 13:38:13','Vừa xong');
INSERT INTO "users" VALUES('usr_002','Nguyễn Hoàng Long','long.nh@gmail.com','12345678','student','Free','active',5,18,'','{}','2026-10-31 13:38:13','2 giờ trước');
INSERT INTO "users" VALUES('usr_003','ThS. Trần Thị Mai','mai.tran@thpt-chuyen.edu.vn','12345678','teacher','Pro','active',22,64,'','{}','2026-10-31 13:38:13','Hôm qua');
INSERT INTO "users" VALUES('usr_004','Lê Quốc Bảo','bao.le@outlook.com','12345678','student','Pro','active',8,32,'','{}','2026-10-31 13:38:13','3 ngày trước');
INSERT INTO "users" VALUES('usr_005','Phạm Thu Trang','trang.pham@yahoo.com','12345678','student','Free','locked',0,4,'','{}','2026-10-31 13:38:13','12 ngày trước');
INSERT INTO "users" VALUES('usr_006','Thầy Đỗ Quang Huy','huy.do@supham.edu.vn','12345678','teacher','Pro','active',30,95,'','{}','2026-10-31 13:38:13','Hôm nay');
INSERT INTO "users" VALUES('usr_007','Ngô Thanh Vân','van.ngo@hotmail.com','12345678','student','Free','active',2,9,'','{}','2026-10-31 13:38:13','5 ngày trước');
INSERT INTO "users" VALUES('usr_008','Vũ Đức Thành','admin@edumind.ai','admin123','admin','Pro','active',45,120,'','{}','2026-10-31 13:38:13','Trực tuyến');
COMMIT;
