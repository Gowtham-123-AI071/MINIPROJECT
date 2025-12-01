import csv, datetime, os

def clean_price(price_str):
    return float(price_str.replace("₹", "").replace(",", "").strip())

def save_price(name, site, price_str):
    try:
        price = clean_price(price_str)
    except ValueError:
        print(f"⚠️ Price save error: {price_str}")
        return

    filename = "price_history.csv"
    today = datetime.date.today().isoformat()

    # ✅ Removed os.makedirs line
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, site, today, price])

def get_price_history(name):
    history = []
    if not os.path.exists("price_history.csv"):
        return history

    with open("price_history.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == name:
                history.append({"date": row[2], "price": float(row[3])})
    return history[-7:]
