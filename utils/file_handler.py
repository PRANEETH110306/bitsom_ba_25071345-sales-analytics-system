# =========================
#       TASK 1.1
# =========================


def read_sales_file(file_path):
    """
    Reads the sales data file safely and returns
    a list of non-empty lines.
    Handles non-UTF-8 encoding issues.
    """
    lines = []

    try:
        with open(file_path, "r", encoding="latin-1", errors="ignore") as file:
            for line in file:
                line = line.strip()
                if line:  # skip empty lines
                    lines.append(line)

    except FileNotFoundError:
        print("Sales data file not found.")
    except Exception as e:
        print("Error reading sales data file:", e)

    return lines

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw transaction lines (strings)
    """

    encodings = ["utf-8", "latin-1", "cp1252"]
    lines = []

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc, errors="strict") as file:
                for line in file:
                    line = line.strip()

                    # Skip empty lines
                    if not line:
                        continue

                    # Skip header row
                    if line.startswith("TransactionID"):
                        continue

                    lines.append(line)

            # If reading succeeds, stop trying other encodings
            break

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    return lines
