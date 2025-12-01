from flask import Flask, render_template, request, jsonify
from scraper import scrape_all
from price import save_price, get_price_history
import matplotlib.pyplot as plt # pyright: ignore[reportMissingModuleSource]
import io, base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/search")
def search():
    query = request.args.get("query")
    if not query:
        return render_template("index.html", products=[])

    products = scrape_all(query)

    for p in products:
        save_price(p["name"], p["site"], p["price"])
        history = get_price_history(p["name"])
        p["graph"] = create_price_graph(history) if history else None
        p["reviews"] = ["Great phone!", "Battery life could be better.", "Excellent camera!"]

    return render_template("index.html", query=query, products=products)


def create_price_graph(history):
    dates = [h["date"] for h in history]
    prices = [h["price"] for h in history]
    plt.figure(figsize=(6,3))
    plt.plot(dates, prices, marker='o')
    plt.title("7-Day Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Price (₹)")
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


if __name__ == '__main__':
    print("✅ Starting Flask server...")
    app.run(debug=True)
