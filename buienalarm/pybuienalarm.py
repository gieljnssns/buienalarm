#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import subprocess
from datetime import datetime
from datetime import timedelta
import time
import logging

# import requests

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

    def __init__(self, lon=None, lat=None, region='nl', unit='mm/h'):
        self.lon = lon
        self.lat = lat
        self.region = region
        self.unit = unit
        
    def get_precipitation(self):
        """   """
        values = getData(self.__API_URL.format(
            self.lat, self.lon, self.region))
        if values["success"] is False:
            LOG.error(values.get("reason"))
        else:
            return values


def getData(url):
    command = "curl -X GET "
    options = "'" + url + "'"
    p = subprocess.Popen(command + " " + options,
                         shell=True, stdout=subprocess.PIPE)
    p.wait()
    data, errors = p.communicate()
    if p.returncode != 0:
        LOG.error("Request for buienalarm failed")
        values = {}
    else:
        values = json.loads(data.decode("utf-8"))
    return values


# Vervallen?
def value2mmph(value):
    if value > 0:
        return round(10 ** ((value - 109) / 32), 1)
    else:
        return 0
