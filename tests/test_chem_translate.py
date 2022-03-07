from reaction_web.chem_translate import LatexConvertor, get_num, translate


def test_get_num():
    assert get_num("123HELLO") == "123"
    assert get_num("123") == "123"
    assert get_num("") == ""
    assert get_num("HELLO") == ""
    assert get_num("HELLO123") == ""


def test_translate():
    assert translate("H2O -> H+ + OH-") == "H$_2$O -> H$^+$ + OH$^-$"
    assert translate("H2O + NH3 -> OH- + NH4+") == "H$_2$O + NH$_3$ -> OH$^-$ + NH$_4^+$"


def test_LatexConvertor():
    assert LatexConvertor.mol_convertor("H2O") == "H$_2$O"
    assert LatexConvertor.mol_convertor("(NH4)(PO4)^2-") == "(NH$_4$)(PO$_4$)$^{2-}$"
    assert LatexConvertor.mol_convertor("(MgO2)2(PbCl32)3^2-") == "(MgO$_2$)$_2$(PbCl$_32$)$_3^{2-}$"

    assert LatexConvertor.convert("H3O+ + NH3 -> H2O + NH4+") == "H$_3$O$^+$ + NH$_3$ -> H$_2$O + NH$_4^+$"
