from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

gptclient = OpenAI(api_key=os.getenv('API_KEY'))

with open('categories.json', 'r') as f:
    categories = json.load(f)

with open('attribute_data.json', 'r') as g:
    attribute_data = json.load(g)

with open('additional_info.json', 'r') as h:
    additional_info = json.load(h)

def categorize_products(title, description, product_url):
    response = gptclient.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        top_p=1,
        messages=[
            {
                "role":"user",
                "content":f"""
                I have a strict list of categories and sub-categories. Categorize the following product. 
                I also have a strict list of attributes, find any applicable attributes for the product.
                I also have a strict list of additional info, use it to find any additional information about the product.
                
                Use the supplied product title, description, brand name and product URL to find the above requested information. Parse information from the website to retrieve data. 
                
                Title: {title}
                Description: {description}
                Product URL: {product_url}
                Brand Name: {brand_name}
                
                Categories and sub-categories are:
                {categories}

                Attribute codes are:
                {attribute_data}

                Additional Information:
                {additional_info}

                Only choose from the listed categories and sub-categories. Format response in JSON.

                Only match found attributes to the attribute codes from attribute_data. Format response in JSON.

                Additional information - Use your best judgment to reply with additional information. Format response in JSON.
                
                If you aren't confident what the categories should be, do not hallucinate them. Reply with "Categories:null"
                If you aren't confident what the attributes should be, do not hallucinate them. Reply with "Attributes:null"
                If you are not able to find additional information, do not include it.
                """
            }
        ]
    )
    
    return response.choices[0].message.content.strip()

brand_name = 'Oniva'
title = "Reclining Camp Chair"
description = """ Plush, portable, and packable, the Picnic Time Reclining Camp Chair is your camping cockpit with three reclining positions, an extra-wide, padded polyester seat and armrests, and much more. """
product_url = "https://www.picnictime.com/products/reclining-camp-chair"

categorized = categorize_products(title, description, product_url)

print(f"{categorized}")