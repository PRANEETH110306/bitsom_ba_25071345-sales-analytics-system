import os

from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, validate_and_filter

# Task 2
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

# Task 3
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

# Task 4
from utils.data_processor import generate_sales_report


def main():
    try:
        # Build file path safely
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "data", "sales_data.txt")

        # Task 1.1: Read raw sales data
        raw_lines = read_sales_data(file_path)

        if not raw_lines:
            print("No data read from file.")
            return

        print(f"Raw records read: {len(raw_lines)}")

        # Task 1.2: Parse and clean data
        transactions = parse_transactions(raw_lines)
        print(f"Parsed transactions: {len(transactions)}")

        # Task 1.3: Validate and filter data & Task 5.1: User interaction for filters
        choice = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region = None
        min_amount = None
        max_amount = None

        if choice == "y":
            region = input("Enter region (or press Enter to skip): ").strip() or None

            min_amt = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_amt = input("Enter maximum amount (or press Enter to skip): ").strip()

            min_amount = float(min_amt) if min_amt else None
            max_amount = float(max_amt) if max_amt else None

        valid_transactions, invalid_count, summary = validate_and_filter(
            transactions,
            region=region,        # you can change this to "North" for testing
            min_amount=min_amount,    # e.g., 5000
            max_amount=max_amount
        )

        print("\nValidation & Filter Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")

        print("\nFinal valid transactions:", len(valid_transactions))

        print("Total Revenue:", calculate_total_revenue(valid_transactions))
        print("Region-wise:", region_wise_sales(valid_transactions))
        print("Top Products:", top_selling_products(valid_transactions))
        print("Customers:", list(customer_analysis(valid_transactions).items())[:3])
        print("Daily Trend:", list(daily_sales_trend(valid_transactions).items())[:3])
        print("Peak Day:", find_peak_sales_day(valid_transactions))
        print("Low Products:", low_performing_products(valid_transactions))

        # -------- TASK 3 --------
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)

        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        save_enriched_data(enriched_transactions)


        # -------- TASK 4 --------
        generate_sales_report(
        valid_transactions,
        enriched_transactions
    )

        print("Sales report generated at output/sales_report.txt")

    except Exception as e:
        print("\n An unexpected error occurred:")
        print(e)

if __name__ == "__main__":
    main()

