// Renders the todo list (plus the loading/error/empty states). No state of
// its own, just shows what it's given.

import PropTypes from "prop-types";

export function TodoList({ todos, loading, error }) {
  if (loading && todos.length === 0) {
    return <p>Loading todos…</p>;
  }

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  if (todos.length === 0) {
    return <p>No todos yet. Add one below!</p>;
  }

  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>{todo.description}</li>
      ))}
    </ul>
  );
}

TodoList.propTypes = {
  todos: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      description: PropTypes.string.isRequired,
    })
  ).isRequired,
  loading: PropTypes.bool,
  error: PropTypes.string,
};

TodoList.defaultProps = {
  loading: false,
  error: null,
};

export default TodoList;
