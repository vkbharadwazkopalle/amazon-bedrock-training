# app.py
"""Main Flask application for the evaluation engine.

The app exposes a single page where users can paste a model response and a reference
text.  Upon submission, the server calculates a ROUGE‑L score and displays the
result.
"""

from flask import Flask, render_template, request
from evaluator import rouge_l_score

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    if request.method == "POST":
        model_text = request.form.get("model_text", "")
        reference_text = request.form.get("reference_text", "")
        if model_text and reference_text:
            score = rouge_l_score(model_text, reference_text)
    return render_template("index.html", score=score)

if __name__ == "__main__":
    app.run(debug=True)
