#!/usr/bin/python3

import sys
import os
from panflute import run_filter, CodeBlock, RawBlock

from codeprocessor import process_code


def prepare(doc):
    pass


def action(elem, doc):
    if type(elem) == CodeBlock and "pseudo" in elem.classes:
        text = elem.text
        text = process_code(text)
        return RawBlock(text, format='latex')
        # return None -> element unchanged
        # return [] -> delete element


def finalize(doc):
    pass


def main(doc=None):
    return run_filter(action,
                      prepare=prepare,
                      finalize=finalize,
                      doc=doc)


if len(sys.argv) == 2:
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], 'r') as f:
            readcode = f.read()
        print(process_code(readcode)[:-1])
    elif sys.argv[1] == "latex":
        main()
