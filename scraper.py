from bs4 import BeautifulSoup
import pandas as pd

def get_laptops_offline():
    print("Reading the local Amazon file...")
    
    # 1. Open the file you saved manually
    try:
        with open("amazon_search.html", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("ERROR: Could not find 'amazon_search.html'. Make sure you saved it in the pulsepick_ai folder.")
        return

    soup = BeautifulSoup(content, "html.parser")
    laptop_list = []

    # 2. Find the Product Cards (Amazon's HTML structure)
    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    print(f"Parsing data from {len(products)} products...")

    for item in products[:10]: # Let's get 10 laptops now
        try:
            # Extract Name
            name = item.h2.text.strip()
            
            # Extract Price
            price_box = item.find("span", "a-price-whole")
            price = price_box.text if price_box else "N/A"
            
            # Extract Rating
            rating_box = item.find("span", "a-icon-alt")
            rating = rating_box.text.split(" ")[0] if rating_box else "N/A"

            laptop_list.append({
                "Product Name": name,
                "Price (INR)": price,
                "Rating (Out of 5)": rating
            })
        except Exception as e:
            continue

    # 3. Saving to CSV
    if laptop_list:
        df = pd.DataFrame(laptop_list)
        df.to_csv("laptops_data.csv", index=False)
        print("SUCCESS: 10 laptops extracted and saved to 'laptops_data.csv'!")
        print("Check your folder now.")
    else:
        print("Failed to find products in the HTML. Check the file content.")

if __name__ == "__main__":
    get_laptops_offline()