import requests
from bs4 import BeautifulSoup
import time
import csv
import random
from datetime import datetime

def scrape_car_data(page_number):
    # Prepare the URL for including the page_number
    url = f"https://www.cars.com/shopping/results/?list_price_max=&makes[]=&maximum_distance=30&models[]=&page={page_number}&stock_type=all&zip=63301"

    # Send a request to the website
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Request to {url} returned status code {response.status_code}")
        return []

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the relevant data points and extract them
    car_data = []
    for car_listing in soup.find_all('div', class_='vehicle-card-main js-gallery-click-card'):
        car_name = car_listing.find('h2', class_='title').text
        car_price = car_listing.find('span', class_='primary-price').text

        # Find the URL of the individual listing
        car_url = car_listing.find('a')['href']
        car_url = "https://www.cars.com" + car_url  # Complete the URL if it's relative

        # Send a request to the individual listing
        car_response = requests.get(car_url)
        car_soup = BeautifulSoup(car_response.content, 'html.parser')

        # Find the mileage and other specs
        car_specs = car_soup.find('dl', class_='fancy-description-list')
        specs_dict = {}
        for term, desc in zip(car_specs.find_all('dt'), car_specs.find_all('dd')):
            spec_name = term.text.strip()
            if spec_name in ['Exterior color', 'Interior color', 'Drivetrain', 'Fuel type', 'Transmission', 'Engine', 'VIN', 'Mileage']:
                specs_dict[spec_name] = desc.text.strip()

        # Add the scraping timestamp (could be useful for time series analysis)
        timestamp = datetime.now()

        car_data.append([car_name, car_price, specs_dict.get('Mileage'), specs_dict.get('Exterior color'), specs_dict.get('Interior color'), specs_dict.get('Drivetrain'), specs_dict.get('Fuel type'), specs_dict.get('Transmission'), specs_dict.get('Engine'), specs_dict.get('VIN'), timestamp])

        # Add a randomized delay between requests to avoid getting blocked
        time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds

    return car_data

#Scrape data from the first 30 pages.
all_car_data = []
for page_number in range(1, 31):
    car_data = scrape_car_data(page_number)
    all_car_data.extend(car_data)  # Add the data from this page to the total
    print(f"Page {page_number} car data: {car_data}")
    time.sleep(5)  # Wait for 5 seconds

print(f"Total car data: {all_car_data}")


#Write the data to a CSV file
with open('car_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Car Name", "Car Price", "Car Mileage", "Exterior Color", "Interior Color", "Drivetrain", "Fuel Type", "Transmission", "Engine", "VIN"])  # write the header
    writer.writerows(all_car_data)  # write the data