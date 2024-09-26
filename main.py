import requests 
from bs4 import BeautifulSoup #for parsing html data
import pandas as pd

API_KEY = '45d5542a1b72dad81f5b7567'
def get_exchange_rates():
    base_url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"#base url for api request
    try:
        response = requests.get(base_url)#send a get request to the api
        response.raise_for_status()
        
        return response.json()['conversion_rates']#return the conversion rates as a dictionary
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")  #print the error if any
        return None

def scrape_population_data():#scraping population data
    url = "https://worldpopulationreview.com/countries"
    try:
        response = requests.get(url)#send a get request to the url
        response.raise_for_status()#raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')#parse html response
        table = soup.find('table')#find the table in the html
        country_data = []#initialize an empty list to store data

        if table:
            rows = table.find_all('tr')[1:]#find all table rows and skip the header row
            for row in rows:
                cols = row.find_all('td')#find all columns in the row
                if len(cols) >= 7:
                    country_data.append({  #append a dictionary of country data
                        'Country': cols[0].get_text(strip=True),
                        '2024 Population': cols[1].get_text(strip=True),
                        '2023 Population': cols[2].get_text(strip=True),
                        'Area': cols[3].get_text(strip=True), 
                        'Density': cols[4].get_text(strip=True),
                        'Growth Rate': cols[5].get_text(strip=True),
                        'World Rank': cols[6].get_text(strip=True)
                    })
        return country_data #return the list of country data
    
    except requests.exceptions.RequestException as e:
        print(f"Error scraping population data: {e}")#print the error if any
        return []#return an empty list in case of failure

def get_currency_code(country_name, currency_codes):
    country_to_currency = {  #a dict to map country names to their currency codes
        "India": "INR", "China": "CNY", "United States": "USD", "Indonesia": "IDR",
        "Pakistan": "PKR", "Nigeria": "NGN", "Brazil": "BRL", "Bangladesh": "BDT",
        "Russia": "RUB", "Ethiopia": "ETB", "Mexico": "MXN", "Japan": "JPY",
        "Egypt": "EGP", "Philippines": "PHP", "DR Congo": "CDF", "Vietnam": "VND",
        "Iran": "IRR", "Turkey": "TRY", "Germany": "EUR", "Thailand": "THB",
        "United Kingdom": "GBP", "France": "EUR", "Italy": "EUR", "South Africa": "ZAR",
        "Tanzania": "TZS", "Myanmar": "MMK", "Kenya": "KES", "South Korea": "KRW",
        "Colombia": "COP", "Spain": "EUR", "Uganda": "UGX", "Argentina": "ARS",
        "Algeria": "DZD", "Sudan": "SDG", "Ukraine": "UAH", "Iraq": "IQD",
        "Afghanistan": "AFN", "Poland": "PLN", "Canada": "CAD", "Morocco": "MAD",
        "Saudi Arabia": "SAR", "Uzbekistan": "UZS", "Peru": "PEN", "Angola": "AOA",
        "Malaysia": "MYR", "Mozambique": "MZN", "Ghana": "GHS", "Yemen": "YER",
        "Nepal": "NPR", "Venezuela": "VES", "Madagascar": "MGA", "Cameroon": "XAF",
        "Côte d'Ivoire": "XOF", "North Korea": "KPW", "Australia": "AUD", "Niger": "XOF",
        "Taiwan": "TWD", "Sri Lanka": "LKR", "Burkina Faso": "XOF", "Mali": "XOF",
        "Romania": "RON", "Malawi": "MWK", "Chile": "CLP", "Kazakhstan": "KZT",
        "Zambia": "ZMW", "Guatemala": "GTQ", "Ecuador": "USD", "Syria": "SYP",
        "Netherlands": "EUR", "Senegal": "XOF", "Cambodia": "KHR", "Chad": "XAF",
        "Somalia": "SOS", "Zimbabwe": "ZWL", "Guinea": "GNF", "Rwanda": "RWF",
        "Benin": "XOF", "Burundi": "BIF", "Tunisia": "TND", "Bolivia": "BOB",
        "Belgium": "EUR", "Haiti": "HTG", "Cuba": "CUP", "South Sudan": "SSP",
        "Dominican Republic": "DOP", "Czech Republic": "CZK", "Greece": "EUR",
        "Jordan": "JOD", "Portugal": "EUR", "Azerbaijan": "AZN", "Sweden": "SEK",
        "Honduras": "HNL", "United Arab Emirates": "AED", "Hungary": "HUF",
        "Tajikistan": "TJS", "Belarus": "BYN", "Austria": "EUR", "Papua New Guinea": "PGK",
        "Serbia": "RSD", "Israel": "ILS", "Switzerland": "CHF", "Togo": "XOF",
        "Sierra Leone": "SLL", "Hong Kong": "HKD", "Laos": "LAK", "Paraguay": "PYG",
        "Bulgaria": "BGN", "Libya": "LYD", "Lebanon": "LBP", "Nicaragua": "NIO",
        "Kyrgyzstan": "KGS", "El Salvador": "USD", "Turkmenistan": "TMT",
        "Singapore": "SGD", "Denmark": "DKK", "Finland": "EUR", "Congo": "XAF",
        "Slovakia": "EUR", "Norway": "NOK", "Oman": "OMR", "State of Palestine": "ILS",
        "Costa Rica": "CRC", "Liberia": "LRD", "Ireland": "EUR", "Central African Republic": "XAF",
        "New Zealand": "NZD", "Mauritania": "MRU", "Panama": "PAB", "Kuwait": "KWD",
        "Croatia": "HRK", "Moldova": "MDL", "Georgia": "GEL", "Eritrea": "ERN",
        "Uruguay": "UYU", "Bosnia and Herzegovina": "BAM", "Mongolia": "MNT",
        "Armenia": "AMD", "Jamaica": "JMD", "Qatar": "QAR", "Albania": "ALL",
        "Puerto Rico": "USD", "Lithuania": "EUR", "Namibia": "NAD", "Gambia": "GMD",
        "Botswana": "BWP", "Gabon": "XAF", "Lesotho": "LSL", "North Macedonia": "MKD",
        "Slovenia": "EUR", "Guinea-Bissau": "XOF", "Latvia": "EUR", "Bahrain": "BHD",
        "Equatorial Guinea": "XAF", "Trinidad and Tobago": "TTD", "Estonia": "EUR",
        "Timor-Leste": "USD", "Mauritius": "MUR", "Cyprus": "EUR", "Eswatini": "SZL",
        "Djibouti": "DJF", "Fiji": "FJD", "Réunion": "EUR", "Comoros": "KMF",
        "Guyana": "GYD", "Bhutan": "BTN", "Solomon Islands": "SBD", "Macau": "MOP",
        "Luxembourg": "EUR", "Montenegro": "EUR", "Western Sahara": "MAD",
        "Suriname": "SRD", "Cabo Verde": "CVE", "Maldives": "MVR", "Malta": "EUR",
        "Brunei": "BND", "Guadeloupe": "EUR", "Belize": "BZD", "Bahamas": "BSD",
        "Martinique": "EUR", "Iceland": "ISK", "Vanuatu": "VUV", "French Guiana": "EUR",
        "Barbados": "BBD", "New Caledonia": "XPF", "French Polynesia": "XPF",
        "Mayotte": "EUR", "Sao Tome & Principe": "STN", "Samoa": "WST", "Saint Lucia": "XCD",
        "Channel Islands": "GBP", "Guam": "USD", "Curaçao": "ANG", "Kiribati": "AUD",
        "Micronesia": "USD", "Grenada": "XCD", "St. Vincent & Grenadines": "XCD",
        "Aruba": "AWG", "Tonga": "TOP", "U.S. Virgin Islands": "USD", "Seychelles": "SCR",
        "Antigua and Barbuda": "XCD", "Isle of Man": "GBP", "Andorra": "EUR",
        "Dominica": "XCD", "Cayman Islands": "KYD", "Bermuda": "BMD", "Marshall Islands": "USD",
        "Northern Mariana Islands": "USD", "Greenland": "DKK", "American Samoa": "USD",
        "Saint Kitts & Nevis": "XCD", "Faeroe Islands": "DKK", "Sint Maarten": "ANG",
        "Monaco": "EUR", "Turks and Caicos": "USD", "Saint Martin": "EUR",
        "Liechtenstein": "CHF", "San Marino": "EUR", "Gibraltar": "GIP", "British Virgin Islands": "USD",
        "Caribbean Netherlands": "USD", "Palau": "USD", "Cook Islands": "NZD", "Anguilla": "XCD",
        "Tuvalu": "AUD", "Wallis & Futuna": "XPF", "Nauru": "AUD", "Saint Barthelemy": "EUR",
        "Saint Helena": "SHP", "Saint Pierre & Miquelon": "EUR", "Montserrat": "XCD",
        "Falkland Islands": "FKP", "Niue": "NZD", "Tokelau": "NZD", "Vatican City": "EUR"
    }
    
    if country_name in country_to_currency:#check if the country is in the dictionary
        code = country_to_currency[country_name]
        if code in currency_codes:
            return code  # return the currency code
    return None #return none if no match found

def create_dataset():
    population_data = scrape_population_data() #scrape population data
    exchange_rates = get_exchange_rates() #get exchange rates from api
    
    if exchange_rates:
        currency_codes = exchange_rates.keys()#get the available currency codes
        for country in population_data:
            currency_code = get_currency_code(country['Country'], currency_codes) #get the currency code for each country
            if currency_code:
                country['Currency Code'] = currency_code
                country['Exchange Rate to USD'] = exchange_rates[currency_code]
            else:
                country['Currency Code'] = 'N/A'  #assign NA if no currency code is found
                country['Exchange Rate to USD'] = 'N/A'  # assign NA if no exchange rate is found
    else:
        for country in population_data: 
            country['Currency Code'] = 'N/A' 
            country['Exchange Rate to USD'] = 'N/A' 

    df = pd.DataFrame(population_data)#create a pandas dataframe from the country data
    return df#return the dataframe

def save_dataset(df):
    filename = f'global_population_currency.csv'
    df.to_csv(filename, index=False)
    print(f"Dataset saved as {filename}")

def population_range_filter(df):
    while True:#loop until valid input is provided
        try:
            min_pop = int(input("Enter minimum population: "))#get minimum population from user
            max_pop = int(input("Enter maximum population: "))#get maximum population from user
            if min_pop > max_pop:
                print("Minimum population should be less than maximum population. Please try again.")  # error message
                continue
            break
        except ValueError:  # handle invalid input
            print("Please enter valid integer values for population.") #error message

    df['2024 Population'] = df['2024 Population'].str.replace(',', '').astype(int)#convert population to integer after removing commas
    filtered_df = df[(df['2024 Population'] >= min_pop) & (df['2024 Population'] <= max_pop)]#filter the dataframe by the population range
    
    if filtered_df.empty:#check if the filtered dataframe is empty
        print("No countries found in the specified population range.") 
    else:
        print(filtered_df[['Country', '2024 Population', 'Growth Rate', 'Currency Code', 'Exchange Rate to USD']])  # print the filtered results

    return filtered_df  # return the filtered dataframe

if __name__ == "__main__":
    dataset = create_dataset()#create the dataset
    save_dataset(dataset)#save the dataset to a csv file
    
    print("\nPopulation Range Filter")  #introduce the population range filter
    filtered_dataset = population_range_filter(dataset)#filter the dataset by population range
    
    save_dataset(filtered_dataset)#save the filtered dataset
