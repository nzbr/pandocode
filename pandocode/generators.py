from sys import stderr, exit

def get_generator(keyword):
    """Get the corresponding generator to a given keyword"""
    return {
        'def'    : function_generator,
        'while'  : create_generator("\\While"        , ["\\EndWhile"], "while" , True ,  0, gen_param ),
        'if'     : create_generator("\\If"           , ["\\EndIf"]   , "if"    , True ,  0, gen_param ),
        'else'   : create_generator("\\Else"         , None          , "else"  , False, -1, gen_prefix),
        'elif'   : create_generator("\\ElsIf"        , None          , "elif"  , False, -1, gen_param ),
        'for'    : create_generator("\\For"          , ["\\EndFor"]  , "for"   , True ,  0, gen_param ),
        'return' : create_generator("\\State\\Return", None          , "return", True ,  0, gen_prefix)
    }.get(keyword, create_generator("\\State"        , None          , None    , True ,  0, gen_prefix)) #Default


def get_keyword(line):
    return line.split(' ')[0].strip()


def generate_comment_line(comment):
    return "\\State //" + comment


def gen_param(code, prefix):
    """Generate LaTeX in the Format \\Prefix{code}"""
    return prefix+"{"+code+"}"


def gen_prefix(code, prefix):
    """Generate LaTeX in the Format \\Prefix code"""
    return prefix+" "+code


def function_generator(code):
    """Generate LaTeX for function definitions"""
    code = remove_keyword(code, "def").strip()
    code = code.split("(")
    if not len(code) == 2:
        die("Malformed def statement!")
    code = [code[0]] + code[1].split(")")
    if not len(code) == 3:
        die("Malformed def statement!")
    name, params, _ = code
    return "\\Function{"+name+"}{"+params+"}", ["\\EndFunction"], True, 0


def die(err):
    stderr.write(err)
    stderr.flush()
    exit(1)


def remove_keyword(code, keyword):
    if keyword is not None:
        code = code[len(keyword):]+" "
    return code.strip()


def create_generator(prefix, terminator, keyword, process_lvl, transform, function):
    """Creates a generator function that accepts a line of code and returns LaTeX"""
    return lambda code : (function(remove_keyword(code, keyword), prefix), terminator, process_lvl, transform)
