"""Helper functions."""

# Values from NIST
energy_conversions = {
    "hartree": {
        "hartree": 1,
        "kJ/mol": 2625.49962,
        "kcal/mol": 627.509,
        "eV": 27.21138602,
        "1/cm": 2.194746313702e5,
    },
    "kJ/mol": {
        "hartree": 3.8088e-4,
        "kJ/mol": 1,
        "kcal/mol": 0.23901,
        "eV": 1.0364e-2,
        "1/cm": 83.593,
    },
    "kcal/mol": {
        "hartree": 1.5936e-3,
        "kJ/mol": 4.1840,
        "kcal/mol": 1,
        "eV": 4.3363e-2,
        "1/cm": 349.75,
    },
    "eV": {
        "hartree": 3.6749e-2,
        "kJ/mol": 96.485,
        "kcal/mol": 23.061,
        "eV": 1,
        "1/cm": 8065.5,
    },
    "1/cm": {
        "hartree": 4.556335252767e-6,
        "kJ/mol": 1.1963e-2,
        "kcal/mol": 2.8591e-3,
        "eV": 1.2398e-4,
        "1/cm": 1,
    },
}


def energy_conversion(from_e: str, to_e: str) -> float:
    """Convert energy from one unit to another."""
    try:
        return energy_conversions[from_e][to_e]
    except KeyError as err:
        raise ValueError("Unable to convert {from_e} to {to_e}") from err
