
from dateutil.parser import parse


class Entity(object):
    """ Entity object with helper functions and
    properties.
    """

    @property
    def id(self):
        if not self.key:
            return None
        return self.key.id


def _ensure_date(date):
    """ Checks that date is not a string. May also
    have more type conditions in the future.

    :type date: str or datetime or none
    :param date: date to check condition and convert

    :rtype: datetime
    :returns: returns parsed datetime object
    """
    if type(date) == str:
        return parse(created)
    return date
