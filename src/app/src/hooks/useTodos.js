// Hook that holds the todos and the load/add logic, so App can just render.

import { useCallback, useEffect, useRef, useState } from "react";

import { createTodo, fetchTodos } from "../api/todos";

export function useTodos() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // If a request finishes after the component is gone, don't call setState
  // (React warns about that). This flag tracks whether we're still mounted.
  const mountedRef = useRef(true);
  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
    };
  }, []);

  const loadTodos = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchTodos();
      if (mountedRef.current) {
        setTodos(Array.isArray(data) ? data : []);
      }
    } catch (err) {
      if (mountedRef.current) {
        setError(err.message || "Failed to load todos.");
      }
    } finally {
      if (mountedRef.current) {
        setLoading(false);
      }
    }
  }, []);

  // Load once on mount.
  useEffect(() => {
    loadTodos();
  }, [loadTodos]);

  const addTodo = useCallback(
    async (description) => {
      // Save it, then reload from the server so the list shows what's
      // actually in the database.
      await createTodo(description);
      await loadTodos();
    },
    [loadTodos]
  );

  return { todos, loading, error, addTodo, reload: loadTodos };
}
