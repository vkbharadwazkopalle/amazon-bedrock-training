# File Comparator

A tiny Rust full‑stack application that lets you upload two text files and see a line‑by‑line diff in the browser.

## Architecture

* **Backend** – Actix‑Web server exposing two endpoints:
  * `GET /` – serves a simple HTML form.
  * `POST /compare` – accepts two multipart files, runs a basic diff algorithm, and returns JSON.
* **Diff logic** – a pure Rust function that compares the files line by line and prefixes differences with `-` or `+`.
* **Frontend** – plain HTML/JS that posts the form via `fetch` and displays the diff in a `<pre>` block.

## Prerequisites

* Rust 1.70+ (recommended via `rustup`)

## Setup & Run

```bash
# Clone the repository
git clone https://github.com/yourname/file-comparator.git
cd file-comparator

# Build and run the server
cargo run
```

The server will start on `http://127.0.0.1:8080`. Open that URL in a browser, choose two text files, and click **Compare**. The diff will appear below the form.

## Testing the API directly

You can also test the `/compare` endpoint with `curl`:

```bash
curl -X POST \
  -F "file1=@path/to/file1.txt" \
  -F "file2=@path/to/file2.txt" \
  http://127.0.0.1:8080/compare
```

The response will be a JSON object:

```json
{ "diff": [ "  line1", "- old line", "+ new line" ] }
```

## License

MIT