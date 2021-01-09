from requests import get
import subprocess
import json
import os


class location_info():
    def __init__(self):
        self.local_ip = self.set_local_ip()
        print(self.local_ip)
        self.location = self.set_location()
        print(self.location)
        self.address = (self.set_address()
                        if self.location is not False
                        else False)
        print(self.address)
        self.wifi = self.set_wifi()
        print(self.set_wifi())

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
        lat = self.location[0]
        lon = self.location[1]
        response = get('https://maps.googleapis.com/maps/api/geocode/json?'
                       f'latlng={lat},{lon}&key={key}').text
        jsonData = json.loads(response)
        address = jsonData["results"][0]["formatted_address"]
        return address

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
