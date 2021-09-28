from climate import ClimateRecord

def testing_the_test():
    assert 1 == 1

def TestClimateRecord():
    cr = ClimateRecord("Mountain top", -22.2, 1.0)
    assert cr.output == f"Time: {cr.timestamp}, Location: Mountain top, Temp: -22.2C, Humidity: 1.0%"
