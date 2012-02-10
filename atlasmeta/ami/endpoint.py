
class AMIEndPoint:

    type = "main"

    @staticmethod
    def getEndPoint():

        if AMIEndPoint.getType() == "replica":
            return "https://atlas-ami.cern.ch/AMI/services/AMIWebService"
        else:
            return "https://ami.in2p3.fr/AMI/services/AMIWebService"

    @staticmethod
    def getXSLURL():

        if AMIEndPoint.getType() == "replica":
            return "https://atlas-ami.cern.ch/AMI/AMI/xsl/"
        else:
            return "https://ami.in2p3.fr/AMI/AMI/xsl/"

    @staticmethod
    def setType(newType):

        AMIEndPoint.type = newType
        return

    @staticmethod
    def getType():

        return AMIEndPoint.type
