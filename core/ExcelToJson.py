import pandas as pd
import json

# Read the Excel file
df = pd.read_excel("data.xlsx")

# Convert to JSON
result = []
for _, row in df.iterrows():
    entry = {
        "invoice_number": row["invoice_number"],
        "age": row["age"],
        "seller": {
            "name": row["seller.name"],
            "phone": row["seller.phone"],
            "address": row["seller.address"]
        },
        "buyer": {
            "name": row["buyer.name"],
            "phone": row["buyer.phone"],
            "address": row["buyer.address"]
        },
        "purchases": [],
        "sales": []
    }
    # Add hobbies
    purchase = {
        "metal_type": row["purchases.name"],
        "weight": row["purchases.weight"]
    }
    entry["purchases"].append(purchase)
    result.append(entry)

# Save to JSON file
with open("output.json", "w") as f:
    json.dump(result, f, indent=4)