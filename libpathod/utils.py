import os, re
import rparse

class AnchorError(Exception): pass


def parse_anchor_spec(s, settings):
    """
        For now, this is very simple, and you can't have an '=' in your regular
        expression.
    """
    if not "=" in s:
        raise AnchorError("Invalid anchor definition: %s"%s)
    rex, spec = s.split("=", 1)
    try:
        re.compile(rex)
    except re.error:
        raise AnchorError("Invalid regex in anchor: %s"%s)
    try:
        rparse.parse(settings, spec)
    except rparse.ParseException, v:
        raise AnchorError("Invalid page spec in anchor: '%s', %s"%(s, str(v)))

    return rex, spec


class Data:
    def __init__(self, name):
        m = __import__(name)
        dirname, _ = os.path.split(m.__file__)
        self.dirname = os.path.abspath(dirname)

    def path(self, path):
        """
            Returns a path to the package data housed at 'path' under this
            module.Path can be a path to a file, or to a directory.

            This function will raise ValueError if the path does not exist.
        """
        fullpath = os.path.join(self.dirname, path)
        if not os.path.exists(fullpath):
            raise ValueError, "dataPath: %s does not exist."%fullpath
        return fullpath


data = Data(__name__)
