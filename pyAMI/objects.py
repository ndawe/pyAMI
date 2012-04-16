from string import rjust
from cStringIO import StringIO


class DatasetInfo(object):

    def __init__(self, dataset):

        self.dataset = dataset
        self.info = {}
        self.extra = {}
        self.comments = {}
        self.properties = {}

    def __repr__(self):

        return self.__str__()

    def __str__(self):

        out = StringIO()
        if self.info:
            print >> out, ""
            print >> out, "Dataset Parameters"
            print >> out, "========================"
            for name, value in self.info.items():
                spaces = rjust(" ", 30 - len(name))
                print >> out, name + spaces + value
        if self.comments:
            print >> out, ''
            print >> out, "Comments"
            print >> out, "========================"
            for name, value in self.comments.items():
                spaces = rjust(" ", 30 - len(name))
                print >> out, name + spaces + value
        if self.extra:
            print >> out, ''
            print >> out, "Extra Parameters"
            print >> out, "========================"
            for name, value in self.extra.items():
                spaces = rjust(" ", 30 - len(name))
                print >> out, name + spaces + value
        if self.properties:
            print >> out, ''
            print >> out, "Other Physics Properties"
            print >> out, "========================"
            for physProp, tmpDict in self.properties.items():
                valueToPrint = ''
                if tmpDict.get("min") == tmpDict.get("max"):
                    valueToPrint = tmpDict.get("min")
                else:
                    valueToPrint = ' - '.join([tmpDict.get("min"), tmpDict.get("max")])
                print >> out, physProp + rjust(' ', 30 - len(physProp)) + \
                        ' '.join([valueToPrint, tmpDict.get("unit"), '(%s)' % tmpDict.get("description")])
        return out.getvalue()


class RunPeriod(object):

    def __init__(self, project, name, level,
                 status,
                 description,
                 year=0):

        self.project = project
        self.year = year
        self.name = name
        self.level = level
        self.status = status
        self.description = description

    def __cmp__(self, other):

        if self.year > other.year:
            return 1
        elif self.year < other.year:
            return -1
        return cmp(self.name, other.name)

    def __repr__(self):

        return self.__str__()

    def __str__(self):

        return '%s %s' % (self.project, self.name)
