"""FitTracker - 数据库模块"""

import os
import sqlite3
import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fittracker.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY DEFAULT 1,
            height REAL NOT NULL,
            weight REAL NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            target_weight REAL,
            activity_level TEXT DEFAULT 'moderate',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date DATE NOT NULL,
            meal_type TEXT NOT NULL,
            food_name TEXT NOT NULL,
            calories REAL NOT NULL,
            protein REAL DEFAULT 0,
            carbs REAL DEFAULT 0,
            fat REAL DEFAULT 0,
            image_url TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date DATE NOT NULL,
            exercise_type TEXT NOT NULL,
            duration INTEGER NOT NULL,
            calories_burned REAL NOT NULL,
            steps INTEGER,
            distance REAL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date DATE NOT NULL UNIQUE,
            total_intake REAL DEFAULT 0,
            total_burned REAL DEFAULT 0,
            net_calories REAL DEFAULT 0,
            weight REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            target_weight REAL NOT NULL,
            daily_calorie_target REAL NOT NULL,
            protein_percent REAL DEFAULT 30,
            carbs_percent REAL DEFAULT 40,
            fat_percent REAL DEFAULT 30,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# ── User Profile ──────────────────────────────────────────────
def get_user_profile():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def save_user_profile(height, weight, age, gender, target_weight=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO user_profile (id, height, weight, age, gender, target_weight, updated_at)
        VALUES (1, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (height, weight, age, gender, target_weight))
    conn.commit()
    conn.close()

# ── Meals ─────────────────────────────────────────────────────
def add_meal(log_date, meal_type, food_name, calories, protein=0, carbs=0, fat=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO meals (log_date, meal_type, food_name, calories, protein, carbs, fat)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (log_date, meal_type, food_name, calories, protein, carbs, fat))
    conn.commit()

    # 更新daily_log
    _update_daily_log(log_date)
    conn.close()

def get_today_meals(log_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meals WHERE log_date = ? ORDER BY recorded_at DESC", (log_date,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_meal(meal_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT log_date FROM meals WHERE id = ?", (meal_id,))
    row = cursor.fetchone()
    if row:
        log_date = row['log_date']
        cursor.execute("DELETE FROM meals WHERE id = ?", (meal_id,))
        conn.commit()
        _update_daily_log(log_date)
    conn.close()

# ── Exercises ─────────────────────────────────────────────────
def add_exercise(log_date, exercise_type, duration, calories_burned, steps=None, distance=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO exercises (log_date, exercise_type, duration, calories_burned, steps, distance)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (log_date, exercise_type, duration, calories_burned, steps, distance))
    conn.commit()

    # 更新daily_log
    _update_daily_log(log_date)
    conn.close()

def get_today_exercises(log_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exercises WHERE log_date = ? ORDER BY recorded_at DESC", (log_date,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_exercise(exercise_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT log_date FROM exercises WHERE id = ?", (exercise_id,))
    row = cursor.fetchone()
    if row:
        log_date = row['log_date']
        cursor.execute("DELETE FROM exercises WHERE id = ?", (exercise_id,))
        conn.commit()
        _update_daily_log(log_date)
    conn.close()

# ── Daily Logs ────────────────────────────────────────────────
def get_daily_log(log_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_logs WHERE log_date = ?", (log_date,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def _update_daily_log(log_date):
    conn = get_connection()
    cursor = conn.cursor()

    # 计算总摄入
    cursor.execute("SELECT COALESCE(SUM(calories), 0) as total FROM meals WHERE log_date = ?", (log_date,))
    total_intake = cursor.fetchone()['total']

    # 计算总消耗
    cursor.execute("SELECT COALESCE(SUM(calories_burned), 0) as total FROM exercises WHERE log_date = ?", (log_date,))
    total_burned = cursor.fetchone()['total']

    net_calories = total_intake - total_burned

    cursor.execute("""
        INSERT OR REPLACE INTO daily_logs (log_date, total_intake, total_burned, net_calories)
        VALUES (?, ?, ?, ?)
    """, (log_date, total_intake, total_burned, net_calories))

    conn.commit()
    conn.close()

# ── Plans ─────────────────────────────────────────────────────
def save_plan(start_date, end_date, target_weight, daily_calorie_target, protein_percent=30, carbs_percent=40, fat_percent=30):
    conn = get_connection()
    cursor = conn.cursor()

    # 停用旧计划
    cursor.execute("UPDATE plans SET status = 'completed' WHERE status = 'active'")

    cursor.execute("""
        INSERT INTO plans (start_date, end_date, target_weight, daily_calorie_target, protein_percent, carbs_percent, fat_percent)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (start_date, end_date, target_weight, daily_calorie_target, protein_percent, carbs_percent, fat_percent))

    conn.commit()
    conn.close()

def get_active_plan():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM plans WHERE status = 'active' ORDER BY created_at DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

# ── Clear Data ────────────────────────────────────────────────
def clear_all_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM meals")
    cursor.execute("DELETE FROM exercises")
    cursor.execute("DELETE FROM daily_logs")
    cursor.execute("DELETE FROM plans")
    cursor.execute("DELETE FROM user_profile")
    conn.commit()
    conn.close()
