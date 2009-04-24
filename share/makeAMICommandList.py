#! /usr/bin/env python
# Solveig Albrand December 2007
# A utility script which recurses into a directory structure
# to find the lists of python Commands defined for AMI
# eg : /afs/cern.ch/user/a/albrand/public/pyAMI
# given as the input parameter,
# finds the packages which are sub directories of the given root
# and which contain amiCommands files
# The commands to make the alias are made
# This script is run by the AMI developers to make the
# part of the cmt requirements file which sets up the aliases.
# It can also be run by users who wish to install a stand alone
# version of the python AMI client
####################################

import sys, re, os, fnmatch, commands
from string import *


        
def filefind(pattern, startdir=os.curdir):
    matches = []
    # call the function findvisitor with arguments((matches, pattern),dirname, names)
    # for each directory dirname, rooted at startdir
    # including startdir itself.
    # "names" = os.listdir(dirname)
    
    os.path.walk(startdir, findAllFiles, (matches, pattern))
    matches.sort
    return matches
   

def findAllFiles( (matches, pattern), thisdir, nameshere):
    for name in nameshere:
        if fnmatch.fnmatch(name, pattern):
            fullpath = os.path.join(thisdir, name)
            matches.append(fullpath)
	    

def writeLine(stream,name):
        stream.write( name)
	stream.write( "\n")

try:
	
	# this is the path to the wrappers. sys.path[0] returns the
	# place from where the script is being run (the share directory).
	path = sys.path[0]+'/../pyAMI/commands'
	print 'Looking for commands in '+ path

except:
	print 'No path found for the AMI commands'
	sys.exit()

# current working directory?
cwd = os.getcwd()
print 'writing alias maker scripts in '+cwd
outl= open(cwd+'/aliasMaker.sh','w');
outlc= open(cwd+'/aliasMaker.csh','w');
writeLine(outl,"#!/bin/zsh")
writeLine(outlc,"#!/bin/csh")
#writeLine(outl,"alias amiCommand='python "+path+"/pyAMI.py'")
#writeLine(outlc,"alias amiCommand 'python "+path+"/pyAMI.py'")
outc = open('listAllAMICommands.txt','w')
# get the list of sub directories of "commands"
mylist = os.listdir(path)
for container in mylist:

   comm = filefind('ami*.py',path+'/'+container)
		
# at this point comm is a vector containing a list of files which are amiCommands
		
   if comm:          
       writeLine(outl,"# "+container+" commands") 
       writeLine(outc,"# "+container+" commands") 
       for command in comm:
          sfilename = command.rsplit("/",1)[1].replace(".py","")
	  writeLine(outl,"alias "+sfilename+"='python "+command+"'")
	  writeLine(outlc,"alias "+sfilename+" 'python "+command+"'")
	  writeLine(outc,sfilename)		
	
outl.close()
outlc.close()
outc.close()


	




