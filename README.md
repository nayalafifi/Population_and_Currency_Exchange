# Global Population and Currency Exchange Dataset

## Project Description

This project uses a web scraper to gather population data from [World Population Review](https://worldpopulationreview.com/countries) and an API (ExchangeRate-API) to collect real-time currency exchange rates. The purpose of the project is to create a dataset that provides comprehensive information about the population of various countries in 2024 and their respective exchange rates to USD. This dataset can be useful for data analysts, economists, and researchers interested in demographic and financial data comparisons.

The dataset includes:
- **2024 Population**: Population of each country in 2024.
- **2023 Population**: Population of each country in 2023.
- **Area**: Area of each country in square kilometers.
- **Density**: Population density per square kilometer.
- **Growth Rate**: The population growth rate from 2023 to 2024.
- **World Rank**: The world rank of the country based on population.
- **Currency Code**: The standard currency code for the country.
- **Exchange Rate to USD**: The exchange rate of the country's currency to USD, fetched from the ExchangeRate-API.

### Why this Website and API?
We chose the World Population Review because it provides up-to-date and reliable population statistics for all countries in a structured format. The ExchangeRate-API was chosen for its easy-to-use and real-time exchange rate data, which complements the population data well by allowing economic analysis.

### Value of the Dataset
This dataset provides a unique combination of demographic and economic data, allowing for deeper analysis into trends such as population growth, economic power through currency comparison, and geographic size. While population datasets are commonly available, datasets that combine real-time exchange rates and population statistics in one place are rare or often hidden behind paywalls.

By combining data from two sources, the dataset provides users with an integrated view of global populations and economic factors, making it useful for:
- Comparative analysis of population growth and economic power.
- Development of applications for economic or demographic forecasting.
- Educational tools for teaching international economics and geography.


Clone the repository using the following command:
```bash
git clone https://github.com/nayalafifi/Population_and_Currency_Exchange.git
