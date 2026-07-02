/**
 * Simple Todo List Application
 * Manages todo items with localStorage persistence
 */

class TodoApp {
    constructor() {
        this.todos = this.loadTodos();
        this.initializeElements();
        this.attachEventListeners();
        this.render();
    }

    /**
     * Cache DOM element references
     */
    initializeElements() {
        this.todoInput = document.getElementById('todoInput');
        this.addButton = document.getElementById('addButton');
        this.todoList = document.getElementById('todoList');
        this.clearCompletedButton = document.getElementById('clearCompleted');
        this.totalCount = document.getElementById('totalCount');
        this.activeCount = document.getElementById('activeCount');
        this.completedCount = document.getElementById('completedCount');
    }

    /**
     * Attach event listeners to interactive elements
     */
    attachEventListeners() {
        this.addButton.addEventListener('click', () => this.addTodo());
        this.todoInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.addTodo();
            }
        });
        this.clearCompletedButton.addEventListener('click', () => this.clearCompleted());
    }

    /**
     * Load todos from localStorage
     * @returns {Array} Array of todo objects
     */
    loadTodos() {
        const stored = localStorage.getItem('todos');
        return stored ? JSON.parse(stored) : [];
    }

    /**
     * Save todos to localStorage
     */
    saveTodos() {
        localStorage.setItem('todos', JSON.stringify(this.todos));
    }

    /**
     * Add a new todo item
     */
    addTodo() {
        const text = this.todoInput.value.trim();
        
        if (text === '') {
            this.todoInput.focus();
            return;
        }

        const todo = {
            id: Date.now(),
            text: text,
            completed: false,
            createdAt: new Date().toISOString()
        };

        this.todos.unshift(todo);
        this.todoInput.value = '';
        this.todoInput.focus();
        
        this.saveTodos();
        this.render();
    }

    /**
     * Toggle the completed status of a todo
     * @param {number} id - Todo item ID
     */
    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            this.saveTodos();
            this.render();
        }
    }

    /**
     * Delete a todo item
     * @param {number} id - Todo item ID
     */
    deleteTodo(id) {
        this.todos = this.todos.filter(t => t.id !== id);
        this.saveTodos();
        this.render();
    }

    /**
     * Remove all completed todos
     */
    clearCompleted() {
        this.todos = this.todos.filter(t => !t.completed);
        this.saveTodos();
        this.render();
    }

    /**
     * Get statistics about todos
     * @returns {Object} Stats object with total, active, and completed counts
     */
    getStats() {
        const total = this.todos.length;
        const completed = this.todos.filter(t => t.completed).length;
        const active = total - completed;
        
        return { total, active, completed };
    }

    /**
     * Update the statistics display
     */
    updateStats() {
        const stats = this.getStats();
        
        this.totalCount.textContent = `${stats.total} total`;
        this.activeCount.textContent = `${stats.active} active`;
        this.completedCount.textContent = `${stats.completed} completed`;
        
        this.clearCompletedButton.disabled = stats.completed === 0;
    }

    /**
     * Create a DOM element for a todo item
     * @param {Object} todo - Todo object
     * @returns {HTMLElement} List item element
     */
    createTodoElement(todo) {
        const li = document.createElement('li');
        li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
        li.dataset.id = todo.id;

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'todo-checkbox';
        checkbox.checked = todo.completed;
        checkbox.addEventListener('change', () => this.toggleTodo(todo.id));

        const textSpan = document.createElement('span');
        textSpan.className = 'todo-text';
        textSpan.textContent = todo.text;

        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-button';
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', () => this.deleteTodo(todo.id));

        li.appendChild(checkbox);
        li.appendChild(textSpan);
        li.appendChild(deleteButton);

        return li;
    }

    /**
     * Render the entire todo list and update UI
     */
    render() {
        this.todoList.innerHTML = '';

        if (this.todos.length === 0) {
            const emptyState = document.createElement('div');
            emptyState.className = 'empty-state';
            emptyState.textContent = 'No todos yet. Add one above!';
            this.todoList.appendChild(emptyState);
        } else {
            this.todos.forEach(todo => {
                const todoElement = this.createTodoElement(todo);
                this.todoList.appendChild(todoElement);
            });
        }

        this.updateStats();
    }
}

// Initialize the app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new TodoApp());
} else {
    new TodoApp();
}