"""
Module implemeening all unit enums
"""
from enum import Enum
from enum import unique


@unique
class BasicUnits(str, Enum):
    """
    Basic units for insertion factors
    """
    kWh = 'kWh'
    kg = 'kg'
    unit = 'unit'
    ton = 'ton'
    toe = 'toe'
    tonkm = 'ton.km'
    km = 'km'
    pax = 'passenger'
    paxkm = 'passenger.km'
    L = 'L'
    vehiclekm = 'vehicle.km'
    vehicleyear = 'vehicle.year'
    ha = 'ha'
    m2 = 'm2'
    m3 = 'm3'
    m3km = 'm3.km'
    device = 'device'
    kEUR = 'k EUR'
    XPF = 'Franc CFP'
    MJ = 'MJ'
    GJ = 'GJ'
    mL = 'mL'
    errand = 'errand'
    kgH2 = 'kgH2'


@unique
class BasicUSUnits(str, Enum):
    kgCO2 = 'kgCO2'
    gCH4 = 'gCH4'
    gN2O = 'gN2O'
    lbCO2 = 'lbCO2'
    lbCH4 = 'lbCH4'
    lbN2O = 'lbN2O'


@unique
class DivisorUSUnits(str, Enum):
    mmBtu = 'mmBtu'
    tn = 'short ton'
    scf = 'scf'
    gal = 'gal'
    mile = 'mi'
    MWh = 'MWh'
    vehicle_mile = 'vehicle.mi'
    ton_mile = 'ton.mi'
    passenger_mile = 'passenger.mi'
    kg = 'kg'
