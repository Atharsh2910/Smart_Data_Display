import requests
import pandas as pd

def fetch_books(query="data science", limit=25):
    url = f"https://openlibrary.org/search.json?q={query}&limit={limit}"
    response = requests.get(url)
    data = response.json()

    books = []
    for item in data['docs'][:limit]:
        books.append({
            "title": item.get("title", "N/A"),
            "author": ", ".join(item.get("author_name", [])),
            "isbn": item.get("isbn", ["N/A"])[0],
            "language": item.get("language", ["N/A"])[0] if "language" in item else "N/A",
            "publisher": ", ".join(item.get("publisher", [])),
            "first_publish_year": item.get("first_publish_year", "N/A")
        })

    df = pd.DataFrame(books)
    df.to_csv("../data/books.csv", index=False)
    print("Saved books.csv")

def fetch_fake_products(category, filename):
    url = f"https://fakestoreapi.com/products/category/{category}"
    response = requests.get(url)
    data = response.json()
    
    products = []
    for item in data[:25]:
        products.append({
            "title": item.get("title"),
            "description": item.get("description"),
            "price": item.get("price"),
            "rating": item.get("rating", {}).get("rate"),
            "image": item.get("image"),
            "category": item.get("category")
        })

    df = pd.DataFrame(products)
    df.to_csv(f"../data/{filename}.csv", index=False)
    print(f"Saved {filename}.csv")

if __name__ == "__main__":
    fetch_books()
    fetch_fake_products("electronics", "electronics")
