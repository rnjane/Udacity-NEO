
"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    with open(neo_csv_path, 'r') as neo_csv_file:
        neo_csv_reader = csv.DictReader(neo_csv_file)
        near_earth_objects = []
        for row in neo_csv_reader:
            diameter = float(row.get('diameter')) if row.get(
                'diameter') else None
            hazardous = True if row.get('pha') == "Y" else False
            near_earth_objects.append(NearEarthObject(
                designation=row.get('pdes'),
                name=row.get('name') or None,
                diameter=diameter,
                hazardous=hazardous
            ))
    return near_earth_objects


def load_approaches(cad_json_path):
    """
    Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    close_approaches = []

    with open(cad_json_path, 'r') as approaches_json_file:
        approaches = json.load(approaches_json_file)

        for approach_data in approaches.get('data'):
            approach = dict(zip(approaches.get('fields'), approach_data))
            close_approaches.append(
                CloseApproach(
                    designation=approach.get("des"),
                    time=approach.get("cd"),
                    distance=float(approach.get("dist")),
                    velocity=float(approach.get("v_rel"))
                )
            )

    return close_approaches
