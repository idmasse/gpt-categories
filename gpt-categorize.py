from openai import OpenAI
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

gptclient = OpenAI(api_key=os.getenv('API_KEY'))

with open('categories.json', 'r') as f:
    categories = json.load(f)

with open('attribute_data.json', 'r') as g:
    attribute_data = json.load(g)

with open('additional_info.json', 'r') as h:
    additional_info = json.load(h)

def categorize_products(product_info):
    response = gptclient.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        top_p=1,
        messages=[
            {   
                "role":"user",
                "content":f"""
                I have a strict list of categories and sub-categories. Use them to categorize the following product. 
                I also have a strict list of attributes. Use them find any applicable attributes for the product.
                I also have a strict list of additional info, use it to find any additional information about the product. 
                
                Categories and sub-categories are:
                {categories}

                Attribute codes are:
                {attribute_data}

                Additional Information:
                {additional_info}

                Instructions:
                - These are the products you are categorizing: {product_info}
                - Use the supplied product title, description, and product URL https://refinerynumberone.com/.
                - Only choose from the listed categories and sub-categories. Format the response as JSON.
                - Only match found attributes to the attribute codes from attribute_data. Format the response as JSON.
                - Use your best judgment to reply with additional information. Format the response as JSON.
                - If you aren't confident about the categories, reply with `"Categories": null`.
                - If you aren't confident about the attributes, reply with `"Attributes": null`.
                - If you are not able to find additional information, do not include it in the response.
                """
            }
        ]
    )
    
    return response.choices[0].message.content.strip()

# Specify the folder containing the product_info files
input_folder_path = 'split_json_missing'
# Specify the folder to save the results
output_folder_path = 'refinery-gpt-results2'

# Ensure the output folder exists
os.makedirs(output_folder_path, exist_ok=True)

# Loop through all files in the input folder
for filename in os.listdir(input_folder_path):
    if filename.endswith('.json'):  # Check if the file is a JSON file
        input_file_path = os.path.join(input_folder_path, filename)
        with open(input_file_path, 'r') as f:
            product_info = json.load(f)
        
        categorized = categorize_products(product_info)
        
        # Define the output file path
        output_file_path = os.path.join(output_folder_path, f"gpt_{filename}")
        
        # Write the raw response to the output file
        with open(output_file_path, 'w') as out_f:
            out_f.write(categorized)
        
        print(f"Processed {filename}, result saved to {output_file_path}")
        time.sleep(5)
