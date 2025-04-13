const fs = require('fs');

function transformMarketData() {
    const data = JSON.parse(fs.readFileSync('facilities_progress.json', 'utf-8'));
    const transformedData = { markets: {} };

    for (const marketKey in data.markets) {
        const market = data.markets[marketKey];
        const trimmedMarketName = marketKey.split('\n')[0].trim();

        transformedData.markets[trimmedMarketName] = {
            name: trimmedMarketName,
            link: market.link,
            completed: market.completed,
            facilities: {}
        };

        if (Array.isArray(market.facilities)) {
            market.facilities.forEach((facility, index) => {
                const facilityLines = facility.text.split('\n').map(line => line.trim());
                const name = facilityLines[0] || 'Unknown';
                const address = facilityLines.slice(1, -1).join(', ') || 'Unknown';
                const description = facilityLines[facilityLines.length - 1] || 'Unknown';

                transformedData.markets[trimmedMarketName].facilities[`facility_${index + 1}`] = {
                    name: name,
                    address: address,
                    description: description,
                    url: facility.url || '',
                    table_info: {} // Placeholder for future structured data
                };
            });
        }
    }

    fs.writeFileSync('facilities_progress_transformed.json', JSON.stringify(transformedData, null, 2));
    console.log('Transformed JSON saved as facilities_progress_transformed.json');
}

transformMarketData();
