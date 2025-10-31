from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import collections

DB = "tasks.db"
app = Flask(__name__)
CORS(app)

# ---------- Database Connection ----------
def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Initialize Database ----------
def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database created successfully with all required columns!")

# ---------- List Tasks ----------
@app.route("/tasks", methods=["GET"])
def list_tasks():
    conn = get_conn()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(t) for t in tasks])

# ---------- Create Task ----------
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Title required"}), 400

    description = data.get("description")
    priority = data.get("priority") or "Medium"
    due_date = data.get("due_date")
    status = "Pending"

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tasks (title, description, priority, due_date, status)
        VALUES (?, ?, ?, ?, ?)
    """, (title, description, priority, due_date, status))
    conn.commit()
    task_id = cur.lastrowid
    task = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    conn.close()
    return jsonify(dict(task)), 201

# ---------- Update Task (PATCH) ----------
@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json() or {}
    allowed = {"title", "description", "priority", "due_date", "status"}
    updates = {k: v for k, v in data.items() if k in allowed}
    if not updates:
        return jsonify({"error": "Nothing to update"}), 400

    set_clause = ", ".join(f"{k}=?" for k in updates)
    params = list(updates.values()) + [task_id]

    conn = get_conn()
    conn.execute(f"UPDATE tasks SET {set_clause} WHERE id=?", params)
    conn.commit()
    task = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    conn.close()
    return jsonify(dict(task))

# ---------- Delete Task ----------
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    if not deleted:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"deleted": task_id})

# ---------- Insights (Summary) ----------
@app.route("/insights", methods=["GET"])
def insights():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    tasks = [dict(r) for r in rows]

    total = len(tasks)
    if total == 0:
        return jsonify({
            "total": 0,
            "status": {},
            "priority": {},
            "due_soon": 0,
            "overdue": 0,
            "busiest_day": None,
            "summary": "✨ You have no tasks yet. Add one and start being awesome!"
        })

    # Counters
    status_counts = collections.Counter(t["status"] for t in tasks)
    priority_counts = collections.Counter(t["priority"] or "Medium" for t in tasks)

    # Date analysis
    today = datetime.utcnow().date()
    soon_cutoff = today + timedelta(days=7)
    due_soon = 0
    overdue = 0
    by_day = collections.Counter()

    for t in tasks:
        dd = t.get("due_date")
        if not dd:
            continue
        try:
            d = datetime.strptime(dd, "%Y-%m-%d").date()
            if d < today and t["status"] != "Completed":
                overdue += 1
            elif today <= d <= soon_cutoff:
                due_soon += 1
            by_day[d.isoformat()] += 1
        except Exception:
            continue

    # Find busiest day
    busiest_day, busiest_count = (None, 0)
    if by_day:
        busiest_day, busiest_count = max(by_day.items(), key=lambda kv: kv[1])

    # Summary generation
    completed = status_counts.get("Completed", 0)
    pending = status_counts.get("Pending", 0)
    top_priority = priority_counts.most_common(1)[0][0]

    summary_parts = [
        f"📋 Total tasks: {total}",
        f"✅ Completed: {completed}",
        f"⏳ Pending: {pending}",
        f"⚠️ Overdue: {overdue}",
        f"📅 Due soon (7 days): {due_soon}",
        f"🔥 Common priority: {top_priority}"
    ]
    if busiest_day:
        summary_parts.append(f"🗓️ Busiest day: {busiest_day} ({busiest_count} tasks)")
    summary = " | ".join(summary_parts)

    return jsonify({
        "total": total,
        "status": dict(status_counts),
        "priority": dict(priority_counts),
        "due_soon": due_soon,
        "overdue": overdue,
        "busiest_day": busiest_day,
        "busiest_count": busiest_count,
        "summary": summary
    })


# ---------- Run App ----------
if __name__ == "__main__":
    init_db()
    print("🚀 Starting Flask server at http://127.0.0.1:5000")
    app.run(debug=True)
