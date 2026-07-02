# Eval Engine

A minimal Python full‑stack application that evaluates model responses against reference texts using a ROUGE‑L metric.

## Architecture

* **Backend** – Flask app (`app.py`) that handles form submission and score calculation.
* **Evaluator** – Pure Python module (`evaluator.py`) implementing ROUGE‑L.
* **Frontend** – Simple Jinja2 template (`templates/index.html`) with a textarea form.

## Setup & Run

```bash
# 1. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py
```

Open your browser at `http://127.0.0.1:5000/` to use the evaluator.
