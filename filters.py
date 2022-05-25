"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest from
the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You'll edit this file in Tasks 3a and 3c.
"""
import itertools
import operator


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes.

    An `AttributeFilter` represents the search criteria pattern comparing some
    attribute of a close approach (or its attached NEO) to a reference value. It
    essentially functions as a callable predicate for whether a `CloseApproach`
    object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value, and
    calling the filter (with __call__) executes `get(approach) OP value` (in
    infix notation).

    Concrete subclasses can override the `get` classmethod to provide custom
    behavior to fetch a desired attribute from the given `CloseApproach`.
    """

    def __init__(self, op, value):
        """Construct a new `AttributeFilter` from an binary predicate and a reference value.

        The reference value will be supplied as the second (right-hand side)
        argument to the operator function. For example, an `AttributeFilter`
        with `op=operator.le` and `value=10` will, when called on an approach,
        evaluate `some_attribute <= 10`.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a close approach.

        Concrete subclasses must override this method to get an attribute of
        interest from the supplied `CloseApproach`.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest, comparable to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        """Repr method used to compare filter attribute."""
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"


class DistanceFilter(AttributeFilter):
    """This class does all filtration related to distance of an approach."""

    def __init__(self, op, value):
        """Construct a new `DistanceFilter` from an binary predicate and a reference value."""
        super().__init__(op, value)

    @classmethod
    def get(cls, approach):
        """Get the distance of a close approach."""
        return approach.distance


class DiameterFilter(AttributeFilter):
    """This class does all filtration related to diameter of an approach."""

    def __init__(self, op, value):
        """Construct a new `DiameterFilter` from an binary predicate and a reference value."""
        super().__init__(op, value)

    @classmethod
    def get(cls, approach):
        """Get the diameter of a close approach."""
        return approach.neo.diameter


class VelocityFilter(AttributeFilter):
    """This class does all filtration related to velocity of an approach."""

    def __init__(self, op, value):
        """Construct a new `VelocityFilter` from an binary predicate and a reference value."""
        super().__init__(op, value)

    @classmethod
    def get(cls, approach):
        """Get the velocity of a close approach."""
        return approach.velocity


class HazardousFilter(AttributeFilter):
    """This class does all filtration related to hazardousness of an approach."""

    def __init__(self, op, value):
        """Construct a new `HazardousFilter` from an binary predicate and a reference value."""
        super().__init__(op, value)

    @classmethod
    def get(cls, approach):
        """Get the hazardousness of a close approach."""
        return approach.neo.hazardous


class DateFilter(AttributeFilter):
    """This class does all filtration related to date of an approach."""

    def __init__(self, op, value):
        """Construct a new `DateFilter` from an binary predicate and a reference value."""
        super().__init__(op, value)

    @classmethod
    def get(cls, approach):
        """Get the date of a close approach."""
        return approach.time.date()


def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    """
    Retuern a collection of filters from user specified filtration criterion.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """
    specified_filters = []

    # date filters
    if date:
        specified_filters.append(DateFilter(operator.eq, date))
    if start_date:
        specified_filters.append(DateFilter(operator.ge, start_date))
    if end_date:
        specified_filters.append(DateFilter(operator.le, end_date))

    # velocity filters
    if velocity_min:
        specified_filters.append(VelocityFilter(operator.ge, velocity_min))
    if velocity_max:
        specified_filters.append(VelocityFilter(operator.le, velocity_max))

    # distance filter
    if distance_min:
        specified_filters.append(DistanceFilter(operator.ge, distance_min))
    if distance_max:
        specified_filters.append(DistanceFilter(operator.le, distance_max))

    # hazardous filter
    if hazardous is not None:
        specified_filters.append(HazardousFilter(operator.eq, hazardous))

    # diameter filters
    if diameter_min:
        specified_filters.append(DiameterFilter(operator.ge, diameter_min))
    if diameter_max:
        specified_filters.append(DiameterFilter(operator.le, diameter_max))

    return specified_filters


def limit(iterator, n=None):
    """Limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    if n == 0 or n is None:
        return iterator
    return list(itertools.islice(iterator, 0, n))
