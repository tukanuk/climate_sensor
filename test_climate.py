from ClimateRecord import ClimateRecord


def testing_the_test():
    assert 1 == 1


def test_ClimateRecord_output():
    # nothing wrong with the plain text output
    cr = ClimateRecord("Mountain top", -22.2, 1.0)
    assert cr.output() == (
        f"Time: {cr.timestamp}, Location: Mountain top, Temp: -22.2C, Humidity: 1.0%")


def test_ClimateRecord_json():
    # consisant json output
    cr = ClimateRecord('Dark Hallway', -10.0, 55.5)
    assert cr.json(
    ) == {'timestamp': str(cr.timestamp), 'location': 'Dark Hallway', 'temperature': -10.0, 'humidity': 55.5}
