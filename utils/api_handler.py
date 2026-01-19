import requests

def fetch_product_info(product_id):
    """
    Fetches dummy product data from API
    """
    url = "https://dummyjson.com/products/1"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


# =========================
#       TASK 3.1
# =========================

BASE_URL = "https://dummyjson.com/products"

# ---------------- TASK 3.1 (a) ----------------
def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns list of product dictionaries
    """
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        cleaned_products = []
        for p in products:
            cleaned_products.append({
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "price": p.get("price"),
                "rating": p.get("rating")
            })

        print(f"API SUCCESS: Fetched {len(cleaned_products)} products")
        return cleaned_products

    except requests.exceptions.RequestException as e:
        print("API FAILURE:", e)
        return []


# ---------------- TASK 3.1 (b) ----------------
def create_product_mapping(api_products):
    """
    Creates mapping of product ID -> product info
    """
    product_mapping = {}

    for product in api_products:
        pid = product.get("id")
        if pid is not None:
            product_mapping[pid] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "rating": product.get("rating")
            }

    return product_mapping


# =========================
#       TASK 3.2
# =========================

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches sales data with API information
    """
    enriched_transactions = []

    for txn in transactions:
        enriched_txn = txn.copy()

        try:
            # Extract numeric ID from ProductID (P101 → 101)
            product_id_str = txn.get("ProductID", "")
            numeric_id = int("".join(filter(str.isdigit, product_id_str)))

            api_product = product_mapping.get(numeric_id)

            if api_product:
                enriched_txn["API_Category"] = api_product["category"]
                enriched_txn["API_Brand"] = api_product["brand"]
                enriched_txn["API_Rating"] = api_product["rating"]
                enriched_txn["API_Match"] = True
            else:
                enriched_txn["API_Category"] = None
                enriched_txn["API_Brand"] = None
                enriched_txn["API_Rating"] = None
                enriched_txn["API_Match"] = False

        except Exception:
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None
            enriched_txn["API_Match"] = False

        enriched_transactions.append(enriched_txn)

    return enriched_transactions


# ---------------- HELPER: SAVE TO FILE ----------------
def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched sales data to pipe-delimited file
    """
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(headers) + "\n")

        for txn in enriched_transactions:
            row = []
            for h in headers:
                val = txn.get(h)
                row.append("" if val is None else str(val))
            f.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")
