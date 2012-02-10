
import sys, os
from .webservices import *
from .exceptions import *
from cStringIO import StringIO
#from xml.sax import make_parser, saxutils, xmlreader
import re
from sys import stdout
from .config import AMIConfig
from xml.dom import minidom, Node
#from Ft.Xml.Xslt import Transform
import cPickle as pickle
from .endpoint import AMIEndPoint
import base64


def tutorial():
    return """
    This is the generic way of sending a command to the AMI server.
    The first argument must be the name of the server command.
    The other arguments follow as argumentName=argumentValue pairs.
    For complete help see the PyAMI User guide
    http://ami.in2p3.fr/opencms/opencms/AMI/www/Client/pyAMIUserGuide.pdf
    """


def set_endpoint_type(argv):

    #print 'function parse'
    for i in range (0, len(argv)):
        #print argv[i]
        curArg = argv[i]
        curVal = ""
        if curArg.startswith('-'):
            curArg = curArg[1:]
            if curArg.startswith('-'):
                curArg = curArg[1:]
        if curArg.find('=') > 0:
            curVal = curArg[curArg.find('=') + 1:]
            curVal = curVal.replace('=', '\=')
            curArg = curArg[0:curArg.find('=')]

        #print 'arg:'+curArg
        #print 'val:'+curVal
        if curArg == 'replica':
            argv.pop(i)
            AMIEndPoint.setType('replica')
            break


class AMIResult:
    """
    Python class representing the XML reply from the AMI Web Service.
    The default transformation produces text.
    """
    _xslt = 'text'

    def __init__(self , dom):

        self._dom = dom

    def get_dom(self):

        return self._dom

    def setxslt(self , xslt):

        self._xslt = xslt

    def write_gpickle(self, filenameBase):

        if filenameBase.endswith('.gpickle'):
            filename = filenameBase
        else:
            filename = filenameBase + '.gpickle'
        try:
            errorFile = open(filename, 'w')
        except IOError:
            print "WARNING: Could not write gpickle report to file %s" % filename
            return False
        else:
            self.__changed = False
            pickle.dump(self. get_dict(), errorFile, 0) # text format
            errorFile.close()
            return True

    def get_dict(self):

        resultDict = {}

        rowsets = self._dom.getElementsByTagName('rowset')
        cptRowset = 0
        for rowset in rowsets:
            cptRowset = cptRowset + 1
            rowsetDict = {}
            rowsetLabel = "rowset_" + str(cptRowset)
            if "type" in rowset.attributes.keys():
                rowsetLabel = rowset.attributes['type'].value
            rows = rowset.getElementsByTagName('row')
            cptRow = 0
            for row in rows:
                rowDict = {}
                if "type" in row.attributes.keys():
                    rowLabel = row.attributes['type'].value
                else:
                    rowLabel = "row_" + str(cptRow + 1)
                cptRow = cptRow + 1
                fields = row.getElementsByTagName('field')
                cptField = 0
                for field in fields:
                    fieldLabel = field.attributes['name'].value
                    cptField = cptField + 1
                    if field.firstChild:
                        value = field.firstChild.nodeValue
                    else:
                        value = ""
                    rowDict.update({fieldLabel:value})
                rowsetDict.update({rowLabel:rowDict})
            resultDict.update({rowsetLabel:rowsetDict})

        return resultDict

    def list_rowsets(self):

        infos = self._dom.getElementsByTagName('info')
        errors = self._dom.getElementsByTagName('error')
        rowsets = self._dom.getElementsByTagName('rowset')
        for rowset in rowsets:
            rowsetLabel = "#rowset:"
            if "type" in rowset.attributes.keys():
                rowsetLabel = rowsetLabel + rowset.attributes['type'].value
            rowsetLabel = rowsetLabel + "#"
            print rowsetLabel
            rows = rowset.getElementsByTagName('row')
            cpt = 0
            for row in rows:
                if cpt == 0:
                    fields = row.getElementsByTagName('field')
                    line = ""
                    for field in fields:
                        line = line + "[" + field.attributes['name'].value + "]"
                    print line
                cpt = cpt + 1
                line = ""
                fields = row.getElementsByTagName('field')
                for field in fields:
                    if field.firstChild:
                        value = field.firstChild.nodeValue
                        line = line + "{" + value + "}"
                    else:
                        line = line + "{}"
                print line

    def iterrows(self):

        rowsets = self._dom.getElementsByTagName('rowset')
        for rowset in rowsets:
            rows = rowset.getElementsByTagName('row')
            for row in rows:
                fields = row.getElementsByTagName('field')
                field_dict = {}
                for field in fields:
                    name = str(field.attributes['name'].value)
                    if field.firstChild:
                        field_dict[name] = str(field.firstChild.nodeValue)
                    else:
                        field_dict[name] = 'NULL'
                yield field_dict

    def transform(self , xslt=None):

        if 'gpickle' not in xslt.lower():
            """
            f = StringIO(self._dom.toxml())
            if xslt is None:
                return None
            """
            return self._dom.toxml()
            """
            else:
                result = Transform(f, self.set_transform(xslt))
                return result
            """
        else:
            outputfile = "output.gpickle"
            if(xslt.lower() != 'gpickle'):
                outputfile = xslt
            self.write_gpickle(outputfile)
            return "result printed in " + outputfile + " gpickle file "

    def output(self):

        return self.transform(self._xslt)

    def set_transform(self, xslt=None):

        amiurl = AMIEndPoint.getXSLURL()
        if xslt is None:
            return None
        elif xslt.lower() == 'csv':
            return amiurl + 'AMIXmlToCsv.xsl'
        elif xslt.lower() == 'htmltable':
            return amiurl + 'AMIXmlToHtmlTable.xsl'
        elif xslt.lower() == 'html':
            return amiurl + 'AMIXmlToHtml.xsl'
        elif xslt.lower() == 'text':
            return amiurl + 'AMIXmlToText.xsl'
        elif xslt.lower() == 'verbose':
            return amiurl + 'AMIXmlToTextVerbose.xsl'
        elif xslt.lower() == 'xml':
            return 'xml'
        else:
            return xslt


class AMI_WS_Client:
    """
    AMI Web Service Client for Python. Most methods defined in this
    class mirror the methods recognised by the AMI Web Service.
    Mandatory parameters are enforced and atlasmeta will complain if
    they are left out. All other parameters not recognised
    by atlasmeta will be passed on to the AMI Web Service.

    NB: atlasmeta expects XML format when it tries to parse replies from the AMI Web Service.
    """

    _xslt = 'text'
    _transdict = None

    def __init__(self, user=None, password=None, cert_auth=False, transdict=None, verbose=False):
        """
        Parameters
        ----------
        *user*
            :Description: User ID for access to the AMI Web Service.
            :Type: String
            :Default: None

        *password*
            :Description: Password for access to the AMI Web Service.
            :Type: String
            :Default: None
        """
        self.verbose = verbose
        self.config = AMIConfig()

        if user is not None:
            self.config.set('AMI', 'AMIUser', user)

        if password is not None:
            self.config.set('AMI', 'AMIPass', password)

        self._loc = AMISecureWebServiceServiceLocator()
        if cert_auth:
            ssl = self._loc.getAMISecureWebServiceAddress().startswith('https')
            if not ssl:
                self._transdict = None
            else:
                if transdict is None:
                    self._transdict = self.setup_identity()
                else:
                    self._transdict = transdict

            kw = {'transdict':self._transdict}
        else:
            # for SSLv3 SSLv23 problems use amiHttpLib.HTTPSConnection
            #kw = {'transdict':None, 'transport':amiHttpLib.HTTPSConnection}
            kw = {'transdict':None}

        self._ami = self._loc.getAMISecureWebService(url=None, **kw)

    def reset_cert_auth(self):

        kw = {}
        self._ami = self._loc.getAMISecureWebService(url=None, **kw)

    def set_cert_auth(self , transdict=None):

        kw = {}
        if transdict is None:
            kw = {'transdict':self.setup_identity()}
        else:
            kw = {'transdict':transdict}
        self._ami = self._loc.getAMISecureWebService(url=None, **kw)

    def is_authenticated(self):
        """
        Returns `True` if user is authenticated, `False` otherwise.
        """
        if self.config.get('AMI', 'AMIPass') and self.config.get('AMI', 'AMIUser'):
            return True
        else:
            return False

    def authenticate(self, user, password):
        """
        Sets User ID and password with *user* and *password* parameters respectively.
        """
        self.config.set('AMI', 'AMIUser', user)
        self.config.set('AMI', 'AMIPass', password)

    def setup_identity(self):

        try:
            if hasattr(os, "geteuid"):
                user_id = os.geteuid()
            else:
                user_id=-1
        except:
            ## In case client aren't running on linux system
            user_id = -1
        options = {}
        #options['capath']= "/etc/grid-security/certificates"

        if user_id == 0:
            ## we are running as root, use host certificate
            options['cert_file'] = "/etc/grid-security/hostcert.pem"
            options['key_file'] = "/etc/grid-security/hostkey.pem"
        else:
            proxy_fname = "/tmp/x509up_u%d" % user_id
            ## look for a proxy in X509_USER_PROXY env variable
            if os.environ.has_key("X509_USER_PROXY") and os.path.exists(os.environ['X509_USER_PROXY']):
                options['cert_file'] = os.environ['X509_USER_PROXY']
                options['key_file'] = os.environ['X509_USER_PROXY']
            ## look for a proxy
            elif os.path.exists(proxy_fname):
                options['cert_file'] = proxy_fname
                options['key_file'] = proxy_fname
                # use common certificate
                """
                elif os.environ.has_key("X509_cert_file") and os.path.exists(os.environ['X509_cert_file']) :
                         options['cert_file'] = os.environ['X509_cert_file']
                         options['key_file'] = os.environ['X509_key_file']
                """
                # look in the .globus directory
                """
                elif os.environ.has_key("HOME") and os.path.exists(os.path.join(os.environ['HOME'],".globus", "usercert.pem"))and os.path.exists(os.path.join(os.environ['HOME'],".globus", "userkey.pem")):
                       options['cert_file'] = os.path.join(os.environ['HOME'],".globus", "usercert.pem")
                         options['key_file'] = os.path.join(os.environ['HOME'],".globus", "userkey.pem")
                """
                ## no configured environnement, using https with no client authentication
            else:
                options = None
        return options

    def _check_authentication(self):

        if not self.is_authenticated():
            raise AMI_Error("AMIUser and AMIPass must be defined!")

    def _check_format(self, argDict):

        try:
            if argDict[ 'format' ] != 'XML':
                raise AMI_Info("pyAMI supports the XML format only.")
        except KeyError:
            pass

    def reset_config(self):
        """
        Resets parameter values in the pyAMI.cfg to default values.
        """
        self.config.reset()

    def exec_command(self, _parameters):
        """
        This method is called internally by other methods to assemble parameters
        in the format recognised by the exec_command_arrary() method supplied by the AMI Web Service.
        """
        self._check_format(_parameters)
        if 'command' not in _parameters:
            raise AMI_Error("You must provide a command")
        _parameters = self.config.include(_parameters)
        request = execAMICommand_arrayRequest()
        request._args = []
        for x in _parameters:
            if not(x == "AMIUser" and _parameters[x] == "") and \
               not(x == "AMIPass" and _parameters[x] == "") :
                value = _parameters[x]
                if x == 'AMIPass':
                    value = base64.b64decode(value)
                request._args.append('-' + x + '=' + value)
                #print x, _parameters[x]
        try:
            """
            if self.verbose:
                print ' '.join(request._args)
            """
            reply = self._ami.execAMICommand_array(request)
        except Exception, msg:
            error = str(msg)
            if error.find('<?') < 0 :
                error = "<?xml version=\"1.0\" ?><AMIMessage><error>" + error + "</error></AMIMessage>"
            f = StringIO(error[error.find('<?'):error.find('</AMIMessage>') + 13])
            try:
                doc = minidom.parse(f)
                self._result = AMIResult(doc)
                self._result.setxslt(self._xslt)
                outputmsg = self._result.output()
            except Exception:
                raise AMI_Error("cannot parse error : " + error)
            raise AMI_Error(outputmsg)
        else:
            return reply
        #return self._ami.execAMICommand_array( request )

    def upload_proxy(self):

        #try:
        if self._transdict is None:
            raise AMI_Error("No proxy file to upload.")

        proxy_fname = self._transdict['cert_file']
        args = {}
        proxFile = open(proxy_fname, 'r')
        proxyFileContent = proxFile.read()
        proxFile.close()
        args.update({'proxyFileContent':proxyFileContent})
        request = upload_proxyRequest(**args)
        self._ami.upload_proxy(request)._upload_proxyReturn
        return "Proxy successfully uploaded"
        #except Exception, msg:
        #return msg

    def get_results(self):

        return self._result

    def _parse_data(self, xmlReply):
        """
        This method makes a dom object and then applies a transformation
        """
        f = StringIO(xmlReply._execAMICommand_arrayReturn.encode('utf-8'))
        doc = minidom.parse(f)
        self._result = AMIResult(doc)
        self._result.setxslt(self._xslt)
        return self._result

    def parse_args(self , argv):

        arguments = {}
        arguments.update({'command':argv[0]})
        #print 'function parse'
        for i in range (1, len(argv)):
        #print argv[i]
            curArg = argv[i]
            curVal = ""
            if curArg.startswith('-'):
                curArg = curArg[1:]
                if curArg.startswith('-'):
                    curArg = curArg[1:]
            if curArg.find('=') > 0:
                curVal = curArg[curArg.find('=') + 1:]
                curVal = curVal.replace('=', '\=')
                curArg = curArg[0:curArg.find('=')]
            #print 'arg:'+curArg
            #print 'val:'+curVal
            if curArg == 'output':
                self._xslt = curVal
            else:
                arguments.update({curArg:curVal})
        return arguments


class AMI:
    """
    This is the generic way of sending a command to the AMI server.
    The first argument must be the name of the server command.
    The other arguments follow as argumentName=argumentValue pairs.
    For complete help see the PyAMI User guide
    http://ami.in2p3.fr/opencms/opencms/AMI/www/Client/pyAMIUserGuide.pdf
    """

    _client = None
    _authMethod = None # could be x509 or password

    def __init__(self, cert_auth=True, transdict=None, verbose=False):

        if (cert_auth):
            self._authMethod = "x509"
        self._client = AMI_WS_Client("", "", cert_auth, transdict, verbose=verbose)
        self.verbose = verbose

    def auth(self, user, password):

        self._authMethod = "password"
        self._client.reset_cert_auth()
        self._client.authenticate(user, password)

    def cert_auth(self, transdict=None):

        self._authMethod = "x509"
        self._client.set_cert_auth(transdict)

    def write_config(self, fp):

        self._client.config.write(fp)

    def read_config(self, fpname):

        self._client.config.read(fpname)

    def execute(self, argv):

        if len(argv) == 0:
            raise AMI_Error("You must provide a command. Try 'amiCommand help'.")
        if (argv[0] == 'help') or (argv[0] == '-help'):
            raise AMI_Error(tutorial())
        if self.verbose:
            print "query:"
            print ' '.join(argv)
        if len(argv) == 1 and argv[0] == "UploadProxy":
            self.upload_proxy()
            f = StringIO("<?xml version=\"1.0\" ?><AMIMessage><info>Proxy uploaded</info></AMIMessage>");
            doc = minidom.parse(f)
            xmlResults = AMIResult(doc)
            xmlResults.setxslt("text")
        else:
            # here we filter out those commands which have a locally generated help.
            if(argv[0] == "help"):
                raise AMI_Error("")
            arguments = self._client.parse_args(argv)
            amiReply = self._client.exec_command(arguments)
            #print amiReply._execAMICommand_arrayReturn.encode('utf-8')
            xmlResults = self._client._parse_data(amiReply)
        if self.verbose:
            print "reply:"
            print xmlResults._dom.toxml()
        return xmlResults

    def upload_proxy(self):

        return self._client.upload_proxy()

    def set_user_credentials(self,argv):

        password="None"
        user="None"
        remove = []
        for i in range (0, len(argv)):
            #print argv[i]
            curArg = argv[i]
            save = curArg
            curVal = ""
            if curArg.startswith('-'):
                curArg = curArg[1:]
                if curArg.startswith('-'):
                    curArg = curArg[1:]
            if curArg.find('=') > 0:
                curVal = curArg[curArg.find('=') + 1:]
                curVal = curVal.replace('=', '\=')
                curArg = curArg[0:curArg.find('=')]
            if curArg == 'AMIPass':
                remove.append(save)
                password=curVal
            if curArg == 'AMIUser':
                remove.append(save)
                user=curVal
        if ((user!="None")and(password!="None")):
            self._client.authenticate(user, password)
        out = []
        for item in argv:
            if ( not remove.__contains__(item)):
                out.append(item)
        return out

    def check_auth(self):

        try:
            argv = []
            argv.append("GetLevelInfo")
            argv.append("levelName=motherDatabase")
            argv.append("output=xml")
            result = self.execute(argv)
            msg = result.output()
            return msg[msg.find('amiLogin="') + 10:msg.find('" database')]
        except Exception, error:
            return None


"""
The code lines in this main method show how to
use the client from another python program
They could be copied from here to a command wrapper

    #execute a command and get result in a result object
    # argv[0] must contain the name of the command
    # The other elements of arg contain the arguments to the command
    # Please see the command wrappers for more information
    # about passing arguments
    #to use the main server ( set the default here)
    # These next four lines are the essential ones for all pyAMI wrappers
    # The first line grabs the "replica" from the command line if it is there. The default end point is "main"

    set_endpoint_type(argv)
    amiclient = AMI()
    result = amiclient.execute(argv)
    print result.output()

    # The rest of this file contains examples
    #NEW in version 3-2.*
    # Possibility to connect to the CERN replica
    #to use the replica - for READONLY
    AMIEndPoint.setType("replica")
    # or simply put -replica in command arguments
    set_endpoint_type(argv)

    #NEW in version 3.4
    #read a config file
    # To read the password and username in a configuration file (or other parameters)
    amiclient.read_config("pyAMI.cfg")

    # Or if the arguments are in the command line they can be usefully extracted to a config object
    # argv=amiclient.set_user_credentials(argv)
    # The above has been done in the READ wrappers in this version

    # DEFAULT uses certificate proxy authentication
    #prepare custom credential (optional)
    transdict = {'cert_file' : "~/.globus/usercert.pem",
                                    'key_file' : "~/.globus/userkey.pem",
                                    'capath' : "/etc/grid-security/certificates"
                                    }
    # use client certificate authentication with custom credential (optional)
    amiclient=AMI(True,transdict)

    # to get an AMI client without certificate proxy authentication
    # implies username and password will be used, otherwise it will not work.
    #amiclient=AMI(False)

    #set user password (override proxy authentication, mandatory to read after November 2011)
    #amiclient.auth("user","pass")

    #explicit upload of grid proxy to AMI server.
    #msg= amiclient.upload_proxy()

    #Example of a simple command

    argv.append("GetDatasetInfo")
    argv.append("logicalDatasetName=data11_7TeV.00190256.physics_CosmicCalo.merge.NTUP_TRIG.f408_m1000")
    argv.append("output=xml")
    result = amiclient.execute(argv)

    # OUTPUT
    #print the default output of the command result
    # The default output=text, but others can be set using argument output.
    print result.output()

    # return a dictionary (of dictionaries of dictionaries )containing all rowsets in the result
    resultDict=result.get_dict()

    # write a GPickle file containing a dictionary of all rowsets in the result
    # file named 'test.gpickle'
    result.write_gpickle('test.gpickle')

    #print the result using a specific xls transformation
    # These are the XSLT which are provided on the server
    # XML is the native output.
    print result.transform('xml')
    print result.transform('html')
    print result.transform('htmlTable')
    print result.transform('csv')
    print result.transform('test.gpickle')
    print result.transform('gpickle')

    #
    # text = some information removed, only useful fields displayed
    #
    print result.transform('text')

    # verbose = all information
    print result.transform('verbose')
    #
    # Or you can use your own XSLT to transform the native XML
    # set fileURL to the URL where an XSLT can be found
    #fileURL=""
    print result.transform(fileURL)

    # This is a method which shows how to navigate across xml result
    result.list_rowsets()

    #Or obtain the DOM object which will allow you
    # to go directly to an element of the result
    #
    dom=result.get_dom()
"""
