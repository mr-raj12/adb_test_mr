// The "add a todo" form. It tracks the text box; saving is the parent's job
// via the onSubmit prop.

import PropTypes from "prop-types";
import { useState } from "react";

export function TodoForm({ onSubmit }) {
  const [description, setDescription] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const trimmed = description.trim();
    if (!trimmed) {
      setError("Please enter a todo.");
      return;
    }

    setSubmitting(true);
    setError(null);
    try {
      await onSubmit(trimmed);
      setDescription(""); // clear only on success
    } catch (err) {
      setError(err.message || "Failed to add todo.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="todo">ToDo: </label>
        <input
          id="todo"
          type="text"
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          disabled={submitting}
        />
      </div>
      <div style={{ marginTop: "5px" }}>
        <button type="submit" disabled={submitting}>
          {submitting ? "Adding…" : "Add ToDo!"}
        </button>
      </div>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}

TodoForm.propTypes = {
  // Saves the todo. Can be async and can throw if the save fails.
  onSubmit: PropTypes.func.isRequired,
};

export default TodoForm;
