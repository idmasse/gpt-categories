import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

company_id = 'mnml-la'

url = f"https://api.convictional.com/buyer/products?page=0&limit=50&companyId={company_id}"

headers = {
    "accept": "application/json",
    "Authorization": os.getenv('CONVICTIONAL_API_KEY')  # flipshop api key
}


def get_product_details(url):
    product_details = {}
    
    while url:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            break
        
        data = response.json()

        # extract product and variant details
        for product in data['data']:
            parent_id = product.get('id', 'n/a')
            if parent_id not in product_details:
                product_details[parent_id] = []
                
            variants = product.get('variants', [])
            for variant in variants:
                variant_id = variant.get('id', 'n/a')
                product_details[parent_id].append(variant_id)
        
        # check if there's more pages of data
        if data.get("hasMore", False):
            url = data.get('next', None)
        else:
            break

    return product_details

# get all product details
product_details = get_product_details(url)

# print the results
print(json.dumps(product_details, indent=4))

# save the results to a file
output_file = f"{company_id}_ids.json"
with open(output_file, 'w') as f:
    json.dump(product_details, f, indent=4)

print(f"Parent and variant IDs for {company_id} saved to {output_file}")
