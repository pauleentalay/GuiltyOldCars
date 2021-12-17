import requests
from scrape import EbayResults, CarInfo
from sqlalchemy import func
from schema import Session, engine, Link, Car, create_database, drop_database
import time
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

local_session = Session(bind=engine)


def main():
    drop_database()
    create_database()

    ebay_pages = get_results_page(52)
    car_links = get_Ebay_links(ebay_pages)
    new_car_links = flatten_list(car_links)
    add_EbayResults(new_car_links)

    local_session.commit()

    for link in new_car_links:
        try:
            car = get_CarInfo(link)
            add_CarInfo(car)
        except:
            pass

    local_session.commit()

    carbon_data = get_carbon_data('de_car_data_brand.csv')
    update_emissions_CarInfo(carbon_data)

    car_emit = get_total_emissions_by_brand()
    print(car_emit)
    plot_emission(car_emit)


def get_url(url):
    response = requests.get(url, headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0"})
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e}')
    return response


def get_results_page(num_page=1):
    pages = []
    for page in range(1, num_page+1):
        response = get_url(f'https://www.ebay.de/sch/9801/i.html?_from=R40&_nkw=auto&_pgn={page}')
        pages.append(response)
        time.sleep(2)
    return pages


def get_Ebay_links(link_pages):
    car_links = []
    for link in link_pages:
        many_car_links = EbayResults(link)
        car_links.append(many_car_links)
    return car_links


def add_EbayResults(car_links):
    for link in car_links:
        new_link = Link(link=link)
        local_session.add(new_link)


def flatten_list(lst):
    new_list = []
    for item_lst in lst:
        item_links = item_lst.get_car_links()
        new_list.extend(item_links)
    return new_list


def get_CarInfo(url):
    link = get_url(url)
    car = CarInfo(link)
    return car


def add_CarInfo(car):
    car = Car(brand=car.Marke,
              model=car.Modell,
              fuel=car.Kraftstoff,
              price=car.Price,
              mileage=car.Kilometerstand)
    if car.brand and car.price and car.mileage is not None:
        local_session.add(car)
    time.sleep(2)


def get_carbon_data(filename):
    carbon_data = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            carbon_data[row[0].lower()] = row[1]
    print(carbon_data)
    return carbon_data


def update_emissions_CarInfo(carbon_data):
    for key, value in carbon_data.items():
        try:
            emission_add = local_session.query(Car).filter(Car.brand == key)
            emission_add.update({'emission': value})
        except:
            pass
    local_session.commit()


def get_total_emissions_by_brand():
    car_table = local_session.query(Car.brand,
                                    (func.avg(Car.emission) * func.sum(Car.mileage) / 1000000),
                                    func.count(Car.brand),
                                    func.sum(Car.price) / (func.sum(Car.emission) * func.sum(Car.mileage)/1000000)).\
                                    group_by(Car.brand).all()
    df = pd.DataFrame(car_table, columns=('brands', 'emissions', 'counts', 'price_emission'))
    df = df.dropna(subset=['emissions'])
    return df


def plot_emission(data_frame):
    data_frame = data_frame.sort_values(by=['emissions'])
    data_frame = data_frame.query('counts > 5')

    brands_1 = data_frame['brands']
    emissions = data_frame['emissions']
    counts = data_frame['counts']
    prices = data_frame['price_emission']
    y_pos = np.arange(data_frame['brands'].size)

    fig, ax = plt.subplots(figsize=(12, 8))

    emi = [f'{round(emission, 2)} t CO\N{SUBSCRIPT TWO}' for emission in emissions]
    price_per_c = [f'{round(price, 2)} EUR /t CO\N{SUBSCRIPT TWO}\n (n={count})' for price, count in zip(prices, counts)]

    h_bars = ax.barh(y_pos, width=emissions, align='edge', color=('whitesmoke', 'wheat', 'tan', 'peru', 'sienna',
                                                                  'silver', 'gray'))
    ax.invert_yaxis()
    ax.set_yticks(y_pos, labels=brands_1)
    ax.set_xlabel('Total Emission, t')
    ax.set_ylabel('Car brands')
    ax.set_title('Total Amount of CO\N{SUBSCRIPT TWO}\n emitted by Car Brands currently in ebay.de (n>5)')
    ax.bar_label(h_bars, labels=price_per_c, padding=5)
    ax.bar_label(h_bars, labels=emi, label_type='center')

    plt.show()


if __name__ == '__main__':
    main()
