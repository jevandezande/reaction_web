"""Translates chemical formulae to LaTeX or Unicode."""

from abc import ABC, abstractmethod
from typing import Literal


def get_num(string: str) -> str:
    """
    Get the leading number from a string.

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


def translate(string: str, to: Literal["latex", "unicode"] = "latex") -> str:
    """
    Translate a chemical formula to the desired format.

    :param string: the chemical formula
    :param to: the desired format (latex or unicode)
    :return: the translated formula

    >>> translate("H2O + NH3 -> OH- + NH4+", "unicode")
    'H₂O + NH₃ -> OH⁻ + NH₄⁺'
    """
    if to == "latex":
        return LatexConvertor.convert(string)
    elif to == "unicode":
        return UnicodeConvertor.convert(string)

    raise ValueError(f"{to=} is not a supported translation")


class Convertor(ABC):
    r"""
    Convert a chemical formula into the desired format.

    >>> UnicodeConvertor.convert("H2O + NH3 -> OH- + NH4+")
    'H₂O + NH₃ -> OH⁻ + NH₄⁺'
    >>> LatexConvertor.convert("2(NH4)(PO4)^2- + 3Ca(NO3)2 -> Ca3(PO4)2 + 6NH4NO3")
    '2$\\cdot$(NH$_4$)(PO$_4$)$^{2-}$ + 3$\\cdot$Ca(NO$_3$)$_2$ -> Ca$_3$(PO$_4$)$_2$ + 6$\\cdot$NH$_4$NO$_3$'
    """

    OPERATIONS = {"+", "=", ";", "->", "<-", "<>"}

    @classmethod
    def convert(cls, string: str) -> str:
        """Convert a string to the chemical format."""
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
        r"""
        Convert a molecular formula to the desired format.

        >>> LatexConvertor.mol_convertor("H2O")
        'H$_2$O'
        >>> LatexConvertor.mol_convertor("2(NH4)(PO4)^2-")
        '2$\\cdot$(NH$_4$)(PO$_4$)$^{2-}$'
        >>> UnicodeConvertor.mol_convertor("3(MgO2)2(PbCl32)3^2-")
        '3·(MgO₂)₂(PbCl₃₂)₃²⁻'
        """
        out = ""

        # Leading number: stoichiometric ratio
        if string[0].isnumeric():
            number = get_num(string)
            out += number + cls.cdot()  # type: ignore
            string = string[len(number) :]

        while string:
            increment = 1
            char = string[0]
            if char.isnumeric():
                number = get_num(string)
                increment = len(number)
                out += cls.subscript_number(number)
            elif char == "^":
                number = get_num(string[1:])
                increment = len(number) + 2
                charge_radical = string[len(number) + 1]
                assert charge_radical in CHARGE_RADICAL
                out += cls.superscript_number_charge_or_radical(number, charge_radical)
            elif char in ["-", "+", "."]:
                out += cls.superscript_number_charge_or_radical("", char)
            else:
                out += char

            string = string[increment:]

        return cls.finalize(out)

    @classmethod
    @abstractmethod
    def subscript_number(cls, number: str) -> str:
        """Convert a number to subscript."""
        ...

    @classmethod
    @abstractmethod
    def superscript_number_charge_or_radical(cls, number: str, charge_radical: str) -> str:
        """Convert a number and charge/radical to superscript."""
        ...

    @classmethod
    @abstractmethod
    def cdot(cls) -> str:
        """Make a middle dot."""
        ...

    @classmethod
    def finalize(cls, string: str) -> str:
        """Perform cleanup operations on the string."""
        return string


class LatexConvertor(Convertor):
    """
    Converts a string to latex.

    >>> LatexConvertor.convert("H2O + NH3 -> OH- + NH4+")
    'H$_2$O + NH$_3$ -> OH$^-$ + NH$_4^+$'
    """

    @classmethod
    def finalize(cls, string: str) -> str:
        """
        Perform cleanup operations on the string.

        Remove double dollar signs.

        :param string: the string to finalize
        :return: the finalized string

        >>> LatexConvertor.finalize("$123$$456$")
        '$123456$'
        """
        return string.replace("$$", "")

    @classmethod
    def subscript_number(cls, number: str) -> str:
        """
        Convert a number to subscript.

        :param number: the number to convert
        :return: the string as subscripts

        >>> LatexConvertor.subscript_number("123")
        '$_123$'
        """
        return f"$_{number}$"

    @classmethod
    def superscript_number_charge_or_radical(cls, number: str, charge_radical: str) -> str:
        r"""
        Convert a number and charge/radical to superscript.

        :param number: the number to convert
        :param charge_radical: the charge or radical to convert
        :return: the converted string

        >>> LatexConvertor.superscript_number_charge_or_radical("123", "-")
        '$^{123-}$'
        >>> LatexConvertor.superscript_number_charge_or_radical("", "+")
        '$^+$'
        >>> LatexConvertor.superscript_number_charge_or_radical("2", ".")
        '$^{2\\cdot}$'
        """
        charge_radical = charge_radical if charge_radical != "." else "\\cdot"
        return f"$^{{{number}{charge_radical}}}$" if number else f"$^{charge_radical}$"

    @classmethod
    def cdot(cls) -> str:
        """Make a middle dot."""
        return "$\\cdot$"


class UnicodeConvertor(Convertor):
    """
    Convert a string to unicode.

    >>> UnicodeConvertor.convert("H2O + NH3 -> OH- + NH4+")
    'H₂O + NH₃ -> OH⁻ + NH₄⁺'
    """

    @classmethod
    def subscript_number(cls, number: str) -> str:
        """
        Convert a number to subscript.

        >>> UnicodeConvertor.subscript_number("123")
        '₁₂₃'
        """
        return str.translate(number, UNICODE_SUBSCRIPT_TRANSLATION)

    @classmethod
    def superscript_number_charge_or_radical(cls, number: str, charge_radical: str) -> str:
        """
        Convert a number and charge or radical to superscript.

        Note: there is no superscript dot in Unicode, thus a middle dot is used.

        >>> UnicodeConvertor.superscript_number_charge_or_radical("123", "-")
        '¹²³⁻'
        >>> UnicodeConvertor.superscript_number_charge_or_radical("", "+")
        '⁺'
        >>> UnicodeConvertor.superscript_number_charge_or_radical("2", ".")
        '²·'
        """
        out = str.translate(number, UNICODE_SUPERSCRIPT_TRANSLATION) if number else ""
        return out + str.translate(charge_radical, UNICODE_CHARGE_RADICAL_TRANSLATION)

    @classmethod
    def cdot(cls) -> str:
        """Make a middle dot."""
        return "·"


UNICODE_SUPERSCRIPT_TRANSLATION = {ord(str(i)): v for i, v in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹")}
UNICODE_SUBSCRIPT_TRANSLATION = {ord(str(i)): v for i, v in enumerate("₀₁₂₃₄₅₆₇₈₉")}
UNICODE_CHARGE_RADICAL_TRANSLATION = {ord("+"): "⁺", ord("-"): "⁻", ord("."): "·"}
CHARGE_RADICAL = ["-", "+", "."]
