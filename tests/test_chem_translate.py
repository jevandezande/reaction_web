from pytest import mark, raises

from reaction_web.chem_translate import LatexConvertor, UnicodeConvertor, get_num, translate


@mark.parametrize(
    "string, num",
    [
        ("123HELLO", "123"),
        ("123", "123"),
        ("", ""),
        ("HELLO", ""),
        ("HELLO123", ""),
    ],
)
def test_get_num(string, num):
    assert get_num(string) == num


@mark.parametrize(
    "string, latex_str, unicode_str",
    [
        (
            "2H2O -> H3O+ + OH-",
            "2$\\cdot$H$_2$O -> H$_3$O$^+$ + OH$^-$",
            "2·H₂O -> H₃O⁺ + OH⁻",
        ),
        (
            "H2O + NH3 -> OH- + NH4+",
            "H$_2$O + NH$_3$ -> OH$^-$ + NH$_4^+$",
            "H₂O + NH₃ -> OH⁻ + NH₄⁺",
        ),
    ],
)
def test_translate(string, latex_str, unicode_str):
    assert translate(string, to="latex") == latex_str
    assert translate(string, to="unicode") == unicode_str

    with raises(ValueError):
        translate(string, to="html")


@mark.parametrize(
    "string, latex_str, unicode_str",
    [
        (
            "H3O+ + NH3 -> H2O + NH4+",
            "H$_3$O$^+$ + NH$_3$ -> H$_2$O + NH$_4^+$",
            "H₃O⁺ + NH₃ -> H₂O + NH₄⁺",
        )
    ],
)
def test_Convertor(string, latex_str, unicode_str):
    assert LatexConvertor.convert(string) == latex_str
    assert UnicodeConvertor.convert(string) == unicode_str


@mark.parametrize(
    "mol, latex_mol, unicode_mol",
    [
        ("H2O", "H$_2$O", "H₂O"),
        ("(NH4)(PO4)^2-", "(NH$_4$)(PO$_4$)$^{2-}$", "(NH₄)(PO₄)²⁻"),
        ("(MgO2)2(PbCl32)3^2-", "(MgO$_2$)$_2$(PbCl$_32$)$_3^{2-}$", "(MgO₂)₂(PbCl₃₂)₃²⁻"),
        ("OH.", "OH$^\\cdot$", "OH·"),
    ],
)
def test_mol_convertor(mol, latex_mol, unicode_mol):
    assert LatexConvertor.mol_convertor(mol) == latex_mol
    assert UnicodeConvertor.mol_convertor(mol) == unicode_mol
