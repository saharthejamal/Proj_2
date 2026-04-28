from flask import Flask, request, render_template
from apriori_2636123 import run_apriori_from_text

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        uploaded_file = request.files["input_file"]
        min_support = int(request.form["min_support"])

        file_content = uploaded_file.read().decode("utf-8")

        result = run_apriori_from_text(file_content, min_support)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)