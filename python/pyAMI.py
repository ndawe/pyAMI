#!/usr/bin/env python
"""
:File:        pyAMI.py
:Description: AMI Web Service client for Python.    
:Author:      Jerome Fulachier (1st version from  Chun Lik Tan (Alvin))
:Institution: LPSC Grenoble
:Email:       jerome.fulachier@lpsc.in2p3.fr
:Created:     13 Aug 2004
:Modified:    07 Oct 2005
:Modified:    December 2007
:Modified:    October 2008 (S.A.) 
:Version:     2.0.2
:Bugs:        Report all bugs to author or to atlas-bookkeeping@cern.ch.
:Requires:    Python v2.3 or higher
              ZSI v1.5.0 or higher.
              PyXML v0.8.3 or higher.
              4Suite v1.0.2 or higher
:Features:    Implements all methods exposed by AMI Web Service.
"""


import sys
from AMIWebServiceService_services import *
from pyAMIErrors import *
from StringIO import StringIO
from xml.sax import make_parser, saxutils, xmlreader
import re
from sys import stdout
from pyAMIConfig import pyAMIConfig
from xml.dom import minidom, Node
from Ft.Xml.Xslt import Transform
import cPickle as pickle
import shutil


COMPATIBILITY_WARNING = "Please use %s instead.\nSupport for %s will be removed in future releases."

def pyAMI_tutorial():
	return """
	       Needs update   
	       """


class AMI_result:
	"""
   Python class representing the XML reply from the AMI Web Service.
   The default transformation produces text.
   """
	_xslt='text'   


	def __init__( self , dom):
		self._dom = dom
	def getAMIdom( self ):
		return self._dom

	def setxslt( self , xslt):
		self._xslt=xslt  


	def writeGPickle(self,filenameBase):

		if filenameBase.endswith('.gpickle'):
			filename = filenameBase
		else:
			filename = filenameBase + '.gpickle'
		try:
			errorFile = open(filename,'w')
		except IOError:
			print "WARNING: Could not write gpickle report to file %s" % filename
			return False
		else:
			self.__changed = False   
			pickle.dump(self. getDict(),errorFile,0) # text format 
			errorFile.close()

			return True   
	def getDict( self ):		
		resultDict={}

		rowsets = self._dom.getElementsByTagName('rowset')  	
		cptRowset=0
		for rowset in rowsets:
			cptRowset=cptRowset+1
			rowsetDict={}
			rowsetLabel="rowset_"+str(cptRowset)
			if "type" in rowset.attributes.keys():
				rowsetLabel=rowset.attributes['type'].value


			rows = rowset.getElementsByTagName('row')  	
			cptRow=0
			for row in rows:
				rowDict={}
				if "type" in row.attributes.keys():
				    rowLabel=row.attributes['type'].value
				    
				else:
                                    rowLabel="row_"+str(cptRow+1)
                                 
				cptRow=cptRow+1
				line=""
				fields = row.getElementsByTagName('field')  	
				cptField=0
				for field in fields:
					fieldLabel=field.attributes['name'].value
					cptField=cptField+1
					if field.firstChild:
						value=field.firstChild.nodeValue
					else: 
						value=""
					rowDict.update({fieldLabel:value})
				rowsetDict.update({rowLabel:rowDict})
			resultDict.update({rowsetLabel:rowsetDict})
			
		return resultDict




	def listRowsets( self ):	

		infos = self._dom.getElementsByTagName('info')	         

		errors =  self._dom.getElementsByTagName('error') 

		rowsets = self._dom.getElementsByTagName('rowset')  	

		for rowset in rowsets:
			rowsetLabel="#rowset:"

			if "type" in rowset.attributes.keys():
				rowsetLabel=rowsetLabel+rowset.attributes['type'].value
			rowsetLabel=rowsetLabel+"#"
			print rowsetLabel
			rows = rowset.getElementsByTagName('row')  	
			cpt=0
			for row in rows:
				if cpt==0:
					fields = row.getElementsByTagName('field')  
					line=""
					for field in fields:
						line = line +"["+field.attributes['name'].value+"]"
					print line		
				cpt=cpt+1
				line=""
				fields = row.getElementsByTagName('field')  	
				for field in fields:
					if field.firstChild:
						value=field.firstChild.nodeValue
						line = line +"{"+value+"}"
					else: 
						line = line +"{}"

				print line

	def transform( self , xslt=None ):

		if xslt.find('gpickle') < 0:      
			f = StringIO( self._dom.toxml() ) 
			if xslt is None:
				return None
			elif xslt=='xml':
				return self._dom.toxml()
			else:
				result = Transform(f, self.setTransform(xslt))
				return result
		else:
			outputfile="output.gpickle"
			if(xslt!='gpickle'):
				outputfile=xslt
			self.writeGPickle(outputfile)
			return "result printed in "+outputfile+" gpickle file "

	def output( self  ):
		return self.transform( self._xslt )   

	def setTransform( self, xslt=None ):

		amiurl = 'https://atlastagcollector.in2p3.fr:8443/AMI/AMI/xsl/'
		if xslt is None:
			return None
		elif xslt == 'csv':
			return amiurl+'AMIXmlToCsv.xsl'
		elif xslt == 'htmlTable':
			return amiurl+'AMIXmlToHtmlTable.xsl'
		elif xslt == 'html':
			return amiurl+'AMIXmlToHtml.xsl'
		elif xslt == 'text':
			return amiurl+'AMIXmlToText.xsl'
		elif xslt == 'verbose':
			return amiurl+'AMIXmlToTextVerbose.xsl'
		elif xslt == 'xml':
			return 'xml'
		else:
			return xslt







class AMI_WS_Client:
	"""
   AMI Web Service Client for Python. Most methods defined in this class mirror the methods recognised by the AMI Web Service. Mandatory parameters are enforced and pyAMI will complain if they are left out. All other parameters not recognised by pyAMI will be passed on to the AMI Web Service.

   Examples:
      >>> AC = AMI_WS_Client( '__myID__', '__myPassword__' )
      >>> xmlResult = AC.listEntityProperties( 'dataset' )

   NB: pyAMI expects XML format when it tries to parse replies from the AMI Web Service.
   """

	_xslt='text'      

	def __init__( self, amiUser=None, amiPass=None ):
		"""
      Parameters
      ----------
         *amiUser*
            :Description: User ID for access to the AMI Web Service.
            :Type: String
            :Default: None

         *amiPass*
            :Description: Password for access to the AMI Web Service.
            :Type: String
            :Default: None
      """
		self.pyAMICfg = pyAMIConfig()

		if amiUser is not None:
			self.pyAMICfg.set( 'AMI', 'AMIUser', amiUser )

		if amiPass is not None:
			self.pyAMICfg.set( 'AMI', 'AMIPass', amiPass )

		self._loc = AMIWebServiceServiceLocator()
		self._ami = self._loc.getAMIWebService( ssl = self._loc.getAMIWebServiceAddress().startswith('https') )

	def isAuthenticated( self ):
		"""
      Returns `True` if user is authenticated, `False` otherwise.
      """
		if self.pyAMICfg.get( 'AMI', 'AMIPass' ) and self.pyAMICfg.get( 'AMI', 'AMIUser' ):
			return True
		else:
			return False


	def getAuthenticated( self, amiUser, amiPass ):
		"""
      Sets User ID and password with *amiUser* and *amiPass* parameters respectively.
      """
		self.pyAMICfg.set( 'AMI', 'AMIUser', amiUser )
		self.pyAMICfg.set( 'AMI', 'AMIPass', amiPass )

	def _checkAuthentication( self ):
		if not self.isAuthenticated():
			raise AMI_Error( "AMIUser and AMIPass must be defined!" )

	def _checkFormat( self, argDict ):
		try:
			if argDict[ 'format' ] != 'XML':
				raise AMI_Info( "pyAMI supports the XML format only." )
		except KeyError:
			pass

	def resetCfg( self ):
		"""
      Resets parameter values in the pyAMI.cfg to default values.
      """
		self.pyAMICfg.reset_pyAMI_config()


	def execAMICommand( self, _parameters ):
		"""
      This method is called internally by other methods to assemble parameters in the format recognised by the execAMICommand_arrary() method supplied by the AMI Web Service.
      """
		self._checkFormat( _parameters )



		if 'command' not in _parameters:
			raise AMI_Error( "You must provide a command" )


		_parameters = self.pyAMICfg.includeCfg( _parameters ) 

		request = execAMICommand_arrayRequestWrapper()
		request._args = []

		for x in _parameters:
			if not(x=="AMIUser" and _parameters[x]=="") and not(x=="AMIPass" and _parameters[x]=="") :  
				request._args.append( '-'+x+'='+_parameters[x] )
				#print x,_parameters[x]

		try:
			reply = self._ami.execAMICommand_array( request )
		except Exception, msg:
			error = str(msg) 
			f = StringIO( error[error.find(': \n')+3:] )    

			try:
				doc = minidom.parse(f)


				self._result = AMI_result(doc)
				self._result.setxslt(self._xslt)


				outputmsg=self._result.output()
			except Exception:
				raise AMI_Error( "cannot parse error : " +error)

			raise AMI_Error( outputmsg )

		else:
			return reply 

		#return self._ami.execAMICommand_array( request )


	def getResults( self ):
		return self._result


	def _parseData( self ,xmlReply):
		"""
       This method makes a dom object and then applies a transformation
       """
		f = StringIO( xmlReply._execAMICommand_arrayReturn.encode('utf-8'))
		doc = minidom.parse(f)
		self._result = AMI_result(doc)
		self._result.setxslt(self._xslt)
		return self._result



	def parseArguments(self , argv ):
		arguments={}
		arguments.update({'command':argv[0]})
		#print 'function parse'
		for i in range (1,len(argv)):
			#print argv[i]
			curArg=argv[i]
			curVal=""
			if curArg.startswith('-'):
				curArg=curArg[1:]
				if curArg.startswith('-'):
					curArg=curArg[1:]
			if curArg.find('=')>0:
				curVal=curArg[curArg.find('=')+1:]
				curVal=curVal.replace('=','\=')
				curArg=curArg[0:curArg.find('=')]

			#print 'arg:'+curArg
			#print 'val:'+curVal   
			if curArg!='output':
				arguments.update({curArg:curVal})
			else:
				self._xslt=curVal     
		return arguments

class AMI:

	_client=None

	def __init__( self ):

		self._client=AMI_WS_Client("","")

		return 

	def auth(self, user, password ):
		self._client.getAuthenticated(user,password)


	def execute(self,argv ):


		if len(argv)==0:
			raise AMI_Error( "You must provide a command" )
		#todo

		# here we filter out those commands which have a locally generated help.
		if(argv[0]=="help"):
			raise AMI_Error( "" )  

		arguments=self._client.parseArguments(argv)

		amiReply=self._client.execAMICommand(arguments) 
		#print amiReply._execAMICommand_arrayReturn.encode('utf-8')	
		xmlResults=self._client._parseData(amiReply) 
		return xmlResults


def main(argv):
	"""
   The code lines in this main method show how to
   use the client from another python program
   They could be copied from here to a command wrapper
   """
	try:     

		#get an AMI client	
		amiclient=AMI()


		#set user password (not mandatory to read)	
		#amiclient.auth("user",";pass;")


		#execute a command and get result in a result object
		# argv[0] should contain the name of the command
		# The other elements of arg contain the arguments to the command
		# Please see the command wrappers for more information
		# about passing arguments
		# 

		result= amiclient.execute(argv)		

		#print the default output of the command result
		# The default output=text, but others can be set using argument output.
		print result.output()


		# return a dictionary (of dictionaries of dictionaries )containing all rowsets in the result
		#resultDict=result.getDict()


		# write a GPickle file containing a dictionary of all rowsets in the result 
		# file named 'test.gpickle' 
		#result.writeGPickle('test.gpickle')


		#
		#print the result using a specific xls transformation
		# These are the XSLT which are provided on the server
		# XML is the native output.
		#print result.transform('xml')
		#print result.transform('html')
		#print result.transform('htmlTable')
		#print result.transform('csv')
		#print result.transform('test.gpickle')
		#print result.transform('gpickle')
		#
		# text = some information removed, only useful fields displayed
		#
		#print result.transform('text')
		# verbose = all information
		#print result.transform('verbose')
		#
		#
		# Or you can use your own XSLT to transform the native XML
		# set fileURL to the URL where an XSLT can be found
		#fileURL=""
		#print result.transform(fileURL)

		# This is a method which shows how to navigate across xml result
		#result.listRowsets()

		#Or obtain the DOM object which will allow you
		# to go directly to an element of the result
		#
		#dom=result.getAMIdom()








	except Exception, msg:	 
		print msg


if __name__=='__main__':

	main(sys.argv[1:])
	#print pyAMI_tutorial()




