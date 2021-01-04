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
        self.address = self.set_address() if self.location != False else False
        #print(self.address)
        #self.wifi = self.set_wifi()
        #print(self.set_wifi())

    def set_local_ip(self):
        return get('https://api.ipify.org').text

    def set_location(self):
        status, output = self.callSubProcess(
            "termux-location"
        )
        if status == 0:
            jsonData = json.loads(output)
            coordinates = (jsonData["latitude"], jsonData["longitude"])
            return coordinates
        else:
            return False
    
    def set_address(self):
        APIKey = os.environ.get('GEOCODINGAPIKEY')
        response = get(f'https://maps.googleapis.com/maps/api/geocode/json?latlng={self.location[0]},{self.location[1]}&key={APIKey}').text
        jsonData = json.loads(response)
        address = jsonData["results"][0]["formatted_address"]
        print (address)
    
    def set_wifi(self):
        status, output = self.callSubProcess(
          "termux-wifi-connectioninfo"
        )
        if status == 0:
            jsonData = json.loads(output)
            return True if jsonData["supplicant_state"] == "COMPLETED" else False
        else:
            return False
            
    def callSubProcess(self, command):
        status, output = subprocess.getstatusoutput(
          command
        )
        return (status, output)