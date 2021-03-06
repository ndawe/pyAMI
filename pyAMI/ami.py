#!/usr/bin/env python

# Author: Noel Dawe

import os
import sys

if 'PYAMI_LIBRARY_PATH' in os.environ:
    sys.path.insert(0, os.environ['PYAMI_LIBRARY_PATH'])

from pyAMI.extern import argparse
import pyAMI
from pyAMI.info import VERSION, AUTHOR_EMAIL, URL
from pyAMI.query import *
from pyAMI.schema import *
from pyAMI.defaults import YEAR, PROJECT, STREAM, TYPE, PRODSTEP
from pyAMI.xslt import XSLT
from pyAMI import userdata


class formatter_class(argparse.ArgumentDefaultsHelpFormatter,
                      argparse.RawTextHelpFormatter):
    pass


class CreditsAction(argparse.Action):

    def __init__(self,
                 option_strings,
                 version=None,
                 dest=argparse.SUPPRESS,
                 default=argparse.SUPPRESS,
                 help=None):

        super(CreditsAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)
        self.version = version

    def __call__(self, parser, namespace, values, option_string=None):

        parser.exit(message=pyAMI.info.__doc__)


parser = argparse.ArgumentParser(
    formatter_class=formatter_class,
    description=("documentation can be found here: %s\n"
                 "please send questions to %s")
                 % (URL, AUTHOR_EMAIL))
parser.add_argument('-v', '--verbose', action='store_true', default=False,
                    help="show verbose output")
parser.add_argument('-d', '--debug', action='store_true', default=False,
                    help="show a stack trace")
parser.add_argument('-f', '--format',
                    dest='output',
                    default='text',
                    choices=XSLT.keys(),
                    help="format of verbose output")
parser.add_argument('-s', '--server',
                    help="set the server", choices=('main', 'replica'),
                    default='main')
parser.add_argument('--version', action='version', version=VERSION,
                    help="show the version number and exit")
parser.add_argument('--credits', action=CreditsAction,
                    help="show the credits and exit")
subparsers = parser.add_subparsers()

"""
Authorize
"""
parser_auth = subparsers.add_parser('auth')
parser_auth.set_defaults(op='auth')

"""
List
"""
parser_list = subparsers.add_parser('list')
subparsers_list = parser_list.add_subparsers()

def search_query_args(parser, entity, include_pattern=True):

    for field in entity.fields.keys():
        option = '--%s' % field.replace('_','-')
        if not parser._get_option_tuples(option):
            parser.add_argument(option,
                    default=entity.defaults.get(field, None))
    if entity.foreign is not None:
        for name, foreign_entity in entity.foreign.items():
            for field in foreign_entity.fields.keys():
                option = '--%s' % (('%s.%s' % (name, field)).replace('_','-'))
                if not parser._get_option_tuples(option):
                    parser.add_argument(option,
                            default=None) # don't use foreign default here
    parser.add_argument('-o', '--order', default=None,
                        help="order results by this field")
    parser.add_argument('-l', '--limit', type=int, default=None,
                        help="limit number of results")
    parser.add_argument('-f', '--fields', default=None,
                        help="extra fields (comma-separated) to display in output")
    parser.add_argument('--show-archived', action='store_true',
                        default=False, help="search in archived catalogues as well")
    if include_pattern:
        parser.add_argument('pattern', help="matches must contain this pattern (glob with %%)",
                            default='%', nargs='?')
    parser.set_defaults(flatten=True)
    parser.set_defaults(op=get_datasets)
    parser.set_defaults(pr=print_table)

parser_list_datasets = subparsers_list.add_parser('datasets',
    description="List datasets matching a given pattern")
search_query_args(parser_list_datasets, DATASET_TABLE)
parser_list_datasets.add_argument('--parent-type', default=None)
parser_list_datasets.add_argument('-L', '--literal-match',
    action='store_true', default=False,
    help="perform a literal match where all "
         "results must be identical to the query string")
parser_list_datasets.add_argument('-F', '--from-file',
    action='store_true', default=False,
    help="read patterns from file "
         "(ignore empty lines and lines beginning with #)")
parser_list_datasets.set_defaults(op=get_datasets)

parser_list_types = subparsers_list.add_parser('types',
    description="List ATLAS data types")
search_query_args(parser_list_types, TYPE_TABLE)
parser_list_types.set_defaults(op=get_types)

parser_list_subtypes = subparsers_list.add_parser('subtypes',
    description="List ATLAS data subtypes")
search_query_args(parser_list_subtypes, SUBTYPE_TABLE)
parser_list_subtypes.set_defaults(op=get_subtypes)

parser_list_nomens = subparsers_list.add_parser('nomenclatures',
    description="List ATLAS nomenclatures")
search_query_args(parser_list_nomens, NOMENCLATURE_TABLE)
parser_list_nomens.set_defaults(op=get_nomenclatures)

parser_list_prodsteps = subparsers_list.add_parser('prodsteps',
    description="List ATLAS production steps")
search_query_args(parser_list_prodsteps, PRODSTEP_TABLE)
parser_list_prodsteps.set_defaults(op=get_prodsteps)

parser_list_projects = subparsers_list.add_parser('projects',
    description="List ATLAS projects")
search_query_args(parser_list_projects, PROJECT_TABLE)
parser_list_projects.set_defaults(op=get_projects)

parser_list_subprojects = subparsers_list.add_parser('subprojects',
    description="List ATLAS subprojects")
search_query_args(parser_list_subprojects, SUBPROJECT_TABLE)
parser_list_subprojects.set_defaults(op=get_subprojects)

parser_list_data_datasets = subparsers_list.add_parser('data',
    description="List data datasets",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser_list_data_datasets.add_argument('-p', '--project', default=PROJECT,
                                       help='data project name')
parser_list_data_datasets.add_argument('--parent-type', default=None)
parser_list_data_datasets.add_argument('-s', '--stream', default=STREAM,
                                       help='data stream')
parser_list_data_datasets.add_argument('-t', '--type', default=TYPE,
                                       help='data type')
parser_list_data_datasets.add_argument('--prod-step', default=PRODSTEP,
                                       help='production step')
parser_list_data_datasets.add_argument('--periods', help='data periods',
                                       default=None)
parser_list_data_datasets.add_argument('--grl', default=None,
                                       help='only show runs in the specified good runs list')
parser_list_data_datasets.add_argument('--latest', action='store_true',
                                       help="only show latest version of datasets", default=False)
parser_list_data_datasets.add_argument('tag_pattern', metavar='PATTERN',
                                       help="match tags with pattern (glob with %%)", default=None, nargs='?')
search_query_args(parser_list_data_datasets, DATASET_TABLE, include_pattern=False)
parser_list_data_datasets.set_defaults(flatten=True)
parser_list_data_datasets.set_defaults(op=get_data_datasets)
parser_list_data_datasets.set_defaults(pr=print_table)

parser_list_periods = subparsers_list.add_parser('periods',
    description="List periods at a specified detail level for a given year",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser_list_periods.add_argument('-y', '--year', type=int, default=YEAR)
parser_list_periods.add_argument('-l', '--level', type=int, default=2, help="1 (high), 2 (default), or 3 (low)")
parser_list_periods.set_defaults(op=get_periods)
parser_list_periods.set_defaults(pr=str)

parser_list_runs = subparsers_list.add_parser('runs',
    description="List runs in a data period for a given year",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser_list_runs.add_argument('-y', '--year', type=int, default=YEAR,
                              help='year')
parser_list_runs.add_argument('periods', help="period name(s) i.e. M1 M2", nargs='*')
parser_list_runs.set_defaults(op=get_runs)
parser_list_runs.set_defaults(pr=str)


parser_list_files = subparsers_list.add_parser('files', add_help=False,
    description="List files in dataset or container")
parser_list_files.add_argument('--help', action='help',
                               help="show this help message and exit")
parser_list_files.add_argument('--limit', type=int, default=None, help="limit number of results")
parser_list_files.add_argument('-c', '--total',
                               action='store_true', default=False,
                               help="produce a grand total")
parser_list_files.add_argument('-h', '--human-readable', dest='human_readable',
                               action='store_true', default=False,
                               help="print sizes in human readable format")
parser_list_files.add_argument('-l', dest='long', action='store_true',
                               default=False, help="display verbose output")
parser_list_files.add_argument('dataset', help="either a dataset container name or a TID dataset name")
parser_list_files.set_defaults(op=list_files)
parser_list_files.set_defaults(pr=None)

"""
Dataset
"""
parser_dataset = subparsers.add_parser('dataset')
subparsers_dataset = parser_dataset.add_subparsers()

parser_dataset_prov = subparsers_dataset.add_parser('prov',
    description="List the provenance for a dataset")
parser_dataset_prov.add_argument('--type', default=None)
parser_dataset_prov.add_argument('dataset', help="full name of dataset")
parser_dataset_prov.set_defaults(op=get_provenance)
parser_dataset_prov.set_defaults(pr=print_provenance)

parser_dataset_info = subparsers_dataset.add_parser('info',
    description="Display dataset metadata")
parser_dataset_info.add_argument('dataset', help="full name of dataset")
parser_dataset_info.set_defaults(op=get_dataset_info)
parser_dataset_info.set_defaults(pr=str)

parser_dataset_evtinfo = subparsers_dataset.add_parser('evtinfo',
    description="Display metadata of parent event generator dataset")
parser_dataset_evtinfo.add_argument('dataset', help="full name of dataset")
parser_dataset_evtinfo.set_defaults(op=get_event_info)
parser_dataset_evtinfo.set_defaults(pr=str)

"""
Config tags
"""
parser_configtag = subparsers.add_parser('config-tag')
parser_configtag.add_argument('tag', help="config tag")
parser_configtag.set_defaults(op=get_configtags)
parser_configtag.set_defaults(pr=print_dict)

'''
parser_configtagfields = subparsers.add_parser('config-tag-fields')
parser_configtagfields.add_argument('tag', help="config tag")
parser_configtagfields.set_defaults(op=get_configtagfields)
parser_configtagfields.set_defaults(pr=str)
'''

"""
Add
"""
"""
parser_add = subparsers.add_parser('add')
parser_add.add_argument('args', nargs='+')
parser_add.set_defaults(op=add_datatype)
"""

"""
Trash
"""
"""
parser_trash = subparsers.add_parser('trash')
parser_trash.add_argument('args', nargs='+')
parser_trash.set_defaults(op=None)
"""

"""
Update
"""
"""
parser_update = subparsers.add_parser('update')
parser_update.add_argument('args', nargs='+')
parser_update.set_defaults(op=None)
"""

"""
default -> raw ami command
"""
parser_command = subparsers.add_parser('cmd', description="A raw ami command to execute")
parser_command.add_argument('amiCommand', nargs=1, help="An AMI command (mandatory)")
parser_command.add_argument('args', nargs=argparse.REMAINDER, help="Some arguments (optional)")
parser_command.set_defaults(op='exec')
parser_command.set_defaults(pr=None)

"""
Reset to default settings and remove user config data
"""
parser_reset = subparsers.add_parser('reset',
                    description="Reset to default settings "
                                "and remove user config data")
parser_reset.set_defaults(op=userdata.reset)


def ami():

    args = parser.parse_args()

    from pyAMI import endpoint
    # this must be done before an import of webservices anywhere
    endpoint.TYPE = args.server

    from pyAMI.auth import AMI_CONFIG, create_auth_config
    from pyAMI.client import AMIClient, AMIResult
    from pyAMI.exceptions import AMI_Error

    if args.op == 'exec':
        args.op = AMIClient.execute

    try:
        if args.op == 'auth':
            create_auth_config()
        elif args.op == userdata.reset:
            userdata.reset()
        else:
            amiclient = AMIClient(verbose=args.verbose,
                                  verbose_format=args.output)
            cmd_args = dict(args._get_kwargs())
            del cmd_args['op']
            del cmd_args['pr']
            del cmd_args['verbose']
            del cmd_args['debug']
            del cmd_args['output']
            del cmd_args['server']
            if 'help' in cmd_args:
                del cmd_args['help']
            if 'amiCommand' in cmd_args:
                cmd_args['args'] = cmd_args['amiCommand'] + cmd_args['args']
                del cmd_args['amiCommand']
            result = args.op(amiclient, **cmd_args)
            if args.op == get_periods:
                print_periods(result)
            elif isinstance(result, AMIResult):
                print result.output(xslt=args.output)
            elif args.pr and result:
                if args.pr == print_table:
                    args.pr(result)
                elif isinstance(result, (list, tuple)):
                    for thing in result:
                        rep = args.pr(thing)
                        if rep:
                            print rep
                else:
                    rep = args.pr(result)
                    if rep is not None:
                        print rep

    except KeyboardInterrupt:
        sys.exit('\n')

    except Exception, e:
        if args.debug:
            # If in debug mode show full stack trace
            import traceback
            traceback.print_exception(*sys.exc_info())
        elif isinstance(e, AMI_Error):
            sys.exit(str(e))
        else:
            sys.exit("%s: %s" % (e.__class__.__name__, e))

if __name__ == '__main__':
    ami()
