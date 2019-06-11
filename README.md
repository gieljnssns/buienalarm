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
    
    # get current precipitation
    print b.get_precipitation_now()
    
    # get current temperature
    print b.get_temperature()
    
    # get the total expected precipitation within the time-frame
    print b.get_precipitation_forecast_total()
    
    # get the average expected precipitation within the time-frame
    print b.get_precipitation_forecast_average()



## Thanks to
https://github.com/Xorfor since this packet is based on https://github.com/Xorfor/Domoticz-Buienalarm-Plugin
