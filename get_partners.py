import requests
import os
from dotenv import load_dotenv

load_dotenv()

# fetch all pages and search for the specified seller
def search_seller(seller_name):
    url = "https://api.convictional.com/partners?page="
    headers = {
        "accept": "application/json",
        "Authorization": os.getenv('CONVICTIONAL_API_KEY')
    }
    
    page = 1
    while True:
        response = requests.get(f"{url}{page}", headers=headers)

        if response.status_code != 200:
            print(f"Failed to retrieve data from page {page}: {response.status_code}")
            break
        
        data = response.json()
        
        # check if the data field exists and contains items
        if "data" in data and len(data["data"]) > 0:
            for brand in data["data"]:
                if brand["sellerName"].lower() == seller_name.lower():
                    return {
                        "companyId": brand.get("companyId"),
                        "sellerName": brand.get("sellerName"),
                        "partner_id": brand.get("_id")
                    }
        else:
            break
        
        page += 1
    
    return "Seller not found."

if __name__ == "__main__":
    seller_to_find = "Refinery Number One"
    result = search_seller(seller_to_find)
    print(result)

