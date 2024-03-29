"""
Module listing possible emission factor sectors
"""
from enum import Enum
from enum import unique


@unique
class Sector(str, Enum):
    """
    Ppossible emission factor sectors

    NB: close but different from EcoInvent classification!
    see EcoInvent insertor for more details.
    """
    Electricity = 'Electricity'
    Goods_Purchase = 'Purchase of goods'
    Services_Purchase = 'Purchase of services'
    Fuels = 'Fuels'
    Heat = 'Heat and heating networks'
    Cool = 'Cooling networks'
    Transport = 'Transport (goods and pax)'
    Waste_Recycling = 'Waste treatment and recycling'
    LULUCF = 'Land use, land-use change, and forestry'
    Territorial_Stats = 'Territorial statistics'
    Process = 'Process and fugitive emissions'
    Refrigerant = 'Refrigerant'
    Resource_Extraction = 'Resource Extraction'
    Wood = 'Wood'
    Chemicals = 'Chemicals (production)'
    Agriculture = 'Agriculture & Animal Husbandry'
    Electronics = 'Electronics'
    Metals = 'Metals'
    Concrete = 'Cement & Concrete'
    Infrastructure = 'Infrastructure & Machinery'
    Fishing = 'Fishing & Aquaculture'
    Minerals = 'Minerals'
    Paper = 'Pulp & Paper'
    Water = 'Water Supply'
    Textiles = 'Textiles'
    Material_Use = 'Material use'
