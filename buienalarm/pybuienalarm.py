#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import json
# import subprocess
from datetime import datetime
from datetime import timedelta
import time
import logging

import requests

LOG = logging.getLogger(__name__)


class Buienalarm:
    """
    Buienalarm
    """

    """
    Full url:
    https://cdn-secure.buienalarm.nl/api/3.4/forecast.php?lat={}&lon={}&region=nl&unit=mm/u
    """
    __API_DOMAIN = "https://cdn-secure.buienalarm.nl/api/"
    __API_VERSION = "3.4"
    __API_PARAMETERS = "/forecast.php?lat={}&lon={}&region={}&unit=mm/u"
    __API_URL = __API_DOMAIN + __API_VERSION + __API_PARAMETERS
    __REQUEST_URL = "https://cdn-secure.buienalarm.nl/api/3.4/forecast.php"

    def __init__(self, lon=None, lat=None, region='nl', unit='mm/h', timeframe=60):
        self.lon = lon
        self.lat = lat
        self.region = region
        self.unit = unit
        self.precip = {}
        self.total = 0
        self.timeframe = int(timeframe / 5)
        
    # def get_precipitation(self):
    #     """   """
    #     values = getdata(self.__API_URL.format(
    #         self.lat, self.lon, self.region))
    #     print(self.__API_URL.format(
    #         self.lat, self.lon, self.region))
    #     if values["success"] is False:
    #         LOG.error(values.get("reason"))
    #     else:
    #         return values

    def get_data(self):
        """ """
        payload = {
            "lat": self.lat,
            "lon": self.lon,
            "region": self.region,
            "unit": self.unit,
        }

        try:
            resp = requests.get(self.__REQUEST_URL, params=payload)
            # print(resp.url)
            data = resp.json()
            if data["success"] is False:
                LOG.error(data.get("reason"))
            else:
                return data
        except requests.exceptions.RequestException as e:
            LOG.error("Request for buienalarm failed due ", e)
            return None

    def get_precipitation(self):
        """ """
        data = self.get_data()
        precip = data.get("precip", [])
        t = data.get("start_human")
        now = datetime.now()
        startdata = now.strftime("%Y-%m-%d") + " " + t

        # Avoid bug in Python
        try:
            brDT = datetime.strptime(startdata, "%Y-%m-%d %H:%M")
        except TypeError:
            brDT = datetime(
                *(time.strptime(startdata, "%Y-%m-%d %H:%M")[0:6]))

        i = 0
        j = 0
        print(precip)

        for p in precip:
            dt = brDT + timedelta(minutes=i * 5)

            i += 1
            # We are sometimes also getting 'old' data. Skip this!
            if dt >= now:
                if j < self.timeframe:
                    j += 1
                    # print(p)
                    self.precip[int(j)] = float(p)

        return self.precip

    def get_temperature(self):
        """ """
        return self.get_data()

    def total_precipitation(self):
        """ """
        self.get_precipitation()
        self.total = round(sum(p for p in self.precip.values()), 2)

        return self.total

    def average_precipitation(self):
        """ """
        total = self.total_precipitation
        return round(total / self.timeframe, 2)


# def get_data(self):
#     payload = {
#             "lat": self.lat,
#             "lon": self.lon,
#             "region": self.region,
#             "unit": self.unit,
#         }
#
#     try:
#         resp = requests.get(self.__REQUEST_URL, params=payload)
#         print(resp.url)
#         data = resp.json()
#         return data
#     except requests.exceptions.RequestException as e:
#         LOG.error("Request for buienalarm failed due ", e)
#         return None
#
# def getdata(url):
#     command = "curl -X GET "
#     options = "'" + url + "'"
#     p = subprocess.Popen(command + " " + options,
#                          shell=True, stdout=subprocess.PIPE)
#     p.wait()
#     data, errors = p.communicate()
#     if p.returncode != 0:
#         LOG.error("Request for buienalarm failed")
#         values = {}
#     else:
#         values = json.loads(data.decode("utf-8"))
#     return values


# Vervallen?
def value2mmph(value):
    if value > 0:
        return round(10 ** ((value - 109) / 32), 1)
    else:
        return 0
