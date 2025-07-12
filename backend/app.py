from flask import Flask, request, jsonify
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

app = Flask(__name__)
CORS(app)

# === Utility to load CSV data ===
def load_data(category):
    try:
        filepath = f"../data/{category}.csv"
        df = pd.read_csv(filepath)

        # Ensure rating is a float and price is int
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)
        df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)

        # Add default image for books if not present
        if category == "books" and "image" not in df.columns:
            df["image"] = "https://via.placeholder.com/150"

        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error loading {category}: {e}")
        return []

# === Product API ===
@app.route("/api/products")
def get_products():
    category = request.args.get("category", "books")
    search = request.args.get("search", "").lower()
    sort = request.args.get("sort", "")  # price_asc, price_desc, rating_desc

    products = load_data(category)

    # Filter by search query
    if search:
        products = [p for p in products if search in p.get("title", "").lower()]

    # Sort results
    if sort == "price_asc":
        products.sort(key=lambda x: x.get("price", 0))
    elif sort == "price_desc":
        products.sort(key=lambda x: x.get("price", 0), reverse=True)
    elif sort == "rating_desc":
        products.sort(key=lambda x: x.get("rating", 0), reverse=True)

    return jsonify(products)

# === Chatbot API ===
@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        user_message = request.json.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Please enter a message."}), 400

        # === MOCK REPLY if Ollama not available ===
        if not OLLAMA_ENABLED:
            return jsonify({
                "response": f"(Simulated AI) You asked: '{user_message}' — here's a demo reply!"
            })

        # === Real Ollama Chat ===
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
        return jsonify({"response": "Something went wrong while generating a response."}), 500

# === Main entry point ===
if __name__ == "__main__":
    app.run(debug=True)
