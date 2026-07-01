import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import App from "./App";
import * as todosApi from "./api/todos";

jest.mock("./api/todos");

describe("App", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("loads and displays todos from the API on mount", async () => {
    todosApi.fetchTodos.mockResolvedValue([
      { id: "1", description: "Learn Docker" },
      { id: "2", description: "Learn React" },
    ]);

    render(<App />);

    expect(await screen.findByText("Learn Docker")).toBeInTheDocument();
    expect(screen.getByText("Learn React")).toBeInTheDocument();
    expect(todosApi.fetchTodos).toHaveBeenCalledTimes(1);
  });

  test("shows empty state when there are no todos", async () => {
    todosApi.fetchTodos.mockResolvedValue([]);

    render(<App />);

    expect(await screen.findByText(/no todos yet/i)).toBeInTheDocument();
  });

  test("creates a todo and refreshes the list", async () => {
    // First load: empty. After creating, list returns the new todo.
    todosApi.fetchTodos
      .mockResolvedValueOnce([])
      .mockResolvedValueOnce([{ id: "1", description: "Buy milk" }]);
    todosApi.createTodo.mockResolvedValue({ id: "1", description: "Buy milk" });

    render(<App />);
    await screen.findByText(/no todos yet/i);

    await userEvent.type(screen.getByLabelText(/todo/i), "Buy milk");
    await userEvent.click(screen.getByRole("button", { name: /add todo/i }));

    expect(await screen.findByText("Buy milk")).toBeInTheDocument();
    expect(todosApi.createTodo).toHaveBeenCalledWith("Buy milk");
    // once on mount, once after create
    expect(todosApi.fetchTodos).toHaveBeenCalledTimes(2);
  });

  test("shows an error message when loading fails", async () => {
    todosApi.fetchTodos.mockRejectedValue(new Error("Network down"));

    render(<App />);

    expect(await screen.findByText("Network down")).toBeInTheDocument();
  });
});
