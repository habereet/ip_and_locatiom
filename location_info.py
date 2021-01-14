from requests import get
from subprocess import getstatusoutput
import json
from os import environ
from os import path


class location_info():
    def __init__(self):
        self.cache_path = "addresses.cache"
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
        # if the latitude and longitude
        # are not in cache
        if cache_results is False:
            key = environ.get('GEOCODINGAPIKEY')
            # Get json response from Google Maps'
            # Reverse Geocoding APi
            response = get('https://maps.googleapis.com/maps/api/geocode/json?'
                           f'latlng={lat},{lon}&key={key}').text
            jsonData = json.loads(response)
            # return the first formatted address in the json
            address = jsonData["results"][0]["formatted_address"]
            # write the latitude and longitude to cache
            self.write_to_cache((float(lat), float(lon)), address)
            return address
        # if latitude and longitude are in cache
        else:
            return cache_results

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
        # if the cache file exists
        if path.exists(self.cache_path) is True:
            lat = round(float_coordinates[0], 3)
            lon = round(float_coordinates[1], 3)
            # read the cache in
            cache = readJson(self.cache_path)
            key = f'lat{lat},lon{lon}'
            # check if latitude and
            # longitude in cache
            # return value or False
            if key in cache.keys():
                return cache[key]
            else:
                return False
        else:
            return False

    def write_to_cache(self, float_coordinates, address):
        lat = round(float_coordinates[0], 3)
        lon = round(float_coordinates[1], 3)
        # if cache file does not exist
        if path.exists(self.cache_path) is False:
            # create a one-entry dict that
            # will start our cache
            cache = {f'lat{lat},lon{lon}': address}
            # write cache as json
            with open(self.cache_path, 'w') as outfile:
                json.dump(cache, outfile)
        # if cache file does exist
        else:
            # read cache file in as json
            cache = readJson(self.cache_path)
            # add location to the dictionary
            cache[f'lat{lat},lon{lon}'] = address
            # write to cache file
            # TODO: add check that write was successful
            writeJson(self.cache_path, cache)


# read json and return
def readJson(cache_path):
    with open(cache_path) as json_file:
        return json.load(json_file)


# write json (cache) to directory (cache_path)
def writeJson(cache_path, cache):
    with open(cache_path, 'w') as outfile:
        json.dump(cache, outfile)
