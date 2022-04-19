import csv
import sys

INTERESTED_COLUMNS = ["Date", "Amount", "Payee", "Reference"]
KNOWN_CATEGORY_TO_REFERENCES = {
    "Groceries": ["pak n save", "countdown", "hellofresh"],
    "Petrol": ["npd", "petrol", "gull", "waitomo"]
}

NOT_RECORDED_ITEMS = ["powershop"]

OUTPUT_COLUMNS = ["Date", "Payee", "Amount", "Category"]


def process(path: str) -> None:
    print("Processing " + path)
    rows = []
    with open("../resources/input/" + path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["Amount"].startswith("-") and row["Reference"] != "INTERNET XFR" and row["Payee"] not in NOT_RECORDED_ITEMS and row["Tran Type"] != "FT":
                row_with_columns = remove_uninterested_columns(row)
                if row_with_columns["Payee"] == "Elya cox" and row_with_columns["Reference"] != "":
                    row_with_columns["Payee"] = row_with_columns["Reference"]
                row_with_columns["Category"] = get_category(row_with_columns["Payee"], row_with_columns["Reference"])
                if row_with_columns["Category"] != "FILL ME":
                    row_with_columns["Payee"] = row_with_columns["Category"]
                row_with_columns.pop("Reference", None)
                row_with_columns["Amount"] = row_with_columns["Amount"].lstrip("-")
                rows.append(row_with_columns)

    with open("../resources/output/output.csv", "w", encoding="UTF8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(rows)


def get_category(payee: str, reference: str) -> str:
    for category, references in KNOWN_CATEGORY_TO_REFERENCES.items():
        for ref in references:
            if ref in payee.lower():
                return category
    return "FILL ME"


def remove_uninterested_columns(budget_dict: dict) -> dict:
    result: dict = {}
    for column in INTERESTED_COLUMNS:
        result[column] = budget_dict[column]
    return result


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Too few arguments. Run with file name of csv")
        sys.exit()
    if len(sys.argv) > 2:
        print("Too many arguments. Run with file name of csv")
        sys.exit()

    process(str(sys.argv[1]))
