import requests
from bs4 import BeautifulSoup
import time

def scrape_car_data(url):
    #Send a request to the website
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Request to {url} returned status code {response.status_code}")
        return []

    #Make sure the request was successful
    assert response.status_code == 200


    #Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    #Find the relevant data points and extract them
    
    car_data = []
    for i, car_listing in enumerate(soup.find_all('div', class_='vehicle-card-main js-gallery-click-card')):
        car_name = car_listing.find('h2', class_='title').text
        car_price = car_listing.find('span', class_='primary-price').text
        car_data.append([car_name, car_price])

        if i >=4: #Stop after collecting 5 itmes
            break

    return car_data

#Test the function
url = "https://www.cars.com/shopping/results/?stock_type=all&makes%5B%5D=&models%5B%5D=&list_price_max=&maximum_distance=30&zip=63301"
car_data = scrape_car_data(url)
print(car_data)