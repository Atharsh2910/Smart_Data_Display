from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
import traceback

# Optional Ollama chatbot support
try:
    from ollama import Client
    ollama_client = Client()
    OLLAMA_ENABLED = True
except Exception:
    ollama_client = None
    OLLAMA_ENABLED = False

# Initialize Flask app
app = Flask(__name__, static_folder='templates/static', template_folder='templates')
CORS(app)

# === Serve React frontend (index.html + static files) ===
@app.route('/')
def serve_index():
    return send_from_directory('templates', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    full_path = os.path.join('templates', path)
    if os.path.exists(full_path):
        return send_from_directory('templates', path)
    return send_from_directory('templates', 'index.html')

# === Load CSV data safely using absolute path ===
def load_data(category):
    try:
        filepath = os.path.join(os.path.dirname(__file__), "data", f"{category}.csv")
        print(f"[DEBUG] Trying to load file: {filepath}")
        df = pd.read_csv(filepath)
        df["rating"] = pd.to_numeric(df.get("rating", 0), errors="coerce").fillna(0)
        df["price"] = pd.to_numeric(df.get("price", 0), errors="coerce").fillna(0)
        products = df.to_dict(orient="records")
        print(f"[DEBUG] Loaded {len(products)} products for category '{category}'")
        return products
    except Exception as e:
        print(f"[ERROR] Failed to load data for category '{category}': {e}")
        traceback.print_exc()
        return []


# === API: Get products by category, search, and sort ===
@app.route("/api/products")
def get_products():
    category = request.args.get("category", "books")
    search = request.args.get("search", "").lower()
    sort = request.args.get("sort", "")

    products = load_data(category)

    if search:
        products = [p for p in products if search in str(p.get("title", "")).lower()]

    if sort == "price_asc":
        products.sort(key=lambda x: x.get("price", 0))
    elif sort == "price_desc":
        products.sort(key=lambda x: x.get("price", 0), reverse=True)
    elif sort == "rating_desc":
        products.sort(key=lambda x: x.get("rating", 0), reverse=True)

    print(f"[DEBUG] Returning {len(products)} products for category: {category}")
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
                "response": f"(Mock AI) You asked: '{user_message}' — this is a simulated response."
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
        return jsonify({"response": "An error occurred in the chatbot."}), 500

# === Start the server on Render with dynamic PORT ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
