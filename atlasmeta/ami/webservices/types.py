##################################################
# AMISecureWebServiceService_services_types.py
# generated by ZSI.generate.wsdl2python
##################################################


import ZSI
import ZSI.TCcompound
from ZSI.schema import LocalElementDeclaration, ElementDeclaration, TypeDefinition, GTD, GED
from ZSI.generate.pyclass import pyclass_type
from ..endpoint import AMIEndPoint
##############################
# targetNamespace
# https://ccami01.in2p3.fr:8443/AMI/services/AMIWebService
##############################

class ns1:
#targetNamespace = AMIEndPoint.getEndPoint()

    class ArrayOf_soapenc_string_Def(ZSI.TC.Array, TypeDefinition):
        #complexType/complexContent base="SOAP-ENC:Array"
        schema = AMIEndPoint.getEndPoint()
        type = (schema, "ArrayOf_soapenc_string")
        schema = ""
        type = ""
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ofwhat = ZSI.TC.String(None, typed=False)
            atype = (u'http://schemas.xmlsoap.org/soap/encoding/', u'string[]')
            ZSI.TCcompound.Array.__init__(self, atype, ofwhat, pname=pname, childnames='item', **kw)

    # end class ns1 (tns: https://ami.in2p3.fr/AMI/services/AMIWebService)

##############################
# targetNamespace
# http://xml.apache.org/xml-soap
##############################

class ns0:
    targetNamespace = "http://xml.apache.org/xml-soap"

    class mapItem_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://xml.apache.org/xml-soap"
        type = (schema, "mapItem")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.mapItem_Def.schema
            TClist = [ZSI.TC.AnyType(pname="key", aname="_key", minOccurs=1, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.AnyType(pname="value", aname="_value", minOccurs=1, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._key = None
                    self._value = None
                    return
            Holder.__name__ = "mapItem_Holder"
            self.pyclass = Holder

    class Map_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://xml.apache.org/xml-soap"
        type = (schema, "Map")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.Map_Def.schema
            TClist = [GTD("http://xml.apache.org/xml-soap", "mapItem", lazy=False)(pname="item", aname="_item", minOccurs=0, maxOccurs="unbounded", nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._item = []
                    return
            Holder.__name__ = "Map_Holder"
            self.pyclass = Holder

# end class ns0 (tns: http://xml.apache.org/xml-soap)