#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Buienalarm API."""

from datetime import datetime, timedelta
from typing import Any, List, Mapping, NamedTuple, Optional
import logging

import requests


PrecipitationAt = NamedTuple(
    "PrecipitationAt",
    [
        ("timestamp", datetime),
        ("value", float),
    ])


_LOGGER = logging.getLogger(__name__)

API_TIMEOUT = timedelta(seconds=10)


class Buienalarm:
    """
    Buienalarm class.

    Full url:
    https://cdn-secure.buienalarm.nl/api/3.4/forecast.php?lat={}&lon={}&region=nl&unit=mm/u
    """
    __REQUEST_URL = "https://cdn-secure.buienalarm.nl/api/3.4/forecast.php"

    def __init__(
        self,
        lon: float,
        lat: float,
        region: str = "nl",
        unit: str = "mm/u"
    ) -> None:
        """Initializer."""
        self.lon = lon
        self.lat = lat
        self.region = region
        self.unit = unit

        self.updated_at: Optional[datetime] = None
        self.data: Mapping[str, Any] = {}

    @property
    def temperature(self) -> Optional[float]:
        """Get the temperature on this moment."""
        return self.data.get("temp")

    @property
    def precipitation_now(self) -> Optional[float]:
        """Get the amount of precipitation on this moment."""
        for precip in self.precipitation_from_now:
            return precip.value
        return None

    @property
    def precipitation_forecast_average(self) -> Optional[float]:
        """Get the average expected precipitation."""
        precipitation = self.precipitation
        if not precipitation:
            return None
        return self.precipitation_forecast_total / len(precipitation)

    @property
    def precipitation_forecast_total(self) -> float:
        """Get total expected precipitation."""
        return sum(item[1] for item in self.precipitation)

    @property
    def levels(self) -> Mapping[str, float]:
        """Get levels."""
        return self.data.get("levels", {})

    @property
    def delta(self) -> timedelta:
        """Get delta between precipitation values."""
        delta = self.data.get("delta", 0)
        return timedelta(seconds=delta)

    @property
    def precipitation(self) -> List[PrecipitationAt]:
        """Get precipitation."""
        start_timestamp = self.data["start"]
        start = datetime.fromtimestamp(start_timestamp)
        delta_secs = self.delta.total_seconds()
        return [
            PrecipitationAt(start + timedelta(seconds=i * delta_secs), float(val))
            for i, val in enumerate(self.data.get("precip", []))
        ]

    @property
    def precipitation_from_now(self) -> List[PrecipitationAt]:
        """Get precipitation from now."""
        now = datetime.now()
        return [
            precip for precip in self.precipitation
            if precip.timestamp >= now
        ]

    @property
    def has_data(self) -> bool:
        """Test if data is available."""
        return bool(self.data)

    def update(self, timeout: timedelta = API_TIMEOUT, safe: bool = False) -> None:
        """
        Update the buienalarm data.

        Raises exceptions on connection errors and/or json errors.
        """
        now = datetime.now()

        # Fetch/store data.
        if safe:
            data = self._fetch_data_safe(timeout)
            if not data:
                # Error fetching data, return so updated_at isn't updated.
                _LOGGER.debug("Data: %s, updated at: %s", self.data, self.updated_at)
                return
            self.data = data
        else:
            self.data = self._fetch_data(timeout)

        # Store update timestamps.
        self.updated_at = now
        _LOGGER.debug("Data: %s, updated at: %s", self.data, self.updated_at)

    def _fetch_data(self, timeout: timedelta) -> Mapping[str, Any]:
        """Fetch the data."""
        params = {
            "lat": str(self.lat),
            "lon": str(self.lon),
            "region": self.region,
            "unit": self.unit,
        }
        resp = requests.get(self.__REQUEST_URL, params=params, timeout=timeout.total_seconds())
        resp.raise_for_status()
        _LOGGER.debug("URL: %s, Data: %s", resp.url, resp.text)

        data = resp.json()
        if not data.get("success"):
            _LOGGER.error("Received failed response, reason: %s", data.get("reason"))
            return {}

        return data

    def _fetch_data_safe(self, timeout: timedelta) -> Mapping[str, Any]:
        """Fetch the data, but don't """
        try:
            return self._fetch_data(timeout)
        except requests.exceptions.RequestException as exc:
            _LOGGER.warning("Error fetching data safely: %s", exc)

        return {}
