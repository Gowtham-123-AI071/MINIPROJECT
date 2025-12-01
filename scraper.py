import requests
import json

def scrape_all(query):
    print(f"🧠 Searching for: {query}")

    API_KEY = "4ed8da13f1b37fea331107a9c41b81b3638a345f75d0dae2cb5e3d0967384626"
    params = {
        "engine": "google_shopping",
        "q": query,
        "location": "India",
        "hl": "en",
        "gl": "in",
        "api_key": API_KEY
    }

    response = requests.get("https://serpapi.com/search.json", params=params)
    print(f"🔗 Request URL: {response.url}")
    print(f"🌐 Status Code: {response.status_code}")

    if response.status_code != 200:
        print("❌ Error: Bad response from SerpAPI.")
        return []

    data = response.json()

    # 🧠 Print the full structure for debugging
    print("📦 Full API Response:")
    print(json.dumps(data, indent=2)[:2000])  # print first 2000 chars

    # ✅ Extract products if present
    results = []
    for item in data.get("shopping_results", []):
        results.append({
            "name": item.get("title"),
            "price": item.get("price"),
            "site": item.get("source"),
            "link": item.get("link"),
            "image": item.get("thumbnail")
        })

    print(f"✅ Found {len(results)} products total.")
    return results
