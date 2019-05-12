#!/usr/bin/python3

import sys
import os
import panflute as pf
from panflute import CodeBlock, RawBlock


def for_generator(code):
    code = code.replace("for ", "")
    return "\\For{" + code + "}", "\\EndFor"


def while_generator(code):
    code = code.replace("while ", "")
    return "\\While{" + code + "}", "\\EndWhile"


def if_generator(code):
    code = code.replace("if ", "")
    return "\\If{" + code + "}", "\\EndIf"


def else_generator(code):
    return "\\Else", None


def return_generator(code):
    code = code.replace("return ", "")
    return "\\State\\Return " + code, None


def state_generator(code):
    return "\\State " + code, None


def get_generator(fn):
    fn = fn.strip()
    fn = fn.split(" ")
    return {
        'while': while_generator,
        'if': if_generator,
        'else': else_generator,
        'for': for_generator,
        'return': return_generator
    }.get(fn[0], state_generator)


def global_substitutions(text):
    subst = [
        ("\\\\", "\\"),
        ("\\=", "="),
        ("==", "="),
        ("\\<", "<"),
        ("\\>", ">"),
        ("<=", "$\\leq$"),
        (">=", "$\\geq$"),
        ("<", "$<$"),
        (">", "$>$"),
        (" = ", " $\\leftarrow$ "),
        ("=", " $\\leftarrow$ "),
        (" to ", " \\textbf{to} "),
        (" in ", " $\\in$ "),
        (" and ", " $ \\land $ "),
        (" or ", " $\\lor$ "),
        (" not ", " $\\lnot$ ")
    ]
    subst = [(subst[x][0], "|:" + str(x) + ":|", subst[x][1]) for x in range(len(subst))]
    for s in subst:
        text = text.replace(s[0], s[1])
    for s in subst:
        text = text.replace(s[1], s[2])
    return text


def generate_indentation(lvl):
    indent = ""
    for x in range(lvl + 1):
        indent += "    "
    return indent


def process_pseudocode(pcode):
    if pcode[-1] == "\n":  # Remove trailing newline
        pcode = pcode[:-1]
    tex = ""
    terminators = []
    llvl = 0
    for line in pcode.split('\n'):
        lvl = 0

        if line == '':  # Remove empty lines
            tex += generate_indentation(llvl) + "\\Statex\n"
            continue
        mod = line
        mod = mod.replace("\t", "    ")

        if not mod.strip().startswith("else"):
            modsp = mod.split("    ")
            for s in modsp:
                if s == "":
                    lvl = lvl + 1
                else:
                    break
            if lvl < llvl:
                for x in range(llvl - lvl):
                    term = terminators.pop()
                    tex += generate_indentation(lvl) + term + "\n"
            llvl = lvl
        else:
            lvl = llvl-1

        modsp = mod.split("#")
        comment = ""
        if len(modsp) > 1:
            if len(modsp[-2]) == 0 or not modsp[-2][-1] == "\\":
                comment = modsp[-1]
                mod = "\\#".join(modsp[:-1])
            else:
                if not len(modsp[-2]) == 0:
                    modsp[-2] = modsp[-2][:-1]
                mod = "\\#".join(modsp)
        comment = comment.strip()

        mod = mod.strip()
        try:
            if mod[-1] == ":":
                mod = mod[:-1]
        except IndexError:
            pass
        mod = global_substitutions(mod)
        generator = get_generator(mod)
        if mod == "":
            mod = "\\State //" + comment
        else:
            mod, terminator = generator(mod)
            if terminator is not None:
                terminators += [terminator]
            if not comment == "":
                mod += " \\Comment{" + comment + "}"

        if not mod[-1] == "\n":  # Ensure newline
            mod += "\n"

        tex += generate_indentation(lvl) + mod  # Add generated line to result

    i=llvl
    while len(terminators) > 0:
        term = terminators.pop()
        llvl -= 1
        tex += generate_indentation(llvl) + term + "\n"
    texbegin = "\\algrenewcomment[1]{\\textsf{\\hfill//#1}}\n\\begin{algorithmic}[1]\\ttfamily\n"
    texend = "\\end{algorithmic}\n"
    return texbegin + tex + texend


def prepare(doc):
    pass


def action(elem, doc):
    if type(elem) == CodeBlock and "pseudo" in elem.classes:
        text = elem.text
        text = process_pseudocode(text)
        return RawBlock(text, format='latex')
        # return None -> element unchanged
        # return [] -> delete element


def finalize(doc):
    pass


def main(doc=None):
    return pf.run_filter(action,
                         prepare=prepare,
                         finalize=finalize,
                         doc=doc)


if len(sys.argv) == 2:
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], 'r') as f:
            readcode = f.read()
        print(process_pseudocode(readcode)[:-1])
    elif sys.argv[1] == "latex":
        main()
