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
    product_details = []
    
    while url:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            break
        
        data = response.json()

        # extract product and variant details
        for product in data['data']:
            product_info = {
                "parent_id":product.get('id', 'n/a'),
                "product_title": product.get('title', 'n/a'),
                "product_description": product.get('description', 'n/a'),
                "variants": []
            }
            variants = product.get('variants', [])
            for variant in variants:
                # get color and size from the 'options' list
                color = next((option['value'] for option in variant['options'] if option['name'] == 'Color'), 'n/a')
                size = next((option['value'] for option in variant['options'] if option['name'] == 'Size'), 'n/a')
                
                variant_info = {
                    "variant_id": variant.get('id'),
                    "color": color,
                    "size": size
                }
                product_info["variants"].append(variant_info)
            
            product_details.append(product_info)
        
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
output_file = f"{company_id}_product_details.json"
with open(output_file, 'w') as f:
    json.dump(product_details, f, indent=4)

print(f"Product details for {company_id} saved to {output_file}")
