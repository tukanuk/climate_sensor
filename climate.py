import Adafruit_DHT
import time
import sys
from datetime import datetime, timezone
import json
import requests

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

if "-l" in opts:
    location = args[0]
    print(f"The location is: {location}")
else:
    location = "unknown"

print(opts)
print(args)

ClimateRecords = []

def write_json(new_record, filename="climate_data.json"):
    with open(filename, "r+") as fp:
        file_data = json.load(fp)
        file_data.append(new_record)
        fp.seek(0)
        json.dump(file_data, fp, indent=4)

def postData(jsonRecord):

    url = "http://benintosh.local:5000/climate"

    payload = json.dumps(jsonRecord)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(f"{response.status_code}: {response.text}")

        

class ClimateRecord:

    def __init__(self, location, temperature, humidity):
        self.timestamp = datetime.now(timezone.utc)
        self.location = location
        self.temperature = temperature
        self.humidity = humidity

    def output(self):
        print(f"Time: {self.timestamp}, Location: {self.location}, Temp: {self.temperature}C, Humidity: {self.humidity}%")
    
    def json(self):
        return({"timestamp": str(self.timestamp), "location": self.location, "temperature": self.temperature, "humidity": self.humidity})


 
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
        temp.output()
        # print(temp.json())
        write_json(temp.json())

    else:
        print("Sensor failure. Check wiring.");
    time.sleep(10);
 