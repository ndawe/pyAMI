"""
:File:        pyAMIConfig.py
:Description: pyAMI in-memory configuration / initialisation.
:Author:      Jerome Fulachier (1st version from  Chun Lik Tan (Alvin))
:Institution: LPSC Grenoble
:Email:       jerome.fulachier@lpsc.in2p3.fr
:Created:     26 Aug 2004
:Modified:    11 Aug 2005
"""

from ConfigParser import *
from os.path import exists, expandvars

class pyAMIConfig( ConfigParser ):
   def __init__( self ):
      ConfigParser.__init__( self )
      self.create_pyAMI_config()

   def optionxform( self, name ):
      return str( name )

   def create_pyAMI_config( self ):
      """
      Populates in-memory config with common/mandatory parameters and their default values.
      """
      self.add_section( 'AMI' )
      self.add_section( 'AMIMISC' )
      self.reset_pyAMI_config()

   def reset_pyAMI_config( self ):
      """
      Reset the configuration parameters.
      """
      self.set( 'AMI', 'AMIUser', '')
      self.set( 'AMI', 'AMIPass', '')
      self.set( 'AMIMISC', 'separator', ';' )

   def includeCfg( self, extraParamsDict ):
      """
      This method only updates mandatory configuration parameters and their values with those specified in extraParamsDict. Returns a dictionary with mandatory parameters in 'AMI' section and extraParamsDict merged (priority given to extraParamsDict parameters).
      """
      _t = {}
      # Populate _t with current configuration from config file
      for _opt in self.options( 'AMI' ):
         _t[ _opt ] = self.get( 'AMI', _opt )
      # Overwrite and/or add new parameters to _t
      for x in extraParamsDict:
         _t[ x ] = extraParamsDict[ x ]
         # find correct section to update option
         if self.has_option( 'AMI', x ):
            self.set( 'AMI', x, _t[ x ] )
      return _t
