################################################## 
# AMIWebServiceService_services.py 
# generated by ZSI.wsdl2python 
# 
# 
##################################################


from AMIWebServiceService_services_types import *
from AMIWebServiceService_services_types import \
    xml_apache_org_xml_soap as ns1
from AMIWebServiceService_services_types import \
    https___atlastagcollector_in2p3_fr_8443_AMI_services_AMIWebService as ns2
import urlparse, types
from ZSI.TCcompound import Struct
from ZSI import client
import ZSI

class AMIWebServiceServiceInterface:
    def getAMIWebService(self, portAddress=None, **kw):
        raise NonImplementationError, "method not implemented"


class AMIWebServiceServiceLocator(AMIWebServiceServiceInterface):
    AMIWebService_address = "https://atlastagcollector.in2p3.fr:8443/AMI/services/AMIWebService"
    def getAMIWebServiceAddress(self):
        return AMIWebServiceServiceLocator.AMIWebService_address

    def getAMIWebService(self, portAddress=None, **kw):
        return AMIWebServiceSoapBindingSOAP(portAddress or AMIWebServiceServiceLocator.AMIWebService_address, **kw)


class AMIWebServiceSoapBindingSOAP:

    def __init__(self, addr, **kw):
        netloc = (urlparse.urlparse(addr)[1]).split(":") + [80,]
        if not kw.has_key("host"):
            kw["host"] = netloc[0]
        if not kw.has_key("port"):
            kw["port"] = int(netloc[1])
        if not kw.has_key("url"):
                 # kw["url"] =  urlparse.urlparse(addr)[2]
            kw["url"] =  addr 
        self.binding = client.Binding(**kw)


    def execAMICommand(self, request):
        """
        @param: request to execAMICommandRequest::
          _args: ns1.Map_Def
            _item: ns1.mapItem_Def, optional
              _key: str, optional
              _value: str, optional
          _confArgs: ns1.Map_Def

        @return: response from execAMICommandResponse::
          _execAMICommandReturn: str
        """

        if not isinstance(request, execAMICommandRequest) and\
            not issubclass(execAMICommandRequest, request.__class__):
            raise TypeError, "%s incorrect request type" %(request.__class__)
        kw = {}
        response = self.binding.Send(None, None, request, soapaction="", **kw)
        response = self.binding.Receive(execAMICommandResponseWrapper())
        if not isinstance(response, execAMICommandResponse) and\
            not issubclass(execAMICommandResponse, response.__class__):
            raise TypeError, "%s incorrect response type" %(response.__class__)
        return response


    def execAMICommand_array(self, request):
        """
        @param: request to execAMICommand_arrayRequest::
          _args: ns2.ArrayOf_xsd_string_Def
            _element: str

        @return: response from execAMICommand_arrayResponse::
          _execAMICommand_arrayReturn: str
        """

        if not isinstance(request, execAMICommand_arrayRequest) and\
            not issubclass(execAMICommand_arrayRequest, request.__class__):
            raise TypeError, "%s incorrect request type" %(request.__class__)
        kw = {}
        response = self.binding.Send(None, None, request, soapaction="", **kw)
        response = self.binding.Receive(execAMICommand_arrayResponseWrapper())
        if not isinstance(response, execAMICommand_arrayResponse) and\
            not issubclass(execAMICommand_arrayResponse, response.__class__):
            raise TypeError, "%s incorrect response type" %(response.__class__)
        return response


    def execAMICommand_map(self, request):
        """
        @param: request to execAMICommand_mapRequest::
          _args: ns1.Map_Def
            _item: ns1.mapItem_Def, optional
              _key: str, optional
              _value: str, optional

        @return: response from execAMICommand_mapResponse::
          _execAMICommand_mapReturn: str
        """

        if not isinstance(request, execAMICommand_mapRequest) and\
            not issubclass(execAMICommand_mapRequest, request.__class__):
            raise TypeError, "%s incorrect request type" %(request.__class__)
        kw = {}
        response = self.binding.Send(None, None, request, soapaction="", **kw)
        response = self.binding.Receive(execAMICommand_mapResponseWrapper())
        if not isinstance(response, execAMICommand_mapResponse) and\
            not issubclass(execAMICommand_mapResponse, response.__class__):
            raise TypeError, "%s incorrect response type" %(response.__class__)
        return response


    def execAMICommand_map_array(self, request):
        """
        @param: request to execAMICommand_map_arrayRequest::
          _args: ns2.ArrayOf_xsd_string_Def
            _element: str
          _confArgs: ns1.Map_Def
            _item: ns1.mapItem_Def, optional
              _key: str, optional
              _value: str, optional

        @return: response from execAMICommand_map_arrayResponse::
          _execAMICommand_map_arrayReturn: str
        """

        if not isinstance(request, execAMICommand_map_arrayRequest) and\
            not issubclass(execAMICommand_map_arrayRequest, request.__class__):
            raise TypeError, "%s incorrect request type" %(request.__class__)
        kw = {}
        response = self.binding.Send(None, None, request, soapaction="", **kw)
        response = self.binding.Receive(execAMICommand_map_arrayResponseWrapper())
        if not isinstance(response, execAMICommand_map_arrayResponse) and\
            not issubclass(execAMICommand_map_arrayResponse, response.__class__):
            raise TypeError, "%s incorrect response type" %(response.__class__)
        return response



class execAMICommandRequest (ZSI.TCcompound.Struct): 
    def __init__(self, name=None, ns=None):
        self._confArgs = ns1.Map_Def()
        self._args = ns1.Map_Def()

        oname = None
        if name:
            oname = name
            if ns:
                oname += ' xmlns="%s"' % ns
            ZSI.TC.Struct.__init__(self, execAMICommandRequest, [ns1.Map_Def( name="confArgs", ns=ns ),ns1.Map_Def( name="args", ns=ns ),], pname=name, aname="_%s" % name, oname=oname )

class execAMICommandRequestWrapper(execAMICommandRequest):
    """wrapper for rpc:encoded message"""

    typecode = execAMICommandRequest(name='execAMICommand', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net')
    def __init__( self, name=None, ns=None, **kw ):
        execAMICommandRequest.__init__( self, name='execAMICommand', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net' )

class execAMICommandResponse (ZSI.TCcompound.Struct): 
    def __init__(self, name=None, ns=None):
        self._execAMICommandReturn = None

        oname = None
        if name:
            oname = name
            if ns:
                oname += ' xmlns="%s"' % ns
            ZSI.TC.Struct.__init__(self, execAMICommandResponse, [ZSI.TC.String(pname="execAMICommandReturn",aname="_execAMICommandReturn",optional=1),], pname=name, aname="_%s" % name, oname=oname )

class execAMICommandResponseWrapper(execAMICommandResponse):
    """wrapper for rpc:encoded message"""

    typecode = execAMICommandResponse(name='execAMICommandResponse', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net')
    def __init__( self, name=None, ns=None, **kw ):
        execAMICommandResponse.__init__( self, name='execAMICommandResponse', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net' )

class execAMICommand_arrayRequest (ZSI.TCcompound.Struct): 
    def __init__(self, name=None, ns=None):
        self._args = ns2.ArrayOf_xsd_string_Def()

        oname = None
        if name:
            oname = name
            if ns:
                oname += ' xmlns="%s"' % ns
            ZSI.TC.Struct.__init__(self, execAMICommand_arrayRequest, [ns2.ArrayOf_xsd_string_Def( name="args", ns=ns ),], pname=name, aname="_%s" % name, oname=oname )

class execAMICommand_arrayRequestWrapper(execAMICommand_arrayRequest):
    """wrapper for rpc:encoded message"""

    typecode = execAMICommand_arrayRequest(name='execAMICommand_array', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net')
    def __init__( self, name=None, ns=None, **kw ):
        execAMICommand_arrayRequest.__init__( self, name='execAMICommand_array', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net' )

class execAMICommand_arrayResponse (ZSI.TCcompound.Struct): 
    def __init__(self, name=None, ns=None):
        self._execAMICommand_arrayReturn = None

        oname = None
        if name:
            oname = name
            if ns:
                oname += ' xmlns="%s"' % ns
            ZSI.TC.Struct.__init__(self, execAMICommand_arrayResponse, [ZSI.TC.String(pname="execAMICommand_arrayReturn",aname="_execAMICommand_arrayReturn",optional=1),], pname=name, aname="_%s" % name, oname=oname )

class execAMICommand_arrayResponseWrapper(execAMICommand_arrayResponse):
    """wrapper for rpc:encoded message"""

    typecode = execAMICommand_arrayResponse(name='execAMICommand_arrayResponse', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net')
    def __init__( self, name=None, ns=None, **kw ):
        execAMICommand_arrayResponse.__init__( self, name='execAMICommand_arrayResponse', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net' )

class execAMICommand_mapRequest (ZSI.TCcompound.Struct): 
    def __init__(self, name=None, ns=None):
        self._args = ns1.Map_Def()

        oname = None
        if name:
            oname = name
            if ns:
                oname += ' xmlns="%s"' % ns
            ZSI.TC.Struct.__init__(self, execAMICommand_mapRequest, [ns1.Map_Def( name="args", ns=ns ),], pname=name, aname="_%s" % name, oname=oname )

class execAMICommand_mapRequestWrapper(execAMICommand_mapRequest):
    """wrapper for rpc:encoded message"""

    typecode = execAMICommand_mapRequest(name='execAMICommand_map', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net')
    def __init__( self, name=None, ns=None, **kw ):
        execAMICommand_mapRequest.__init__( self, name='execAMICommand_map', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net' )

class execAMICommand_mapResponse (ZSI.TCcompound.Struct): 
    def __init__(self, name=None, ns=None):
        self._execAMICommand_mapReturn = None

        oname = None
        if name:
            oname = name
            if ns:
                oname += ' xmlns="%s"' % ns
            ZSI.TC.Struct.__init__(self, execAMICommand_mapResponse, [ZSI.TC.String(pname="execAMICommand_mapReturn",aname="_execAMICommand_mapReturn",optional=1),], pname=name, aname="_%s" % name, oname=oname )

class execAMICommand_mapResponseWrapper(execAMICommand_mapResponse):
    """wrapper for rpc:encoded message"""

    typecode = execAMICommand_mapResponse(name='execAMICommand_mapResponse', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net')
    def __init__( self, name=None, ns=None, **kw ):
        execAMICommand_mapResponse.__init__( self, name='execAMICommand_mapResponse', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net' )

class execAMICommand_map_arrayRequest (ZSI.TCcompound.Struct): 
    def __init__(self, name=None, ns=None):
        self._confArgs = ns1.Map_Def()
        self._args = ns2.ArrayOf_xsd_string_Def()

        oname = None
        if name:
            oname = name
            if ns:
                oname += ' xmlns="%s"' % ns
            ZSI.TC.Struct.__init__(self, execAMICommand_map_arrayRequest, [ns1.Map_Def( name="confArgs", ns=ns ),ns2.ArrayOf_xsd_string_Def( name="args", ns=ns ),], pname=name, aname="_%s" % name, oname=oname )

class execAMICommand_map_arrayRequestWrapper(execAMICommand_map_arrayRequest):
    """wrapper for rpc:encoded message"""

    typecode = execAMICommand_map_arrayRequest(name='execAMICommand_map_array', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net')
    def __init__( self, name=None, ns=None, **kw ):
        execAMICommand_map_arrayRequest.__init__( self, name='execAMICommand_map_array', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net' )

class execAMICommand_map_arrayResponse (ZSI.TCcompound.Struct): 
    def __init__(self, name=None, ns=None):
        self._execAMICommand_map_arrayReturn = None

        oname = None
        if name:
            oname = name
            if ns:
                oname += ' xmlns="%s"' % ns
            ZSI.TC.Struct.__init__(self, execAMICommand_map_arrayResponse, [ZSI.TC.String(pname="execAMICommand_map_arrayReturn",aname="_execAMICommand_map_arrayReturn",optional=1),], pname=name, aname="_%s" % name, oname=oname )

class execAMICommand_map_arrayResponseWrapper(execAMICommand_map_arrayResponse):
    """wrapper for rpc:encoded message"""

    typecode = execAMICommand_map_arrayResponse(name='execAMICommand_map_arrayResponse', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net')
    def __init__( self, name=None, ns=None, **kw ):
        execAMICommand_map_arrayResponse.__init__( self, name='execAMICommand_map_arrayResponse', ns='http://Webservice.AMI.Bookkeeping.Database.atlas.hep.net' )
