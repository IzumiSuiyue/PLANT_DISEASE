import os
import sqlite3
from datetime import datetime
from PIL import Image

# 📁 存储历史记录和图像缩略图的目录
RECORD_DIR = "records"
os.makedirs(RECORD_DIR, exist_ok=True)
DB_PATH = os.path.join(RECORD_DIR, "history.db")

# ✅ 初始化数据库（若不存在）
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recognition (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_path TEXT,
                    result TEXT,
                    advice TEXT,
                    timestamp TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS qa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT,
                    advice TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

# 📝 保存记录
def save_record(agent: str, **kwargs):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if agent == "recognition":
        image = kwargs["image"]
        result = kwargs["result"]
        advice = kwargs["advice"]
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        image_path = os.path.join(RECORD_DIR, filename)
        image.save(image_path)
        c.execute("INSERT INTO recognition (image_path, result, advice, timestamp) VALUES (?, ?, ?, ?)",
                  (image_path, result, advice, now))
    elif agent == "qa":
        question = kwargs["question"]
        advice = kwargs["advice"]
        c.execute("INSERT INTO qa (question, advice, timestamp) VALUES (?, ?, ?)",
                  (question, advice, now))
    conn.commit()
    conn.close()

# 🔍 加载记录
def load_records(agent: str):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if agent == "recognition":
        c.execute("SELECT id, image_path, result, advice FROM recognition ORDER BY id DESC")
        rows = c.fetchall()
        return [{"id": r[0], "image_path": r[1], "result": r[2], "advice": r[3]} for r in rows]
    elif agent == "qa":
        c.execute("SELECT id, question, advice FROM qa ORDER BY id DESC")
        rows = c.fetchall()
        return [{"id": r[0], "question": r[1], "advice": r[2]} for r in rows]
    return []

# 🗑️ 删除单条
def delete_record(record_id: int):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM recognition WHERE id=?", (record_id,))
    c.execute("DELETE FROM qa WHERE id=?", (record_id,))
    conn.commit()
    conn.close()

# 🗑️ 删除全部
def delete_all(agent: str):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if agent == "recognition":
        c.execute("DELETE FROM recognition")
    elif agent == "qa":
        c.execute("DELETE FROM qa")
    conn.commit()
    conn.close()
