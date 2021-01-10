from requests import get
import subprocess
import json
import os


class location_info():
    def __init__(self):
        self.local_ip = self.set_local_ip()
        print(f'IP Address: {self.local_ip}')
        self.wifi = self.set_wifi()
        print('Connected to Wi-Fi'
              if self.set_wifi() is True else
              'Not connected to Wi-Fi')
        self.location = self.set_location()
        print('Latitude and Longitude: '
              f'{self.location[0]}, '
              f'{self.location[1]}')
        self.address = (self.set_address()
                        if self.location is not False
                        else False)
        print(f'Address: {self.address}'
              if self.address is not False else
              'Address not found')

    def set_local_ip(self):
        # return your external IP
        return get('https://api.ipify.org').text

    def set_location(self):
        # when set up, termux-location returns
        # a json with information representing
        # the devices location
        # more info - https://wiki.termux.com/wiki/Termux-location
        status, output = self.callSubProcess(
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
        key = os.environ.get('GEOCODINGAPIKEY')
        # get latitute and longitude from location tuple
        lat = self.location[0]
        lon = self.location[1]
        # Get json response from Google Maps'
        # Reverse Geocoding APi
        response = get('https://maps.googleapis.com/maps/api/geocode/json?'
                       f'latlng={lat},{lon}&key={key}').text
        jsonData = json.loads(response)
        # return the first formatted address in the json
        return jsonData["results"][0]["formatted_address"]

    def set_wifi(self):
        status, output = self.callSubProcess(
          "termux-wifi-connectioninfo"
        )
        if status == 0:
            jsonData = json.loads(output)
            return (True
                    if jsonData["supplicant_state"] == "COMPLETED"
                    else False)
        else:
            return False

    def callSubProcess(self, command):
        status, output = subprocess.getstatusoutput(
          command
        )
        return (status, output)
