#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
import time
import json
import logging

import requests

LOG = logging.getLogger(__name__)


class Buienalarm:
    """
    Buienalarm class
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

    def __init__(self, lon=None, lat=None, region='nl', unit='mm/u', timeframe=60):
        self.lon = lon
        self.lat = lat
        self.region = region
        self.unit = unit
        self.precipitation = {}
        self.total = 0
        self.timeframe = int(timeframe / 5)
        self.renew = None
        self.data = None
        self.update()

    def get_forecast(self):
        """Get the precipitation forecast"""
        if self.renew < time.time():
            self.update()
        return json.dumps([v for v in self.precipitation.values()])
    
    def get_precipitation_now(self):
        """Get the amount of precipitation on this moment"""
        if self.renew < time.time():
            self.update()
        return self.precipitation[1]

    def get_temperature(self):
        """Get the temperature on this moment"""
        if self.renew < time.time():
            self.update()
        return self.data["temp"]

    def get_precipitation_forecast_total(self):
        """Get the total expected precipitation within the time-frame"""
        if self.renew < time.time():
            self.update()
        return round(self.total / 12, 2)

    def get_precipitation_forecast_average(self):
        """Get the average expected precipitation within the time-frame"""
        if self.renew < time.time():
            self.update()
        return round(self.total / self.timeframe, 2)

    def update(self):
        """Update the buienalarm data"""
        payload = {
            "lat": self.lat,
            "lon": self.lon,
            "region": self.region,
            "unit": self.unit,
        }
        try:
            resp = requests.get(self.__REQUEST_URL, params=payload)
            LOG.debug(resp.url)
            data = resp.json()
            if data["success"] is False:
                LOG.error(data.get("reason"))
            else:
                self.data = data
        except requests.exceptions.RequestException as e:
            LOG.error("Request for buienalarm failed due ", e)

        LOG.debug(self.data)

        precip = self.data["precip"]
        self.renew = int(self.data["start"] + 670)
        t = self.data["start_human"]
        now = datetime.now()
        start_data = now.strftime("%Y-%m-%d") + " " + t

        # Avoid bug in Python
        try:
            t = datetime.strptime(start_data, "%Y-%m-%d %H:%M")
        except TypeError:
            t = datetime(
                *(time.strptime(start_data, "%Y-%m-%d %H:%M")[0:6]))

        i = 0
        j = 0

        for p in precip:
            dt = t + timedelta(minutes=i * 5)
            i += 1
            # We are sometimes also getting 'old' data. Skip this!
            if dt >= now and j < self.timeframe:

                j += 1
                self.precipitation[int(j)] = float(p)

        LOG.debug("self.precipitation", self.precipitation)

        self.total = round(sum(p for p in self.precipitation.values()), 2)
