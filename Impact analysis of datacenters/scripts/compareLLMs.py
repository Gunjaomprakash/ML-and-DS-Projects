import os
import json
import csv
import openai
from time import sleep

# Set your OpenAI API key (or set it via your environment variable)
openai.api_key = "API_KEY"

def extract_fields_from_json(facility_json_str: str, model: str) -> dict:
    """
    Sends the facility JSON (as a string) to the specified OpenAI model for extraction.
    Returns a dict with standardized fields.
    """
    prompt = f"""
You are an AI assistant that extracts specific standardized information from a facility's JSON data.
Below is the facility data delimited by triple backticks:
{facility_json_str}
Extract and return the following fields as a valid JSON object (use empty string if not found):
- Name
- Street Address
- City
- State
- Zip Code
- Provider
- Country(US, UK, etc.)
- Whitespace(Total building area in Sq. Ft.)
- Area(Building area in Sq. Ft.)
- Year Built(YYYY)
- Power(in KW)
- Scale(Hyperscale, Enterprise, etc.)
- Certifications
- URL

Output format (strict JSON):
{{
  "Name": "",
  "Provider": "",
  "StreetAddress": "",
  "City": "",
  "ZipCode": "",
  "State": "",
  "Country": "",
  "Whitespace": "",
  "Area": "",
  "YearBuilt": "",
  "Power": "",
  "Scale": "",
  "Certifications": "",
  "URL": ""
}}
Do not include any extra keys.
    """
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI that extracts structured information from JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=300
        )
        content = response.choices[0].message.content.strip()
        extracted_data = json.loads(content)
    except Exception as e:
        print("Error during extraction:", e)
        extracted_data = {
            "Name": "",
            "Provider": "",
            "StreetAddress": "",
            "City": "",
            "ZipCode": "",
            "State": "",
            "Country": "",
            "Whitespace": "",
            "Area": "",
            "YearBuilt": "",
            "Power": "",
            "Scale": "",
            "Certifications": "",
            "URL": ""
        }
    return extracted_data

def load_progress(output_file: str):
    """Load already processed records if the output file exists."""
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            progress = json.load(f)
    else:
        progress = []
    return progress

def save_progress(output_file: str, data: list):
    """Save the progress as a CSV file instead of JSON."""
    if not data:
        return  # Skip if no data to write
    
    # Define CSV headers (same as extracted fields)
    headers = [
        "unique_key", "source", "Name", "Provider", "StreetAddress", "City",
        "ZipCode", "State", "Country", "Whitespace", "Area", "YearBuilt",
        "Power", "Scale", "Certifications", "URL"
    ]

    # Write CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()  # Write column names
        writer.writerows(data)  # Write extracted data as rows

def process_data(input_file: str, output_file: str, model: str, max_rows: int = 50):
    """
    Generic function to process JSON data with a limit of max_rows.
    Works for datacenterhawk, datacenters.com, and datacentermap.
    """
    progress = []
    count = 0

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for key, value in data.items():
        if count >= max_rows:
            break
        unique_key = key  # Unique identifier
        facility_json_str = json.dumps(value, ensure_ascii=False)
        extracted = extract_fields_from_json(facility_json_str, model)
        result = {
            "unique_key": unique_key,
            "source": input_file.split("_")[0],  # Derive source from filename
            "Name": extracted.get("Name", ""),
            "Provider": extracted.get("Provider", ""),
            "StreetAddress": extracted.get("StreetAddress", ""),
            "City": extracted.get("City", ""),
            "ZipCode": extracted.get("ZipCode", ""),
            "State": extracted.get("State", ""),
            "Country": extracted.get("Country", ""),
            "Whitespace": extracted.get("Whitespace", ""),
            "Area": extracted.get("Area", ""),
            "YearBuilt": extracted.get("YearBuilt", ""),
            "Power": extracted.get("Power", ""),
            "Scale": extracted.get("Scale", ""),
            "Certifications": extracted.get("Certifications", ""),
            "URL": extracted.get("URL", "") or value.get("Url", "")
        }
        progress.append(result)
        count += 1
        print(f"[{model}] Processed {unique_key}")
        sleep(0.5)  # Reduce API rate limit issues

    save_progress(output_file, progress)
    print(f"[{model}] Finished processing {input_file}. Total records: {count}")

def main():
    # Set the maximum rows for testing
    test_rows = 50
    
    # Define the models to test
    models = ["gpt-3.5-turbo", "gpt-4"]

    # Input files and output filenames for CSV
    datasets = {
        "datacentermap": "map_final.json",
        "datacenterhawk": "hawk_final.json",
        "datacenters": "centers_final.json"
    }

    for model in models:
        print(f"=== Testing with model: {model} ===")
        for dataset, input_file in datasets.items():
            output_file = f"{dataset}_extracted_{model}.csv"
            process_data(input_file, output_file, model, test_rows)

if __name__ == "__main__":
    main()