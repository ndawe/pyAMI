
class Table(object):

    pass


class PRODSTEP(Table):

    fields = {
        'name': 'productionStepName',
        'tag': 'productionStepTag',
        'write_status': 'writeStatus',
        'read_status': 'readStatus'
    }

    primary = 'productionStepName'

    foreign = None


class FILE(Table):

    fields = {
        'lfn': 'LFN',
        'guid': 'fileFUID',
        'events': 'events',
        'size': 'fileSize'
    }

    primary = 'lfn'

    foreign = None


class DATASET(Table):

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
        'prod_step': 'productionStep',
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
    }

    primary = 'logicalDatasetName'

    foreign = {
        'files': FILE
    }


class NOMENCLATURE(Table):

    fields = {
        'template': 'nomenclatureTemplate',
        'name': 'nomenclatureName',
        'tag': 'nomenclatureTag',
        'write_status': 'writeStatus',
        'read_status': 'readStatus',
    }

    primary = 'nomenclatureName'

    foreign = None


class PROJECT(Table):

    fields = {
        'tag': 'projectTag',
        'description': 'description',
        'is_base_type': 'isBaseType',
        'read_status': 'readStatus',
        'write_status': 'writeStatus',
        'manager': 'projectManager',
    }

    primary = 'projectTag'

    foreign = {
        'nomenclature': NOMENCLATURE
    }


class SUBPROJECT(Table):

    fields = {
        'tag': 'subProjectTag',
        'description': 'description',
        'is_base_type': 'isBaseType',
        'read_status': 'readStatus',
        'write_status': 'writeStatus',
        'manager': 'projectManager',
    }

    primary = 'subProjectTag'

    foreign = {
        'nomenclature': NOMENCLATURE
    }


class TYPE(Table):

    fields = {
        'type': 'dataType',
        'description': 'description',
        'write_status': 'writeStatus',
        'read_status': 'readStatus',
    }

    primary = 'dataType'

    foreign = None


class SUBTYPE(Table):

    fields = {
        'type': 'subDataType',
        'description': 'description',
        'write_status': 'writeStatus',
        'read_status': 'readStatus',
    }

    primary = 'subDataType'

    foreign = None


TABLES = {
    'data_type': TYPE,
    'subData_type': SUBTYPE,
    'projects': PROJECT,
    'subProjects': SUBPROJECT,
    'dataset': DATASET,
    'nomenclature': NOMENCLATURE,
    'productionStep': PRODSTEP
}
