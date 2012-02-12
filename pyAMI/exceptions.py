
class _AMI_Error_Base(Exception):
    """
    Simple wrapper for errors.
    """
    def __init__(self, msg=None):

        if msg is None:
            self.errMsg = ''
        else:
            self.errMsg = msg

    def __repr__(self):

        return self.errMsg

    def __str__(self):

        return self.errMsg


class AMI_Info(_AMI_Error_Base):
    """
    Simple wrapper to show AMI information.
    """
    pass


class AMI_Error(_AMI_Error_Base):

    pass


class AMI_Info(_AMI_Error_Base):

    pass
