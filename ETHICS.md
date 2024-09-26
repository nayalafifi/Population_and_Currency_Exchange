
# Ethical Considerations

## Data Privacy

This project respects the privacy policies of the websites and APIs used. I only used publicly available data from the World Population Review and ExchangeRate-API, which do not require user-specific permissions or any login credentials to access. The population data and exchange rates collected are publicly accessible and do not contain any sensitive or personally identifiable information.

## Website Scraping Ethics

Scraping is done responsibly by limiting the number of requests made to the website. We ensure that the scraping process does not overload the website's servers by adhering to good practices, such as:
- Respecting the website's `robots.txt` file (even though World Population Review allows scraping).
- Limiting the request rate to avoid server overload.

Additionally, the data collected is not modified or misrepresented. Users are made aware of the source of the data, and the dataset reflects accurate population and currency information.

## API Usage and Fair Access

The project uses the free tier of ExchangeRate-API, which comes with rate-limiting and usage quotas. I've ensured that the API requests stay within the bounds of acceptable use as per the API's documentation. 

## Copyright and Attribution

- **World Population Review**: The data scraped from this website is publicly available, and i've give full credit to the source in our documentation.
- **ExchangeRate-API**: Similarly, the ExchangeRate-API is a free service.


