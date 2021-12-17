import requests
from bs4 import BeautifulSoup


class EbayResults:  # one results page, one object

    def __init__(self, link_response):
        self.__link = link_response
        self.__soup = BeautifulSoup(self.__link.text, 'html.parser')
        self.__set_car_links()

    def __set_car_links(self):
        results = self.__soup.find_all('div', {'class': 's-item__wrapper clearfix'})

        try:
            del results[0]              # removes redundant general item in list
        except:
            pass

        self.__car_links = [result.find('a', {'class': 's-item__link'})['href'] for result in results]
        return self.__car_links

    def get_car_links(self):
        return self.__car_links


class CarInfo:
    def __init__(self, link_response):
        self.__link = link_response
        self.__soup = BeautifulSoup(self.__link.text, 'html.parser')
        self.__car_info = self.__set_car_info()
        self.set_current_price()
        self.__fix_kilometerstand()

    def __set_car_info(self):
        descriptions = []
        values = []
        results = self.__soup.find_all('div', {'class': 'ux-layout-section__row'})
        for item in results:
            description = item.find_all('div', {'class': 'ux-labels-values__labels'})
            description = [i.text.replace(':', '').strip() for i in description]
            descriptions.extend(description)
            value = item.find_all('div', {'class': 'ux-labels-values__values'})
            value = [i.text.strip().lower() for i in value]
            values.extend(value)
            self.__car_info = dict(zip(descriptions, values))
        return self.__car_info

    def set_current_price(self):  # not private so can  be updated
        price = float(self.__soup.find('span', {'class': 'notranslate'})
                      .text.replace('EUR ', '').replace('.', '').replace(',', '.'))
        self.__car_info['Price'] = price

    def __fix_kilometerstand(self):
        try:
            reading = float(self.__car_info['Kilometerstand']
                            .replace('TKm', '').replace('.', '').replace(',', '.').strip())

        except:
            self.Kilometerstand = None

        else:
            self.Kilometerstand = reading

        finally:
            return self.Kilometerstand

    def get_car_info(self):
        return self.__car_info

    def __getattr__(self, description):
        return self.__car_info.get(description, None)


