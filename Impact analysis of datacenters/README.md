# DSC672 Group 9 Project

## Project Overview
This project explores the relationship between weather patterns and data center power consumption/generation. By analyzing geographical, climate, and facility data from multiple sources, we investigate how environmental factors influence data center operations and efficiency.

## Repository Structure
- **data/**: Contains datasets used in the analysis
  - `power_imputed_dataset.csv`: Cleaned dataset with imputed power values
  - `weather_data_merged_dataset.csv`: Processed weather data
  - **area_power/**: Area and power data by source
  - **cleaned/**: Processed datasets ready for analysis
  - **power/**: Raw power consumption data

- **notebooks/**: Jupyter notebooks for data analysis
  - `Inital data preparation.ipynb`: Data cleaning and preparation
  - `Futher_refining_datasets.ipynb`: Additional data processing
  - `climatedata.ipynb`: Analysis of climate factors
  - `power_estimation.ipynb`: Power consumption models
  - `Final Analysis.ipynb`: Final analysis and visualization

- **scripts/**: Utility scripts
  - Web scraping: `Puppeteer_Scraper.js`, `Selenium_Scraper.py`, `simple_crawler.py`
  - LLM tools: `compareLLMs.py`, `hostLLm.py`, `openaiExt.py`
  - Data processing: `extractInfo.py`, `find.py`, `findYear.py`, `latlong.py`

- **reports/**: Documentation and findings
  - `Final Report.docx`: Comprehensive project report

## Setup and Installation
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. For JavaScript-based scrapers, install Node.js dependencies:
   ```bash
   npm install puppeteer cli-progress
   ```

## Data Collection
This project combines data from multiple sources:
- Data center information (location, size, power capacity) scraped from:
  - DatacenterHawk
  - Datacenters.com
  - DatacenterMap
- Weather data obtained through climate APIs
- Power consumption metrics

## Analysis Process
The analysis follows these steps:
1. Data collection and scraping using custom web scrapers
2. Initial data preparation and cleaning
3. Geospatial clustering of data centers
4. Weather data collection for each cluster
5. Integration of power and facility data
6. Statistical analysis of weather patterns vs. power metrics
7. Visualization and interpretation of results

## Key Features
- Geospatial clustering of data centers
- Microclimate analysis for data center locations
- Power consumption estimation models
- Interactive visualizations of findings
- LLM-assisted data extraction and processing

## Contributors
Om Prakash Gunja 
Raju Meesala
Rishab Manish Oswal