#!/usr/bin/env python

import sys
from itertools import imap
import simplejson
from xml.etree import ElementTree
from collections import defaultdict
import re
from timex3 import Timex3Entity

def print_timex(timex):
    print "-------- "
    print "text: ", timex.text
    print "attribs: \n\t", "\n\t".join("%s :%s" %i for i in timex.attrib.items())

if __name__ == '__main__':

    for infile in sys.argv[1:]:
        #sys.stderr.write("reading from %s\n" %infile)
        try:
            json_data = simplejson.load(open(infile))
        except:
            continue
        seen_expressions = set()
        for sentence in json_data['sentences']:
            for word, annotation in sentence['words']:
                if not 'Timex' in annotation:
                    continue
                timex = ElementTree.fromstring(annotation['Timex'])
                tid = timex.attrib['tid']
                if not tid in seen_expressions:
                    if not timex.attrib['type'] == 'DATE':
                        continue
                    print_timex(timex)
                    if 'value' in timex.attrib:
                        print "AMR:", Timex3Entity(timex)
                    else:
                        print "skipping (no value)"

                seen_expressions.add(tid)
