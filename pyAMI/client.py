
import sys
import os
from cStringIO import StringIO
import re
import cPickle as pickle
import base64
import urlparse

if sys.version_info < (2, 6):
    from pyAMI.backports import urllib2
else:
    import urllib2

from pyAMI.webservices import *
from pyAMI.exceptions import *
from pyAMI import endpoint
from pyAMI.config import AMIConfig
from pyAMI.userdata import DATA_ROOT
from pyAMI.xslt import XSLT
from xml.dom import minidom, Node

AMI_CONFIG = os.path.join(DATA_ROOT, 'ami.cfg')

USE_LXML = True
try:
    from lxml import etree
except ImportError:
    USE_LXML = False


class AMIResult(object):
    """
    Python class representing the XML reply from the AMI Web Service.
    The default transformation produces text.
    """
    def __init__(self, dom):

        self.dom = dom
        self.errors = dom.getElementsByTagName('error')
        self.infos = dom.getElementsByTagName('info')
        self.rowsets = dom.getElementsByTagName('rowset')

    def pickle(self, filename):

        root, ext = os.path.splitext(filename)
        if not ext:
            filename += '.pickle'
        try:
            pickle_file = open(filename, 'w')
        except IOError:
            print "WARNING: Could not write gpickle report to file %s" % filename
            return False
        else:
            pickle.dump(self.to_dict(), pickle_file, 0)
            pickle_file.close()
            return True

    def to_dict(self):
        """
        Convert the DOM into a dictionary and return it
        """
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

    def print_rows(self):
        """
        Print the rows in the DOM
        """
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

    def rows(self):
        """
        Return an iterator over the rows in the DOM
        """
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

    def output(self, xslt='text'):
        """
        Return the DOM in the specified format using an XSLT
        """
        xslt = xslt.lower()
        if xslt == 'xml':
            return self.dom.toxml()
        elif xslt in XSLT:
            if not USE_LXML:
                raise ImportError("lxml must be installed to "
                                  "perform XSLT transformations")
            xslt_url = urlparse.urljoin(endpoint.get_XSL_URL(), XSLT[xslt])
            xslt_root = etree.XML(urllib2.urlopen(xslt_url).read())
            transform = etree.XSLT(xslt_root)
            doc = etree.fromstring(self.dom.toxml())
            return transform(doc)
        else:
            raise ValueError("'%s' is not a valid "
                             "AMIResult XSLT output format" % xslt)


class AMIClient(object):
    """
    AMIClient handles sending a command to the AMI server and receiving the
    response.
    """
    def __init__(self, verbose=False, verbose_format='text'):

        self.verbose = verbose
        self.verbose_format = verbose_format
        self.config = AMIConfig()
        # AMI web service locator
        self.ami_service_locator = AMISecureWebServiceServiceLocator()
        self.cert_info = None
        # AMI Secure Web Service instance
        self.ami_service = None

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
        return ((self.config.get('AMI', 'AMIPass') != '') and
                (self.config.get('AMI', 'AMIUser') != ''))

    def authenticate(self, user, password):
        """
		Sets User ID and password with *user* and *password* parameters
        respectively.
		"""
        self.config.set('AMI', 'AMIUser', user)
        self.config.set('AMI', 'AMIPass', base64.b64encode(password))

    """
	Certificate authentication
	--------------------------
	"""
    def reset_cert_auth(self):

        self.ami_service = self.ami_service_locator.getAMISecureWebService(
                url=None)

    def set_cert_auth(self):

        try:
            if hasattr(os, "geteuid"):
                user_id = os.geteuid()
            else:
                user_id = -1
        except:
            # in case client isn't running on linux system
            user_id = -1
        options = {}
        #options['capath']= "/etc/grid-security/certificates"
        if user_id == 0:
            # we are running as root, use host certificate
            options['cert_file'] = "/etc/grid-security/hostcert.pem"
            options['key_file'] = "/etc/grid-security/hostkey.pem"
        else:
            proxy_fname = "/tmp/x509up_u%d" % user_id
            # look for a proxy in X509_USER_PROXY env variable
            if (os.environ.has_key("X509_USER_PROXY") and
                    os.path.exists(os.environ['X509_USER_PROXY'])):
                options['cert_file'] = os.environ['X509_USER_PROXY']
                options['key_file'] = os.environ['X509_USER_PROXY']
            # look for a proxy
            elif os.path.exists(proxy_fname):
                options['cert_file'] = proxy_fname
                options['key_file'] = proxy_fname
            # no configured environment
            # using https with no client authentication
            else:
                options = None
        self.cert_info = options
        self.ami_service = self.ami_service_locator.getAMISecureWebService(
                url=None,
                transdict=options)

    """
    Authentication from AMICommand arguments
    ----------------------------------------
    """
    def set_user_credentials(self, args):

        password = None
        user = None
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
        if (user is not None) and (password is not None):
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
                    "levelName=motherDatabase"]
            result = self.execute(args)
            msg = result.output(xslt='xml')
            return msg[msg.find('amiLogin="') + 10:msg.find('" database')]
        except Exception, error:
            return None

    """
    AMIConfig settings
    ------------------
    """
    def write_config(self, fp):

        self.config.write(fp)

    def read_config(self, fpname):

        self.config.read(fpname)

    def reset_config(self):
        """
        Resets parameter values in the pyAMI.cfg to default values.
        """
        self.config.reset()

    """
    Execute Method
    --------------

    The first argument must be the name of the server command.
    The other arguments follow as argumentName=argumentValue pairs.
    For complete help see the PyAMI User guide
    http://ami.in2p3.fr/opencms/opencms/AMI/www/Client/pyAMIUserGuide.pdf

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
            print
            print ' '.join(args)
        if len(args) == 1 and args[0] == "UploadProxy":
            self.upload_proxy()
            f = StringIO(
                    "<?xml version=\"1.0\" ?><AMIMessage>"
                    "<info>Proxy uploaded</info></AMIMessage>")
            doc = minidom.parse(f)
            result = AMIResult(doc)
        else:
            args = self._parse_args(args)
            if 'command' not in args:
                raise AMI_Error("You must provide a command")
            args = self.config.include(args)
            request = execAMICommand_arrayRequest()
            request._args = []
            for name, value in args.items():
                if (not (name == "AMIUser" and value == "") and
                   not (name == "AMIPass" and value == "")):
                    if name == 'AMIPass':
                        value = base64.b64decode(value)
                    request._args.append('-%s=%s' % (name, value))
            try:
                reply = self.ami_service.execAMICommand_array(request)
            except Exception, msg:
                error = str(msg)
                try:
                    if 'alert certificate expired' in error:
                        error = ('No password or config file found, '
                                 'expecting VOMS proxy...\n'
                                 'Cannot find a valid VOMS proxy, please renew '
                                 'it with voms-proxy-init.')
                    if '<?' not in error:
                        error = ('<?xml version="1.0" ?><AMIMessage><error>'
                                 '%s</error></AMIMessage>') % error
                    f = StringIO(error[error.find('<?'): error.find('</AMIMessage>') + 13])
                    doc = minidom.parse(f)
                    result = AMIResult(doc)
                    outputmsg = str(result.output())
                except Exception:
                    raise AMI_Error("cannot parse error : " + error)
                raise AMI_Error(outputmsg)
            f = StringIO(reply._execAMICommand_arrayReturn.encode('utf-8'))
            doc = minidom.parse(f)
            result = AMIResult(doc)
        if self.verbose:
            print
            print "reply:"
            print
            print result.output(xslt=self.verbose_format)
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
                arguments.update({arg:value})
        return arguments

    def upload_proxy(self):

        if self.cert_info is None:
            raise AMI_Error(
                    "No proxy file to upload. "
                    "Call client.set_cert_auth first.")
        proxy_fname = self.cert_info['cert_file']
        proxFile = open(proxy_fname, 'r')
        proxyFileContent = proxFile.read()
        proxFile.close()
        request = uploadProxyRequest(
                proxyFileContent=proxyFileContent)
        self.ami_service.uploadProxy(request)._upload_proxyReturn
        # proxy successfully uploaded


class AMI(AMIClient):
    pass
