# Author: Noel Dawe

from __future__ import division
import re
import sys
import textwrap

from pyAMI.objects import DatasetInfo, RunPeriod
from pyAMI.schema import *
from pyAMI.defaults import YEAR, STREAM, TYPE, PROJECT, PRODSTEP


DATA_PATTERN = re.compile('^(?P<project>\w+).(?P<run>[0-9]+).(?P<stream>[a-zA-Z_\-0-9]+).(recon|merge).(?P<type>[a-zA-Z_\-0-9]+).(?P<version>\w+)$')

ESD_VERSION_PATTERN = '(?P<la>f|r)(?P<lb>[0-9]+)'
AOD_VERSION_PATTERN = ESD_VERSION_PATTERN + '_(?P<ma>m|p)(?P<mb>[0-9]+)'
NTUP_VERSION_PATTERN = AOD_VERSION_PATTERN + '_p(?P<rb>[0-9]+)'

ESD_VERSION_PATTERN = re.compile('^%s$' % ESD_VERSION_PATTERN)
AOD_VERSION_PATTERN = re.compile('^%s$' % AOD_VERSION_PATTERN)
NTUP_VERSION_PATTERN = re.compile('^%s$' % NTUP_VERSION_PATTERN)


def __clean_dataset(dataset):
    """
    Remove trailing slashes

    *dataset*: str
        dataset name
    """
    if dataset is None:
        return None
    return dataset.rstrip('/')


def flatten_results(things, fields):
    """
    Convert list of dicts to list of tuples
    tuple elements are in the same order as in fields

    *things*: list
        list of dicts

    *fields*: [ tuple | list ]
        keys of each dict to include in tuples
    """
    return [[thing[field.split('.')[-1]] for field in fields] for thing in things]


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
                raise ValueError('%s is not associated with %s' % (table.__name__, foreign_name))
            if foreign_field not in foreign_entity.fields.values():
                foreign_field = foreign_entity.fields[foreign_field]
            name = '%s.%s' % (foreign_name, foreign_field)
        else:
            name = table.fields[name]
    except KeyError:
        raise ValueError(('field %s does not exist\n' % name) + \
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


def _expand_period_contraints(periods):
    """
    period=B -> period like B%
    period=B2 -> period=B2
    """
    if isinstance(periods, basestring):
        periods = periods.split(',')
    selection = []
    # single character
    single_chars = [p for p in periods if len(p) == 1]
    selection += ["period like '%s%%'" % p for p in single_chars]
    # multiple characters
    mult_chars = [p for p in periods if len(p) > 1]
    selection += ["period='%s'" % p for p in mult_chars]
    return " OR ".join(selection)


def search_query(client,
                 entity,
                 cmd='SearchQuery',
                 cmd_args=None,
                 pattern=None,
                 order=None,
                 limit=None,
                 fields=None,
                 flatten=False,
                 mode='defaultField',
                 project_name='Atlas_Production',
                 processing_step_name='Atlas_Production',
                 show_archived=False,
                 **kwargs):
    try:
        table = TABLES[entity]
    except KeyError:
        raise TypeError('Entity %s does not exist' % entity)
    primary_field = table.primary

    query_fields = parse_fields(fields, table)
    if primary_field not in query_fields:
        query_fields.append(primary_field)
    query_fields_str = ', '.join(query_fields)

    if cmd_args is None:
        cmd_args = {}

    if pattern is None:
        pattern = '%'
    else:
        pattern = re.sub('%+', '%', pattern)
        if not pattern.startswith('%'):
            pattern = '%' + pattern
        if not pattern.endswith('%'):
            pattern += '%'

    constraints = "%s like '%s'" % (primary_field, pattern)
    if kwargs:
        for name, value in kwargs.items():
            if value is not None:
                name = validate_field(name, table)
                """
                Case of multiple values for a given field -> search with OR
                """
                if name == 'period':
                    constraints += " AND (%s)" % _expand_period_contraints(value)
                else:
                    if isinstance(value, (list, tuple)):
                        constraints += " AND (%s)" % (" OR ".join(["%s='%s'" %
                                       (name, val) for val in value]))
                    else:
                        constraints += " AND %s='%s'" % (name, value)

    if order is None:
        order_field = primary_field
    else:
        order_field = validate_field(order, table)

    if isinstance(limit, (list, tuple)):
        limit = ' LIMIT %i,%i' % tuple(limit)
    elif limit is not None:
        limit = ' LIMIT 0,%i' % limit
    else:
        limit = ''

    args = [cmd,
            "entity=%s" % entity,
            "glite=SELECT "
                + query_fields_str
                + (" WHERE (%s)" % constraints)
                + (" ORDER BY %s" % order_field)
                + limit,
            "project=%s" % project_name,
            "processingStep=%s" % processing_step_name,
            "mode=%s" % mode]
    for item in cmd_args.items():
        args.append("%s=%s" % item)
    if show_archived:
        args.append('showArchived=true')

    result = client.execute(args)
    things = [thing for thing in result.rows()]
    if flatten:
        things = flatten_results(things, query_fields)
    return query_fields, things


def get_types(client,
              pattern,
              order=None,
              limit=None,
              fields=None,
              flatten=False,
              show_archived=False,
              **kwargs):
    """
    A command to list all ATLAS types.
    Only those with writeStatus=valid can be used for new names.
    """
    if 'write_status' not in kwargs:
        kwargs['write_status'] = 'valid'
    query_fields, types = search_query(client=client, entity='data_type', pattern=pattern,
                                       processing_step_name='*',
                                       order=order, limit=limit, fields=fields, show_archived=show_archived, **kwargs)
    if flatten:
        types = flatten_results(types, query_fields)
    return types


def get_subtypes(client,
              pattern,
              order=None,
              limit=None,
              fields=None,
              flatten=False,
              show_archived=False,
              **kwargs):
    """
    A command to list all ATLAS subtypes.
    Only those with writeStatus=valid can be used for new names.
    """
    if 'write_status' not in kwargs:
        kwargs['write_status'] = 'valid'
    query_fields, types = search_query(client=client, entity='subData_type', pattern=pattern,
                                       processing_step_name='*',
                                       order=order, limit=limit, fields=fields, show_archived=show_archived, **kwargs)
    if flatten:
        types = flatten_results(types, query_fields)
    return types


def add_type(client, type):
    """
    Add a type
    """
    args = ['Addtype', type]
    return client.execute(args)


def get_nomenclatures(client,
                      pattern,
                      order=None,
                      limit=None,
                      fields=None,
                      flatten=False,
                      show_archived=False,
                      **kwargs):
    """
    Return list of ATLAS nomenclatures
    """
    if 'write_status' not in kwargs:
        kwargs['write_status'] = 'valid'
    query_fields, nomens = search_query(client=client, entity='nomenclature', pattern=pattern,
                                        processing_step_name='*',
                                        order=order, limit=limit, fields=fields, show_archived=show_archived, **kwargs)
    if flatten:
        nomens = flatten_results(nomens, query_fields)
    return nomens


def get_projects(client,
                 pattern,
                 order=None,
                 limit=None,
                 fields=None,
                 flatten=False,
                 show_archived=False,
                 **kwargs):
    if 'write_status' not in kwargs:
        kwargs['write_status'] = 'valid'
    query_fields, projects = search_query(client=client, entity='projects', pattern=pattern,
                                          processing_step_name='*',
                                          order=order, limit=limit, fields=fields, show_archived=show_archived, **kwargs)
    if flatten:
        projects = flatten_results(projects, query_fields)
    return projects


def get_subprojects(client,
                    pattern,
                    order=None,
                    limit=None,
                    fields=None,
                    flatten=False,
                    show_archived=False,
                    **kwargs):
    if 'write_status' not in kwargs:
        kwargs['write_status'] = 'valid'
    query_fields, projects = search_query(client=client, entity='subProjects', pattern=pattern,
                                          processing_step_name='*',
                                          order=order, limit=limit, fields=fields, show_archived=show_archived, **kwargs)
    if flatten:
        projects = flatten_results(projects, query_fields)
    return projects


def get_prodsteps(client,
                  pattern,
                  order=None,
                  limit=None,
                  fields=None,
                  flatten=False,
                  show_archived=False,
                  **kwargs):
    if 'write_status' not in kwargs:
        kwargs['write_status'] = 'valid'
    query_fields, steps = search_query(client=client, entity='productionStep', pattern=pattern,
                                       processing_step_name='*',
                                       order=order, limit=limit, fields=fields, show_archived=show_archived, **kwargs)
    if flatten:
        steps = flatten_results(steps, query_fields)
    return steps


def get_datasets(client,
                 pattern,
                 parent_type=None,
                 order=None,
                 limit=None,
                 fields=None,
                 flatten=False,
                 show_archived=False,
                 **kwargs):
    """
    Return list of datasets matching pattern
    """
    if 'ami_status' not in kwargs:
        kwargs['ami_status'] = 'VALID'
    cmd_args = {}
    if parent_type is not None and 'parent_type' not in kwargs:
        cmd_args['parentType'] = parent_type
    pattern = __clean_dataset(pattern)
    query_fields, datasets = search_query(client=client,
                                          cmd='DatasetSearchQuery',
                                          cmd_args=cmd_args,
                                          entity='dataset',
                                          pattern=pattern,
                                          order=order, limit=limit,
                                          fields=fields,
                                          show_archived=show_archived, **kwargs)
    if flatten:
        datasets = flatten_results(datasets, query_fields)
    return datasets


def get_periods_for_run(client, run):
    """
    Return data periods which contain this run
    """
    result = client.execute(['GetDataPeriodsForRun', '-runNumber=%i' % run])
    periods = sorted([RunPeriod(level=int(e['periodLevel']), name=str(e['period']), project=str(e['project'])) \
                      for e in result.to_dict()['Element_Info'].values() ])
    return periods


def get_periods(client, year=YEAR, level=2):
    """
    Return all periods at a specified detail level in the given year
    """
    cmd = ['ListDataPeriods', '-createdSince=2009-01-01 00:00:00' ]
    if year > 2000:
        year %= 1000
    cmd += [ '-projectName=data%02i%%' % year]
    if level in [1, 2, 3]:
        cmd += [ '-periodLevel=%i' % level ]
    else:
        raise ValueError('level must be 1, 2, or 3')
    result = client.execute(cmd)
    periods = [RunPeriod(project=e['projectName'],
                      year=year,
                      name=str(e['period']),
                      level=level,
                      status=e['status'],
                      description=e['description']) \
            for e in result.to_dict()['Element_Info'].values()]
    periods.sort()
    return periods


def get_all_periods(client):
    """
    Return all periods
    """
    all_periods = []
    p = re.compile("(?P<period>(?P<periodletter>[A-Za-z]+)(?P<periodnumber>\d+)?)$")
    result = get_periods(client, year=0, level=0)
    for period, projectName in result:
        m = p.match(period)
        if not m:
            continue
        year = int(projectName[4:6])
        period_letter = m.group('periodletter')
        if m.group('periodnumber'):
            period_number = int(m.group('periodnumber'))
        else:
            period_number = 0
        if len(period_letter) != 1:
            pc = 0
        else:
            pc = 10000 * year + 100 * (ord(period_letter.upper()) - 65) + period_number
        all_periods += [ ((year, period, pc), projectName + ".period" + period) ]
    all_periods.sort()
    return all_periods


def print_periods(periods, wrap_desc=True, wrap_width=50, stream=None):

    if stream is None:
        stream = sys.stdout
    table = [['Project', 'Name', 'Status', 'Description']]
    for period in periods:
        table.append([period.project,
                      period.name,
                      period.status,
                      period.description])
    print_table(table,
                wrap_last=wrap_desc,
                wrap_width=wrap_width,
                vsep='-',
                stream=stream)


def get_runs(client, periods=None, year=YEAR):
    """
    Return all runs contained in the given periods in the specified year
    """
    if year > 2000:
        year %= 1000
    if not periods:
        periods = [period.name for period in get_periods(client, year=year, level=1)]
    elif isinstance(periods, basestring):
        periods = periods.split(',')
    runs = []
    # remove duplicate periods
    for period in set(periods):
        cmd = ['GetRunsForDataPeriod', '-period=%s' % period]
        cmd += [ '-projectName=data%02i%%' % year ]
        result = client.execute(cmd)
        runs += [ int(e['runNumber']) for e in result.to_dict()['Element_Info'].values() ]
    # remove duplicates
    runs = list(set(runs))
    runs.sort()
    return runs


def get_provenance(client, dataset, type=None, **kwargs):
    """
    Return all parent dataset of the given dataset
    """
    dataset = __clean_dataset(dataset)
    args = ["ListDatasetProvenance",
            "logicalDatasetName=%s" % dataset,
            'output=xml']
    if kwargs:
        args += ['%s=%s' % item for item in kwargs.items()]
    result = client.execute(args)
    dom = result.dom
    graph = dom.getElementsByTagName('graph')
    dictOfLists = {}
    for line in graph:
        nodes = line.getElementsByTagName('node')
        for node in nodes:
            level = int(node.attributes['level'].value)
            dataset = node.attributes['name'].value
            if type and (type in dataset):
                levelList = dictOfLists.get(level, [])
                levelList.append(dataset)
                dictOfLists[level] = levelList
            elif not type:
                levelList = dictOfLists.get(level, [])
                levelList.append(dataset)
                dictOfLists[level] = levelList
    return dictOfLists


def print_provenance(result):

    for key in sorted(result.keys()):
        print "generation =", key
        for dataset in sorted(result[key]):
            print " ", dataset


def get_dataset_info(client, dataset, **kwargs):
    """
    Return a DatasetInfo instance (the dataset metadata)

    *client*: AMIClient

    *dataset*: str

    *kwargs*: dict
    """
    dataset = __clean_dataset(dataset)
    args = ["GetDatasetInfo",
            "logicalDatasetName=%s" % dataset]
    if kwargs:
        args += ['%s=%s' % item for item in kwargs.items()]
    dataset_info = DatasetInfo(dataset=dataset)
    result = client.execute(args)
    dom = result.dom
    # get the rowsets
    rowsets = dom.getElementsByTagName('rowset')
    for rowset in rowsets:
        rowsetLabel = ""
        if "type" in rowset.attributes.keys():
            rowsetLabel = rowsetLabel + rowset.attributes['type'].value
            rows = rowset.getElementsByTagName('row')
            if (rowsetLabel == "Element_Info"):
                for row in rows:
                    fields = row.getElementsByTagName("field")
                    for field in fields:
                        if field.firstChild:
                            tableName = field.attributes['table'].value
                            if tableName == "dataset":
                                value = field.firstChild.nodeValue
                                name = field.attributes['name'].value
                                dataset_info.info[name] = value
                            elif tableName == "dataset_extra":
                                value = field.firstChild.nodeValue
                                name = field.attributes['name'].value
                                dataset_info.extra[name] = value
                            elif (tableName == "dataset_added_comment") or \
                                 (tableName == "dataset_comment"):
                                value = field.firstChild.nodeValue
                                name = field.attributes['name'].value
                                dataset_info.comments[name] = value
                            elif (tableName == "dataset_property"):
                                propertyName = field.attributes['name'].value.split('_')[0]
                                if propertyName in dataset_info.properties:
                                    tmpDict = dataset_info.properties[propertyName]
                                else:
                                    tmpDict = {"type": "",
                                               "min": "",
                                               "max": "",
                                               "unit": "",
                                               "description": ""}
                                propertyNameSubField = field.attributes['name'].value
                                try:
                                    propertyNameSubValue = field.firstChild.nodeValue
                                except:
                                    propertyNameSubValue = ""
                                if propertyNameSubField == propertyName + "_type":
                                    tmpDict["type"] = propertyNameSubValue
                                if propertyNameSubField == propertyName + "_min":
                                    tmpDict["min"] = propertyNameSubValue
                                if propertyNameSubField == propertyName + "_max":
                                    tmpDict["max"] = propertyNameSubValue
                                if propertyNameSubField == propertyName + "_unit":
                                    tmpDict["unit"] = propertyNameSubValue
                                if propertyNameSubField == propertyName + "_desc":
                                    tmpDict["description"] = propertyNameSubValue
                                dataset_info.properties[propertyName] = tmpDict
    return dataset_info


def get_event_info(client, dataset, **kwargs):
    """
    Return the metadata of the parent event generator dataset

    *client*: AMIClient

    *dataset*: str

    *kwargs*: dict
    """
    dataset = __clean_dataset(dataset)
    if 'EVNT' not in dataset:
        prov = get_provenance(client, dataset, type='EVNT', **kwargs)
        evgen_datasets = []
        for key, dsets in prov.items():
            evgen_datasets += dsets
    else:
        evgen_datasets = [dataset]
    results = []
    for dset in set(evgen_datasets):
        results.append(get_dataset_info(client, dset, **kwargs))
    return results


def get_dataset_xsec_effic(client, dataset, **kwargs):
    """
    Return the cross section and generator filter efficiency

    *client*: AMIClient

    *dataset*: str

    *kwargs*: dict
    """
    infos = get_event_info(client, dataset, **kwargs)
    if len(infos) > 1:
        raise ValueError('Dataset %s has multiple parent event generator datasets' % dataset)
    elif not infos:
        raise ValueError('Event info not found for dataset %s' % dataset)
    info = infos[0]
    try:
        xsec = float(info.extra['crossSection_mean'])
    except KeyError:
        raise ValueError('No cross section listed for dataset %s' % dataset)
    try:
        effic = float(info.extra['GenFiltEff_mean'])
    except KeyError:
        raise ValueError('No generator filter efficiency listed for dataset %s' % dataset)
    return xsec, effic


def get_dataset_xsec_min_max_effic(client, dataset, **kwargs):
    """
    Return the cross section mean, min, max, and generator filter efficiency

    *client*: AMIClient

    *dataset*: str

    *kwargs*: dict
    """
    infos = get_event_info(client, dataset, **kwargs)
    if len(infos) > 1:
        raise ValueError('Dataset %s has multiple parent event generator datasets' % dataset)
    elif not infos:
        raise ValueError('Event info not found for dataset %s' % dataset)
    info = infos[0]
    try:
        xsec = float(info.extra['crossSection_mean'])
    except KeyError:
        raise ValueError('No cross section listed for dataset %s' % dataset)
    try:
        xsec_min = float(info.properties['crossSection']['min'])
        xsec_max = float(info.properties['crossSection']['max'])
    except KeyError:
        raise ValueError('No cross section min or max listed for dataset %s' % dataset)
    try:
        effic = float(info.extra['GenFiltEff_mean'])
    except KeyError:
        raise ValueError('No generator filter efficiency listed for dataset %s' % dataset)
    return xsec, xsec_min, xsec_max, effic


def get_data_datasets(client,
                      tag_pattern=None,
                      periods=None,
                      project=PROJECT,
                      stream=STREAM,
                      type=TYPE,
                      prod_step=PRODSTEP,
                      parent_type=None,
                      grl=None,
                      fields=None,
                      latest=False,
                      flatten=False,
                      **kwargs
                     ):
    """
    *client*: AMIClient

    *tag_pattern*: [ str | None ]

    *periods*: [ list | tuple | str | None ]

    *project*: str

    *stream*: str

    *type*: str

    *prod_step*: str

    *parent_type*: str

    *fields*: [ list | tuple | str | None ]

    *latest*: bool

    *flatten*: bool

    Returns a list of dicts if flatten==False
    else list of tuples with elements in same order as fields
    """

    """
        Transmit period(s) as kwargs in order to do only one query
    """
    if periods is not None:
        if isinstance(periods, basestring):
            periods = periods.split(',')
        kwargs['period'] = periods

    if grl is not None:
        # need to be compatible with Python 2.4
        # so no ElementTree here...
        from xml.dom import minidom
        doc = minidom.parse(grl)
        run_nodes = doc.getElementsByTagName('Run')
        runs = []
        for node in run_nodes:
            runs.append(int(node.childNodes[0].data))
        kwargs['run'] = runs

    datasets = get_datasets(client, tag_pattern, fields=fields,
                            project=project, stream=stream, type=type,
                            prod_step=prod_step,
                            parent_type=parent_type,
                            **kwargs)

    if latest:
        if type.startswith('NTUP'):
            VERSION_PATTERN = NTUP_VERSION_PATTERN
        elif type.startswith('AOD'):
            VERSION_PATTERN = AOD_VERSION_PATTERN
        elif type.startswith('ESD'):
            VERSION_PATTERN = ESD_VERSION_PATTERN
        else:
            raise TypeError('\'latest\' not implemented for type %s' % type)
        ds_unique = {}
        for ds in datasets:
            name = ds['logicalDatasetName']
            match = re.match(DATA_PATTERN, name)
            if match:
                new_version = re.match(VERSION_PATTERN, match.group('version'))
                if not new_version:
                    continue
                run = int(match.group('run'))
                if run not in ds_unique:
                    ds_unique[run] = ds
                else:
                    curr_version = re.match(VERSION_PATTERN, re.match(DATA_PATTERN, ds_unique[run]['logicalDatasetName']).group('version'))
                    if type.startswith('NTUP'):
                        if new_version.group('la') == 'r' and curr_version.group('la') == 'f' or \
                           ((new_version.group('la') == curr_version.group('la') and \
                             int(new_version.group('lb')) >= int(curr_version.group('lb')) and \
                             int(new_version.group('mb')) >= int(curr_version.group('mb')) and \
                             int(new_version.group('rb')) >= int(curr_version.group('rb')))):
                            ds_unique[run] = ds
                    elif type.startswith('AOD'):
                        if new_version.group('la') == 'r' and curr_version.group('la') == 'f' or \
                           ((new_version.group('la') == curr_version.group('la') and \
                             int(new_version.group('lb')) >= int(curr_version.group('lb')) and \
                             int(new_version.group('mb')) >= int(curr_version.group('mb')))):
                            ds_unique[run] = ds
                    elif type.startswith('ESD'):
                        if new_version.group('la') == 'r' and curr_version.group('la') == 'f' or \
                           ((new_version.group('la') == curr_version.group('la') and \
                             int(new_version.group('lb')) >= int(curr_version.group('lb')))):
                            ds_unique[run] = ds
        datasets = ds_unique.values()
        datasets.sort()
    if flatten:
        fields = parse_fields(fields, DATASET_TABLE)
        fields.append('logicalDatasetName')
        return flatten_results(datasets, fields)
    return datasets


# does not work...
def get_configtagfields(client, tag, *args, **kwargs):
    """
    *client*: AMIClient

    *tag*: str

    *args*: tuple
        tuple of args to add to AMI command

    *kwargs*: dict
        dict of keyword args to add to AMI commmand as key=value
    """
    argv = ['ListConfigTagFields',
            'configTag=%s' % tag]
    argv.extend(args)
    for name, value in kwargs.items():
        argv.append("%s='%s'" % (name, value))
    result = client.execute(argv)
    return result


def get_configtags(client, tag, *args, **kwargs):
    """
    *client*: AMIClient

    *tag*: str

    *args*: tuple
        tuple of args to add to AMI command

    *kwargs*: dict
        dict of keyword args to add to AMI commmand as key=value
    """
    argv = ['ListConfigurationTag',
            'configTag=%s' % tag]
    argv.extend(args)
    for name, value in kwargs.items():
        argv.append("%s='%s'" % (name, value))
    result = client.execute(argv)
    return [row for row in result.rows()]


def get_files(client, dataset, limit=None):
    """
    *client*: AMIClient

    *dataset*: str

    *limit*: [ tuple | list | int | None ]
    """
    dataset = __clean_dataset(dataset)
    args = ['ListFiles', 'logicalDatasetName=%s' % dataset]
    if limit is not None:
        if isinstance(limit, (list, tuple)):
            limit = 'limit=%i,%i' % tuple(limit)
        else:
            limit = 'limit=0,%i' % limit
        args.append(limit)
    result = client.execute(args)
    return result.rows()


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


def list_files(client, dataset, limit=None, total=False, human_readable=False, long=False, stream=None):
    """
    *client*: AMIClient

    *dataset*: str

    *limit*: [ tuple | list | int | None ]

    *total*: bool

    *human_readable*: bool

    *long*: bool

    *stream*: file
    """
    if stream is None:
        stream = sys.stdout
    if long:
        table = []
        total_size = 0
        total_events = 0
        for file in get_files(client, dataset, limit=limit):
            size = file['fileSize']
            if size != 'NULL':
                total_size += int(size)
                if human_readable:
                    size = humanize_bytes(int(size))
            events = file['events']
            if events != 'NULL':
                total_events += int(events)
            table.append(["size: %s" % size, "events: %s" % events, file['LFN'], "GUID: %s" % file['fileGUID']])
        if total:
            if human_readable:
                total_size = humanize_bytes(total_size)
            table.append(["size: %s" % total_size, "events: %i" % total_events, "total", ""])
        print_table(table, stream=stream)
    else:
        for file in get_files(client, dataset, limit=limit):
            print >> stream, file['LFN']


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
