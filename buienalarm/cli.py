#!/usr/bin/env python3
"""Buienalarm API CLI."""

import argparse
import logging
from typing import List

from .pybuienalarm import Buienalarm, PrecipitationAt


logging.basicConfig()
_LOGGER = logging.getLogger("buienalarm")
_LOGGER.setLevel(logging.ERROR)

GRAPH_SYMBOL = "#"
VALUE_SCALE = 10.0


parser = argparse.ArgumentParser(description="buienalarm")
parser.add_argument("lon", help="Longitude")
parser.add_argument("lat", help="Latitude")
parser.add_argument("--region", help="Region, 'nl' or 'be'")
parser.add_argument("--debug", help="Debug mode", action="store_true")

args = parser.parse_args()


def graph(precipitations: List[PrecipitationAt]):
    """Print a small vertical bar chart."""
    for precipitation in precipitations:
        scaled_value = 1 + int(precipitation.value * VALUE_SCALE)
        graph_bar = GRAPH_SYMBOL * scaled_value
        print(f'{precipitation.timestamp}: {precipitation.value:.2f} {graph_bar}')


def main() -> None:
    """Main entry point."""
    if args.debug:
        _LOGGER.setLevel(logging.DEBUG)

    api = Buienalarm(args.lon, args.lat)
    api.update()
    if not api.has_data:
        print('Failed getting data')
        return

    print(f'Temperature: {api.temperature}C')
    print('Precipitation forecast:')
    graph(api.precipitation_from_now)


if __name__ == "__main__":
    main()
