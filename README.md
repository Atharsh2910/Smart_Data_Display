# Smart Product Explorer

A fullstack web application to discover, compare, and chat about Books, Electronics, and Personal Care products—all in one place.

## Features
- **Product Browsing:** View and filter books, electronics, and personal care products.
- **Search & Sort:** Search by name and sort by price or rating.
- **AI Chatbot:** Ask product-related questions via a floating chatbot.
- **Modern UI:** Responsive, clean, and user-friendly interface.

---

## Tech Stack
- **Frontend:** React (with functional components, hooks, and custom CSS)
- **Backend:** Python Flask (REST API)
- **Data:** CSV files for product data

---

## Getting Started

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Engineering_Intern_Project_Maketronics
```

### 2. Backend Setup
1. Navigate to the backend directory:
    ```bash
    cd backend
    ```
2. (Optional) Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r ../requirements.txt
    ```
4. Run the backend server:
    ```bash
    python app.py
    ```
   The backend will start on `http://localhost:5000`.

### 3. Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
    ```bash
    cd frontend/smart-frontend
    ```
2. Install dependencies:
    ```bash
    npm install
    ```
3. Start the frontend development server:
    ```bash
    npm start
    ```
   The frontend will start on `http://localhost:3000`.

---

## Usage
- Browse products by category, search, and sort.
- Click the floating chat icon (bottom right) to ask the AI chatbot about products.
- Click on category images in the hero section to jump directly to that category.

---

## Project Structure
```
Engineering_Intern_Project_Maketronics/
├── backend/
│   ├── app.py
│   ├── fetch_data.py
│   └── ...
├── data/
│   ├── books.csv
│   ├── electronics.csv
│   └── personal_health.csv
├── frontend/
│   └── smart-frontend/
│       ├── src/
│       ├── public/
│       └── ...
├── requirements.txt
└── README.md
```

---

## Notes
- The chatbot uses a mock AI reply unless you configure a real AI backend (see `app.py`).
- Data is loaded from CSV files in the `data/` directory.
- For production, build the frontend and serve it with a production server.

---

## License
This project is for educational and demonstration purposes. 