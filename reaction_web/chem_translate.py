OPERATIONS = ["+", "=", ";", "->", "<-", "<>"]


def get_num(string: str) -> str:
    """
    >>> get_num("123HELLO")
    '123'
    >>> get_num("123")
    '123'
    >>> get_num("")
    ''
    >>> get_num("HELLO")
    ''
    >>> get_num("HELLO123")
    ''
    """
    i = 0
    for char in string:
        if not char.isnumeric():
            break
        i += 1
    return string[:i]


def translate(string: str, to: str = "latex") -> str:
    if to == "latex":
        return to_latex(string)
    raise ValueError(f"{to=} is not a supported translation")


def to_latex(string: str) -> str:
    """
    Converts a string to latex
    >>> to_latex("H2O + NH3 -> OH- + NH4+")
    'H$_2$O + NH$_3$ -> OH$^-$ + NH$_4^+$'
    """
    out = []

    chunks = [c for chunk in string.split() for c in chunk.split(";")]
    for chunk in chunks:
        if chunk in OPERATIONS or len(chunk) == 1:
            out.append(chunk)
            continue

        out.append(mol_to_latex(chunk))

    return " ".join(out)


def mol_to_latex(string: str) -> str:
    """
    Converts a molecular formula to latex
    >>> mol_to_latex("H2O")
    'H$_2$O'
    >>> mol_to_latex("(NH4)(PO4)^2-")
    '(NH$_4$)(PO$_4$)$^{2-}$'
    >>> mol_to_latex("(MgO2)2(PbCl32)3^2-")
    '(MgO$_2$)$_2$(PbCl$_32$)$_3^{2-}$'
    """
    out = ""

    # Leading number: stoichiometric ratio
    if string[0].isnumeric():
        number = get_num(string)
        out += f"{number}$\\cdot$"
        string = string[len(number) :]

    while string:
        increment = 1
        if (char := string[0]).isnumeric():
            number = get_num(string)
            increment = len(number)
            out += f"$_{number}$"
        elif char == "^":
            number = get_num(string[1:])
            increment = len(number) + 2
            charge = string[len(number) + 1]
            assert charge in ["-", "+"]
            out += f"$^{{{number}{charge}}}$"
        elif char in ["-", "+"]:
            out += f"$^{char}$"
        else:
            out += char

        string = string[increment:]

    return out.replace("$$", "")
