from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
import traceback

# Optional Ollama support
try:
    from ollama import Client
    ollama_client = Client()
    OLLAMA_ENABLED = True
except Exception:
    ollama_client = None
    OLLAMA_ENABLED = False

app = Flask(__name__, static_folder='templates/static', template_folder='templates')
CORS(app)

# === Serve React Frontend (static + index) ===
@app.route('/')
def serve_index():
    return send_from_directory('templates', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # Serve static files or fallback to index.html (React routing)
    full_path = os.path.join('templates', path)
    if os.path.exists(full_path):
        return send_from_directory('templates', path)
    return send_from_directory('templates', 'index.html')

# === Utility to Load Product Data from CSV ===
def load_data(category):
    try:
        filepath = f"data/{category}.csv"
        df = pd.read_csv(filepath)
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)
        df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error loading {category} data:", e)
        return []

# === API: Get Products ===
@app.route("/api/products")
def get_products():
    category = request.args.get("category", "books")
    search = request.args.get("search", "").lower()
    sort = request.args.get("sort", "")

    products = load_data(category)

    if search:
        products = [p for p in products if search in p.get("title", "").lower()]

    if sort == "price_asc":
        products.sort(key=lambda x: x.get("price", 0))
    elif sort == "price_desc":
        products.sort(key=lambda x: x.get("price", 0), reverse=True)
    elif sort == "rating_desc":
        products.sort(key=lambda x: x.get("rating", 0), reverse=True)

    return jsonify(products)

# === API: Chatbot ===
@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        user_message = request.json.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Please enter a message."}), 400

        if not OLLAMA_ENABLED:
            return jsonify({
                "response": f"(Mock AI) You asked: '{user_message}' — this is a demo response."
            })

        response = ollama_client.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": "You are a helpful product assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response["message"]["content"]
        return jsonify({"response": reply})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"response": "Something went wrong with the chatbot."}), 500

# === Start App ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
