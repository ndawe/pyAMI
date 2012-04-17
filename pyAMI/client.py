
import sys
import os
from cStringIO import StringIO
import re
from sys import stdout
import cPickle as pickle
import base64
import urlparse

if sys.version_info < (2, 6):
    from pyAMI.backports import urllib2
else:
    import urllib2

from pyAMI.webservices import *
from pyAMI.exceptions import *
from pyAMI.exceptions import _AMI_Error_Base
from pyAMI import endpoint
from pyAMI.config import AMIConfig
from pyAMI.userdata import DATA_ROOT
from xml.dom import minidom, Node

AMI_CONFIG = os.path.join(DATA_ROOT, 'ami.cfg')

USE_LXML = True
try:
    from lxml import etree
except ImportError:
    USE_LXML = False


def set_endpoint_type(args):

    for i, arg in enumerate(args):
        value = ""
        # this can be done in a better way with regex
        if arg.startswith('-'):
            arg = arg[1:]
            if arg.startswith('-'):
                arg = arg[1:]
        if '=' in arg:
            value = arg[arg.find('=') + 1:]
            value = value.replace('=', '\=')
            arg = arg[0:arg.find('=')]
        if arg == 'replica':
            args.pop(i)
            endpoint.TYPE = 'replica'
            return


class AMIResult(object):
    """
    Python class representing the XML reply from the AMI Web Service.
    The default transformation produces text.
    """

    XSLT = {
        'xml':       None,
        'csv':       'AMIXmlToCsv.xsl',
        'htmltable': 'AMIXmlToHtmlTable.xsl',
        'html':      'AMIXmlToHtml.xsl',
        'text':      'AMIXmlToText.xsl',
        'verbose':   'AMIXmlToTextVerbose.xsl',
    }

    _xslt = None

    def __init__(self, dom):

        self.dom = dom
        self.errors = dom.getElementsByTagName('error')
        self.infos = dom.getElementsByTagName('info')
        self.rowsets = dom.getElementsByTagName('rowset')

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
            pickle.dump(self.get_dict(), errorFile, 0)
            errorFile.close()
            return True

    def get_dict(self):

        resultDict = {}
        cptRowset = 0
        for rowset in self.rowsets:
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

    def rows(self):

        for rowset in self.rowsets:
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

        for rowset in self.rowsets:
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

    def output(self, format=None):

        if format is None:
            if self._xslt is not None:
                format = self._xslt
            else:
                format = 'text'
        format = format.lower()
        if format == 'xml':
            return self.dom.toxml()
        if format.endswith('gpickle'):
            outputfile = "output.gpickle"
            if format != 'gpickle':
                outputfile = format
            self.write_gpickle(outputfile)
            return None
        elif format in self.XSLT:
            if not USE_LXML:
                raise ImportError("lxml must be installed to "
                                  "perform XSLT transformations")
            xslt_url = urlparse.urljoin(endpoint.get_XSL_URL(), self.XSLT[format])
            xslt_root = etree.XML(urllib2.urlopen(xslt_url).read())
            transform = etree.XSLT(xslt_root)
            doc = etree.fromstring(self.dom.toxml())
            return transform(doc)
        else:
            raise ValueError("Format '%s' is not a valid "
                             "AMIResult format" % format)


class AMIClient(object):
    """
    This is the generic way of sending a command to the AMI server.
    The first argument must be the name of the server command.
    The other arguments follow as argumentName=argumentValue pairs.
    For complete help see the PyAMI User guide
    http://ami.in2p3.fr/opencms/opencms/AMI/www/Client/pyAMIUserGuide.pdf
    """
    """
    AMI Web Service Client for Python. Most methods defined in this
    class mirror the methods recognised by the AMI Web Service.
    Mandatory parameters are enforced and pyAMI will complain if
    they are left out. All other parameters not recognised
    by pyAMI will be passed on to the AMI Web Service.

    NB: pyAMI expects XML format when it tries to parse replies from the AMI Web Service.
    """

    _xslt = None

    def __init__(self, verbose=False, verbose_format='text'):
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
        self.verbose_format = verbose_format
        self._config = AMIConfig()
        # AMI web service locator
        self._locator = AMISecureWebServiceServiceLocator()
        self._transdict = None
        # AMI Secure Web Service instance
        self._ami = None

    """
    User/password authentication
    ----------------------------
    """
    def auth(self, user, password):

        self.reset_cert_auth()
        self.authenticate(user, password)

    def is_authenticated(self):
        """
		Returns `True` if user is authenticated, `False` otherwise.
		"""
        return (self._config.get('AMI', 'AMIPass') != '') and (self._config.get('AMI', 'AMIUser') != '')

    def authenticate(self, user, password):
        """
		Sets User ID and password with *user* and *password* parameters respectively.
		"""
        self._config.set('AMI', 'AMIUser', user)
        self._config.set('AMI', 'AMIPass', base64.b64encode(password))

    """
	Certificate authentication
	--------------------------
	"""
    def reset_cert_auth(self):

        kw = {}
        self._ami = self._locator.getAMISecureWebService(url=None, **kw)

    def set_cert_auth(self):

        kw = {'transdict':self.setup_identity()}
        self._ami = self._locator.getAMISecureWebService(url=None, **kw)

    def setup_identity(self):

        try:
            if hasattr(os, "geteuid"):
                user_id = os.geteuid()
            else:
                user_id = -1
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
            ## no configured environnement, using https with no client authentication
            else:
                options = None
        return options

    """
    Authentication from AMICommand arguments
    ----------------------------------------
    """
    def set_user_credentials(self, args):

        password = "None"
        user = "None"
        remove = []
        for arg in args:
            save = arg
            value = ""
            if arg.startswith('-'):
                arg = arg[1:]
                if arg.startswith('-'):
                    arg = arg[1:]
            if arg.find('=') > 0:
                value = arg[arg.find('=') + 1:]
                value = value.replace('=', '\=')
                arg = arg[0:arg.find('=')]
            if arg == 'AMIPass':
                remove.append(save)
                password = value
            if arg == 'AMIUser':
                remove.append(save)
                user = value
        if (user != "None") and (password != "None"):
            self.authenticate(user, password)
        out = []
        for arg in args:
            if arg not in remove:
                out.append(arg)
        return out

    """
    Authentication checking
    -----------------------
    """
    def check_auth(self):

        try:
            args = ["GetLevelInfo",
                    "levelName=motherDatabase",
                    "output=xml"]
            result = self.execute(args)
            msg = result.output()
            return msg[msg.find('amiLogin="') + 10:msg.find('" database')]
        except Exception, error:
            return None

    def _check_authentication(self):

        if not self.is_authenticated():
            raise AMI_Error("AMIUser and AMIPass must be defined!")

    """
    AMIConfig settings
    ------------------
    """
    def write_config(self, fp):

        self._config.write(fp)

    def read_config(self, fpname):

        self._config.read(fpname)

    def reset_config(self):
        """
        Resets parameter values in the pyAMI.cfg to default values.
        """
        self._config.reset()

    """
    Execute methods
    --------------
    Here we check authentication methods:
    	- Argument AMIUser and AMIPass from command line
    	- Config file
    	- VOMS proxy
    """
    def execute(self, args):

        args = self.set_user_credentials(args)
        if not self.is_authenticated():
            if os.path.exists(AMI_CONFIG):
                self.read_config(AMI_CONFIG)
                self.reset_cert_auth()
            elif not self.is_authenticated():
                    self.set_cert_auth()
        else:
            self.reset_cert_auth()

        if self.verbose:
            print
            print "query:"
            print ' '.join(args)
        if len(args) == 1 and args[0] == "UploadProxy":
            self.upload_proxy()
            f = StringIO("<?xml version=\"1.0\" ?><AMIMessage><info>Proxy uploaded</info></AMIMessage>");
            doc = minidom.parse(f)
            result = AMIResult(doc)
            result.setxslt("text")
        else:
            args = self._parse_args(args)
            self._check_format(args)
            if 'command' not in args:
                raise AMI_Error("You must provide a command")
            args = self._config.include(args)
            request = execAMICommand_arrayRequest()
            request._args = []
            for name, value in args.items():
                if not (name == "AMIUser" and value == "") and \
                   not (name == "AMIPass" and value == "") :
                    if name == 'AMIPass':
                        value = base64.b64decode(value)
                    request._args.append('-%s=%s' % (name, value))
            try:
                reply = self._ami.execAMICommand_array(request)
            except Exception, msg:
                error = str(msg)
                try:
                    if 'alert certificate expired' in error:
                        error = ('No password or config file found, '
                                 'expecting VOMS proxy...\n'
                                 'Cannot find a valid VOMS proxy, please renew '
                                 'it with voms-proxy-init.')
                    if '<?' not in error:
                        error = '<?xml version="1.0" ?><AMIMessage><error>%s</error></AMIMessage>' % error
                    f = StringIO(error[error.find('<?'):error.find('</AMIMessage>') + 13])
                    doc = minidom.parse(f)
                    result = AMIResult(doc)
                    outputmsg = str(result.output())
                except Exception:
                    raise AMI_Error("cannot parse error : " + error)
                raise AMI_Error(outputmsg)
            result = self._parse_reply(reply)
        if self.verbose:
            print
            print "reply:"
            print result.output(format=self.verbose_format)
            print
        return result

    def _parse_args(self, args):

        arguments = {}
        arguments.update({'command':args[0]})
        for arg in args[1:]:
            value = ""
            if arg.startswith('-'):
                arg = arg[1:]
                if arg.startswith('-'):
                    arg = arg[1:]
            if arg.find('=') > 0:
                value = arg[arg.find('=') + 1:]
                value = value.replace('=', '\=')
                arg = arg[0:arg.find('=')]
            #if arg != 'output':
            #    arguments.update({arg:value})
            if arg == 'output':
                self._xslt = value
            else:
                arguments.update({arg:value})
        return arguments

    def _parse_reply(self, reply):
        """
        This method makes a dom object and then applies a transformation
        """
        f = StringIO(reply._execAMICommand_arrayReturn.encode('utf-8'))
        doc = minidom.parse(f)
        self._result = AMIResult(doc)
        self._result.setxslt(self._xslt)
        return self._result

    def _check_format(self, argDict):

        try:
            if argDict['format'] != 'XML':
                raise AMI_Info("pyAMI supports the XML format only.")
        except KeyError:
            pass

    def upload_proxy(self):

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


class AMI(AMIClient):
    pass
