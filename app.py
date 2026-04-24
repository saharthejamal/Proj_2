from flask import Flask, request, render_template
from apriori_2636123 import run_apriori_from_text

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        data = request.form["data"]
        min_support = int(request.form["min_support"])
        result = run_apriori_from_text(data, min_support)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)