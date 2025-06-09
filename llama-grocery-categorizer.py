import os

import ollama

input_file = "./docs/grocery_list.txt"
output_file = "./docs/categorized_grocery_list.txt"


if not os.path.exists(input_file):
    print(f"Input file {input_file} does not exist. Exiting...")
    exit(1)


with open(input_file, "r") as f:
    items = f.read().splitlines()


prompt = f"""
    You are an assistant that categorizes and sorts grocery items.
    
    Here's the list of items:
    {items}
    
    You must categorize on following basis
    
    1. Categorize these items into appropriate categories such as Produce, Dairy, Meat, Bakery
    2. Sort the items alphabetically within each category
    3. Present the categorized list in clear organized manner, using bullet points or numbers
"""

try:
    response = ollama.generate(model="llama3.2", prompt=prompt)
    generated_text = response.get("response", "")

    with open(output_file, "w") as f:
        f.write(generated_text)

    print(f"Generated list items have been written to {output_file}")
except Exception as e:
    print(e)
