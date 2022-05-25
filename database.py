"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

"""
class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        designations_with_indices = {}
        for index, neo in enumerate(self._neos):
            designations_with_indices[neo.designation] = index

        for approach in approaches:
            if approach.designation in designations_with_indices.keys():
                approach.neo = self._neos[designations_with_indices[approach.designation]]
                self._neos[designations_with_indices[approach.designation]].approaches.append(
                    approach)

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        for neo in self._neos:
            if neo.designation == designation.upper():
                return neo
        return None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        for neo in self._neos:
            if neo.name == name.capitalize():
                return neo
        return None

    @staticmethod
    def check_approach_against_filters(approach, filters):
        """
        Check if a `CloseApproach` satisfies a collection of filters.

        :param approach: The `CloseApproach` to check.
        :param filters: A collection of filters capturing user-specified criteria.
        :return: `True` if the `CloseApproach` satisfies all filters, `False` otherwise.
        """
        match_filter = True
        for filter in filters:
            if filter(approach):
                continue
            else:
                match_filter = False
        return match_filter

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        if filters:
            for approach in self._approaches:
                # for every approach, check if it satisfies all spedified filters
                if self.check_approach_against_filters(approach, filters):
                    yield approach
        else:
            for approach in self._approaches:
                yield approach
