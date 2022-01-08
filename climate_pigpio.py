# from logging import DEBUG
# import Adafruit_DHT
# import adafruit_dht
import time
import sys
from datetime import datetime, timezone
import json
import requests
import simplelogging
import settings
from pigpio_dht import DHT11

DHT_SENSOR = DHT11(4)
# DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4


# Setup the logging
log = simplelogging.get_logger(logger_level=simplelogging.DEBUG, console=True,
                               console_level=simplelogging.INFO, file_name="log/climate.log", file_level=DEBUG)
log.info("Staring logging")


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



class ClimateRecord:

    def __init__(self, location, temperature, humidity):
        self.timestamp = datetime.now(timezone.utc)
        self.location = location
        self.temperature = temperature
        self.humidity = humidity

    def output(self):
        return (
            f"Time: {self.timestamp}, Location: {self.location}, Temp: {self.temperature}C, Humidity: {self.humidity}%")

    def json(self):
        return({"timestamp": str(self.timestamp), "location": self.location, "temperature": self.temperature, "humidity": self.humidity})


while True:
    # humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    temp_json = DHT_SENSOR.read()
    print(f"New lib: {temp_json}")
    if temp_json['humidity'] is not None and temp_json['temperature'] is not None:
    # if humidity is not None and temperature is not None:
        # print(f"Temp={temperature}C Humidity={humidity:0.1f}%")
        temp = ClimateRecord(location, temp_json['temperature'], temp_json['humidity'])

        # No need to create a list right now
        # ClimateRecords.append(temp)

        # POST data to API
        postData(temp.json())

        # write data to file
        log.info(temp.output())
        # print(temp.json())
        write_json(temp.json())

    else:
        log.error(("Sensor failure. Check wiring."))
    time.sleep(10)