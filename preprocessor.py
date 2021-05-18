def preprocess(code):
    """Pre-processes the code for every generator"""
    code = code.strip()
    if len(code) == 0: # Dont preprocess empty lines
        return code
    if code[-1] == ":":
        code = code[:-1]
    code = apply_substitutions(code)
    return code


def apply_substitutions(text):
    subst = [
        ("\\\\", "\\"),
        ("\\=", "="),
        ("==", "="),
        ("!=", "$\\neq$"),
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
