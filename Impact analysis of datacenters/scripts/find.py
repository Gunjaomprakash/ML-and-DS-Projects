from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Uncomment to run in headless mode

# Initialize the Chrome WebDriver with the new syntax
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

url = "https://www.datacenters.com/locations?query=USA"
driver.get(url)

time.sleep(10)
# Use XPath to locate elements
# elements = driver.find_elements(By.XPATH, "//div[contains(@class,'LocationTile__detailsContainer')]/div/div[3]")
# for element in elements:
#     print(element.text.strip())
driver.find_element(By.XPATH, "//input[@id='locations-search']").send_keys("United States")
time.sleep(5)
item = driver.find_element(By.XPATH, "(//div[contains(@class,'LocationsIndex__pagination')][1]/div/nav/button/div[contains(text(),'➞')])[2]").is_enabled()
while item:
    time.sleep(5)
    elements=driver.find_elements(By.XPATH, "//div[contains(@class,'LocationTile__details__')]") 
    providers= driver.find_elements(By.XPATH, "//div[contains(@class,'LocationTile__provider')]")
    locNames= driver.find_elements(By.XPATH, "//div[contains(@class,'LocationTile__name_')]")
    addresss= driver.find_elements(By.XPATH, "//div[contains(@class,'LocationTile__address_')]")
    
    for element,provider,locName,address in zip(elements,providers,locNames,addresss):
        
        pd.DataFrame({
            'Provider': [provider.text.strip()],
            'Location Name': [locName.text.strip()],
            'Address': [address.text.strip()]
        }).to_csv('datacenters.csv', mode='a', header = False ,index=False)
    
    driver.find_element(By.XPATH, "(//div[contains(@class,'LocationsIndex__pagination')][1]/div/nav/button/div[contains(text(),'➞')])[2]").click()
    if item == False:
        break
driver.quit()