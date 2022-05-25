"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    with open(filename, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            content = {**result.serialize(), **result.neo.serialize()}
            content["name"] = content.get("name", "")
            content["potentially_hazardous"] = str(
                content.get("potentially_hazardous", "False"))
            writer.writerow(content)


def write_to_json(results, filename):
    """
    Write an iterable of `CloseApproach` objects to a JSON file.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    close_approach_collection = []
    for result in results:
        content = {**result.serialize(), **result.neo.serialize()}
        content["name"] = content.get("name", "")
        content["potentially_hazardous"] = content.get(
            "potentially_hazardous", False)
        close_approach_collection.append(
            {
                "datetime_utc": content.get("datetime_utc"),
                "distance_au": content.get("distance_au"),
                "velocity_km_s": float(content.get("velocity_km_s")),
                "neo": {
                    "designation": content.get("designation"),
                    "name": content.get("name"),
                    "diameter_km": float(content.get("diameter_km")),
                    "potentially_hazardous": content.get("potentially_hazardous"),
                },
            }
        )

    with open(filename, "w") as json_file:
        json.dump(close_approach_collection, json_file)
