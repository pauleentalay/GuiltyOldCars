# GuiltyOldCars
On-going project. The project started and was presented for ReDI - Python Intermediate Course, Autumn 2021.
The program scrapes car data from ebay.de and stores in SQL. It extracts information and summarizes carbon dioxide emission from an available car registration file (see source below). The total mileage and rate of carbon dioxide emission for each brand is used to compute the total amount of carbon dioxide emitted of each brand.

Files:
#### scrape:
* Scrapes ebay.de for carlinks in pagea of Autorad & Motorrad: Fahrzeuge -> Automobile 
#### schema:
* Creates a database cars_scrape.db containing the links to individual pages, and the car info obtained
#### main:
1. drops and creates database;
2. get links, adds to database; Change number of pages here if you would want to run the program quickly.
3. gets car info, adds to database, 
4. gets emission data, matches according to brand name, updates database with this emissions data
5. queries by brand: emissions = emission * mileage, count per brand, total cost per total emitted tonne CO2
6. plots horizontal bar graph, arranged accoring to amount of emission; plots only where brand count > 5
#### carbondata:
* see below for source of emissions data
* note: run fix_header and group_by_brand_model if using new data set from said source

* use 'de_car_data_grouped.csv' for extracted columns for car brands, models, and emission in g/Km (specific CO2 emissions in g/Km (NEDC))
* use  'de_car_data_brand.csv' in main.py for fixed and cleaned contianing brands and emission only (manually removed 'vw' in 'volkswagen vw')

#### Project photo so you don't need to run it as it may take sometime:
![projectimage](https://user-images.githubusercontent.com/79509008/148593449-d0d988ce-37a0-4db2-8f1c-66e350ee14fa.png)

#### Carbon dioxide data is from:
[EEA Data: Monitoring of CO2 emissions from passenger cars – Regulation (EU) 2019/631 provided by European Environment Agency (EEA)](http://co2cars.apps.eea.europa.eu/?source=%7B%22track_total_hits%22%3Atrue%2C%22query%22%3A%7B%22bool%22%3A%7B%22must%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22constant_score%22%3A%7B%22filter%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22bool%22%3A%7B%22should%22%3A%5B%7B%22term%22%3A%7B%22year%22%3A2019%7D%7D%5D%7D%7D%2C%7B%22bool%22%3A%7B%22should%22%3A%5B%7B%22term%22%3A%7B%22scStatus%22%3A%22Provisional%22%7D%7D%5D%7D%7D%5D%7D%7D%7D%7D%5D%7D%7D%2C%22filter%22%3A%7B%22bool%22%3A%7B%22should%22%3A%5B%7B%22term%22%3A%7B%22MS%22%3A%22MT%22%7D%7D%2C%7B%22term%22%3A%7B%22MS%22%3A%22DE%22%7D%7D%5D%7D%7D%7D%7D%2C%22display_type%22%3A%22tabular%22%7D)


