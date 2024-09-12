from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

gptclient = OpenAI(api_key=os.getenv('OPENAI_API_KEY')) # initialize gpt client

# load categories and additional info files
with open('categories.json', 'r') as f:
    categories = json.load(f)

with open('additional_info.json', 'r') as h:
    additional_info = json.load(h)

# prompt gpt
def categorize_products(product_info):
    response = gptclient.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        top_p=1,
        messages=[
            {   
                "role":"user",
                "content":f"""
                I have a strict list of categories and sub-categories. Use them to categorize the products.
                I also have a strict list of additional info, use it to find any additional information about the product. 
                
                Categories and sub-categories are:
                {categories}

                Additional Information:
                {additional_info}

                Instructions:
                - Format response as a list of dicts in JSON. Do not include ```JSON in the response.
                - These are the products you are categorizing: {product_info}
                - Only choose from the listed categories and sub-categories.
                - Only choose from the listed additional info. 
                """
            }
        ]
    )
    
    return response.choices[0].message.content.strip()

# specify the folder containing the product_info files
input_folder_path = ''
# specify the folder to save the results
output_folder_path = ''

# ensure the output folder exists
os.makedirs(output_folder_path, exist_ok=True)

# loop through all files in the input folder
for filename in os.listdir(input_folder_path):
    if filename.endswith('.json'):  # check if the file is a JSON file
        input_file_path = os.path.join(input_folder_path, filename)
        with open(input_file_path, 'r') as f:
            product_info = json.load(f)
        
        categorized = categorize_products(product_info)
        
        # define the output file path & append filenames
        output_file_path = os.path.join(output_folder_path, f"gpt_{filename}")
        
        # write the response to the output file
        with open(output_file_path, 'w') as out_f:
            out_f.write(categorized)
        
        print(f"Processed {filename}, result saved to {output_file_path}")
