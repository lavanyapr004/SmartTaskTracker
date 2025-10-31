 Smart Task Tracker — Design Notes

 🧩 Overview
Smart Task Tracker is a lightweight full-stack web app that allows users to create, manage, and analyze daily tasks.
It consists of a **Flask (Python)** backend and a **Vanilla JavaScript + HTML + CSS** frontend, communicating via RESTful APIs.

 🗄️ **Database Design**

Database:'SQLite'(lightweight, file-based, perfect for local apps).
Table: 'tasks'

| Column        | Type         | Description                                             |
| ------------- | ------------ | ------------------------------------------------------- |
| id`           | INTEGER (PK) | Auto-increment primary key                              |
| title         | TEXT         | Task title (required)                                   |
| description   | TEXT         | Optional detailed notes                                 |
| priority      | TEXT         | Enum: Low, Medium, High; default Medium'                |
| due_date      | TEXT         | Stored as YYYY-MM-DD string                             |
| status        | TEXT         | Enum: Pending, Completed; default Pending               |
| created_at    | TEXT         | Auto-timestamp (datetime('now'))                        |

✅ Design Reasoning:

* Simplicity: Only one table is needed for tasks.
* Flexibility: Text-based dates allow easy string manipulation and JSON transfer.
* Maintainability: Using SQLite ensures portability — no setup required.



 ⚙️ Backend Logic (Flask)

* Framework: Flask (Python)
* Core File: main.py
* CORS Enabled: For local API calls from the frontend.
* Database Connection: Lightweight helper get_conn() used across endpoints.

 🔹 Endpoints

| Method   | Endpoint      | Description                                                |
| -------- | ------------- | ---------------------------------------------------------- |
| `GET`    | `/tasks`      | Retrieve all tasks with optional filters (status/priority) |
| `POST`   | `/tasks`      | Add new task                                               |
| `PATCH`  | `/tasks/<id>` | Update task fields (status, priority, etc.)                |
| `DELETE` | `/tasks/<id>` | Delete task by ID                                          |
| `GET`    | `/insights`   | Generate smart summaries and analytics                     |

 🔹 Insights Logic

* Counts total, completed, and pending tasks.
* Calculates tasks due soon (within 7 days).
* Finds the busiest day based on number of due tasks.
* Generates a **summary sentence** like:
  *“You have 8 tasks. Most tasks are ‘High’ priority. 2 are due within 7 days.”*


 🎨 Frontend Logic (client)

* Built using **HTML, CSS, and Vanilla JS** — no framework dependency.
* `app.js` handles all API requests and dynamically updates the DOM.
* `style.css` gives a **dashboard-like look** with:

  * Colored priority badges (`High = red`, `Medium = orange`, `Low = green`)
  * Responsive grid layout
  * Pop-up notifications for task actions



 💡 Design Choices

1. RESTful separation: Clearly defined API endpoints make the backend reusable for any frontend (e.g., React, mobile app).
2. Minimal dependencies:*Uses only Flask + SQLite — easy to set up anywhere.
3. User-friendly UI: Simple dashboard with filters and color-coded priorities.
4. Insights: Encourages productivity by summarizing user’s workload trends.



 🚀 Possible Improvements

1. User Authentication: Add login system with JWT or session-based auth.
2. Reminders: Email or browser notifications for tasks nearing deadlines.
3. Progress Analytics: Charts (via Chart.js) for weekly or monthly performance.
4. Search Bar: Allow text search within task titles and descriptions.
5. Cloud Integration: Use PostgreSQL or Firebase for multi-user scalability.



🧠 Summary

This project demonstrates a complete full-stack workflow —
from database setup → Flask REST API → modern frontend → insight generation —in a minimal, elegant structure that’s easy to maintain and extend.




