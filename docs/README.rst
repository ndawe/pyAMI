
Compiling the Docs
------------------

To build all the docs::

    make


Uploading the Docs
------------------

To update the docs at https://end.web.cern.ch/end/projects/pyAMI/::
   
   mkdir -p ${HOME}/remote/cern
   wdfs https://dfs.cern.ch/dfs/Websites/e/end/ ${HOME}/remote/cern -u end -p <password>
   ./update_noel_docs.sh

To update the docs at https://atlas-ami.cern.ch/AMI/pyAMI/::

   ssh ${USER}@lxplus.cern.ch
   ssh ${USER}@lxvoadm.cern.ch
   ssh voatlas126
   sudo -s
   cd /usr/local/webapps/AMI/pyAMI

Copy the contents of pyAMI/docs/_build/html there.
