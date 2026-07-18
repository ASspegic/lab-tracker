// ---- Courses ----
async function loadCourses() {
  const res = await fetch("/courses");
  const courses = await res.json();
  const list = document.getElementById("course-list");
  list.innerHTML = "";
  courses.forEach((c) => {
    const li = document.createElement("li");
    li.textContent = `#${c.id} — ${c.code}: ${c.name}`;
    list.appendChild(li);
  });
}

document.getElementById("course-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("course-name").value;
  const code = document.getElementById("course-code").value;

  await fetch("/courses", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, code }),
  });

  e.target.reset();
  loadCourses();
});

// ---- Labs ----
async function loadLabs() {
  const res = await fetch("/labs");
  const labs = await res.json();
  const list = document.getElementById("lab-list");
  list.innerHTML = "";
  labs.forEach((l) => {
    const li = document.createElement("li");
    li.textContent = `#${l.id} — ${l.title} (course ${l.course_id}, due ${l.deadline})`;
    list.appendChild(li);
  });
}

document.getElementById("lab-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("lab-title").value;
  const deadline = document.getElementById("lab-deadline").value;
  const course_id = parseInt(document.getElementById("lab-course-id").value);

  const res = await fetch("/labs", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, deadline, course_id }),
  });

  if (res.ok) {
    e.target.reset();
    loadLabs();
  } else {
    const err = await res.json();
    alert(err.detail || "Failed to add lab");
  }
});

// ---- Submissions ----
async function loadSubmissions() {
  const res = await fetch("/submissions");
  const subs = await res.json();
  const list = document.getElementById("submission-list");
  list.innerHTML = "";
  subs.forEach((s) => {
    const li = document.createElement("li");
    li.textContent = `#${s.id} — ${s.student_name} → lab ${s.lab_id} [${s.status}]` +
      (s.grade !== null ? ` — grade: ${s.grade}` : "");
    list.appendChild(li);
  });
}

document.getElementById("submission-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const lab_id = parseInt(document.getElementById("sub-lab-id").value);
  const student_name = document.getElementById("sub-student").value;
  const file_or_link = document.getElementById("sub-link").value;

  const res = await fetch("/submissions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ lab_id, student_name, file_or_link }),
  });

  if (res.ok) {
    e.target.reset();
    loadSubmissions();
  } else {
    const err = await res.json();
    alert(err.detail || "Failed to submit");
  }
});

// ---- Initial load ----
loadCourses();
loadLabs();
loadSubmissions();
