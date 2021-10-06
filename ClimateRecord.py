from datetime import datetime, timezone

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
