const puppeteer = require('puppeteer');
const fs = require('fs');

async function unlockAndFillForm(page) {
    try {
        const unlockButtonXPath = "//div[contains(text(), 'Unlock Full List of Facilities')]";
        const unlockButton = await page.$(`xpath=${unlockButtonXPath}`);
        if (unlockButton) {
            await page.click(`xpath=${unlockButtonXPath}`);
            console.log('Clicked the unlock button');

            // Wait for modal to open
            const modalXPath = "//*[@id='modal']/div/div";
            await page.waitForSelector(`xpath=${modalXPath}`, { visible: true });
            console.log('Modal opened');

            // Click button inside modal to fill form
            const formButtonXPath = "/html/body/div[1]/div/div[1]/main/div/section[2]/div/div[2]/section/div/div[4]/div/div/div[2]/div/span[2]";
            await page.waitForSelector(`xpath=${formButtonXPath}`, { visible: true });
            await page.click(`xpath=${formButtonXPath}`);
            console.log('Clicked button inside modal to fill form');

            // Wait for form to load
            const formXPath = "/html/body/div[1]/div/div[1]/main/div/section[2]/div/div[2]/section/div/div[4]/div/div";
            await page.waitForSelector(`xpath=${formXPath}`, { visible: true });
            console.log('Form loaded');

            // Fill form fields with random data using long XPath
            await page.type(`xpath=/html/body/div[1]/div/div[1]/main/div/section[2]/div/div[2]/section/div/div[4]/div/div/div[3]/form/div[1]/div[1]/input`, 'John');
            await page.type(`xpath=/html/body/div[1]/div/div[1]/main/div/section[2]/div/div[2]/section/div/div[4]/div/div/div[3]/form/div[1]/div[2]/input`, 'Doe');
            await page.type(`xpath=/html/body/div[1]/div/div[1]/main/div/section[2]/div/div[2]/section/div/div[4]/div/div/div[3]/form/div[2]/div[1]/input`, '1234567890');
            await page.type(`xpath=/html/body/div[1]/div/div[1]/main/div/section[2]/div/div[2]/section/div/div[4]/div/div/div[3]/form/div[2]/div[2]/input`, 'johndoe@gmail.com');
            console.log('Form filled successfully');

            // Click submit button
            const submitButtonXPath = "/html/body/div[1]/div/div[1]/main/div/section[2]/div/div[2]/section/div/div[4]/div/div/div[3]/form/div[2]/div[3]/div/span";
            await page.waitForSelector(`xpath=${submitButtonXPath}`, { visible: true });
            await page.click(`xpath=${submitButtonXPath}`);
            console.log('Clicked submit button');

            // Click final confirmation button to return to site
            const finalButtonXPath = "/html/body/div[1]/div/div[1]/main/div/section[2]/div/div[2]/section/div/div[4]/div/div/div[4]/div";
            await page.waitForSelector(`xpath=${finalButtonXPath}`, { visible: true });
            await page.click(`xpath=${finalButtonXPath}`);
            console.log('Clicked final confirmation button');
        }
    } catch (error) {
        console.log('Unlock button not found or already unlocked:', error);
    }
}

async function scrollAndScrape(page) {
    try {
        const repeatButtonXPath = "/html/body/div[1]/div/div[1]/main/div/section[2]/div/div[2]/section/div/div[5]/div/span";
        while (await page.$(`xpath=${repeatButtonXPath}`) !== null) {
            await page.evaluate(() => window.scrollBy(0, 1)); // Scroll down
            await new Promise(resolve => setTimeout(resolve, 3)); // Wait a bit before clicking
            await page.click(`xpath=${repeatButtonXPath}`);
            console.log('Clicked repeat button');
        }
        console.log('No more view more button');
    } catch (error) {
        // console.log('No more view more button');
    }

    // Scrape all container cards
    const facilityCards = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('ul:nth-of-type(1) li div a')).map(card => {
            return {
                text: card.innerText.trim(),
                url: card.href
            };
        });
    });

    return facilityCards;
}

async function processMarkets() {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    const data = JSON.parse(fs.readFileSync('facilities_progress.json', 'utf-8'));

    for (const marketKey in data.markets) {
        const market = data.markets[marketKey];
        if (!market.completed) {
            console.log(`Processing market: ${market.name}`);
            await page.goto(market.link, { waitUntil: 'networkidle2' });
            
            // Unlock and fill form if unlock button is found
            await unlockAndFillForm(page);
            
            const facilities = await scrollAndScrape(page);
            data.markets[marketKey].facilities = facilities;
            data.markets[marketKey].completed = true;
            fs.writeFileSync('facilities_progress.json', JSON.stringify(data, null, 2));
            console.log(`Completed: ${market.name}`);
        }
    }

    await browser.close();
}

(async () => {
    await processMarkets();
    console.log('All markets processed successfully');
})();
