
TYPE = 'main'


def get_endpoint():

    if TYPE == "replica":
        return "https://atlas-ami.cern.ch:8443/AMI/services/AMIWebService"
    else:
        return "https://ami.in2p3.fr/AMI/services/AMIWebService"


def get_XSL_URL():

    if TYPE == "replica":
        return "https://atlas-ami.cern.ch:8443/AMI/AMI/xsl/"
    else:
        return "https://ami.in2p3.fr/AMI/AMI/xsl/"
