🧠 Smart Task Tracker  
A simple yet intelligent task management web app built with Flask and Vanilla JS.

📖 Overview
"Smart Task Tracker" helps you manage daily tasks with ease.  
Add, edit, delete, and track your progress — all while receiving smart productivity insights based on your data.  

It’s a lightweight **full-stack app** with:
- "Backend:" Flask (Python) + SQLite  
- "Frontend:" HTML, CSS, JavaScript  
- "API Integration:" RESTful design with CORS enabled  



 🗂️ Project Structure
SmartTask-Tracker/
│
├── server/ # Backend (Flask API)
│ ├── main.py # Flask routes and API logic
│ ├── db_init.py # Initializes SQLite DB
│ ├── tasks.db # Database file (auto-created)
│ └── requirements.txt # Python dependencies
│
└── client/ # Frontend (UI)
├── index.html # Main webpage
├── style.css # Modern, responsive styling
└── app.js # Handles UI logic and API calls


 ⚙️ Setup Instructions

🧩 1. Clone the Repository
git clone https://github.com/yourusername/SmartTask-Tracker.git
cd SmartTask-Tracker

🖥️ 2. Backend Setup (Flask)
cd server
python -m venv venv
venv\Scripts\activate     # On Windows
# or
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
python db_init.py         # Creates SQLite database
python main.py            # Starts Flask server
🟢 Flask server will run on:
http://127.0.0.1:5000

🌐 3. Frontend Setup
No build tools required!
Simply open the file below in your browser:
client/index.html
Make sure the backend Flask server is running while using the app.

🚀 Features
✅ Add, update, delete tasks
✅ Mark tasks as completed or pending
✅ Filter by status and priority
✅ Sort by due date or priority
✅ Smart insights: due soon, busiest day, and task summary
✅ Clean, modern dashboard-style UI

🧩 API Endpoints
Method	Endpoint	Description
GET	/tasks	Fetch all tasks
POST	/tasks	Add a new task
PATCH	/tasks/<id>	Update task fields
DELETE	/tasks/<id>	Delete a task
GET	/insights	Get AI-like task insights

🧠 Example Insights
Example response from /insights:

json
Copy code
{
  "total": 8,
  "status": {"Pending": 5, "Completed": 3},
  "priority": {"High": 4, "Medium": 3, "Low": 1},
  "due_soon": 2,
  "busiest_day": "2025-11-03",
  "busiest_count": 3,
  "summary": "You have 8 tasks. Most tasks are 'High' priority. 2 are due within 7 days. Busiest date: 2025-11-03 (3 tasks)."
}
🧰 Tech Stack
Category	Technology
Backend	Flask (Python)
Database	SQLite
Frontend	HTML5, CSS3, JavaScript
API	REST + JSON
Environment	Localhost (CORS enabled)

🧑‍💻 Author
Name: Lavanya P R
Course: BE Computer Science
Institution: Don Bosco Institute of Technology
Batch: 2026
