const apiBase = 'http://localhost:8335/todos';  //Real host

function getApiKey() {
  return localStorage.getItem('apiKey');
}

function saveApiKey() {
  const key = document.getElementById('apiKeyInput').value.trim();
  if (key === '') {
    alert("API-nyckel kan inte vara tom.");
    return;
  }
  localStorage.setItem('apiKey', key);
  alert("Nyckeln har sparats!");
  fetchTodos();
}

async function fetchTodos() {
  const apiKey = getApiKey();
  if (!apiKey) {
    alert("Ingen API-nyckel är sparad.");
    return;
  }

  const res = await fetch(apiBase, {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  });

  if (!res.ok) {
    alert("Misslyckades att hämta ToDo-lista: " + (await res.text()));
    return;
  }

  const todos = await res.json();
  renderTodos(todos);
}

function renderTodos(todos) {
  const list = document.getElementById('todoList');
  list.innerHTML = '';

  if (todos.length === 0) {
    const noTodos = document.createElement('li');
    noTodos.textContent = "Inga ToDo-noteringar tillgängliga.";
    list.appendChild(noTodos);
    return;
  }

  todos.forEach(todo => {
    const li = document.createElement('li');
    li.className = "flex justify-between items-center border p-2 rounded";

    const label = document.createElement('span');
    label.textContent = todo.title;
    if (todo.done) label.classList.add("line-through", "text-gray-500");

    const actions = document.createElement('div');
    actions.className = "flex gap-2";

    const doneBtn = document.createElement('button');
    doneBtn.textContent = "✔️";
    doneBtn.title = "Markera som klar";
    doneBtn.onclick = () => markDone(todo.id);

    const delBtn = document.createElement('button');
    delBtn.textContent = "🗑️";
    delBtn.title = "Ta bort";
    delBtn.onclick = () => {
      if (confirm("Är du säker på att du vill ta bort denna ToDo?")) {
        deleteTodo(todo.id);
      }
    };

    actions.appendChild(doneBtn);
    actions.appendChild(delBtn);
    li.appendChild(label);
    li.appendChild(actions);
    list.appendChild(li);
  });
}

async function addTodo() {
  const text = document.getElementById('todoInput').value.trim();
  if (!text) {
    alert("ToDo-notering kan inte vara tom.");
    return;
  }

  const apiKey = getApiKey();
  if (!apiKey) {
    alert("Ingen API-nyckel är sparad");
    return;
  }

  const res = await fetch(apiBase, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify({ title: text, category_id: 1 })  
  });

  if (res.ok) {
    document.getElementById('todoInput').value = '';
    fetchTodos();
  } else {
    alert("Kunde inte lägga till notering.");
  }
}

async function markDone(id) {
  const apiKey = getApiKey();
  const now = new Date().toISOString();

  await fetch(`${apiBase}/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify({ done: now })
  });

  fetchTodos();
}

async function deleteTodo(id) {
  const apiKey = getApiKey();

  await fetch(`${apiBase}/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${apiKey}`
    }
  });

  fetchTodos();
}

document.getElementById('addBtn').addEventListener('click', addTodo);
window.addEventListener('DOMContentLoaded', fetchTodos);
