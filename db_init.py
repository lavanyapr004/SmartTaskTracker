# server/db_init.py
import sqlite3

def init_db():
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        priority TEXT CHECK(priority IN ('Low','Medium','High')) DEFAULT 'Medium',
        due_date TEXT, -- store ISO date 'YYYY-MM-DD' as TEXT
        status TEXT CHECK(status IN ('Pending','Completed')) DEFAULT 'Pending',
        created_at TEXT DEFAULT (datetime('now'))
    )
    """)
    conn.commit()
    conn.close()
    print("✅ Database created / validated (tasks table ready).")

if __name__ == "__main__":
    init_db()
