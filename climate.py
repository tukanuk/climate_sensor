import Adafruit_DHT
import time
import sys
from datetime import datetime, timezone
import json
import requests
import simplelogging
import settings
from ClimateRecord import ClimateRecord

# Variables for GPIO pins on RaspberrryPi
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# Setup the logging
log = simplelogging.get_logger(logger_level=simplelogging.DEBUG, console=True,
                               console_level=simplelogging.INFO, file_name="log/climate.log", file_level=simplelogging.DEBUG)
log.info("Staring logging")


# Handle command args
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

if "-l" in opts:
    location = args[0]
    log.info(f"The location is: {location}")
else:
    location = "unknown"
    log.info(f"The location is: {location}")

# print(opts)
# print(args)

ClimateRecords = []


def write_json(new_record, filename="climate_data.json"):
    """Keep a local log of climate data"""
    with open(filename, "r+") as fp:
        file_data = json.load(fp)
        file_data.append(new_record)
        fp.seek(0)
        json.dump(file_data, fp, indent=4)


def postData(jsonRecord):

    url = settings.api_url

    payload = json.dumps(jsonRecord)
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        log.info(f"{response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError as err:
        log.error(f"Request error: {err}")


# class ClimateRecord:

#     def __init__(self, location, temperature, humidity):
#         self.timestamp = datetime.now(timezone.utc)
#         self.location = location
#         self.temperature = temperature
#         self.humidity = humidity

#     def output(self):
#         return (
#             f"Time: {self.timestamp}, Location: {self.location}, Temp: {self.temperature}C, Humidity: {self.humidity}%")

#     def json(self):
#         return({"timestamp": str(self.timestamp), "location": self.location, "temperature": self.temperature, "humidity": self.humidity})

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        # print(f"Temp={temperature}C Humidity={humidity:0.1f}%")
        temp = ClimateRecord(location, temperature, humidity)

        # No need to create a list right now
        # ClimateRecords.append(temp)

        # POST data to API
        postData(temp.json())

        # write data to file
        log.info(temp.output())
        # print(temp.json())
        write_json(temp.json())

    else:
        log.error(
            (f"Sensor failure. Check wiring. t: {temperature} h: {humidity}"))
    time.sleep(10)
