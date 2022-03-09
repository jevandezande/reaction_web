from abc import ABC, abstractmethod


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
        return LatexConvertor.convert(string)
    else:
        raise ValueError(f"{to=} is not a supported translation")


class Convertor(ABC):
    OPERATIONS = ["+", "=", ";", "->", "<-", "<>"]

    @classmethod
    def convert(cls, string: str) -> str:
        out = []

        chunks = [c for chunk in string.split() for c in chunk.split(";")]
        for chunk in chunks:
            if chunk in cls.OPERATIONS or len(chunk) == 1:
                out.append(chunk)
                continue

            out.append(cls.mol_convertor(chunk))

        return " ".join(out)

    @classmethod
    def mol_convertor(cls, string: str) -> str:
        """
        Converts a molecular formula to latex
        >>> LatexConvertor.mol_convertor("H2O")
        'H$_2$O'
        >>> LatexConvertor.mol_convertor("(NH4)(PO4)^2-")
        '(NH$_4$)(PO$_4$)$^{2-}$'
        >>> LatexConvertor.mol_convertor("(MgO2)2(PbCl32)3^2-")
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
                out += cls.subscript_number(number)
            elif char == "^":
                number = get_num(string[1:])
                increment = len(number) + 2
                charge = string[len(number) + 1]
                assert charge in ["-", "+"]
                out += cls.superscript_number_charge(number, charge)
            elif char in ["-", "+"]:
                out += cls.superscript_number_charge("", char)
            else:
                out += char

            string = string[increment:]

        return cls.finalize(out)

    @classmethod
    @abstractmethod
    def subscript_number(cls, number: str) -> str:
        pass

    @classmethod
    @abstractmethod
    def superscript_number_charge(cls, number: str, charge: str) -> str:
        pass

    @classmethod
    def finalize(cls, string: str) -> str:
        return string


class LatexConvertor(Convertor):
    """
    Converts a string to latex
    >>> LatexConvertor.convert("H2O + NH3 -> OH- + NH4+")
    'H$_2$O + NH$_3$ -> OH$^-$ + NH$_4^+$'
    """

    @classmethod
    def finalize(cls, string: str) -> str:
        """
        Removes double dollar signs
        >>> LatexConvertor.finalize("$123$$456$")
        '$123456$'
        """
        return string.replace("$$", "")

    @classmethod
    def subscript_number(cls, number: str) -> str:
        """
        Converts a number to subscript
        >>> LatexConvertor.subscript_number("123")
        '$_123$'
        """
        return f"$_{number}$"

    @classmethod
    def superscript_number_charge(cls, number: str, charge: str) -> str:
        """
        Converts a number and charge to superscript
        >>> LatexConvertor.superscript_number_charge("123", "-")
        '$^{123-}$'
        >>> LatexConvertor.superscript_number_charge("", "+")
        '$^+$'
        """
        return f"$^{{{number}{charge}}}$" if number else f"$^{charge}$"
