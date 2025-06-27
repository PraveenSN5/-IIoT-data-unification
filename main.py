import json
from datetime import datetime, timezone

def convert_data_1_to_result(data_1):
    """
    Converts telemetry data from data-1.json format to the unified target format.
    Assumes:
      - 'deviceId' field in data-1.json maps to 'device_id' in target format
      - 'timestamp' is already in epoch milliseconds
      - 'metrics' dictionary contains 'temp' and 'pressure' fields
    """
    result = {
        "device_id": data_1["deviceId"],
        "timestamp": data_1["timestamp"],  # Already in ms, no conversion needed
        "temperature": data_1["metrics"]["temp"],
        "pressure": data_1["metrics"]["pressure"]
    }
    return result


def convert_data_2_to_result(data_2):
    """
    Converts telemetry data from data-2.json format to the unified target format.
    Handles:
      - 'time' field in ISO 8601 format, converts to epoch milliseconds
      - 'id' field maps to 'device_id'
      - 'temp_celsius' and 'pressure_pascal' map to 'temperature' and 'pressure'
    """
    dt = datetime.strptime(data_2["time"], "%Y-%m-%dT%H:%M:%SZ")
    epoch_ms = int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)

    result = {
        "device_id": data_2["id"],
        "timestamp": epoch_ms,
        "temperature": data_2["temp_celsius"],
        "pressure": data_2["pressure_pascal"]
    }
    return result
