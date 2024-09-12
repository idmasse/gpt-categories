import json
import os

def safe_get(dictionary, key, default=None):
    """Safely get a value from a dictionary."""
    return dictionary.get(key, default)

def transform_product_data(product_data):
    transformed_data = []
    
    for product in product_data:
        parent_info = {
            "parent_id": safe_get(product, "parent_id", ""),
            "product_title": safe_get(product, "product_title", safe_get(product, "title", "")),
            "category": safe_get(product, "category", ""),
            "sub_category": safe_get(product, "sub_category", ""),
            "sub_category_2": safe_get(product, "sub_category_2", ""),
            "attributes": safe_get(product, "attributes", {}),
            "additional_info": safe_get(product, "additional_info", {})
        }
        
        variants = safe_get(product, "variants", [])
        if not variants: # if no variants, create a single product with available information
            transformed_data.append(parent_info)
        else:
            for variant in variants:
                variant_product = parent_info.copy()
                variant_product.update({
                    "variant_id": safe_get(variant, "variant_id", ""),
                    "color": safe_get(variant, "color", ""),
                    "size": safe_get(variant, "size", "")
                })
                transformed_data.append(variant_product)
    
    return transformed_data

# input File path
file_path = os.path.join("mnml", "gpt_results", "mnml_combined_gpt_results.json")

# read JSON data from file
try:
    with open(file_path, 'r') as file:
        product_data = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {file_path} does not contain valid JSON.")
    exit(1)

# transform the data
transformed_data = transform_product_data(product_data)

# print the number of transformed products
print(f"Total number of transformed products: {len(transformed_data)}")

# Print the first transformed product as an example
# if transformed_data:
#     print("\nExample of a transformed product:")
#     print(json.dumps(transformed_data[0], indent=2))
# else:
#     print("\nNo products were transformed.")

# save transformed data to a new file
output_file_path = os.path.join("mnml", "gpt_results", "mnml_results_prep_json_to_csv.json")
with open(output_file_path, 'w') as output_file:
    json.dump(transformed_data, output_file, indent=2)

print(f"\nTransformed data has been saved to {output_file_path}")