import time
import json
import requests
import pandas as pd
from pymongo import MongoClient
from datetime import datetime


class WeatherDataFetcher:
    """A class for fetching weather data from MongoDB or an external API."""

    __version__ = '0.1.0'
    
    def __init__(self, mongo_uri, database_name, api_key):
        """
        Initialize the DataFetcher object.

        Parameters:
        - mongo_uri (str): The MongoDB connection URI.
        - database_name (str): The name of the MongoDB database.
        - api_key (str): The API key for accessing the external weather API.
        """
        self.mongo_uri = mongo_uri
        self.database_name = database_name
        self.api_key = api_key
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.database_name]

    def check_time_format(self,time_str):
        def is_valid_format(time_str, date_format):
            try:
                datetime.strptime(time_str, date_format)
                return True
            except ValueError:
                return False

        formats = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%Y/%m/%d',
            '%d-%m-%Y',
        ]

        valid_formats = [fmt for fmt in formats if is_valid_format(time_str, fmt)]

        if valid_formats:
            return True, valid_formats[0]
        else:
            return False, None


    def get_weather_data_from_api(self, target_date, latitude, longitude):
        """
        Fetch weather data from an external API.

        Parameters:
        - target_date (str): The date for which weather data is requested.
        - latitude (float): The latitude coordinate of the location.
        - longitude (float): The longitude coordinate of the location.

        Returns:
        - dict: The weather data retrieved from the API.
        """
        target_date = str(target_date)

        url = "https://api.openweathermap.org/energy/1.0/solar/data"

        params = {
            "lat": latitude,
            "lon": longitude,
            "date": target_date,
            "appid": self.api_key,
        }

        # Maximum number of retries
        max_retries = 20
        retry_count = 0

        while True:
            response = requests.get(url, params=params)
            # print(response.text)

            if response.status_code == 200:
                print('Fetching Irradiance Data...')
                return response.json()
            else:
                retry_count += 1
                time.sleep(20)
                print(f"Received response code: {response.status_code}. Retrying ({retry_count}/{max_retries})...")

            if retry_count == max_retries:
                print("Maximum retries reached. Failed to get a 200 response.")
                return None
            


    def get_weather_data(self, plant, target_date, latitude, longitude):
        """
        Fetch weather data from either MongoDB or an external API.

        Parameters:
        - plant (str): The name of the plant for which data is requested.
        - target_date (str): The date for which weather data is requested.
        - latitude (float): The latitude coordinate of the location.
        - longitude (float): The longitude coordinate of the location.

        Returns:
        - dict: The weather data retrieved.
        """

        if not isinstance(target_date, str):
            raise TypeError("Input argument 'target_date' must be a string.")

        check = self.check_time_format(target_date)
        if check[0] == True:
            target_date_obj = pd.to_datetime(target_date, format=check[1])
        else:
            raise ValueError("Invalid date format. Please use 'YYYY-MM-DD', 'DD/MM/YYYY', 'DD-MM-YYYY', or a format recognized by pd.to_datetime().")

        # Convert the date object back to string in 'YYYY-MM-DD' format
        target_date = target_date_obj.strftime('%Y-%m-%d')

        try:
            collection = self.db[plant]
            document = collection.find_one({"lat": float(latitude), "lon": float(longitude), "date": target_date})

            if document:
                print("Fetched Data from MongoDB.")
                data = document
            else:
                print("Fetching Data from API.")
                # Iterate over all collections in the database
                for collection_name in self.db.list_collection_names():
                    collection = self.db[collection_name]
                    existing_document = collection.find_one({"lat": float(latitude), "lon": float(longitude), "date": target_date})
                    if existing_document:
                        data = f"Given location co-ordinates already exist for plant named {collection_name} . " 
                        return data  # Return existing document if found
                    
                # If the data is not found in any collection, fetch it from the API
                data = self.get_weather_data_from_api(target_date, latitude, longitude)
                
                # Insert the fetched data into the specified collection
                collection = self.db[plant]
                collection.insert_one(data)
            return data

        except Exception as e:
            print(f"Data fetching failed with exception {e}")

        

    def get_plant_metadata(self):
        """
        Fetch metadata about the plants from MongoDB.

        Returns:
        - DataFrame: A DataFrame containing plant metadata.
        """
        # Get the list of collections
        collections = [collection for collection in self.client[self.database_name].list_collection_names()]
        # Initialize lists to store data
        plant_names = []
        latitudes = []
        longitudes = []

        # Iterate over collections
        for collection_name in collections:
            # Access the collection
            collection = self.db[collection_name]
            # Find one document in the collection
            document = collection.find_one()

            if document:
                # Extract latitude and longitude values if available
                latitude = document.get('lat', "")
                longitude = document.get('lon', "")
            else:
                # If no document found, set latitude and longitude to NaN
                latitude = ""
                longitude = ""

            # Append data to lists
            plant_names.append(collection_name)
            latitudes.append(latitude)
            longitudes.append(longitude)

        # Create a DataFrame
        metadata_df = pd.DataFrame({
            'plant_name': plant_names,
            'latitude': latitudes,
            'longitude': longitudes
        })

        return metadata_df