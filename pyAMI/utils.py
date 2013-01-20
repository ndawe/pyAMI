from __future__ import division
import sys
import textwrap


def read_patterns_from(stream):

    own_file = False
    if isinstance(stream, basestring):
        stream = open(stream, 'r')
        own_file = True
    patterns = [p.strip() for p in stream.readlines()]
    patterns = [p for p in patterns if p and not p.startswith('#')]
    if own_file:
        stream.close()
    return patterns


def flatten_results(things, fields):
    """
    Convert list of dicts to list of tuples
    tuple elements are in the same order as in fields

    *things*: list
        list of dicts

    *fields*: [ tuple | list ]
        keys of each dict to include in tuples
    """
    return [[thing[field.split('.')[-1]]
        for field in fields]
            for thing in things]


def parse_fields(fields, table):
    """
    *fields*: [tuple | list | str ]
        field names. If a string, then comma separated

    *table*: pyAMI.ami.schema.Table
        the schema table containing these fields
    """
    query_fields = []
    if fields:
        if isinstance(fields, basestring):
            fields = fields.split(',')
        for name in fields:
            name = validate_field(name, table)
            query_fields.append(name)
    return query_fields


def validate_field(field, table):

    try:
        if field in table.fields.values():
            return field
        name = field.replace('-', '_')
        if '.' in name:
            foreign_name, foreign_field = name.split('.')
            try:
                foreign_entity = table.foreign[foreign_name]
            except KeyError, AttributeError:
                raise ValueError('%s is not associated with %s' % (
                    table.__name__, foreign_name))
            if foreign_field not in foreign_entity.fields.values():
                foreign_field = foreign_entity.fields[foreign_field]
            name = '%s.%s' % (foreign_name, foreign_field)
        else:
            name = table.fields[name]
    except KeyError:
        raise ValueError(
                ('field %s does not exist\n' % name) +
                 'valid fields are:\n\t' + '\n\t'.join(table.fields.keys()))
    return name


def print_table(table, sep='  ',
                wrap_last=False,
                wrap_width=50,
                header=False,
                vsep=None,
                stream=None):

    if stream is None:
        stream = sys.stdout
    # reorganize data by columns
    cols = zip(*table)
    # compute column widths by taking maximum length of values per column
    col_widths = [max(len(value) for value in col) for col in cols]
    # create a suitable format string
    format = sep.join(['%%-%ds' % width for width in col_widths[:-1] ] + ['%s'])
    # print each row using the computed format
    if wrap_last:
        total_width = sum(col_widths[:-1]) + (len(sep) * (len(cols) - 1)) + wrap_width
        filler = [''] * (len(cols) - 1)
        for i, row in enumerate(table):
            last = textwrap.wrap(row[-1], width=wrap_width)
            print >> stream, format % tuple(row[:-1] + [last[0]])
            for wrapped in last[1:]:
                print >> stream, format % tuple(filler + [wrapped])
            if vsep != None:
                if i < len(table) - 1:
                    print vsep * total_width
    else:
        total_width = sum(col_widths) + (len(sep) * (len(cols) - 1))
        for i, row in enumerate(table):
            print >> stream, format % tuple(row)
            if vsep is not None:
                if i < len(table) - 1:
                    print vsep * total_width


def humanize_bytes(bytes, precision=1):
    """
    *bytes* : int
        number of bytes

    *precision* : int
        precision at which to display human-readable form

    Return a humanized string representation of a number of bytes.

    Assumes `from __future__ import division`.

    >>> from pyAMI.query import humanize_bytes
    >>> humanize_bytes(1)
    '1 byte'
    >>> humanize_bytes(1024)
    '1.0 kB'
    >>> humanize_bytes(1024*123)
    '123.0 kB'
    >>> humanize_bytes(1024*12342)
    '12.1 MB'
    >>> humanize_bytes(1024*12342,2)
    '12.05 MB'
    >>> humanize_bytes(1024*1234,2)
    '1.21 MB'
    >>> humanize_bytes(1024*1234*1111,2)
    '1.31 GB'
    >>> humanize_bytes(1024*1234*1111,1)
    '1.3 GB'
    """
    abbrevs = (
        (1 << 50L, 'PB'),
        (1 << 40L, 'TB'),
        (1 << 30L, 'GB'),
        (1 << 20L, 'MB'),
        (1 << 10L, 'kB'),
        (1, 'bytes')
    )
    if bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)


def print_dict(d, sep=' ', stream=None):
    """
    *d* : dict
        dictionary to print

    *stream* : file
        file-like object to print output on
        defaults to sys.stdout
    """
    if stream is None:
        stream = sys.stdout
    table = [[name, ':', value] for name, value in d.items()]
    print_table(table, sep=' ', stream=stream)
