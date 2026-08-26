"use strict";

const el = id => document.getElementById(id);
const form = el("taskForm");
const apiValues = {status: {todo: "ToDo", in_progress: "InProgress", done: "Done"}, priority: {low: "Low", medium: "Medium", high: "High"}};
const uiStatus = {ToDo: "todo", InProgress: "in_progress", Done: "done"};
let tasks = [];
let toastTimer;

el("today").textContent = new Intl.DateTimeFormat(undefined, {weekday: "long", month: "long", day: "numeric"}).format(new Date());

function escapeHtml(value) {
  return String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");
}
function label(value) { return value === "in_progress" ? "In progress" : value.replace("_", " "); }
function showToast(message) {
  clearTimeout(toastTimer); el("toast").textContent = message; el("toast").classList.add("show");
  toastTimer = setTimeout(() => el("toast").classList.remove("show"), 2600);
}
function showError(error) { showToast(error.message || "Something went wrong"); }

async function request(url, options = {}) {
  const response = await fetch(url, {...options, headers: options.body ? {"Content-Type": "application/json"} : undefined});
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(typeof body.detail === "string" ? body.detail : "Request failed");
  }
  return response.status === 204 ? null : response.json();
}
function normalize(task) { return {...task, status: uiStatus[task.status], priority: task.priority.toLowerCase()}; }

async function loadTasks() {
  const params = new URLSearchParams();
  if (el("statusFilter").value !== "all") params.set("status", apiValues.status[el("statusFilter").value]);
  if (el("priorityFilter").value !== "all") params.set("priority", apiValues.priority[el("priorityFilter").value]);
  const search = el("searchFilter").value.trim();
  if (search) params.set("q", search);
  if (el("overdueFilter").value !== "all") params.set("overdue", el("overdueFilter").value);
  tasks = (await request(`/tasks?${params}`)).map(normalize);
  render();
}

function resetForm() {
  form.reset(); el("taskId").value = ""; el("priority").value = "medium"; el("status").value = "todo";
  el("formTitle").textContent = "Create a task"; el("formNote").textContent = "Add the details that make the next step clear.";
  el("saveButton").textContent = "Add task"; el("cancelButton").hidden = true;
  el("titleError").textContent = ""; el("formError").textContent = "";
}

function render() {
  el("totalStat").textContent = tasks.length;
  el("todoStat").textContent = tasks.filter(t => t.status === "todo").length;
  el("progressStat").textContent = tasks.filter(t => t.status === "in_progress").length;
  el("doneStat").textContent = tasks.filter(t => t.status === "done").length;
  const visible = tasks;
  el("taskCount").textContent = `${visible.length} shown`;
  if (!visible.length) {
    el("taskList").innerHTML = `<div class="empty"><strong>No tasks found</strong>${tasks.length ? "Try adjusting your search." : "Create your first task to get moving."}</div>`;
    return;
  }
  el("taskList").innerHTML = visible.map(task => `
    <article class="task" data-id="${task.id}"><div>
      <h3 class="task-title">${escapeHtml(task.title)}</h3>
      ${task.description ? `<p class="task-description">${escapeHtml(task.description)}</p>` : ""}
      <div class="meta"><span class="pill ${task.status}">${label(task.status)}</span><span class="pill ${task.priority}">${task.priority}</span>${isOverdue(task) ? '<span class="pill overdue">Overdue</span>' : ""}${task.due_date ? `<span class="due-date">Due ${formatDate(task.due_date)}</span>` : ""}${task.assignee ? `<span class="assignee">Assigned to ${escapeHtml(task.assignee)}</span>` : ""}</div>
    </div><div class="task-actions">
      <select data-action="status" aria-label="Change status for ${escapeHtml(task.title)}">${["todo", "in_progress", "done"].map(value => `<option value="${value}" ${value === task.status ? "selected" : ""}>${label(value)}</option>`).join("")}</select>
      <button class="secondary" type="button" data-action="edit">Edit</button><button class="danger" type="button" data-action="delete">Delete</button>
    </div></article>`).join("");
}

function payloadFromForm() {
  return {title: el("title").value.trim(), description: el("description").value.trim() || null,
    status: apiValues.status[el("status").value], priority: apiValues.priority[el("priority").value], assignee: el("assignee").value.trim() || null,
    due_date: el("dueDate").value || null};
}

function isOverdue(task) {
  const today = new Date();
  const localToday = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
  return task.due_date && task.due_date < localToday && task.status !== "done";
}

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, {year: "numeric", month: "short", day: "numeric", timeZone: "UTC"}).format(new Date(`${value}T00:00:00Z`));
}

form.addEventListener("submit", async event => {
  event.preventDefault(); el("titleError").textContent = ""; el("formError").textContent = "";
  if (!el("title").value.trim()) { el("titleError").textContent = "Enter a title that is not only whitespace."; el("title").focus(); return; }
  const id = el("taskId").value;
  try {
    await request(id ? `/tasks/${id}` : "/tasks", {method: id ? "PATCH" : "POST", body: JSON.stringify(payloadFromForm())});
    showToast(id ? "Task updated" : "Task created"); resetForm(); await loadTasks();
  } catch (error) { el("formError").textContent = error.message; }
});

el("cancelButton").addEventListener("click", resetForm);
let searchTimer;
el("searchFilter").addEventListener("input", () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => loadTasks().catch(showError), 250);
});
["statusFilter", "priorityFilter", "overdueFilter"].forEach(id => el(id).addEventListener("change", () => loadTasks().catch(showError)));

el("taskList").addEventListener("click", async event => {
  const button = event.target.closest("button[data-action]"); if (!button) return;
  const id = Number(button.closest(".task").dataset.id); const task = tasks.find(item => item.id === id); if (!task) return;
  if (button.dataset.action === "delete") {
    if (!confirm(`Delete “${task.title}”?`)) return;
    try { await request(`/tasks/${id}`, {method: "DELETE"}); if (Number(el("taskId").value) === id) resetForm(); showToast("Task deleted"); await loadTasks(); } catch (error) { showError(error); }
  } else {
    el("taskId").value = task.id; el("title").value = task.title; el("description").value = task.description || "";
    el("status").value = task.status; el("priority").value = task.priority; el("assignee").value = task.assignee || ""; el("dueDate").value = task.due_date || "";
    el("formTitle").textContent = "Edit task"; el("formNote").textContent = `Updating task #${task.id}`;
    el("saveButton").textContent = "Save changes"; el("cancelButton").hidden = false; el("title").focus();
  }
});

el("taskList").addEventListener("change", async event => {
  if (event.target.dataset.action !== "status") return;
  const id = Number(event.target.closest(".task").dataset.id);
  try { await request(`/tasks/${id}`, {method: "PATCH", body: JSON.stringify({status: apiValues.status[event.target.value]})}); showToast(`Moved to ${label(event.target.value)}`); await loadTasks(); }
  catch (error) { showError(error); await loadTasks(); }
});

loadTasks().catch(showError);
