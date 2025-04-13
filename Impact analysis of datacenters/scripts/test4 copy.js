const puppeteer = require('puppeteer');
const fs = require('fs');
const cliProgress = require('cli-progress');

async function unlockIfRequired(page) {
    try {
        const unlockButtonXPath = "//div[contains(text(), 'Unlock Full List of Facilities')]";
        const modalXPath = "/html/body/div[1]/div/div[1]/main/div/div[3]/div/div";
        const continueWithEmailXPath = "//span[contains(text(), 'Continue with Email')]";
        
        const unlockButton = await page.$(`xpath=${unlockButtonXPath}`);
        const modal = await page.$(`xpath=${modalXPath}`);
        
        if (unlockButton) {
            await page.evaluate((selector) => {
                const element = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (element) {
                    element.scrollIntoView();
                    element.click();
                }
            }, unlockButtonXPath);
        }
        
        if (modal) {
            const isModalVisible = await page.evaluate((selector) => {
                const element = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                return element && window.getComputedStyle(element).display !== 'none' && element.offsetParent !== null;
            }, modalXPath);

            if (isModalVisible) {
                await page.waitForSelector(`xpath=${continueWithEmailXPath}`, { visible: true });
                await page.click(`xpath=${continueWithEmailXPath}`);

                // Wait for the form to load
                const formXPath = "/html/body/div[1]/div/div[1]/main/div/div[3]/div/div";
                await page.waitForSelector(`xpath=${formXPath}`, { visible: true });

                // Fill form fields with random data
                await page.type(`xpath=/html/body/div[1]/div/div[1]/main/div/div[3]/div/div/div[2]/form/div[1]/div[1]/input`, 'John');
                await page.type(`xpath=/html/body/div[1]/div/div[1]/main/div/div[3]/div/div/div[2]/form/div[1]/div[2]/input`, 'Doe');
                await page.type(`xpath=/html/body/div[1]/div/div[1]/main/div/div[3]/div/div/div[2]/form/div[2]/div[1]/input`, '1234567890');
                await page.type(`xpath=/html/body/div[1]/div/div[1]/main/div/div[3]/div/div/div[2]/form/div[2]/div[2]/input`, 'johndoe@gmail.com');

                // Click get access button after form is filled
                const getAccessButtonXPath = "/html/body/div[1]/div/div[1]/main/div/div[3]/div/div/div[2]/form/div[2]/div[3]/div/span";
                await page.waitForSelector(`xpath=${getAccessButtonXPath}`, { visible: true });
                await page.click(`xpath=${getAccessButtonXPath}`);

                // Click final confirmation button to return to site
                // const finalButtonXPath = "/html/body/div[1]/div/div[1]/main/div/div[3]/div/div/div[4]/div";
                // await page.waitForSelector(`xpath=${finalButtonXPath}`, { visible: true });
                // await page.click(`xpath=${finalButtonXPath}`);
            }
        }
    } catch (error) {
        //console.log('No unlock required:', error);
    }
}

async function scrapeFacilityData(page, url) {
    await page.goto(url, { waitUntil: 'networkidle2' });
    await unlockIfRequired(page);

    const facilityData = {};


    try {
        await page.waitForSelector(`xpath=/html/body/div[1]/div/div[1]/main/div/div[1]/div[2]/section[1]/div[2]/div[1]`, { visible: true, timeout: 50 });
        facilityData.name = await page.evaluate(() => document.evaluate("/html/body/div[1]/div/div[1]/main/div/div[1]/div[2]/section[1]/div[2]/div[1]", document, null, XPathResult.STRING_TYPE, null).stringValue.trim());
    } catch (error) {
        facilityData.name = 'Unknown';
    }

    try {
        await page.waitForSelector(`xpath=/html/body/div[1]/div/div[1]/main/div/div[1]/div[2]/section[1]/div[2]/div[2]/div[1]/div`, { visible: true, timeout: 50 });
        facilityData.address = await page.evaluate(() => document.evaluate("/html/body/div[1]/div/div[1]/main/div/div[1]/div[2]/section[1]/div[2]/div[2]/div[1]/div", document, null, XPathResult.STRING_TYPE, null).stringValue.trim());
    } catch (error) {
        facilityData.address = 'Unknown';
    }

    try {
        await page.waitForSelector(`xpath=/html/body/div[1]/div/div[1]/main/div/div[1]/div[2]/section[1]/div[2]/div[3]`, { visible: true, timeout: 50 });
        facilityData.description = await page.evaluate(() => document.evaluate("/html/body/div[1]/div/div[1]/main/div/div[1]/div[2]/section[1]/div[2]/div[3]", document, null, XPathResult.STRING_TYPE, null).stringValue.trim());
    } catch (error) {
        facilityData.description = 'Unknown';
        console.error("Error getting description:", error);
    }

    // Extract table info using XPath for grid layout
    try {
        await page.evaluate(() => window.scrollBy(0, 10));
        await new Promise(resolve => setTimeout(resolve, 3)); // Wait a bit before clicking

        facilityData.tableInfo = await page.evaluate(() => {
            const tableData = {};
            const rows = document.querySelectorAll("div.grid.grid-cols-2.w-full.items-center.py-6.border-b");
            
            rows.forEach(row => {
                const keyElement = row.querySelector("div.font-medium");
                const valueElement = row.querySelector("div.text-sm.text-right");
                
                if (keyElement && valueElement) {
                    tableData[keyElement.innerText.trim()] = valueElement.innerText.trim();
                }
            });
            return tableData;
        });
    } catch (error) {
        facilityData.tableInfo = {};
        console.error("Error getting table info:", error);
    }
    // console.log('Facility Data:', facilityData);
    return facilityData;
}


async function processFacilities() {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    const data = JSON.parse(fs.readFileSync('facilities_progress_transformed.json', 'utf-8'));

    const marketKeys = Object.keys(data.markets);
    let totalFacilities = 0;
    for (const marketKey of marketKeys) {
        totalFacilities += Object.keys(data.markets[marketKey].facilities).length;
    }

    const progressBar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    progressBar.start(totalFacilities, 0);

    let completedFacilities = 0;

    for (const marketKey of marketKeys) {
        const market = data.markets[marketKey];
        const facilityKeys = Object.keys(market.facilities);
        for (const facilityKey of facilityKeys) {
            const facility = market.facilities[facilityKey];
            const scrapedData = await scrapeFacilityData(page, facility.url);
            data.markets[marketKey].facilities[facilityKey] = { ...facility, ...scrapedData };

            completedFacilities++;
            progressBar.update(completedFacilities);
        }
    }

    progressBar.stop();

    fs.writeFileSync('facilities_progress_final.json', JSON.stringify(data, null, 2));

    await browser.close();
}

(async () => {
    await processFacilities();
})();
