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
        # more country mappings...
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
