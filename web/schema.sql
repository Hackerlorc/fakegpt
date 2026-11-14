-- =============================================================================
-- EDUMIND AI - RELATIONAL DATABASE SCHEMA (SQL DDL & DML)
-- Compatible with SQLite, PostgreSQL, MySQL
-- =============================================================================

-- 1. USERS & ACCOUNTS
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL DEFAULT '12345678',
    role VARCHAR(50) NOT NULL DEFAULT 'student', -- 'student', 'teacher', 'admin'
    plan VARCHAR(50) NOT NULL DEFAULT 'Free',    -- 'Free', 'Pro'
    status VARCHAR(50) NOT NULL DEFAULT 'active',-- 'active', 'locked'
    streak INT DEFAULT 1,
    quizzes INT DEFAULT 0,
    notes TEXT,
    survey TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active VARCHAR(100) DEFAULT 'Vừa xong'
);

-- 2. QUIZZES (QUIZ BANK)
CREATE TABLE IF NOT EXISTS quizzes (
    id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    grade VARCHAR(20) DEFAULT '12',
    difficulty VARCHAR(50) DEFAULT 'Trung bình',
    duration_minutes INT DEFAULT 30,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. QUESTIONS
CREATE TABLE IF NOT EXISTS questions (
    id VARCHAR(64) PRIMARY KEY,
    quiz_id VARCHAR(64) NOT NULL,
    text TEXT NOT NULL,
    options_json TEXT NOT NULL,
    correct_index INT NOT NULL,
    explanation TEXT,
    sort_order INT DEFAULT 1,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
);

-- 4. QUIZ ATTEMPTS & SUBMISSIONS
CREATE TABLE IF NOT EXISTS quiz_attempts (
    id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) DEFAULT 'local_user',
    quiz_id VARCHAR(64),
    title VARCHAR(255) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    score DECIMAL(4, 1) NOT NULL,
    total INT DEFAULT 10,
    correct_count INT DEFAULT 0,
    time_spent VARCHAR(50) DEFAULT '15:00',
    answers_json TEXT,
    completed_at VARCHAR(100) DEFAULT 'Hôm nay',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE SET NULL
);

-- 5. KNOWLEDGE GAPS & DIAGNOSTICS
CREATE TABLE IF NOT EXISTS knowledge_gaps (
    id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) DEFAULT 'local_user',
    subject VARCHAR(100) NOT NULL,
    topic VARCHAR(255) NOT NULL,
    accuracy_percent DECIMAL(5, 2) NOT NULL,
    priority VARCHAR(50) DEFAULT 'Trung bình',
    description TEXT
);

-- 6. LEARNING ROADMAPS
CREATE TABLE IF NOT EXISTS roadmaps (
    id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) DEFAULT 'local_user',
    subject VARCHAR(100) NOT NULL,
    current_lesson VARCHAR(255) NOT NULL,
    progress_percent INT DEFAULT 60,
    summary TEXT,
    next_milestone VARCHAR(255),
    updated_at VARCHAR(100) DEFAULT 'Hôm nay'
);

-- 7. CHAT MESSAGES (AI STUDY COACH)
CREATE TABLE IF NOT EXISTS chat_messages (
    id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) DEFAULT 'local_user',
    sender VARCHAR(100) NOT NULL,
    is_ai BOOLEAN DEFAULT 0,
    text TEXT NOT NULL,
    socratic_hint TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
