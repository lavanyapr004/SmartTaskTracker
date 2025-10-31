const API = "http://127.0.0.1:5000";

async function fetchTasks() {
  const res = await fetch(`${API}/tasks`);
  const data = await res.json();
  renderTasks(data);
  fetchInsights();
}

function showMessage(msg, type="success") {
  const el = document.getElementById("message");
  el.textContent = msg;
  el.style.color = type === "error" ? "red" : "green";
  setTimeout(() => el.textContent = "", 2000);
}

async function addTask() {
  const title = document.getElementById("title").value.trim();
  const desc = document.getElementById("desc").value.trim();
  const priority = document.getElementById("priority").value;
  const due_date = document.getElementById("due_date").value;

  if (!title) return showMessage("Enter a title!", "error");

  const res = await fetch(`${API}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, description: desc, priority, due_date })
  });

  if (res.ok) {
    showMessage("✅ Task added!");
    fetchTasks();
    document.getElementById("title").value = "";
    document.getElementById("desc").value = "";
    document.getElementById("due_date").value = "";
  } else {
    showMessage("❌ Failed to add task", "error");
  }
}

async function deleteTask(id) {
  await fetch(`${API}/tasks/${id}`, { method: "DELETE" });
  showMessage("🗑️ Task deleted!");
  fetchTasks();
}

async function toggleStatus(id, currentStatus) {
  const newStatus = currentStatus === "Completed" ? "Pending" : "Completed";
  await fetch(`${API}/tasks/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: newStatus })
  });
  showMessage("🔄 Status updated!");
  fetchTasks();
}

function renderTasks(tasks) {
  const tbody = document.getElementById("taskList");
  tbody.innerHTML = "";
  tasks.forEach(t => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${t.title}</td>
      <td>${t.priority}</td>
      <td>${t.due_date || "-"}</td>
      <td>${t.status}</td>
      <td>
        <button onclick="toggleStatus(${t.id}, '${t.status}')">✔</button>
        <button onclick="deleteTask(${t.id})">🗑</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function fetchInsights() {
  const res = await fetch(`${API}/insights`);
  const data = await res.json();
  document.getElementById("insights").textContent = data.summary;
}

document.getElementById("addBtn").addEventListener("click", addTask);
fetchTasks();
