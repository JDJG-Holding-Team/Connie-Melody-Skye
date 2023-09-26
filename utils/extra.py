from typing import TYPE_CHECKING, Any, NamedTuple


class DataObject(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)


# update stackoverflow example to something better
