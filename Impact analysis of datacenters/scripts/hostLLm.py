import json
import ollama
import jsonify

# Load the input JSON file
input_file = "addresses_extracted.json"
output_file = "structured_output.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Process data centers and structure output
structured_data = []

for state, state_data in data.items():
    for city_details in state_data.get("details", []):
        city_name = city_details.get("name", "Unknown City")
        
        for data_center in city_details.get("addresses", []):
            # Extract fields from JSON
            name = data_center.get("name", "Unknown")
            address = ", ".join(filter(None, [data_center.get("address1"), data_center.get("address2"), data_center.get("address3")]))
            overview = data_center.get("overviewHTML", "")
            specs = data_center.get("specsHtml", "")

            # Construct prompt for Ollama with escaped braces for literal JSON
            prompt = f"""Extract the following details from the given data center information:
- Name
- Address
- Latitude & Longitude 
- Power Capacity (MW)
- Year Built
- Total Area (sq.ft)
- Any other relevant metadata

address: 
{address}
            
Data Center Overview:
{overview}

Specifications:
{specs}
            
            
In following structured format and if the details are unknown then mark them as "Unknown":
structured_entry = {{
    "Name": "",
    "Address": "",
    "Latitude": "",
    "Longitude": "",
    "Power": "",
    "Year Built": "",
    "Area": "",
    "Metadata": {{
        "Other information": "in key value pairs" (information that could be useful for microclimate analysis)
    }}
}}
"""

            # Generate structured details using Ollama
            response = ollama.generate(model="llama3.1", prompt=prompt)
            print(response["response"])
            response_text = response["response"]

            # Attempt to convert response_text into a JSON object
            try:
                response_json = json.loads(response_text)
            except json.JSONDecodeError:
                response_json = {"Generated Output": response_text}

            # Alternatively, if your jsonify module provides a conversion function, you might use:
            # response_json = jsonify(response_text)

            # Construct structured JSON output
            structured_entry = {
                "Name": name,
                "StructuredDetails": response_json
            }
            
            # Append to the final data list
            structured_data.append(structured_entry)
            break
        break
    break

# Save structured data to a new JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(structured_data, f, indent=4)

print(f"Structured output saved to {output_file}")