#!/usr/bin/env python

import re

#Todo: track variable numbers

#### Resources ####
# Todo: externalize

# XXXX-10-31
re_date = [
    re.compile(r'\w{4}-\w{2}-(?P<day>\d\d)'),
    re.compile(r'\w{4}-(?P<month>\w{2})\W'),
    re.compile(r'^(?P<year>\d{4})'),
    re.compile(r'\w{4}-W\w{2}-(?P<weekday>\d)')
]

weekdays = ['Monday','Tuesday','Wednesday',
            'Thursday','Friday','Saturday',
            'Sunday']

timex3_type_to_role = {
    "DATE" : "date-entity"
}

def concept_prototype(concept, var_offset=0):
    """ return concept with placeholder for roles

    eg. name -> (n / name %%s)
    var_offset to be used for variable naming
    """
    variable_name = concept[0].lower()
    if var_offset >0:
        variable_name += str(var_offset)
    return "(%s / %s %%s)" %(variable_name, concept)

def role_str(role, concept=None):
    if concept == None:
        return ":%s" %(role)
    return ":%s %s" %(role, concept)


class Timex3Entity(object):

    def __init__(self, timex):
        #print timex.attrib
        self.timex = dict(timex.attrib)
        self.type = self.timex['type']
        self.date_entity = {}

        # extract info from value and store in self.date_entity
        v = self.timex['value']
        for regexp in re_date:
            m = regexp.search(v)
            if m == None:
                continue
            self.date_entity.update(m.groupdict())

    def weekday_to_string(self, weekday):
        """ converts 3 to :weekday (w/ Wednesday)
        """
        assert weekday > 0 and weekday < 8, "weekday must be in [1,7]"
        wd = weekdays[weekday-1]
        wd_concept = concept_prototype(wd) %('')
        return wd_concept

    def __str__(self):
        # special treatment for weekdays
        if 'weekday' in self.date_entity:
            wd = int(self.date_entity['weekday'])
            self.date_entity['weekday'] = self.weekday_to_string(wd)

        instances = " ".join(role_str(*i) for i in self.date_entity.iteritems())
        return concept_prototype('date-entity') %(instances)
