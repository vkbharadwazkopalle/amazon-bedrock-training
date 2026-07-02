# Simple Todo List

A minimal, client-side todo list application built with vanilla HTML, CSS, and JavaScript. Features persistent storage using localStorage, a clean responsive UI, and full CRUD operations for managing tasks.

## Features

- ✅ Add new todos
- ✅ Mark todos as complete/incomplete
- ✅ Delete individual todos
- ✅ Clear all completed todos
- ✅ Real-time statistics (total, active, completed)
- ✅ Persistent storage across browser sessions
- ✅ Responsive design for mobile and desktop
- ✅ Keyboard shortcuts (Enter to add)

## Architecture

The project follows a clean separation of concerns:

- **index.html** - Semantic HTML structure
- **styles.css** - Modern, responsive styling with gradient background
- **app.js** - TodoApp class managing state, localStorage, and DOM manipulation

## Setup & Run

No build process or dependencies required. Simply open the HTML file:

### Option 1: Direct File Open
```bash
# Open index.html in your browser
open index.html  # macOS
start index.html # Windows
xdg-open index.html # Linux
```

### Option 2: Local Server (Recommended)
```bash
# Using Python 3
python -m http.server 8000

# Using Python 2
python -m SimpleHTTPServer 8000

# Using Node.js (if you have npx)
npx serve
```

Then navigate to `http://localhost:8000` in your browser.

## Usage

1. **Add a todo**: Type in the input field and click "Add" or press Enter
2. **Complete a todo**: Click the checkbox next to the todo text
3. **Delete a todo**: Click the "Delete" button on the right
4. **Clear completed**: Click "Clear Completed" to remove all finished tasks

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

Requires localStorage support (available in all modern browsers).

## Data Storage

Todos are stored in the browser's localStorage under the key `todos`. Data persists across page refreshes and browser restarts but is specific to the domain/origin.

## License

MIT - Feel free to use and modify as needed.
