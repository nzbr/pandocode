from configuration import *

from generators import get_generator, get_keyword, generate_comment_line
from preprocessor import preprocess
from indent import generate_indentation, get_indentation_level
from controlSequences import processControlSequences


def process_line(line):
    if line.strip() == '':  # Don't process empty lines any further
        if cCountEmptyLines:
            return "\\State", None, False, 0
        else:
            return "\\Statex", None, False, 0

    sp = line.split("#")
    comment = ""
    if len(sp) > 1:
        if len(sp[-2]) == 0 or not sp[-2][-1] == "\\":
            comment = sp[-1]
            line = "\\#".join(sp[:-1])
        else:
            if not len(sp[-2]) == 0:
                sp[-2] = sp[-2][:-1]
            line = "\\#".join(sp)

    comment = comment.strip()
    line = line.strip()
    line = preprocess(line)

    terminator = None
    process_lvl = False
    transform = 0
    if line == "":
        line = generate_comment_line(comment)
    else:
        keyword = get_keyword(line)
        generator = get_generator(keyword)
        line, terminator, process_lvl, transform = generator(line)
        if not comment == "":
            line += " \\Comment{" + comment + "}"

    return line, terminator, process_lvl, transform  # Add generated line to result


def process_code(pcode):
    if pcode[-1] == "\n":  # Remove trailing newline
        pcode = pcode[:-1]

    pcode = pcode.split('\n')

    pcode = processControlSequences(pcode)

    tex = ""
    terminators = []
    lastlvl = 0
    for oline in pcode:
        oline = oline.replace("\t", "    ") # Remove tabs

        line = ""
        term = None
        process_lvl = False
        transform = 0

        if oline.strip().startswith(cRawPrefix+" "):
            line = oline.replace(cRawPrefix+" ", "").strip()
        else:
            line, term, process_lvl, transform = process_line(oline)

        if process_lvl:
            lvl = get_indentation_level(oline)
            while lvl < lastlvl:
                if len(terminators) == 0:
                    break
                tex += generate_indentation(lastlvl)+terminators.pop()+"\n"
                lastlvl -= 1
            lastlvl = lvl
        tex += generate_indentation(lastlvl+transform) + line + "\n"

        if term is not None:
            terminators += term

    while len(terminators) > 0:
        term = terminators.pop()
        if lastlvl > 0:
            lastlvl -= 1
        tex += generate_indentation(lastlvl) + term + "\n"
    texbegin = "\\algrenewcomment[1]{\\textsf{\\hfill//#1}}\n\\begin{algorithmic}[1]\\ttfamily\n"
    texend = "\\end{algorithmic}\n"
    return texbegin + tex + texend
