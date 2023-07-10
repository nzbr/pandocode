from .configuration import *
from .generators import get_keyword

def processControlSequences(fullcode):
    if fullcode[0].startswith("#!"): # Remove shebang
        fullcode = fullcode[1:]

    out = []
    usebegin = False
    active = True
    skip = False

    for line in fullcode:
        if skip:
            skip = False
            continue

        sline = line.strip()
        if sline.startswith(cControlPrefix):
            keyword = get_keyword(sline)
            if keyword == cBeginPrefix:
                if not usebegin:
                    out = []
                    usebegin = True
                active = True
                continue
            elif keyword == cEndPrefix:
                active = False
                continue
            elif active:
                if keyword == cSkipPrefix:
                    skip = True
                    continue
                elif keyword == cAddPrefix:
                    out += [line.replace(cAddPrefix + " ", "")]
                    continue
                elif keyword == cReplacePrefix:
                    out += [line.replace(cReplacePrefix + " ", "")]
                    skip = True
                    continue
        elif active:
            out += [line]

    return out
