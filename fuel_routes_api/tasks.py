import logging
import pandas as pd

from .models import FuelStation
from .utils import geocode_address

LOGGER = logging.getLogger(__name__)


def load_fuel_data(file_path):
    """Load fuel station data from a CSV file, clean it with pandas, and save to the database."""
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower()

    # clean upm the data
    df['address'] = df['address'].str.strip()
    df['address'] = df['address'].str.replace(r'\bEXIT\b', 'E', regex=True) # Replace 'EXIT' with 'E' in the address column

    df['truckstop name'] = df['truckstop name'].str.strip()
    df['retail price'] = pd.to_numeric(df['retail price'], errors='coerce')
    df = df.dropna(subset=['address', 'truckstop name', 'retail price'])

    for _, row in df.iterrows():
        # Geocode the addresses
        lat, lng = geocode_address(row['address'])
        if lat and lng:
            fuel_station = FuelStation.objects.get_or_create(
                name=row['truckstop name'],
                address=row['address'],
                latitude=lat,
                longitude=lng,
                retail_price=row['retail price']
            )
            if fuel_station is not None:
                name = row['truckstop name']
                LOGGER.info(f'Fuel station {name}-{lat}-{lng} record created!')