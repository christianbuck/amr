#!/usr/bin/env python

import sys
from itertools import imap
import simplejson
from xml.etree import ElementTree
from collections import defaultdict
import re
from timex3 import Timex3Entity

def print_timex(timex, s_id, w_ids):
    print "-------- "
    print "snt: %s, word %s - %s" %(s_id, min(w_ids), max(w_ids))
    print "text: ", timex.text
    print "attribs: \n\t", "\n\t".join("%s :%s" %i for i in timex.attrib.items())

def find_spans(sentence):
    spans = defaultdict(list)
    for word_id, (word, annotation) in enumerate(sentence['words']):
        if 'Timex' in annotation:
            timex = ElementTree.fromstring(annotation['Timex'])
            tid = timex.attrib['tid']
            spans[tid].append(word_id)
    return spans

if __name__ == '__main__':

    for infile in sys.argv[1:]:
        #sys.stderr.write("reading from %s\n" %infile)
        try:
            json_data = simplejson.load(open(infile))
        except:
            continue
        for sentence_id, sentence in enumerate(json_data['sentences']):
            seen_expressions = set()
            spans = find_spans(sentence)
            for word_id, (word, annotation) in enumerate(sentence['words']):
                if not 'Timex' in annotation:
                    continue
                timex = ElementTree.fromstring(annotation['Timex'])
                tid = timex.attrib['tid']
                assert tid in spans
                if not tid in seen_expressions:
                    print_timex(timex, sentence_id, spans[tid])
                    if timex.attrib['type'] == 'DATE':
                        if 'value' in timex.attrib:
                            print "AMR:", Timex3Entity(timex)
                        else:
                            print "skipping (no value)"

                seen_expressions.add(tid)

