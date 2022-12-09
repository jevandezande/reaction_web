from pytest import approx, mark, raises

from reaction_web.tools.helper import energy_conversion


@mark.parametrize(
    "from_e,to_e,expected",
    [
        ("hartree", "hartree", 1),
        ("hartree", "1/cm", 2.194746313702e5),
        ("kcal/mol", "kJ/mol", 4.1840),
    ],
)
def test_energy_conversion(from_e, to_e, expected):
    assert energy_conversion(from_e, to_e) == approx(expected)


def test_energy_conversion_raises():
    with raises(ValueError):
        energy_conversion("H", "kcal/mol")
