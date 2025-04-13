import json
from bs4 import BeautifulSoup

# Load the JSON file
with open("addresses_with2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Function to extract plain text from HTML
def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=" ", strip=True)

# Iterate over states in the JSON file and update HTML keys with plain text
for state, state_data in data.items():
    details = state_data.get("details", [])
    for detail in details:
        addresses = detail.get("addresses", [])
        for address in addresses:
            if "overviewHTML" in address:
                address["overviewHTML"] = extract_text_from_html(address["overviewHTML"])
            if "specsHtml" in address:
                address["specsHtml"] = extract_text_from_html(address["specsHtml"])

# Save the updated JSON into a new file
with open("addresses_extracted.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated JSON with extracted text saved to addresses_extracted.json.")
