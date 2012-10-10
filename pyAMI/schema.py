
class Table(object):

    defaults = {}


class PRODSTEP_TABLE(Table):

    fields = {
        'name': 'productionStepName',
        'tag': 'productionStepTag',
        'write_status': 'writeStatus',
        'read_status': 'readStatus'
    }

    defaults = {
        'write_status': 'valid',
    }

    primary = 'productionStepName'

    foreign = None


class FILE_TABLE(Table):

    fields = {
        'lfn': 'LFN',
        'guid': 'fileFUID',
        'events': 'events',
        'size': 'fileSize'
    }

    primary = 'lfn'

    foreign = None


class DATASET_TABLE(Table):

    fields = {
        'ami_status': 'amiStatus',
        'nfiles': 'nFiles',
        'events': 'totalEvents',
        'type': 'dataType',
        'prodsys_status': 'prodsysStatus',
        'geometry': 'geometryVersion',
        'version': 'version',
        'transformation': 'TransformationPackage',
        'trigger_config': 'triggerConfig',
        'atlas_release': 'AtlasRelease',
        'job_config': 'jobConfig',
        'project': 'projectName',
        'dataset_number': 'datasetNumber',
        'modified': 'lastModified',
        #'modified-after': 'lastModified>',
        #'modified-before': 'lastModified<',
        'physics_short': 'physicsShort',
        'history': 'productionHistory',
        'prod_step': 'prodStep',
        'requested_by': 'requestedBy',
        'name': 'logicalDatasetName',
        'responsible': 'physicistResponsible',
        'physics_comment': 'physicsComment',
        'modified_by': 'modifiedBy',
        'trash_annotation': 'trashAnnotation',
        'physics_category': 'physicsCategory',
        'trash_date': 'trashDate',
        'trash_trigger': 'trashTrigger',
        'physics_process': 'physicsProcess',
        'principal_physics_group': 'principalPhysicsGroup',
        'created': 'created',
        'created_by': 'createdBy',
        'creation_comment': 'creationComment',
        'stream': 'streamName',
        'in_container': 'inContainer',
        'run': 'runNumber',
        'period': 'period',
        'beam': 'beamType',
        'conditions_tag': 'conditionsTag',
    }

    defaults = {
        'ami_status': 'VALID',
    }

    primary = 'logicalDatasetName'

    foreign = {
        'files': FILE_TABLE
    }


class NOMENCLATURE_TABLE(Table):

    fields = {
        'template': 'nomenclatureTemplate',
        'name': 'nomenclatureName',
        'tag': 'nomenclatureTag',
        'write_status': 'writeStatus',
        'read_status': 'readStatus',
    }

    defaults = {
        'write_status': 'valid',
    }

    primary = 'nomenclatureName'

    foreign = None


class PROJECT_TABLE(Table):

    fields = {
        'tag': 'projectTag',
        'description': 'description',
        'is_base_type': 'isBaseType',
        'read_status': 'readStatus',
        'write_status': 'writeStatus',
        'manager': 'projectManager',
    }

    defaults = {
        'write_status': 'valid',
    }

    primary = 'projectTag'

    foreign = {
        'nomenclature': NOMENCLATURE_TABLE
    }


class SUBPROJECT_TABLE(Table):

    fields = {
        'tag': 'subProjectTag',
        'description': 'description',
        'is_base_type': 'isBaseType',
        'read_status': 'readStatus',
        'write_status': 'writeStatus',
        'manager': 'projectManager',
    }

    defaults = {
        'write_status': 'valid',
    }

    primary = 'subProjectTag'

    foreign = {
        'nomenclature': NOMENCLATURE_TABLE
    }


class TYPE_TABLE(Table):

    fields = {
        'type': 'dataType',
        'description': 'description',
        'write_status': 'writeStatus',
        'read_status': 'readStatus',
    }

    defaults = {
        'write_status': 'valid',
    }

    primary = 'dataType'

    foreign = None


class SUBTYPE_TABLE(Table):

    fields = {
        'type': 'subDataType',
        'description': 'description',
        'write_status': 'writeStatus',
        'read_status': 'readStatus',
    }

    defaults = {
        'write_status': 'valid',
    }

    primary = 'subDataType'

    foreign = None


TABLES = {
    'data_type': TYPE_TABLE,
    'subData_type': SUBTYPE_TABLE,
    'projects': PROJECT_TABLE,
    'subProjects': SUBPROJECT_TABLE,
    'dataset': DATASET_TABLE,
    'nomenclature': NOMENCLATURE_TABLE,
    'productionStep': PRODSTEP_TABLE,
}
