import json
import unittest
from datetime import datetime, timezone

# Load data from files
with open("./data-1.json", "r") as f:
    jsonData1 = json.load(f)

with open("./data-2.json", "r") as f:
    jsonData2 = json.load(f)

with open("./data-result.json", "r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1(jsonObject):
    """
    Converts telemetry data from Format 1 to the unified target format.
    """
    locationParts = jsonObject['location'].split('/')

    result = {
        'deviceID': jsonObject['deviceID'],
        'deviceType': jsonObject['deviceType'],
        'timestamp': jsonObject['timestamp'],
        'location': {
            'country': locationParts[0],
            'city': locationParts[1],
            'area': locationParts[2],
            'factory': locationParts[3],
            'section': locationParts[4]
        },
        'data': {
            'status': jsonObject['operationStatus'],
            'temperature': jsonObject['temp']
        }
    }
    return result


def convertFromFormat2(jsonObject):
    """
    Converts telemetry data from Format 2 to the unified target format,
    including timestamp conversion from ISO 8601 to epoch milliseconds.
    """
    date = datetime.strptime(jsonObject['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
    date = date.replace(tzinfo=timezone.utc)
    timestamp = round(date.timestamp() * 1000)

    result = {
        'deviceID': jsonObject['device']['id'],
        'deviceType': jsonObject['device']['type'],
        'timestamp': timestamp,
        'location': {
            'country': jsonObject['country'],
            'city': jsonObject['city'],
            'area': jsonObject['area'],
            'factory': jsonObject['factory'],
            'section': jsonObject['section']
        },
        'data': jsonObject['data']
    }
    return result


def main(jsonObject):
    """
    Determines the format of the input and applies the appropriate conversion.
    """
    if jsonObject.get('device') is None:
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)


# Unit tests
class TestSolution(unittest.TestCase):

    def test_sanity(self):
        """
        Basic sanity check to ensure jsonExpectedResult loads properly.
        """
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        """
        Tests conversion from Format 1.
        """
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult, 'Converting from Type 1 failed')

    def test_dataType2(self):
        """
        Tests conversion from Format 2.
        """
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult, 'Converting from Type 2 failed')


# Entry point for running tests
if __name__ == '__main__':
    unittest.main()
