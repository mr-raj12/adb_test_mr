// Calls to the todos backend.
//
// All the fetch/URL/error-handling stuff lives here so the components don't
// have to. If the API changes, this is the only file to touch.

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

const TODOS_URL = `${API_BASE_URL}/todos`;

async function parseJsonOrThrow(response) {
  if (!response.ok) {
    // Use the backend's error message if it sent one.
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      if (body && body.detail) detail = body.detail;
    } catch (_) {
      // no JSON body, keep the generic message
    }
    throw new Error(detail);
  }
  return response.json();
}

export async function fetchTodos() {
  const response = await fetch(TODOS_URL, {
    headers: { Accept: "application/json" },
  });
  return parseJsonOrThrow(response);
}

export async function createTodo(description) {
  const response = await fetch(TODOS_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ description }),
  });
  return parseJsonOrThrow(response);
}
