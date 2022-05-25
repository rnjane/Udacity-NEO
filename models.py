"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""
from helpers import cd_to_datetime, datetime_to_str

class NearEarthObject:
    """A near-Earth object (NEO)."""

    def __init__(self, designation, name, diameter, hazardous, **kwargs):
        """Create a new `NearEarthObject`.

        :param designation: The object's primary designation.
        :param name: The object's IAU name.
        :param diameter: The object's estimated diameter in kilometers.
        :param hazardous: Whether the object is potentially hazardous to Earth.
        :param kwargs: other near earth object keyword arguments.
        """
        self.designation = designation
        self.name = name
        self.diameter = diameter or float("nan")
        self.hazardous = hazardous

        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f"{self.designation} {self.name}"
        return f"{self.designation}"

    def __str__(self):
        """Return human-readable string representation of this object."""
        return f"NEO {self.fullname} has a diameter of {self.diameter} km and is {'not ' if not self.hazardous else ''}a potentially hazardous object."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def serialize(self):
        """
        Return a dictionary representation of this object.

        :return: a dictionary of the NearEarthObject object
        """
        return {
            "designation": self.designation,
            "name": self.name,
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous,
        }


class CloseApproach:
    """A close approach to Earth by an NEO."""

    def __init__(self, designation, time, velocity, distance, **close_approach_kwargs):
        """Create a new `CloseApproach`.

        :param designation: the primary designation of the near earth object
        :param time: the date and time of the approach in UTC
        :param velocity: the relative approach velocity in kilometers per second
        :param distance: the nominal approach distance in astronomical units
        :param close_approach_kwargs: close_approach keyword arguments.
        """
        self.designation = designation
        self.time = cd_to_datetime(time)
        self.distance = distance if distance else float("nan")
        self.velocity = velocity if velocity else float("nan")
        self.neo = close_approach_kwargs.get('neo')

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return string representation of a CloseApproach."""
        return f"At {self.time_str}, the {self.neo.fullname} approaches the Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def serialize(self):
        """
        Return a serialized version of this CloseApproach object.

        :return: a dictionary of the CloseApproach object
        """
        return {
            "velocity_km_s": self.velocity,
            "datetime_utc": datetime_to_str(self.time),
            "distance_au": self.distance,
        }
