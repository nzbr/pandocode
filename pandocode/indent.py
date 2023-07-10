def generate_indentation(lvl):
    result = ""
    for x in range(lvl + 1):
        result += "    "
    return result


def get_indentation_level(line):
    sp = line.split("    ")
    lvl = 0
    for s in sp:
        if s == "":
            lvl += 1
        else:
            break
    return lvl