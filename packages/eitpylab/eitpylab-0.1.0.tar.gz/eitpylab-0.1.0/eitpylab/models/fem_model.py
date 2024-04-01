from dataclasses import dataclass, field
from typing import List, TypeVar, Union
    
@dataclass
class ElectrodeProperties:
    """
    Data class representing properties of electrodes in a Finite Element Model (FEM).

    Attributes:
        numberElectrodes (int): Number of electrodes.
        meshTag (List[int]): List of mesh tags associated with electrodes.
        model (str): Model information.
        rho_t (float): Electrical resistivity of the electrode material.

    """
    numberElectrodes: int
    meshTag: List[int]
    model: str
    rho_t: float
    
@dataclass
class RegionProperties:
    """
    Data class representing properties of regions in a Finite Element Model (FEM).

    Attributes:
        label (str): Label or name of the region.
        isActive (bool): Whether the region is active in the model.
        meshTag (List[int]): List of mesh tags associated with the region.
        dimensions (int): Dimensions of the region (e.g., 2D or 3D).
        rho_0 (int): Electrical resistivity of the region material.

    """
    label: str
    isActive: bool
    meshTag: List[int]
    dimentions: int
    rho_0: int
    isGrouped: bool
    
@dataclass
class RotationProperties:
    active: bool
    axis: str
    angle_deg: int
    
@dataclass
class FemModel:
    """
    Data class representing a Finite Element Model (FEM).

    Attributes:
        version (str): Version of the FEM.
        path (str): File path or location of the FEM.
        unit (str): Unit of measurement used in the model.
        dimensions (int): Dimensions of the FEM (e.g., 2D or 3D).
        heightElement (Union[float, None]): Height of elements in the model. Can be None for variable heights.
        electrodes (ElectrodeProperties): Electrode properties in the FEM.
        regions (RegionProperties): Region properties in the FEM.

    """
    version: str
    path: str
    unit: str 
    dimentions: int
    heigthElement: Union[float, None]
    rotation: RotationProperties
    eletrodes: ElectrodeProperties
    regions: RegionProperties