import json
import os

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def process_and_combine_files(product_directory, variant_file):
    # load variant data
    variant_data = load_json_file(variant_file)
    
    # create a dictionary to store variants by parent_id
    variants_by_parent = {}
    for item in variant_data:
        parent_id = item['parent_id']
        if parent_id not in variants_by_parent:
            variants_by_parent[parent_id] = []
        variants_by_parent[parent_id].extend(item.get('variants', []))

    # list to store all combined product data
    all_products = []

    # process all JSON files in the product directory
    for filename in os.listdir(product_directory):
        if filename.endswith('.json'):
            product_file = os.path.join(product_directory, filename)
            product_data = load_json_file(product_file)
            
            for product in product_data:
                parent_id = product['parent_id']
                if parent_id in variants_by_parent:
                    product['variants'] = variants_by_parent[parent_id]
                all_products.append(product)

    # save combined and updated product data
    output_file = os.path.join(product_directory, "mnml_combined_gpt_results.json")
    with open(output_file, 'w') as file:
        json.dump(all_products, file, indent=4)
    
    print(f"Combined and updated data saved to {output_file}")

product_directory = 'mnml/gpt_results'  # path to the directory containing product files to combine
variant_file = 'mnml/mnml_product_details.json'  # path to the file containing variant data to append

process_and_combine_files(product_directory, variant_file)