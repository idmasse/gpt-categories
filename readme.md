### Use chatGPT API to find product categories for approved mapping products

#### This series of scripts pulls product data from convictional, splits the returned convictional data into smaller chunks to call the chatGPT api to categorize the products, recombines the data to match parents/variants, then preps the data for conversion to csv

#### Step 1: get_partners.py | Returns the companyID for partner from convictional
#### Step 2: get_variants.py | Returns parent / variant JSON info for each of the brands products from Convictional. Run this twice, one for only parent data, the other with both parent and variant data.
#### Step 3: split_json.py | Splits the product data JSON into smaller chunks to feed into chatGPT api. Calling the gpt api with smaller chunks reduces the tokens needed which greatly increases the accuracy and detail of the responses.
#### Step 4: gpt_categorize.py | Call the chatGPT api with the split product JSON files
#### Step 5: append_variants.py | Recombines the chatGPT results with the analagous variant IDs from step 2. 
#### Step 6: prep_json_4csv.py | Reorders the combined GPT results for easier conversion to CSV.