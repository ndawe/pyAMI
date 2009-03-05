"""
:File:        pyAMIErrors.py
:Description: pyAMI error classes.
:Author:      Jerome Fulachier (1st version from  Chun Lik Tan (Alvin))
:Institution: LPSC Grenoble
:Email:       jerome.fulachier@lpsc.in2p3.fr
:Created:     13 Aug 2004
"""

class AMI_Error( Exception ):
   """
   Simple wrapper for errors.
   """
   def __init__( self, msg=None ):
      if msg is None:
         self.errMsg = ''
      else:
         self.errMsg = msg

   def __repr__( self ):
      return self.errMsg

   def __str__( self ):
      return self.errMsg

class AMI_Info( AMI_Error ):
   """
   Simple wrapper to show AMI information.
   """
   def __init__( self, msg ):
      AMI_Error.__init__( self )
      self.errMsg = msg

class pyAMI_Error( AMI_Error ):
   def __init__( self, msg ):
      AMI_Error.__init__( self )
      self.errMsg = msg

class pyAMI_Info( AMI_Error ):
   def __init__( self, msg ):
      AMI_Error.__init__( self )
      self.errMsg = msg
