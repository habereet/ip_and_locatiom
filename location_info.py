from requests import get
import subprocess
import json


class location_info():
    def __init__(self):
        self.local_ip = self.set_local_ip()
        #self.location = self.set_location()
        print(self.set_location())
        print(self.set_wifi())
        #self.wifi = self.set_wifi()

    def set_local_ip(self):
        return get('https://api.ipify.org').text

    def set_location(self):
        status, output = subprocess.getstatusoutput(
            "termux-location"
        )
        if status == 0:
            return 1
        else:
            return 0
    
    def set_wifi(self):
        status, output = subprocess.getstatusoutput(
          "termux-wifi-connectioninfo"
        )
        if status == 0:
            return 1
        else:
            return 0