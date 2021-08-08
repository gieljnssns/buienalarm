# buienalarm
This package is for getting data from [Buienalarm](https://www.buienalarm.nl/antwerpen-vlaanderen-belgi%C3%AB/51.2211,4.39971)

## Where has it been tested?
Pybuienalarm is tested in Belgium

## Requirements
 * Python 3
 * requests
 
## Installing
```bash
$ pip install pybuienalarm
```

## Usage
    from buienalarm.pybuienalarm import Buienalarm
    
    # create a new buienalarm instance
    b = Buienalarm(
        longitude, latitude, timeframe)

    # fetch data
    b.update()
    
    # get current precipitation
    print b.precipitation_now
    
    # get current temperature
    print b.temperature
    
    # get the total expected precipitation within the time-frame
    print b.precipitation_forecast_total
    
    # get the average expected precipitation within the time-frame
    print b.precipitation_forecast_average


## CLI
A small CLI tool, called `buienalarm` is included to get the forecast + temperature from your terminal. Usage:
    $ buienalarm 4.9 52.366667
    Temperature: 19C
    Precipitation forecast:
    2021-08-08 18:00:00: 0.00 #
    2021-08-08 18:05:00: 0.00 #
    2021-08-08 18:10:00: 0.00 #
    2021-08-08 18:15:00: 0.00 #
    2021-08-08 18:20:00: 0.00 #
    2021-08-08 18:25:00: 0.00 #
    2021-08-08 18:30:00: 0.00 #
    2021-08-08 18:35:00: 0.00 #
    2021-08-08 18:40:00: 0.00 #
    2021-08-08 18:45:00: 0.00 #
    2021-08-08 18:50:00: 0.00 #
    2021-08-08 18:55:00: 0.15 ##
    2021-08-08 19:00:00: 0.00 #
    2021-08-08 19:05:00: 0.00 #
    2021-08-08 19:10:00: 0.00 #
    2021-08-08 19:15:00: 0.00 #
    2021-08-08 19:20:00: 0.00 #
    2021-08-08 19:25:00: 0.00 #
    2021-08-08 19:30:00: 0.00 #
    2021-08-08 19:35:00: 0.00 #
    2021-08-08 19:40:00: 0.00 #
    2021-08-08 19:45:00: 0.09 #
    2021-08-08 19:50:00: 0.12 ##


## Thanks to
https://github.com/Xorfor since this packet is based on https://github.com/Xorfor/Domoticz-Buienalarm-Plugin
