# =========================
#       QUESTION 1
# =========================


def parse_and_clean_data(lines):
    """
    Parses sales data lines, cleans records,
    returns:
    - valid cleaned records
    - invalid records with reasons
    """

    cleaned_data = []
    removed_data = []

    total_records = 0
    invalid_records = 0

    for line in lines:
        if line.startswith("TransactionID"):
            continue

        total_records += 1
        original_line = line

        fields = line.split("|")

        # 1. Field count validation
        if len(fields) != 8:
            invalid_records += 1
            removed_data.append((original_line, "Invalid field count"))
            continue

        (
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ) = fields

        product_name = product_name.replace(",", "").strip()

        # 2. Transaction ID validation
        if not transaction_id.startswith("T"):
            invalid_records += 1
            removed_data.append((original_line, "TransactionID does not start with 'T'"))
            continue

        # 3. Missing CustomerID or Region
        if not customer_id.strip() or not region.strip():
            invalid_records += 1
            removed_data.append((original_line, "Missing CustomerID or Region"))
            continue

        # 4. Quantity / price format validation
        try:
            quantity = int(quantity)
            unit_price = float(unit_price.replace(",", ""))
        except ValueError:
            invalid_records += 1
            removed_data.append((original_line, "Invalid numeric format"))
            continue

        # 5. Quantity / price value validation
        if quantity <= 0:
            invalid_records += 1
            removed_data.append((original_line, "Quantity ≤ 0"))
            continue

        if unit_price <= 0:
            invalid_records += 1
            removed_data.append((original_line, "UnitPrice ≤ 0"))
            continue

        record = {
            "transaction_id": transaction_id,
            "date": date,
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "customer_id": customer_id,
            "region": region
        }

        cleaned_data.append(record)

    print(f"Total records parsed: {total_records}")
    print(f"Invalid records removed: {invalid_records}")
    print(f"Valid records after cleaning: {len(cleaned_data)}")

    return cleaned_data, removed_data

# =========================
#       TASK 1.2
# =========================


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """

    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        (
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ) = parts

        # Clean ProductName (remove commas)
        product_name = product_name.replace(",", "").strip()

        try:
            quantity = int(quantity)
            unit_price = float(unit_price.replace(",", ""))
        except ValueError:
            continue

        transaction = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        transactions.append(transaction)

    return transactions


# =========================
#       TASK 1.3
# =========================


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0

    prelim_valid = []

    # STEP 1: Basic validation only
    for t in transactions:
        if (
            t["Quantity"] <= 0 or
            t["UnitPrice"] <= 0 or
            not t["TransactionID"].startswith("T") or
            not t["ProductID"].startswith("P") or
            not t["CustomerID"].startswith("C") or
            not t["Region"].strip()
        ):
            invalid_count += 1
            continue

        prelim_valid.append(t)

    # STEP 2: Display options from VALID data only
    regions = sorted(set(t["Region"] for t in prelim_valid))
    print("Available regions:", regions)

    amounts = [t["Quantity"] * t["UnitPrice"] for t in prelim_valid]
    print("Transaction amount range:", min(amounts), "-", max(amounts))

    filtered_by_region = 0
    filtered_by_amount = 0

    # STEP 3: Apply optional filters
    for t in prelim_valid:
        amount = t["Quantity"] * t["UnitPrice"]

        if region and t["Region"] != region:
            filtered_by_region += 1
            continue

        if min_amount and amount < min_amount:
            filtered_by_amount += 1
            continue

        if max_amount and amount > max_amount:
            filtered_by_amount += 1
            continue

        valid_transactions.append(t)

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions)
    }

    return valid_transactions, invalid_count, summary


# =========================
#       TASK 2.1
# =========================


def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    """
    total_revenue = 0.0

    for t in transactions:
        total_revenue += t["Quantity"] * t["UnitPrice"]

    return total_revenue

def region_wise_sales(transactions):
    """
    Analyzes sales by region
    """
    region_data = {}
    total_revenue = calculate_total_revenue(transactions)

    for t in transactions:
        region = t["Region"]
        revenue = t["Quantity"] * t["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += revenue
        region_data[region]["transaction_count"] += 1

    # Calculate percentage
    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / total_revenue) * 100, 2
        )

    # Sort by total_sales descending
    sorted_region_data = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_region_data


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    """
    product_data = {}

    for t in transactions:
        product = t["ProductName"]
        quantity = t["Quantity"]
        revenue = quantity * t["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += quantity
        product_data[product]["revenue"] += revenue

    result = [
        (product, data["quantity"], data["revenue"])
        for product, data in product_data.items()
    ]

    # Sort by total quantity descending
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    """
    customer_data = {}

    for t in transactions:
        customer = t["CustomerID"]
        revenue = t["Quantity"] * t["UnitPrice"]
        product = t["ProductName"]

        if customer not in customer_data:
            customer_data[customer] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customer_data[customer]["total_spent"] += revenue
        customer_data[customer]["purchase_count"] += 1
        customer_data[customer]["products_bought"].add(product)

    # Final formatting
    for customer in customer_data:
        total = customer_data[customer]["total_spent"]
        count = customer_data[customer]["purchase_count"]

        customer_data[customer]["avg_order_value"] = round(total / count, 2)
        customer_data[customer]["products_bought"] = list(
            customer_data[customer]["products_bought"]
        )

    # Sort by total_spent descending
    sorted_customer_data = dict(
        sorted(
            customer_data.items(),
            key=lambda x: x[1]["total_spent"],
            reverse=True
        )
    )

    return sorted_customer_data


# =========================
#       TASK 2.2
# =========================

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    """
    daily_data = {}

    for t in transactions:
        date = t["Date"]
        revenue = t["Quantity"] * t["UnitPrice"]
        customer = t["CustomerID"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(customer)

    # Final formatting
    for date in daily_data:
        daily_data[date]["unique_customers"] = len(daily_data[date]["customers"])
        del daily_data[date]["customers"]

    # Sort by date (chronological)
    sorted_daily_data = dict(sorted(daily_data.items()))

    return sorted_daily_data

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    """
    daily_data = daily_sales_trend(transactions)

    peak_date = None
    peak_revenue = 0.0
    peak_count = 0

    for date, data in daily_data.items():
        if data["revenue"] > peak_revenue:
            peak_revenue = data["revenue"]
            peak_count = data["transaction_count"]
            peak_date = date

    return peak_date, peak_revenue, peak_count


# =========================
#       TASK 2.3
# =========================

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    """
    product_data = {}

    for t in transactions:
        product = t["ProductName"]
        quantity = t["Quantity"]
        revenue = quantity * t["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += quantity
        product_data[product]["revenue"] += revenue

    result = [
        (product, data["quantity"], data["revenue"])
        for product, data in product_data.items()
        if data["quantity"] < threshold
    ]

    # Sort by quantity ascending
    result.sort(key=lambda x: x[1])

    return result

from datetime import datetime
from collections import defaultdict


# =========================
#       TASK 4.1
# =========================


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    """

    # ---------------- BASIC METRICS ----------------
    total_transactions = len(transactions)
    total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [t['Date'] for t in transactions]
    start_date, end_date = min(dates), max(dates)

    # ---------------- REGION ANALYSIS ----------------
    region_data = defaultdict(lambda: {'sales': 0, 'count': 0})
    for t in transactions:
        amount = t['Quantity'] * t['UnitPrice']
        region_data[t['Region']]['sales'] += amount
        region_data[t['Region']]['count'] += 1

    region_summary = []
    for region, data in region_data.items():
        percent = (data['sales'] / total_revenue) * 100 if total_revenue else 0
        region_summary.append((region, data['sales'], percent, data['count']))

    region_summary.sort(key=lambda x: x[1], reverse=True)

    # ---------------- PRODUCT ANALYSIS ----------------
    product_data = defaultdict(lambda: {'qty': 0, 'revenue': 0})
    for t in transactions:
        name = t['ProductName']
        amount = t['Quantity'] * t['UnitPrice']
        product_data[name]['qty'] += t['Quantity']
        product_data[name]['revenue'] += amount

    top_products = sorted(
        product_data.items(),
        key=lambda x: x[1]['qty'],
        reverse=True
    )[:5]

    # ---------------- CUSTOMER ANALYSIS ----------------
    customer_data = defaultdict(lambda: {'spent': 0, 'count': 0})
    for t in transactions:
        cid = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        customer_data[cid]['spent'] += amount
        customer_data[cid]['count'] += 1

    top_customers = sorted(
        customer_data.items(),
        key=lambda x: x[1]['spent'],
        reverse=True
    )[:5]

    # ---------------- DAILY TREND ----------------
    daily_data = defaultdict(lambda: {'revenue': 0, 'count': 0, 'customers': set()})
    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']
        daily_data[date]['revenue'] += amount
        daily_data[date]['count'] += 1
        daily_data[date]['customers'].add(t['CustomerID'])

    daily_summary = sorted(daily_data.items())

    best_day = max(daily_data.items(), key=lambda x: x[1]['revenue'])

    # ---------------- API ENRICHMENT SUMMARY ----------------
    enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
    failed_products = sorted(
        set(t['ProductName'] for t in enriched_transactions if not t.get('API_Match'))
    )
    success_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0

    # ---------------- WRITE REPORT ----------------
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("           SALES ANALYTICS REPORT\n")
        f.write(f"     Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"     Records Processed: {total_transactions}\n")
        f.write("=" * 60 + "\n\n")

        # 1. OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {start_date} to {end_date}\n\n")

        # 2. REGION PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Region':<10}{'Sales':>15}{'% Total':>12}{'Txns':>10}\n")
        for r, s, p, c in region_summary:
            f.write(f"{r:<10}₹{s:>14,.2f}{p:>11.2f}%{c:>10}\n")
        f.write("\n")

        # 3. TOP PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Rank':<5}{'Product':<25}{'Qty':>8}{'Revenue':>15}\n")
        for i, (name, d) in enumerate(top_products, 1):
            f.write(f"{i:<5}{name:<25}{d['qty']:>8}₹{d['revenue']:>14,.2f}\n")
        f.write("\n")

        # 4. TOP CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Rank':<5}{'Customer':<15}{'Spent':>15}{'Orders':>10}\n")
        for i, (cid, d) in enumerate(top_customers, 1):
            f.write(f"{i:<5}{cid:<15}₹{d['spent']:>14,.2f}{d['count']:>10}\n")
        f.write("\n")

        # 5. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Date':<12}{'Revenue':>15}{'Txns':>8}{'Customers':>12}\n")
        for date, d in daily_summary:
            f.write(f"{date:<12}₹{d['revenue']:>14,.2f}{d['count']:>8}{len(d['customers']):>12}\n")
        f.write("\n")

        # 6. PRODUCT PERFORMANCE
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 60 + "\n")
        f.write(f"Best Selling Day: {best_day[0]} (₹{best_day[1]['revenue']:,.2f})\n\n")

        # 7. API SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total Enriched: {enriched_count}\n")
        f.write(f"Success Rate:  {success_rate:.2f}%\n")
        f.write("Failed Products:\n")
        for p in failed_products:
            f.write(f" - {p}\n")

        f.write("\n--- END OF REPORT ---\n")
