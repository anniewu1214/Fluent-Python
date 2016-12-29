import warnings
import inspect
import attribute_osconfeed

DB_NAME = 'attribute_schedule_db2'
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented


class MissingDatabaseError(RuntimeError):
    """Raised when a database is required but was not set."""


class DBRecord(Record):
    """
    Given an event record retrieved from the shelf, reading its venue or
    speakers attributes will not return serial numbers but record objects.

    Subclass of Record adding a ``__db`` class attributes, ``set_db`` and ``get_dt``
    methods to set/get that attribute, a ``fetch`` class method to retrieve records
    from the data, and a ``__repr__`` instance method to support debugging and testing.

     - __db class attribute holds a reference to the opened shelve.Shelf database
    so it can be used by ``fetch`` and ``Event.venue`` and ``Event.speakers`` properties.

    - property is not used to manage __db: properties are class attributes
    designed to manage instance attributes.

    >>> import shelve
    >>> db = shelve.open(DB_NAME)
    >>> if CONFERENCE not in db:
    ...     load_db(db)
    ...
    >>> DBRecord.set_db(db)
    >>> event = DBRecord.fetch('event.33950')
    >>> event
    <Event 'There *Will* Be Bugs'>
    >>> event.venue
    <DBRecord serial='venue.1449'>
    >>> event.venue.name
    'Portland 251'
    >>> for spkr in event.speakers:
    ...     print('{0.serial}: {0.name}'.format(spkr))
    ...
    speaker.3471: Anna Martelli Ravenscroft
    speaker.5199: Alex Martelli
    """

    __db = None

    @staticmethod
    def set_db(db):
        DBRecord.__db = db

    @staticmethod
    def get_db():
        return DBRecord.__db

    @classmethod
    def fetch(cls, ident):
        db = cls.get_db()
        try:
            return db[ident]
        except TypeError:
            if db is None:
                msg = "database not set; call '{}.set_db(my_db)'"
                raise MissingDatabaseError(msg.format(cls.__name__))
            else:
                raise  # re-raise the exception, because we don't know how to handle it

    def __repr__(self):
        # if the record has a serial attribute, use it in the string representations
        if hasattr(self, 'serial'):
            cls_name = self.__class__.__name__
            return '<{} serial={!r}>'.format(cls_name, self.serial)
        # otherwise, defautl to the inherited __repr__
        else:
            return super().__repr__()


class Event(DBRecord):
    """
    Subclass of DBRecord adding venue and speakers properties to retrieve
    linked records, and a specialized ``__repr__`` method
    """

    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)

    @property
    def speakers(self):
        if not hasattr(self, '_speaker_objs'):
            # the 'speakers' attribute is retrieved directely from the instance __dict__
            # to avoid infinite recursion, because the puclic name of this property is also speakers
            spkr_serials = self.__dict__['speakers']
            # if an event record had a key named 'fetch', then the reference self.fetch
            # would retrieve the value of that field, instead of the fetch class method.
            fetch = self.__class__.fetch
            self._speaker_objs = [fetch('speaker.{}'.format(key)) for key in spkr_serials]
        return self._speaker_objs

    def __repr__(self):
        if hasattr(self, 'name'):
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:
            return super().__repr__()


def load_db(db):
    raw_data = attribute_osconfeed.load()
    warnings.warn('loading' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        record_type = collection[:-1]
        # capitalize to get a potential class name
        cls_name = record_type.capitalize()
        # get an object by that name from the module global scope,
        # get DBRecord if there's no such object.
        cls = globals().get(cls_name, DBRecord)
        if inspect.isclass(cls) and issubclass(cls, DBRecord):
            factory = cls
        else:
            factory = DBRecord
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            # the object stored in the database is constructed by factory, which may
            # be DBRecord or a subclass selected according to the record_type
            db[key] = factory(**record)
