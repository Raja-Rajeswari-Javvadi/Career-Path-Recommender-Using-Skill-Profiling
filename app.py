from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from gemini_model import generate_roadmap, chat_with_mentor

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results")
def results_page():
    return render_template("results.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        html_report, motivation = generate_roadmap(request.form)
        return jsonify({
            "report": html_report,
            "motivation": motivation
        })
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"report": "Error generating roadmap"}), 500

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        context = data.get("context", "")
        ai_reply = chat_with_mentor(user_message, context)
        return jsonify({"reply": ai_reply})
    except Exception as e:
        print("CHAT ERROR:", e)
        return jsonify({"reply": "I'm having trouble connecting right now."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)
