import warnings
import attribute_osconfeed

DB_NAME = 'attribute_schedule_db1'
CONFERENCE = 'conference.115'


class Record:
    """Each Record instance implements a custom set of attributes reflexing
     the fields of the underlying JSON record."""

    def __init__(self, **kwargs):
        """A common shortcut to build an instance with attributes
        created from keyword arguments:

            - __dict__ of an object is where its attributes are kept --
            unless __slots__ is declared in the class;

            - so updating an instance __dict__ with a mapping is a quick
            way to create a bunch of attributes in that instance."""
        self.__dict__.update(kwargs)


def load_db(db):
    """
    ``shelve`` provides a simple, efficient way to re-organize the schedule data:
     we read all records from the JSON file and save them to a shelve.Shelf.
     Each key are made from the record type and the serial number and the value
     is an instance of Record.

    >>> import shelve
    >>> db = shelve.open(DB_NAME)
    >>> if CONFERENCE not in db:
    ...     load_db(db)
    ...
    >>> speaker = db['speaker.3471']
    >>> type(speaker)
    <class 'attribute_schedule.Record'>
    >>> speaker.name, speaker.twitter
    ('Anna Martelli Ravenscroft', 'annaraven')
    >>> db.close()
    """
    # fetch JSON feed from the Web
    raw_data = attribute_osconfeed.load()
    warnings.warn('loading' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        # record type is the collection name without the trailing 's'
        record_type = collection[:-1]
        for record in rec_list:
            # build key from the record type and the serial field
            key = '{}.{}'.format(record_type, record['serial'])
            # update the serial field with the full key
            record['serial'] = key
            # build Record instance and save it to the database under the key
            db[key] = Record(**record)
