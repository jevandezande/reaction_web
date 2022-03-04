from reaction_web.chem_translate import get_num, mol_to_latex, to_latex, translate


def test_get_num():
    assert get_num("123HELLO") == "123"
    assert get_num("123") == "123"
    assert get_num("") == ""
    assert get_num("HELLO") == ""
    assert get_num("HELLO123") == ""


def test_translate():
    assert translate("H2O -> H+ + OH-") == "H$_2$O -> H$^+$ + OH$^-$"


def test_to_latex():
    assert to_latex("H2O + NH3 -> OH- + NH4+") == "H$_2$O + NH$_3$ -> OH$^-$ + NH$_4^+$"


def test_mol_to_latex():
    assert mol_to_latex("H2O") == "H$_2$O"
    assert mol_to_latex("(NH4)(PO4)^2-") == "(NH$_4$)(PO$_4$)$^{2-}$"
    assert mol_to_latex("(MgO2)2(PbCl32)3^2-") == "(MgO$_2$)$_2$(PbCl$_32$)$_3^{2-}$"
