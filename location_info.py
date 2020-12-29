from requests import get


class location_info():
    def __init__(self):
        self.local_ip = self.set_local_ip()

    def set_local_ip(self):
        return get('https://api.ipify.org').text
