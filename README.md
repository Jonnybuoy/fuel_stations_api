# Fuel Route Optimization API

The Fuel Route Optimization API project provides an API for calculating optimal fuel stops along a route, factoring in the vehicle range, fuel efficiency, and fuel station prices. The application is built with Django and Django REST Framework.

## Features

- Route Calculation: Determine the optimal route from a start to an end location.
- Fuel Stop Optimization: Identify the best fuel stations along the route based on price and proximity.
- Google Maps Integration: Fetch route details using the Google Maps Directions API.
- Cost Estimation: Calculate total fuel costs for the trip.

## Prerequisites
- Python 3.8 or higher
- Django 3.2.23 or higher
- Django Rest Framework 3.12 or higher
- Geopy for geospatial calculations
- Google Maps API key

## Installation
1. Clone the repository using the following link:
```bash
$ git clone ''
```

2. Navigate to the project directory:
```bash
$ cd fuel_route_api
```

3. Create an env file(.env.dev) and populate it with the following variables:
```text
DB_NAME=fuel_prices_db
DB_USER=route_user
DB_PASSWORD='kapa$$word!'
DB_HOST='127.0.0.1'
DB_PORT=5432
GOOGLE_MAPS_API_KEY="YOUR_GOOGLE_MAPS_API_KEY"
GOOGLE_MAPS_API_URL="https://maps.googleapis.com/maps/api"
```

4. Set up and activate a virtual environment:
```bash
$ python3 -m venv name-of-your-virtualenv
$ source name-of-your-virtualenv/bin/activate
```

5. Install the project requirements.
```bash
(name-of-your-virtualenv)$ pip3 install -r requirements.txt
```

## Setting up the database
On a separate terminal, log in to PostgreSQL as a superuser:

```bash
$ sudo su postgres
$ psql
```
Create a database with the name of your choice and a user and password of your choice as follows:

```bash
postgres=# CREATE DATABASE <your_database_name>;
CREATE DATABASE
postgres=# CREATE USER <your_database_user> WITH password <'your_password'>;
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE <your_database_name> TO <your_database_user>;
GRANT
```
The database name and user/password should be similar to the ones you put in the .env file

## Run the migrations
```bash
(name-of-your-virtualenv)$ python manage.py migrate
```

## Populate the database
Run the management command that reads the csv data and populates the database with the data:

```bash
(name-of-your-virtualenv)$ python manage.py process_fuel_data --file <path_to_the_csv_file>
```
If the command is successful, the following message should be displayed:
```Fuel price data successfully stored to database.```

## Run the project:

```bash
(name-of-your-virtualenv)$ ./manage.py runserver # the information below will be displayed if everything is okay
Performing system checks...

System check identified no issues (0 silenced).
January 10, 2025 - 18:55:56
Django version 3.0, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C
```

## Endpoints
1. Get the route and fuel stations between start and end points:
**URL**: /api/route/
**Method**: GET
**Query Parameters**:
- **start**: Starting location (e.g., "New York, NY").
- **end**: Ending location (e.g., "Los Angeles, CA").

**Response**
```json
{
    "map_url": "https://maps.googleapis.com/maps/api/staticmap?size=800x600&path=color:0x0000ff|weight:5|40.7126819,-74.006577|40.7130581,-74.0072272|40.7152204,-74.0132218|40.7422013,-74.0087341|40.7522421,-74.0008627|40.7522049,-73.99937609999999|40.7545404,-73.9979209|40.7631296,-74.0094858|40.7766538,-74.0427174|40.833793,-74.14692409999999|40.87053239999999,-74.1884079|40.8953865,-74.2481273|40.89779679999999,-74.2514054|40.9816374,-75.1372741|41.1108836,-80.8290634|41.5917597,-87.2285836|41.5847613,-87.2351521|41.5675447,-87.3306248|41.5782434,-87.6705562|41.5798822,-87.6764425|41.4403399,-90.3215232|41.5975348,-90.6757358|41.5968753,-93.77722829999999|41.0358373,-102.1373714|41.0249913,-102.1586647|39.7883368,-105.0682129|39.7158153,-105.3887555|38.5796738,-112.5991174|34.2354499,-117.4239505|34.1424968,-117.4888521|34.1203112,-117.8373983|34.1329381,-117.9518612|34.1328453,-117.9587569|34.0364539,-118.0242049|34.0285341,-118.2092341|34.0539306,-118.2347763|34.0540954,-118.2360698|34.054502,-118.2377974|34.0564958,-118.2411657|34.0549145,-118.2426725&markers=label:1|34.3154473,-81.5817733|label:2|36.730719,-94.9167226|label:3|33.1809151,-101.496048|label:4|37.7136495,-115.8775166&key=AIzaSyBlXUKYfZeSw_egHMkbTad65exvjOrqgME",
    "fuel_stops": [
        {
            "name": "MOUNTAIN ENERGY #126",
            "address": "I-26, E 13",
            "latitude": 34.3154473,
            "longitude": -81.5817733,
            "retail_price": 2.84566666
        },
        {
            "name": "7-ELEVEN #218",
            "address": "I-44, E 4",
            "latitude": 36.730719,
            "longitude": -94.9167226,
            "retail_price": 2.68733333
        },
        {
            "name": "RACEWAY #6973",
            "address": "US-380 & SR-114/SR-101",
            "latitude": 33.1809151,
            "longitude": -101.496048,
            "retail_price": 2.78233333
        },
        {
            "name": "DK",
            "address": "SR-375",
            "latitude": 37.7136495,
            "longitude": -115.8775166,
            "retail_price": 2.699
        }
    ],
    "total_fuel_cost": 550.716666
}
```

## Future Enhancements
- Add user authentication and profiles.
- Advanced filtering options for fuel stations.
- Improved map visualizations with multiple routes.

## Contributions
Contributions are welcome! Please fork the repository and create a pull request.
