from dataclasses import dataclass, field
from typing import List, TypeVar, Union

@dataclass
class NodalVoltageModel:
    """
    Data class representing a model for nodal voltages.

    Attributes:
        active (bool): Whether the nodal voltage model is active.
        filePath (str): File path or location associated with the model.

    """
    active: bool
    filePath: str
    
@dataclass
class FemObjectsModel:
    """
    Data class representing objects in a Finite Element Model (FEM).

    Attributes:
        type (str): Type of the object.
        regionTags (List[int]): List of region tags associated with the object.
        unit (str): Unit of measurement used for the object.
        center (List[float]): Coordinates of the center of the object.
        radius (float): Radius of the object.
        rho (List[float]): List of electrical resistivity values associated with the object.

    """
    type: str
    regionTags: List[int]
    unit: str
    center: List[float]
    radius: float
    rho: List[float]
    
@dataclass
class ForwardProblemModel:
    """
    Data class representing a model for a forward problem in a Finite Element Model (FEM).

    Attributes:
        version (str): Version of the forward problem model.
        numberElectrodes (int): Number of electrodes in the model.
        nodalVoltages (NodalVoltageModel): Nodal voltage model associated with the forward problem.
        exportGmsh (bool): Whether to export Gmsh files.
        measurementOutputPath (str): File path for measurement output.
        objects (FemObjectsModel): Objects present in the FEM for the forward problem.

    """
    version: str
    numberElectrodes: int
    nodalVoltages: NodalVoltageModel
    exportGmsh: bool
    measurementOutputPath: str
    objects: FemObjectsModel
    