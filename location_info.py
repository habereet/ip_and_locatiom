from requests import get
from subprocess import getstatusoutput
import json
from os import environ
from os import path


class location_info():
    def __init__(self):
        self.local_ip = self.set_local_ip()
        print(f'IP Address: {self.local_ip}')
        self.wifi = self.set_wifi()
        print('Connected to Wi-Fi'
              if self.set_wifi() is True else
              'Not connected to Wi-Fi')
        self.map_coordinates = self.set_map_coordinates()
        print('Latitude and Longitude: '
              f'{self.map_coordinates[0]}, '
              f'{self.map_coordinates[1]}')
        self.address = (self.set_address()
                        if self.map_coordinates is not False
                        else False)
        print(f'Address: {self.address}'
              if self.address is not False else
              'Address not found')

    def set_local_ip(self):
        # return your external IP
        return get('https://api.ipify.org').text

    def set_map_coordinates(self):
        # when set up, termux-location returns
        # a json with information representing
        # the devices location
        # more info - https://wiki.termux.com/wiki/Termux-location
        status, output = getstatusoutput(
            "termux-location"
        )
        if status == 0:
            jsonData = json.loads(output)
            # Build a tuple storing
            # latitude and longitude
            return (jsonData["latitude"], jsonData["longitude"])
        else:
            return False

    def set_address(self):
        # get latitute and longitude from location tuple
        lat = self.map_coordinates[0]
        lon = self.map_coordinates[1]
        cache_results = self.check_cache((float(lat), float(lon)))
        if cache_results is False:
            key = environ.get('GEOCODINGAPIKEY')
            # Get json response from Google Maps'
            # Reverse Geocoding APi
            response = get('https://maps.googleapis.com/maps/api/geocode/json?'
                           f'latlng={lat},{lon}&key={key}').text
            jsonData = json.loads(response)
            # return the first formatted address in the json
            address = jsonData["results"][0]["formatted_address"]
            self.write_to_cache((float(lat), float(lon)))
            return address

    def set_wifi(self):
        # when set up, termux-wifi-connectioninfo
        # returns a json with representing
        # the device's wifi info
        # https://wiki.termux.com/wiki/Termux-wifi-connectioninfo
        status, output = getstatusoutput(
          "termux-wifi-connectioninfo"
        )
        if status == 0:
            jsonData = json.loads(output)
            return (False
                    if jsonData["supplicant_state"] == "DISCONNECTED"
                    else True)
        else:
            return False

    def check_cache(self, float_coordinates):
        cache_path = "addresses.cache"
        if path.exists(cache_path) is True:
            lat = round(float_coordinates[0], 4)
            lon = round(float_coordinates[1], 4)
            print((lat, lon))
        else:
            return False

    def write_to_cache(self, float_coordinates):
        cache_path = "addresses.cache"
        print(cache_path)
