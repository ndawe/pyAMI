"""
pyAMI configuration
"""

from ConfigParser import ConfigParser


class AMIConfig(ConfigParser):

    def __init__(self):

        ConfigParser.__init__(self)
        self.optionxform = str
        self.add_section('AMI')
        self.reset()

    def reset(self):
        """
        Reset the configuration parameters.
        """
        self.set('AMI', 'AMIUser', '')
        self.set('AMI', 'AMIPass', '')

    def include(self, params):
        """
        This method only updates mandatory configuration parameters
        and their values with those specified in params.
        Returns a dictionary with mandatory parameters in 'AMI' section
        and params merged (priority given to params parameters).
        """
        _t = {}
        # Populate _t with current configuration from config file
        for _opt in self.options('AMI'):
            _t[ _opt ] = self.get('AMI', _opt)
        # Overwrite and/or add new parameters to _t
        for name, value in params.items():
            _t[name] = value
            # find correct section to update option
            if self.has_option('AMI', name):
                self.set('AMI', name, value)
        return _t

    def add_comment(self, section, comment):

        self.set(section, '; %s' % (comment,), None)

    def write(self, fp):
        """
        Write an .ini-format representation of the configuration state.
        """
        if self._defaults:
            fp.write("[%s]\n" % ConfigParser.DEFAULTSECT)
            for (key, value) in self._defaults.items():
                self._write_item(fp, key, value)
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                self._write_item(fp, key, value)
            fp.write("\n")

    def _write_item(self, fp, key, value):

        if key.startswith(';') and value is None:
            fp.write("%s\n" % (key,))
        else:
            fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
