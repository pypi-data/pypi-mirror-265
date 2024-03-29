"""
Module listing via an enum all the GHG types to consider
"""
from enum import Enum
from enum import unique


@unique
class EmissionType(str, Enum):
    """
    All emission types to consider

    NB:
    * 'Total' corresponds to overall equivalent CO2 emissions.
    * CO2 vs CO2b
        * the default CO2 is "fossil" CO2, which also appears as CO2f in Ademe db.
        * CO2b corresponds to so called "biogenic" CO2 emissions.

    """
    Total = 'CO2e (all GHGs, f/b)'
    CO2 = 'CO2'
    CH4 = 'CH4'
    N2O = 'N2O'
    SF6 = 'SF6'
    CO2b = 'CO2b'
    CH4b = 'CH4b'
    Other = 'Other GHGs'
    Fossil = 'Fossil (CO2e)'
    Biogenic = 'Biogenic (CO2e)'
    LULUC = 'LULUC (CO2e)'
